```markdown
# Rental Management System

## Overview
The Rental Management System is designed to streamline the management of rental properties, tenants, and caretakers. It offers a comprehensive solution for property managers to efficiently handle their operations.

## Components
- **main.py**: Main entry point for running the application.
- **models.py**: Defines the database schema.
- **database.py**: Manages database connections and operations.
- **cli.py**: Command Line Interface for user interactions.
- **register_caretaker.py**: Script to register new caretakers.
- **create_new_db.py**: Script to create a new database.
- **bot.py**: Handles automated tasks and notifications.
- **.env**: Environment variables for configuration.
- **Pipfile** and **Pipfile.lock**: Manage project dependencies.
- **rental_management.db**, **rental_management_backup.db**, and **sss.db**: Database files storing rental management data.

## Setup and Installation
1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd rental_management
   ```
2. Create a virtual environment and install dependencies:
   ```sh
   pipenv install
   ```
3. Create a `.env` file with the necessary environment variables (e.g., database credentials):
   ```sh
   touch .env
   # Add your environment variables in the .env file
   ```
4. Initialize the database:
   ```sh
   python create_new_db.py
   ```
5. Register caretakers using:
   ```sh
   python register_caretaker.py
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

## Authors
- **Griffins Mbae**
  - Phone: 0743269238
  - Email: griffinskirimimbae@gmail.com
```
