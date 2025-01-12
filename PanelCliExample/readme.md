# Panel CLI Example: Remote Command Execution via SSH

This project demonstrates a Dockerized application that uses Panel to provide a web interface for executing SSH commands on a remote server. The setup involves a simple Panel app that sends user-inputted bash commands to a target container configured to accept SSH connections.

## Features

- **Panel Web Interface**: A simple and intuitive web interface for executing remote shell commands.
- **SSH Integration**: Utilizes Paramiko, a Python library, for establishing SSH connections to execute commands.
- **Isolated Environment**: Dockerized setup ensures consistent environments for both the Panel interface and the SSH target.

## Disclaimer

**Security Warning:** This application allows for arbitrary command execution on the server via SSH. While Docker containers provide a degree of isolation, they do not guarantee complete security. Potential risks include:

- **Privilege Escalation**: Malicious actors might attempt to escalate privileges within the container.
- **Container Escape**: There is a possibility of escaping the container to interact with the host system.
  
Use with caution, especially in production environments or with untrusted code. It is recommended to implement strict security measures and monitor container activity.

## Prerequisites

Ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/stepbot/LearnDockerLLM.git
cd LearnDockerLLM/PanelCliExample
```

### 2. Create and Configure the `.env` File for Panel App

Navigate to the `panel_app` directory and create a file named `.env`. Add the necessary environment variables as shown below:

```plaintext
TARGET_HOST=target
TARGET_SSH_USER=testuser
TARGET_SSH_PASS=password
TARGET_SSH_PORT=22
```

These values should reflect your SSH configuration or the desired settings for your panel app to connect.

### 3. Create and Configure the `.env` File for Target SSH

Navigate to the `target_ssh` directory and create a file named `.env`. Add any target-specific environment variables as needed.

(Note: If specific configuration parameters are needed for the target, they should be listed here. Since the setup for the target is not fully detailed, this portion is left flexible for additional configuration.)

### 4. Build and Run the Application

Use Docker Compose to set up and run both Panel and target SSH services:

```bash
docker-compose up --build
```

### 5. Access the Web Interface

Once the services are running, the application will be accessible at [http://localhost:5006](http://localhost:5006). Enter your commands in the interface to execute them on the remote server.

## Component Breakdown

### `app.py`

- **Description**: The main script for the Panel app. It uses Paramiko to establish an SSH connection and execute remote commands on a target container.
- **Dependencies**: Relies on the Paramiko library for SSH functionality and Panel for the web interface.

### `compose.yml`

- **Description**: Defines the Docker services for the Panel app and the SSH target environment. It configures network settings, environment variables, and service dependencies.
- **Services**:
  - `panel`: Hosts the Panel web app.
  - `target`: A mock target set up to accept SSH connections.

### `dockerfile`

- **Description**: Sets up the environment necessary for running the Panel application, based on the Python 3.10 slim image.
- **Details**: Installs Python dependencies and exposes required ports.

## Development

- **Modify Code**: Edit `app.py` to change the SSH logic or Panel interface.
- **Rebuild Containers**: After changes, use the following command to rebuild:
  ```bash
  docker-compose up --build
  ```

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and create a pull request.

## License

This project is licensed under the MIT License. See [license.txt](../license.txt) for details.

## Contact

For any questions or feedback, please open an issue on the repository.