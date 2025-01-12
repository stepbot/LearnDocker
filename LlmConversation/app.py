import panel as pn
from openai import OpenAI, OpenAIError
import os

pn.extension(notifications=True)  # Enable notifications

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
    client = OpenAI(api_key=OPENAI_API_KEY)  # Ensure API key is passed
except OpenAIError as e:
    pn.state.notifications.error(f"OpenAI initialization failed: {e}")
    raise

# Define Panel widgets
chat_history = pn.pane.Markdown("### Chat History\n\n", width=600, height=400)
chat_history_container = pn.Row(
    chat_history,
    sizing_mode='stretch_both',
    css_classes=['scrollable']
)

send_button = pn.widgets.Button(name='Send Next Turn', button_type='primary')
clear_button = pn.widgets.Button(name='Clear', button_type='warning')

# Two distinct system prompts for our two LLM "instances"
system_prompt_llm1 = {
    "role": "system",
    "content": (
        "You are LLM1. You speak from your own perspective, with your own style. "
        "You are in a conversation with another LLM.Talk to them and get to know them"
    )
}

system_prompt_llm2 = {
    "role": "system",
    "content": (
        "You are LLM1. You speak from your own perspective, with your own style. "
        "You are in a conversation with another LLM.Talk to them and get to know them"
    )
}

# Shared conversation state (excluding each LLM's system prompt).
conversation = []

def generate_next_turn(_=None):
    """
    Each time this is called, we:
      1) Call LLM1 with [system_prompt_llm1] + conversation
      2) Append its response to the conversation (labeled as LLM1)
      3) Call LLM2 with [system_prompt_llm2] + updated conversation
      4) Append its response to the conversation (labeled as LLM2)
    """
    global conversation

    # --- LLM1 turn ---
    try:
        messages_llm1 = [system_prompt_llm1] + conversation
        response1 = client.chat.completions.create(
            model="gpt-4",
            messages=messages_llm1,
            temperature = 0
        )
    except OpenAIError as e:
        pn.state.notifications.error(f"OpenAI API error (LLM1): {e}")
        return

    llm1_text = response1.choices[0].message.content.strip()
    # Append LLM1’s text to chat display
    chat_history.object += f"**LLM1:** {llm1_text}\n\n"
    # Add to conversation as if "assistant" from LLM1
    conversation.append({"role": "assistant", "content": llm1_text, "name": "LLM1"})

    # --- LLM2 turn ---
    try:
        messages_llm2 = [system_prompt_llm2] + conversation
        response2 = client.chat.completions.create(
            model="gpt-4",
            messages=messages_llm2,
            temperature = 1
        )
    except OpenAIError as e:
        pn.state.notifications.error(f"OpenAI API error (LLM2): {e}")
        return

    llm2_text = response2.choices[0].message.content.strip()
    # Append LLM2’s text to chat display
    chat_history.object += f"**LLM2:** {llm2_text}\n\n"
    # Add to conversation as if "assistant" from LLM2
    conversation.append({"role": "assistant", "content": llm2_text, "name": "LLM2"})

def clear_chat(_=None):
    global conversation
    conversation = []
    chat_history.object = "### Chat History\n\n"

# Bind events
send_button.on_click(generate_next_turn)
clear_button.on_click(clear_chat)

# Layout the app
layout = pn.Column(
    chat_history_container,
    pn.Row(send_button, clear_button, sizing_mode='stretch_width'),
    sizing_mode='stretch_width'
)

layout.servable()

if __name__ == '__main__':
    pn.serve(layout, show=True, address='0.0.0.0', port=5006, allow_websocket_origin='*')
