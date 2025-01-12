import os
import json
import time
import uuid
import panel as pn
import paramiko
from datetime import datetime
from openai import OpenAI, OpenAIError
# If needed: from openai.error import OpenAIError

pn.extension()

# -------------------------------------------------------------------
# Custom CSS (for scrollable chat pane)
# -------------------------------------------------------------------
pn.config.raw_css.append("""
.scrollable {
    overflow-y: auto;
}
""")

# -------------------------------------------------------------------
# Configuration / Environment Variables
# -------------------------------------------------------------------
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Initialize OpenAI client
try:
    client = OpenAI()
except OpenAIError as e:
    # If you want a Panel notification
    pn.state.notifications.error(f"OpenAI initialization failed: {e}")
    raise

# Try to fetch model list
model_ids = []
try:
    available_models = client.models.list()
    # Filter for relevant models, e.g. only GPT-based
    model_ids = [m.id for m in available_models if "gpt" in m.id]
except OpenAIError as e:
    # Fallback if listing fails
    pass

# Provide fallback if the list is empty
if not model_ids:
    model_ids = ["gpt-4o", "gpt-4"]

# Make a model select widget
model_select = pn.widgets.Select(
    name='LLM Model',
    options=model_ids,
    value="gpt-4o"
)

# SSH environment variables
TARGET_HOST = os.environ.get("TARGET_HOST")
TARGET_SSH_USER = os.environ.get("TARGET_SSH_USER")
TARGET_SSH_PASS = os.environ.get("TARGET_SSH_PASS")
TARGET_SSH_PORT = int(os.environ.get("TARGET_SSH_PORT", "22"))

# -------------------------------------------------------------------
# Persistent SSH Client
# -------------------------------------------------------------------
persistent_ssh_client = None

def get_ssh_client():
    global persistent_ssh_client
    if persistent_ssh_client is None:
        persistent_ssh_client = paramiko.SSHClient()
        persistent_ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        persistent_ssh_client.connect(
            hostname=TARGET_HOST,
            port=TARGET_SSH_PORT,
            username=TARGET_SSH_USER,
            password=TARGET_SSH_PASS,
        )
    return persistent_ssh_client

def run_remote_command_shared(command: str, timeout: float = 5.0) -> str:
    """
    Executes the command on the remote host via a persistent SSH shell channel.
    If timeout <= 0, run indefinitely. Otherwise, forcibly send Ctrl-C after `timeout` seconds.
    """
    try:
        client = get_ssh_client()
        channel = client.invoke_shell(width=120, height=80)
        
        channel.send(command + "\n")
        
        output_chunks = []
        start_time = time.time()

        while True:
            while channel.recv_ready():
                chunk = channel.recv(2048).decode("utf-8", errors="ignore")
                output_chunks.append(chunk)

            # Check if the command ended naturally
            if channel.exit_status_ready():
                break

            # If we have a positive timeout and exceeded it, send Ctrl-C
            if timeout > 0 and (time.time() - start_time) > timeout:
                channel.send("\x03")  # Ctrl-C
                time.sleep(0.5)
                break

            time.sleep(0.1)

        # Grab any remaining data
        time.sleep(0.2)
        while channel.recv_ready():
            chunk = channel.recv(2048).decode("utf-8", errors="ignore")
            output_chunks.append(chunk)

        channel.close()
        result = "".join(output_chunks).strip()
        return result if result else "Command produced no output."
    except Exception as e:
        global persistent_ssh_client
        persistent_ssh_client = None
        return f"Error executing command: {e}"

# -------------------------------------------------------------------
# HELPERS
# -------------------------------------------------------------------
def notify_error(error_message):
    print(error_message)
    chat_history.object += f"> **⚠️ Error:** {error_message}\n\n"

# -------------------------------------------------------------------
# Chat + Function-Calling
# -------------------------------------------------------------------
chat_history = pn.pane.Markdown("### Chat History\n\n", width=600, height=400)
chat_history_container = pn.Row(chat_history, sizing_mode='stretch_both', css_classes=['scrollable'])
user_input = pn.widgets.TextInput(placeholder='Type your message here...', sizing_mode='stretch_width')
send_button = pn.widgets.Button(name='Send', button_type='primary')
clear_button = pn.widgets.Button(name='Clear', button_type='warning')

api_conversation = [
    {"role": "system", "content": (
        "You are a helpful assistant that can execute shell commands remotely via SSH. "
        "When needed, use the 'run_command' tool with the required parameters to run a command. "
        "For example, if a user asks 'What does ls -la / show?', generate a tool call with the command: ls -la /."
    )}
]

# Debug pane
conversation_debug = pn.pane.Markdown("### Conversation Debug\n\n", width=600, height=200)

def update_conversation_debug():
    conversation_debug.object = "### Conversation Debug\n\n```\n" + json.dumps(api_conversation, indent=2) + "\n```"

debug_toggle = pn.widgets.Toggle(name="Show Debug", value=False)
def toggle_debug(event):
    debug_pane.visible = debug_toggle.value

debug_toggle.param.watch(toggle_debug, 'value')
debug_pane = pn.Column(conversation_debug)
debug_pane.visible = False

# The function tool definition
run_command_tool = {
    "type": "function",
    "function": {
        "name": "run_command",
        "description": (
            "Execute a shell command remotely via SSH on the target container. "
            "By default, the command will be forcibly stopped after 5 seconds. "
            "If you set timeout=0, the command can run indefinitely."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to execute on the remote machine."
                },
                "timeout": {
                    "type": "number",
                    "description": (
                        "Optional. Number of seconds before forcibly sending Ctrl-C. "
                        "Set to 0 for indefinite run, defaults to 5 if omitted."
                    )
                }
            },
            "required": ["command"],
            "additionalProperties": False
        }
    }
}

def call_chat_api(messages, tools=None):
    try:
        payload = {
            "model": model_select.value,  # the selected model
            "messages": messages,
        }
        if tools:
            payload["tools"] = tools
        return client.chat.completions.create(**payload)
    except OpenAIError as e:
        notify_error(f"OpenAI API error: {e}")
        return None

def send_message(event=None):
    user_msg = user_input.value.strip()
    if not user_msg:
        pn.state.notifications.warning("Please enter a message.")
        return

    # Append user message
    chat_history.object += f"> **🧑 You:** {user_msg}\n\n"
    api_conversation.append({"role": "user", "content": user_msg})
    update_conversation_debug()
    user_input.value = ""

    # Call the API
    response = call_chat_api(api_conversation, tools=[run_command_tool])
    if not response:
        return

    assistant_message = response.choices[0].message
    assistant_content = assistant_message.content if assistant_message.content else ""
    
    if assistant_message.tool_calls:
        tool_call = assistant_message.tool_calls[0]
        tool_name = tool_call.function.name
        try:
            arguments = json.loads(tool_call.function.arguments)
        except Exception as e:
            arguments = {}
            chat_history.object += f"> **🤖 Assistant (Error):** Invalid tool arguments: {e}\n\n"
        
        if tool_name == "run_command":
            command_to_run = arguments.get("command")
            chat_history.object += f"> **🤖 Assistant requested command execution:** `{command_to_run}`\n\n"
            
            tool_id = tool_call.id
            tool_type = tool_call.type

            # Add assistant message with tool_calls
            assistant_dict = {
                "role": assistant_message.role,
                "content": assistant_content,
                "tool_calls": [
                    {
                        "id": tool_id,
                        "type": tool_type,
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    }
                ]
            }
            api_conversation.append(assistant_dict)
            
            # Execute the remote command
            result = run_remote_command_shared(command_to_run)
            chat_history.object += f"> **🛠️ Ran Command (LLM):** `{command_to_run}`\n\n"
            chat_history.object += f"```\n{result}\n```\n\n"
            manual_output.object += f"> **LLM executed:** `{command_to_run}`\n```\n{result}\n```\n\n"

            # Create tool response message
            tool_response_message = {
                "role": "tool",
                "name": "run_command",
                "content": json.dumps({"command": command_to_run, "result": result}),
                "tool_call_id": tool_id
            }
            api_conversation.append(tool_response_message)
            update_conversation_debug()
            
            # Follow-up call
            response2 = call_chat_api(api_conversation, tools=[run_command_tool])
            if response2:
                new_assistant_message = response2.choices[0].message
                new_assistant_content = new_assistant_message.content or ""
                api_conversation.append({"role": "assistant", "content": new_assistant_content})
                chat_history.object += f"> **🤖 Assistant:** {new_assistant_content}\n\n"
                update_conversation_debug()
        else:
            api_conversation.append({"role": "assistant", "content": assistant_content})
            chat_history.object += f"> **🤖 Assistant:** {assistant_content}\n\n"
            update_conversation_debug()
    else:
        api_conversation.append({"role": "assistant", "content": assistant_content})
        chat_history.object += f"> **🤖 Assistant:** {assistant_content}\n\n"
        update_conversation_debug()

def clear_chat(event):
    global api_conversation
    api_conversation = [
        {"role": "system", "content": (
            "You are a helpful assistant that can execute shell commands remotely via SSH. "
            "When needed, use the 'run_command' tool with the required parameters to run a command."
        )}
    ]
    chat_history.object = "### Chat History\n\n"
    update_conversation_debug()

send_button.on_click(send_message)
user_input.param.watch(send_message, "enter_pressed")
clear_button.on_click(clear_chat)

# -------------------------------------------------------------------
# MANUAL SSH TERMINAL
# -------------------------------------------------------------------
command_input_manual = pn.widgets.TextInput(placeholder="Type bash command here...", width=600)
execute_button_manual = pn.widgets.Button(name='Execute', button_type='primary')
manual_output = pn.pane.Markdown("", min_width=600, min_height=400, sizing_mode="stretch_both", styles={'overflow-y': 'auto'})

def run_manual_command(event):
    cmd = command_input_manual.value.strip()
    if not cmd:
        manual_output.object = "Please enter a command."
        return

    result = run_remote_command_shared(cmd)
    api_conversation.append({"role": "user", 
                             "content": f"User executed a command in the shell:\n{cmd}\nOutput:\n{result}"})
    update_conversation_debug()
    
    manual_output.object += f"> **Manual executed:** `{cmd}`\n```\n{result}\n```\n\n"
    chat_history.object += f"> **Manual executed:** `{cmd}`\n```\n{result}\n```\n\n"

execute_button_manual.on_click(run_manual_command)
manual_ssh_layout = pn.Column(
    "# Manual SSH Terminal",
    command_input_manual,
    execute_button_manual,
    manual_output,
    sizing_mode="stretch_width"
)

# -------------------------------------------------------------------
# COMBINED APP LAYOUT
# -------------------------------------------------------------------
app_layout = pn.Column(
    pn.Row(
        pn.Column(
            "# Model Selection",
            model_select,
        ),
    ),
    pn.Spacer(height=20),
    pn.Row(
        pn.Column(
            "# Chat with LLM (with command tool)",
            chat_history_container,
            pn.Row(user_input, send_button, clear_button, sizing_mode='stretch_width'),
        ),
        pn.Spacer(width=30),
        manual_ssh_layout,
        sizing_mode="stretch_both"
    ),
    pn.Spacer(height=20),
    pn.Row(
        debug_toggle,
        debug_pane,
    )
)

app_layout.servable()

if __name__ == '__main__':
    pn.serve(app_layout, show=True, address='0.0.0.0', port=5006, allow_websocket_origin='*')
