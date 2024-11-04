<p align="center">
  <img src="api/static/images/logo_autolink_white.png" alt="AutoLink Logo" />
</p>

AutoLink provides transparent updates on your car's service status, connecting you directly with your service center. Using live queue feature so client knows his status.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [Contact Information](#contact-information)

## Description

AutoLink is a web application that offers real-time updates on your car's service status. It connects clients directly with their service centers, providing live queue features so clients are always informed about their service status.

## Installation

### Prerequisites

- Python 3.12
- PostgreSQL
- Docker (optional for containerization)

### Steps

1. **Clone the Repository**:
    ```bash
    git clone git@github.com:laguna03/autolink_demo.git
    cd autolink_demo
    ```

2. **Create and Activate a Virtual Environment**:
    ```bash
    pipenv install
    pipenv shell
    ```

3. **Install Dependencies**:
    ```bash
    pipenv install
    ```

4. **Set Up the Database**:
    - Ensure PostgreSQL is running.
    - Create a database named `autolink`.
    - Configure the database connection in the project settings.

5. **Run the Application**:
    ```bash
    uvicorn main:app --reload
    ```

## Usage

1. **Starting the Server**:
    - Run the following command to start the server:
      ```bash
      uvicorn app.main:app --reload
      ```

2. **Accessing the Web Interface**:
    - Open a web browser and go to `http://localhost:8000`.

3. **Example Actions**:
    - Log in as a user.
    - Add a new client to the queue.
    - Start a service and monitor the live queue and ongoing service status.

## API Documentation

### Available Endpoints

#### User Authentication

- **Login**:
    ```http
    POST /auth/token
    ```

- **Create User**:
    ```http
    POST /user/create
    ```

#### Queue Management

- **Get Queue**:
    ```http
    GET /queue
    ```

- **Add to Queue**:
    ```http
    POST /queue/add
    ```

- **Start Service**:
    ```http
    POST /queue/start_service
    ```

- **Update Service**:
    ```http
    POST /queue/update_service
    ```

- **Delete from Queue**:
    ```http
    DELETE /queue/{name}
    ```

#### Statistics

- **Get Stats**:
    ```http
    GET /stats
    ```

- **Reset Visits Count**:
    ```http
    POST /reset_visits_count
    ```


## Technologies Used

- **Python**: Core language for backend development.
- **PostgreSQL**: Database management system.
- **FastAPI**: Web framework for building APIs.
- **HTML/CSS/JavaScript**: Frontend technologies.
- **Docker**: Containerization.
- **Uvicorn**: ASGI server for serving FastAPI applications.

## Contributing

1. **Fork the Repository**:
    - Click the "Fork" button at the top right of the repository page.

2. **Create a New Branch**:
    ```bash
    git checkout -b feature-branch
    ```

3. **Make Your Changes**:
    - Implement your changes and commit them:
    ```bash
    git commit -m "Description of changes"
    ```

4. **Push Your Changes**:
    ```bash
    git push origin feature-branch
    ```

5. **Create a Pull Request**:
    - Open a pull request from your forked repository's feature branch to the main repository's main branch.

## Contact Information

For further information or support, please contact the project maintainers.

