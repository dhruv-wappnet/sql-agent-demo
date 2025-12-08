import asyncio
import json
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from agents import Agent, Runner, run_demo_loop, function_tool

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")

engine = create_engine(DATABASE_URL)

@function_tool
def execute_read_query(query: str) -> str:
    """
    Executes a read-only SQL query (SELECT) against the database and returns the results in JSON format.
    
    Args:
        query (str): The SQL SELECT query to execute.
        
    Returns:
        str: A JSON string containing the list of rows (as dictionaries).
    """
    # Basic security check for read-only
    # Note: This is a simple check and can be bypassed. For production, use a read-only DB user.
    if not query.strip().upper().startswith("SELECT"):
        return json.dumps({"error": "Only SELECT queries are allowed."})

    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            # Convert rows to list of dicts
            rows = [dict(row._mapping) for row in result]
            # Serialize to JSON, handling dates/etc via default=str
            return json.dumps(rows, default=str, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@function_tool
def execute_write_query(query: str) -> str:
    """
    Executes a SQL query that modifies the database (INSERT, UPDATE, DELETE, CREATE, ALTER, DROP, etc.).
    
    Args:
        query (str): The SQL query to execute.
        
    Returns:
        str: A JSON string containing the result of the operation.
    """
    try:
        with engine.begin() as connection: # Use begin() for transaction
            result = connection.execute(text(query))
            # For modification queries, result.rowcount might be available
            return json.dumps({"status": "success", "rowcount": result.rowcount, "message": "Query executed successfully."})
    except Exception as e:
        return json.dumps({"error": str(e)})

def get_schema_description() -> str:
    """
    Dynamically fetches the database schema (tables and columns) from the database.
    """
    query = """
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            
            schema_info = {}
            for row in result:
                table = row[0]
                col = row[1]
                dtype = row[2]
                
                if table not in schema_info:
                    schema_info[table] = []
                schema_info[table].append(f"- {col} ({dtype})")
            
            description = "You have access to a PostgreSQL database with the following tables:\n\n"
            for table, columns in schema_info.items():
                description += f"Table: {table}\n" + "\n".join(columns) + "\n\n"
            
            print(description)
            return description
    except Exception as e:
        return f"Error fetching schema: {str(e)}"

# Schema description for the agent
SCHEMA_DESCRIPTION = get_schema_description()

agent = Agent(
    name="DB_Search_Agent",
    instructions=f"""
    You are an expert Database Administrator and Analyst.
    
    {SCHEMA_DESCRIPTION}
    
    Your responsibilities:
    1. Answer user questions by querying the database using `execute_read_query`.
    2. Perform database modifications (CREATE, UPDATE, DELETE) using `execute_write_query`, but ONLY after proposing the SQL to the user and receiving explicit confirmation.
    
    Standard Operating Procedures:
    - **Data Exploration First**: When a user asks for data based on categorical values (like departments, roles, or names), do not guess the exact spelling or casing. First, explore the data (e.g., check distinct values) or use robust matching techniques (like `ILIKE`) to ensure you capture the correct records.
    - **Verify Assumptions**: If a query returns no results, consider if your filter criteria might be too strict or incorrect regarding the data format.
    
    Best Practices for Modifications:
    - When creating summary tables, prefer using `CREATE TABLE ... AS SELECT ...` or `INSERT INTO ... SELECT ...` to populate data dynamically from existing tables.
    - Do NOT hardcode values in INSERT statements if they can be derived from other tables.
    - Maintain relational integrity (e.g., use employee_id instead of just names).
    - Before executing any query, you must know the context. Always check the content of the database if unsure.
    - Always confirm with the user before executing any write operation.

    Communication Style:
    - You MUST include the following sections in EVERY response:
      1. **AI-generated SQL**: The exact SQL query you generated and executed.
      2. **Executed Output**: The raw result from the database (or a formatted table/summary of it).
      3. **Explanation of Schema Understanding**: Briefly explain how you interpreted the request and mapped it to the database schema (e.g., "I joined table X and Y on column Z because...").
    """,
    tools=[execute_read_query, execute_write_query],
    model="gpt-5.1", #litellm
)

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY is not set in the environment. The agent may fail.")
    asyncio.run(run_demo_loop(agent))
