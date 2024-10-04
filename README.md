# Django Notes API

This project is a backend API for managig notes, utilizing Django, Django Ninja, GraphQL and Celery


## Features

    - CRUD operations for notes, groups and tags
    - GraphQL API for flexible querying
    - REST API using Django Ninja
    - Asynchronous tasks with Celery
    - User authentication
    - Docker containerization for easy deployment

## Installation

    1. Clone the repository
    2. Navigate to the root of the project
    3. Run docker-compose build
    4. run docker-compose up to start the app
    5. the API will be available at 'http://localhost:8000'

## API Documentation

    - REST API documentation is available at '/api/docs'
    - GraphQL playground is available az '/graphql'

## Testing

    - run tests using: docker-compose run test

