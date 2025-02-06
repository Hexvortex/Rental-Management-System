
# Rental Management System

## Overview
The Rental Management System is designed to streamline the management of rental properties, tenants, and caretakers. It offers a comprehensive solution for property managers to efficiently handle their operations.

## Features
- **Property Management**: Track and manage multiple rental properties.
- **Tenant Management**: Maintain records of tenants and their lease agreements.
- **Caretaker Management**: Register and manage caretakers responsible for property maintenance.
- **Automated Notifications**: Automated reminders and notifications for payments and maintenance.
- **Command-Line Interface**: Interact with the system through a user-friendly CLI.

## Components
- **main.py**: Main entry point for running the application.
- **models.py**: Defines the database schema.
- **database.py**: Manages database connections and operations.
- **cli.py**: Command Line Interface for user interactions.
- **create_new_db.py**: Script to create a new database.
- **bot.py**: Handles automated tasks and notifications.
- **.env**: Environment variables for configuration.
- **Pipfile** and **Pipfile.lock**: Manage project dependencies.
- **rental_management.db**: Database file storing rental management data.

## Technologies Used
- **Python**: Primary programming language.
- **SQLite**: Database for storing rental management data.
- **Pipenv**: Dependency management tool.
- **dotenv**: For managing environment variables.
- **SQLAlchemy**: ORM for database interactions.

## Setup and Installation
1. **Clone the repository:**
   ```sh
   git clone <repository_url>
   cd rental_management
   ```
2. **Create a virtual environment and install dependencies:**
   ```sh
   pipenv install
   ```
3. **Create a `.env` file with the necessary environment variables (e.g., database credentials):**
   ```sh
   touch .env
   # Add your environment variables in the .env file
   ```
4. **Initialize the database:**
   ```sh
   python create_new_db.py
   ```

## Running the Application
Interact with the system via the Command Line Interface:
```sh
python cli.py
```

## Automation and Bots
Run the bot script to handle automated tasks and notifications:
```sh
python bot.py
```

## Workflow
1. **Initialization**: Set up the environment and initialize the database.
2. **Register Caretakers**: Use the CLI to register caretakers responsible for properties.
3. **Manage Properties and Tenants**: Add properties and tenants, manage leases, and record payments.
4. **Automated Notifications**: The bot script sends automated reminders for due payments and maintenance tasks.
5. **Regular Operations**: Continue to use the CLI for regular management tasks and updates.

## Simple Explanation

### Project Name
**Rental Management System**

### Project Description
The Rental Management System is a tool designed to help property managers keep track of rental properties, tenants, and caretakers. It makes the job easier by automating tasks like sending payment reminders and scheduling maintenance.

### Project Problem
Managing rental properties can be difficult and confusing. Property managers need to keep track of who is renting, when rent is due, and what maintenance is needed. Doing all this manually can lead to mistakes and take a lot of time.

### Project Solution
The Rental Management System solves these problems by providing a single place to manage everything related to rental properties. It keeps track of tenants, properties, and caretakers, and automatically sends reminders for payments and maintenance. This makes the management process faster and more accurate.

### Minimum Viable Product (MVP)
The MVP of the Rental Management System includes:
1. **Property Management**: Easily add and manage properties.
2. **Tenant Management**: Keep records of tenants and their rental agreements.
3. **Caretaker Management**: Register and manage caretakers.
4. **Automated Notifications**: Automatically send reminders for rent payments and maintenance tasks.
5. **Command-Line Interface (CLI)**: Simple text-based interface to use the system.
6. **Database Integration**: Store all information securely in a database.


