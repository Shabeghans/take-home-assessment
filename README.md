# 🧠 Take-Home Assessment: Financial Data Agent Using Google ADK

Build a simple AI agent system that can answer financial questions about semiconductor companies using structured SQL data. You will use [Google's Agent Development Kit (ADK)](https://google.github.io/adk-docs/) to create:

1. **A Primary Agent** – receives the user’s query.
2. **A Data Agent** – has access to a tool that:
   - Generates SQL queries from natural language questions.
   - Executes them on a SQLite database.

## Instructions

1.  Clone the repository:

    ```bash
    git clone https://github.com/Shabeghans/take-home-assessment.git
    ```

    This repository contains the following files:

    -   `agent.py`:  Where agents and tools are defined, along with the logic for running the agents.  The basic setup is already provided. The primary task is to define the agents and tools.
    -   `data_handling.py`:  Used to create the database from the provided `semiconductor_data.csv` (SQLite is recommended).
    -   `semiconductor_data.csv`: Contains the financial data for semiconductor companies.
    -   `requirements.txt`: Lists the Python packages required for this project.
    -   `README.md`: This file.

2.  Create and activate a Python virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  Install the required packages using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

    If you encounter issues with `requirements.txt`, install the packages individually:

    ```bash
    pip install google-adk
    pip install pandas
    pip install python-dotenv
    ```

4.  Before adding any code, test the setup by running:

    ```bash
    python agent.py
    ```

    This will run a test query to ensure the environment and basic setup are working.

5.  Create the database using `data_handling.py`:

    -   Load `semiconductor_data.csv` using pandas.
    -   Convert the data into a SQLite database (e.g., `semiconductor_data.db`).
    -   Extract the `CREATE TABLE` statement (or the table schema) and save it to a text file (e.g., `schema.txt`).  This schema information will be crucial for providing context to the Data Agent.

6.  Define agents and tools in `agent.py`:

    -   **Data Agent (LlmAgent):**
        -   This agent should have knowledge of the database schema (column names, data types).
        -   Its purpose is to generate SQL queries from natural language questions.
        -   It utilizes a tool to execute these SQL queries against the database.

    -   **SQL Query Tool:**
        -   Accepts SQL queries as input.
        -   Connects to the SQLite database.
        -   Executes the query and returns the result.

    -   **Primary Agent:**
        -   Accepts user questions.
        -   Delegates the question to the Data Agent for SQL generation and execution.
        -   Consolidates the results and generates the final response for the user.

7.  Test your implementation by running the commented queries at the bottom of `agent.py`.

## Key Considerations

-   **Context is King:** The Data Agent needs comprehensive context regarding the database schema.  The `CREATE TABLE` statement or schema representation is crucial for effective SQL query generation.

-   **Prompting is Paramount:** Well-crafted prompts and instructions for each agent are essential for directing their behavior and ensuring accurate responses. Pay careful attention to providing clear and concise instructions.
