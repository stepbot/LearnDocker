# SimpleChat: Basic Chat Interface with LLM Integration

This example demonstrates how to build a simple chat interface powered by a Large Language Model (LLM) using [OpenAI's GPT](https://openai.com/). The application leverages Docker and Panel to create a web-based chat interface that communicates with the LLM for generating responses.

## Features

- **Interactive Chat Interface**: A web-based chat interface that allows users to interact with the LLM in real-time.
- **OpenAI Integration**: Utilizes GPT models via OpenAI API to process and respond to user inputs.
- **Dockerized Setup**: The application is contained within a Docker container for easy deployment and scalability.

## Prerequisites

Ensure you have the following installed:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)
- OpenAI API Key: Obtain an API key from OpenAI.

## Getting Started

Follow these steps to deploy the chat application:

1. **Clone the repository**: 
    ```bash
    git clone https://github.com/stepbot/LearnDockerLLM.git
    cd LearnDockerLLM/SimpleChat
    ```

2. **Set the OpenAI API Key**:
   - Create a `.env` file in the SimpleChat directory if it doesn't already exist.
   - Add your API key: `OPENAI_API_KEY=your-api-key-here`.

3. **Build and run the containers**:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**: 
   The chat interface will be accessible at [http://localhost:5006](http://localhost:5006).

## Usage

- Type messages into the chat interface and receive AI-generated replies via the OpenAI GPT model.
- Customize the conversation model and parameters within the `app.py` file.

## Development

1. **Modify the Application Code**: 
   Edit the `app.py` file to adjust LLM interaction or change UI elements as needed.

2. **Rebuild the Containers**:
   After making any changes, rebuild the containers to apply updates:
   ```bash
   docker-compose up --build
   ```

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and create a pull request.

## License

This project is licensed under the [MIT License](../license.txt). You are free to use, modify, and distribute this software in accordance with the terms of the license.

## Contact

For any questions or feedback, please open an issue on the repository.