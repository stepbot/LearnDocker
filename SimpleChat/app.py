import panel as pn
from openai import OpenAI, OpenAIError
import os

pn.extension()

# Add custom CSS for scrolling
pn.config.raw_css.append("""
.scrollable {
    overflow-y: auto;
}
""")

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Initialize OpenAI client
try:
    client = OpenAI()
except OpenAIError as e:
    pn.state.notifications.error(f"OpenAI initialization failed: {e}")
    raise

# Define widgets
chat_history = pn.pane.Markdown("### Chat History\n\n", width=600, height=400)
chat_history_container = pn.Row(
    chat_history,
    sizing_mode='stretch_both',
    css_classes=['scrollable']
)

# Use TextInput widget
user_input = pn.widgets.TextInput(
    placeholder='Type your message here...',
    sizing_mode='stretch_width'
)
send_button = pn.widgets.Button(name='Send', button_type='primary')
clear_button = pn.widgets.Button(name='Clear', button_type='warning')

# Initialize conversation history
conversation = []

def send_message(event=None):
    user_msg = user_input.value.strip()
    if not user_msg:
        pn.state.notifications.warning("Please enter a message.")
        return

    # Append user message with avatar
    chat_history.object += f"> **🧑 You:** {user_msg}\n\n"
    user_input.value = ""

    # Update conversation history
    conversation.append({"role": "user", "content": user_msg})

    try:
        # Make API call to OpenAI with conversation history
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=conversation,
        )
        bot_reply = completion.choices[0].message.content.strip()
        # Append bot reply with avatar
        chat_history.object += f"> **🤖 Bot:** {bot_reply}\n\n"
        # Update conversation history
        conversation.append({"role": "assistant", "content": bot_reply})
    except OpenAIError as e:
        pn.state.notifications.error(f"OpenAI API error: {e}")

def clear_chat(event):
    global conversation
    conversation = []
    chat_history.object = "### Chat History\n\n"

# Bind events
send_button.on_click(send_message)
user_input.param.watch(send_message, "enter_pressed")  
clear_button.on_click(clear_chat)

# Layout the app
layout = pn.Column(
    chat_history_container,
    pn.Row(user_input, send_button, clear_button, sizing_mode='stretch_width'),
    sizing_mode='stretch_width'
)

layout.servable()

# For direct running
if __name__ == '__main__':
    pn.serve(layout, show=True, address='0.0.0.0', port=5006, allow_websocket_origin='*')
