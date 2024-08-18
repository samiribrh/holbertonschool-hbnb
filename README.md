# HBNB - Airbnb Clone

## Description

This project is an Airbnb clone that provides a platform for users to book accommodations. 


## Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/samiribrh/holbertonschool-hbnb-client.git
    cd holbertonschool-hbnb-client
    ```
2. Add environment variables to the `.env` file. Example:

    ```bash
    echo "DBTYPE=postgresql+psycopg2" > backend/.env
    ```

3. Build and start the Docker containers:

    ```bash
    docker-compose up --build
    ```

## Usage

Once the containers are up and running, you can access the application at `http://localhost:8000`.

## Environment Variables

`DBTYPE`: Database type.  

`HOSTNAME`: Database host.  

`DBPORT`: Database port.  

`POSTGRES_USER`: Postgres user.  

`POSTGRES_DB`: Postgres database.  

`POSTGRES_PASSWORD`: Postgres password.  

`POSTGRES_HOST_AUTH_METHOD`: Postgres host authentication method.  

`POSTGRES_INITDB_ARGS`: Postgres initialization arguments.

`REDIS_HOST`: Redis host.

`REDIS_PORT`: Redis port.

`REDIS_PASSWORD`: Redis password.

`REDIS_DB`: Redis database.

`SMTP_HOST`: SMTP host server.

`SMTP_MAIL`: SMTP mail address.

`SMTP_PASSWORD`: SMTP Mail password.

`PYTHONPATH`: Python path.  

`FLASK_APP`: Flask application entry point.  

`FLASK_RUN_HOST`: Flask run host.  

`FLASK_RUN_PORT`: Flask run port.  

`JWT_SECRET_KEY`: Secret key for JWT authentication.  

## Authors

[Samir Ibrahimov](https://www.linkedin.com/in/samiribrh/)
