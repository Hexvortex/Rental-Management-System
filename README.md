
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

## Authors
- **Griffins Mbae**
  - Phone: 0743269238
  - Email: griffinskirimimbae@gmail.com

