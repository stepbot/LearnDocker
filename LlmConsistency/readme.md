## Overview

This section of the LearnDocker repository focuses on the **LLM Consistency Experiment**. The application is a web-based tool that uses OpenAI's Large Language Models (LLMs) to generate complex math problems, gather multiple answers, and aggregate the results to assess answer consistency.

### Components

1. **Panel App (`app.py`)**:
   - This is the main application script, built with [Panel](https://panel.holoviz.org/).
   - It generates math problems using LLMs and gathers responses to measure consistency over several iterations.
   - Users can adjust parameters like temperature and number of iterations to explore LLM behavior.

2. **Docker Compose File (`compose.yml`)**:
   - Manages the containerization of the app using Docker Compose.
   - Ensures the app runs consistently with environment variables such as the `OPENAI_API_KEY`.

3. **Dockerfile**:
   - Defines an isolated environment for the application using a Python 3.10 slim image.
   - Installs necessary Python dependencies and sets up the environment to serve the Panel app.

4. **Documentation (`readme.md`)**:
   - Provides guidelines on how to set up, run, and contribute to the project.
   - Details on how to use Docker and Docker Compose to manage the app lifecycle.

### Prerequisites

- **Docker**: To build and run containers.
- **OpenAI API Key**: Required for interacting with the OpenAI API.

### Setting Up

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/stepbot/LearnDockerLLM.git
   cd LearnDockerLLM/LlmConsistency
   ```

2. **Configure Environment Variables**:
   Ensure you have your OpenAI API key available and export it in your terminal or include it in your Docker Compose file.

   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   ```

3. **Build and Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

   This command will build the Docker image and start the service as specified in `compose.yml`.

### Usage

Once the service is running, the application will be available at `http://localhost:5006`. Adjust parameters for your experiment using the web interface, and observe the response consistency of the LLMs.

### Contributing

Contributions are appreciated. Please fork the repo, make changes, and open a pull request. Feel free to suggest enhancements or report issues.

### License

This project is licensed under the MIT License. See [license.txt](../license.txt) for details.