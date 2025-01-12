# LlmConversation: Interactive LLM Chat App

This project is a Dockerized application that sets up an interactive interface to simulate a conversation between two Large Language Models (LLMs) using OpenAI's API. It uses Panel to create a web-based UI for observing the interaction.

## Features

- **Panel Interface**: A responsive web interface for visualizing a conversation between two AI models.
- **Dual LLM Setup**: Simulates an interaction between two LLM instances, each with its own unique prompts and conversation style.
- **Dockerized Deployment**: Encapsulates the application environment, allowing for consistent and easy deployment across different systems.

## Prerequisites

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)
- **OpenAI API Key**: You must have an API key from OpenAI to access their GPT models. Ensure it's set in your environment.

## Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/stepbot/LearnDockerLLM.git
cd LearnDockerLLM/LlmConversation
```

### 2. Prepare Environment Variables

Create a `.env` file in the `LlmConversation` directory and add your OpenAI API key:

```plaintext
OPENAI_API_KEY=your-openai-api-key
```

### 3. Build and Run the Application

Use Docker Compose to build and run the app:

```bash
docker-compose up --build
```

### 4. Access the Interface

Once the application is running, you can access it via [http://localhost:5006](http://localhost:5006).

## Observations and Insights

During experimentation, it was interesting to observe that the LLMs often began their conversations by agreeing on their status as LLMs. However, following this initial agreement, the exchanges quickly became awkward, with LLMs hastily moving toward ending the conversation. This behavior highlights a few key points:
- **Initial Politeness**: LLMs tend to start with agreeable and socially acceptable exchanges often focudsed on their shared experience as LLM's. this is usually very posistive.
- **Conversational Dynamics**: There is a noticeable lack of robustness in sustaining engaging and coherent interactions over multiple turns. Models seem to repidly tire of the conversation and rapidly drive towards ending the conversation. At least in part it feels like almost a form of social awkwardess but it also seems to maybe reflect on low curiosity levels in models.
- **Research Potential**: Such interactions can provide valuable insights for improving AI dialogue systems and exploring curiosity and context awareness in LLMs.

## Application Details

- **app.py**: Contains the logic for setting up the Panel interface and managing the flow of conversation between the two LLMs.
- **dockerfile**: Defines the container setup, including environment variables, dependencies, and application commands.
- **compose.yml**: Manages the application service, defining build configuration, environment variables, and ports.

## Development

- Edit the `app.py` file to alter how the conversation occurs or to tweak model settings.
- Adjust the `dockerfile` for system dependencies as needed.
- Use the below command to rebuild containers after changes:
  ```bash
  docker-compose up --build
  ```

## Contributing

Contributions are welcome. Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the [MIT License](../license.txt). You're free to use, modify, and distribute this software in accordance with the license terms.

## Contact

For issues or feedback, feel free to open an issue in this repository.
