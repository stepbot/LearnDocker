import panel as pn
import random
import time
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

# Panel widgets
# Remove problem_selector since problems are now generated automatically
temperature_slider = pn.widgets.FloatSlider(name='Max Temperature', start=0.0, end=1.0, step=0.1, value=0.5)
iterations_spinner = pn.widgets.IntInput(name='Iterations', value=3, step=1)
run_button = pn.widgets.Button(name='Run Experiment', button_type='primary')

# Panel output area
output_area = pn.pane.Markdown("### Experiment Output\n", width=600)

# New helper function to generate a hard math problem using an LLM
def generate_hard_problem(temperature=0.7):
    prompt = ("You are an expert math problem creator. "
              "Generate a challenging math problem that is difficult enough to occasionally cause errors when solved. "
              "Be creative and ensure the problem has multiple steps or twists. "
              "Return only the problem statement.")
    
    system_prompt = {"role": "system", "content": "You are a creative and challenging math problem generator."}
    user_prompt = {"role": "user", "content": prompt}
    messages = [system_prompt, user_prompt]

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=temperature
        )
        problem_text = response.choices[0].message.content.strip()
        return problem_text
    except Exception as e:
        return f"Error generating problem: {e}"

# Helper function to call the LLM for a single answer
def ask_llm(problem_prompt, temperature):
    system_prompt = {"role": "system", "content": "You are a helpful math expert. Answer the question and then provide your confidence in your answer on a scale from 0 to 1 on a separate line."}
    user_prompt = {"role": "user", "content": problem_prompt}
    conversation = [user_prompt]

    # Form the message list
    messages_llm1 = [system_prompt] + conversation

    try:
        # Make the OpenAI API call for the answer
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages_llm1,
            temperature=temperature
        )
        # Parse the response
        answer_text = response.choices[0].message.content.strip()
        return answer_text
    except Exception as e:
        return f"Error in answer: {e}"

# Helper function to aggregate responses with another LLM call
def aggregate_answers(problem_prompt, responses, temperature):
    # Create a prompt for aggregation that includes all the responses
    aggregation_prompt = f"You are an expert judge. Here is a math problem: '{problem_prompt}'. " \
                         f"The following are different answers along with the LLM's self-assessed confidence on a scale from 0 to 1:\n\n"
    for i, response in enumerate(responses, 1):
        aggregation_prompt += f"Answer {i}: {response}\n\n"
    aggregation_prompt += "Based on these responses, provide your best final answer along with a final aggregated confidence rating on a scale from 0 to 1."

    system_prompt = {"role": "system", "content": "You are a helpful and precise math expert aggregator."}
    user_prompt = {"role": "user", "content": aggregation_prompt}
    messages_llm2 = [system_prompt, user_prompt]

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages_llm2,
            temperature=temperature
        )
        aggregated_text = response.choices[0].message.content.strip()
        return aggregated_text
    except Exception as e:
        return f"Error in aggregation: {e}"

# Experiment runner callback
def run_experiment(event):
    output_lines = []
    
    # Generate a hard problem using an LLM call
    generation_temperature = 0.7  # You can adjust this for more or less creative problems
    generated_problem = generate_hard_problem(temperature=generation_temperature)
    output_lines.append(f"**Generated Problem:** {generated_problem}")
    
    max_temperature = temperature_slider.value
    iterations = iterations_spinner.value
    output_lines.append(f"**Max Temperature for Answering:** {max_temperature}")
    output_lines.append(f"**Iterations:** {iterations}\n")

    responses = []
    # Run the experiment for a number of iterations
    for i in range(iterations):
        # Vary temperature randomly between 0 and max_temperature
        random_temperature = random.uniform(0, max_temperature)
        output_lines.append(f"**Iteration {i+1}:** Using temperature {random_temperature:.2f}")
        
        # Optionally modify the problem prompt slightly to simulate seed variance
        random_suffix = f"(iteration {i} - {random.random():.4f})"
        modified_prompt = generated_problem + " " + random_suffix

        answer = ask_llm(modified_prompt, random_temperature)
        responses.append(answer)
        output_lines.append(f"**Answer:** {answer}\n")
        # Optional pause to avoid rate-limiting
        time.sleep(1)

    # Aggregate answers with the second LLM using a fixed low temperature for determinism
    aggregation_temperature = 0
    aggregated_result = aggregate_answers(generated_problem, responses, aggregation_temperature)
    output_lines.append("### Aggregated Answer and Confidence")
    output_lines.append(aggregated_result)

    # Update the output area
    output_area.object = "\n\n".join(output_lines)

# Link the run button to the experiment function
run_button.on_click(run_experiment)

# Layout the Panel app
app_layout = pn.Column(
    pn.pane.Markdown("## LLM Consistency Experiment With Generated Challenges", styles={'font-size': '20px'}),
    temperature_slider,
    iterations_spinner,
    run_button,
    output_area
)

# Serve the app
app_layout.servable()

if __name__ == '__main__':
    pn.serve(app_layout, show=True, address='0.0.0.0', port=5006, allow_websocket_origin='*')
