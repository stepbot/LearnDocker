# Simple: Panel and PostgreSQL Integration

This example demonstrates the integration of a basic Panel web application with a PostgreSQL database using Docker Compose. It provides a straightforward setup to help you get started with building web interfaces that interact with databases efficiently.

## Features

- **Panel Web Application**: A simple web app built with Panel to serve a basic interface.
- **PostgreSQL Database**: A PostgreSQL database that stores and retrieves data for the application.
- **Docker Compose**: Orchestrates the services, allowing for easy setup and execution.

## Prerequisites

Ensure you have the following installed:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Follow these steps to get the project up and running:

1. **Clone the repository**: 
    ```bash
    git clone https://github.com/stepbot/LearnDockerLLM.git
    cd LearnDockerLLM/Simple
    ```

2. **Build and run the containers**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**: 
   Once the containers are up, the web application will be accessible at [http://localhost:5006](http://localhost:5006).

## Usage

- The web application connects to the PostgreSQL database to demonstrate basic data retrieval and storage functionalities.
- You can customize the Panel application by modifying the `app.py` file located in the directory.
- The PostgreSQL service is defined in the `docker-compose.yml`, and any database configuration changes should be made there.

## Development

1. **Modify the Application Code**: 
   Edit the `app.py` file to adjust the web interface or database interactions as needed.

2. **Rebuild the Containers**:
   After making changes, rebuild the containers to see your updates:
   ```bash
   docker-compose up --build
   ```

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and create a pull request.

## License

This project is licensed under the [MIT License](../license.txt). You are free to use, modify, and distribute this software in accordance with the terms of the license.

## Contact

For any questions or feedback, please open an issue on the repository.

