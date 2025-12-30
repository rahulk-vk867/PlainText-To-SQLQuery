import os
import requests
import psycopg2
from dotenv import load_dotenv
from functools import lru_cache
from psycopg2 import pool
import google.generativeai as genai

# Load spaCy model
# Load environment variables from .env file
load_dotenv()

# Access API keys and database URL from environment variables
gemini_api_key = os.getenv("API_KEY")

# Configure the GenAI client
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

if gemini_api_key is None:
    raise ValueError("API_KEY not found in environment variables")

# Create a connection pool
connection_pool = pool.SimpleConnectionPool(
    1, 20,
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME")
)

def clean_sql_query(query):
    query = query.replace('```sql', '').replace('```', '').strip()
    return query.strip()

@lru_cache(maxsize=1)
def get_table_schema():
    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name, column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'public'
        """)
        schema_info = cur.fetchall()
        schema_str = ""
        for table, column, data_type in schema_info:
            schema_str += f"Table: {table}, Column: {column}, Type: {data_type}\n"
        return schema_str
    except psycopg2.Error as e:
        print(f"Error fetching schema: {e}")
        return ""
    finally:
        if cur:
            cur.close()
        if conn:
            connection_pool.putconn(conn)

@lru_cache(maxsize=1)
def get_table_names():
    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        table_names = [table[0] for table in tables]
        return table_names
    except psycopg2.Error as e:
        print(f"Error fetching table names: {e}")
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            connection_pool.putconn(conn)

def generate_sql_query(natural_language_query):
    try:
        # Validate the input
        if not isinstance(natural_language_query, str) or len(natural_language_query) < 1:
            return "Invalid input.Please enter a valid natural language query."

        # Check if table name is mentioned
        table_names = get_table_names()
        if not any(table_name.lower() in natural_language_query.lower() for table_name in table_names):
            return "Please mention the table name in your query."

        # Use the Gemini API to generate a SQL query
        schema_info = get_table_schema()
        prompt = f"""Generate a PostgreSQL query for: {natural_language_query}. 
Use the following schema information:
{schema_info}
Return only the SQL query without any explanations or markdown formatting. 
Ensure to use ILIKE for case-insensitive text comparisons where appropriate."""

        response = model.generate_content(prompt)
        generated_text = response.text
        cleaned_query = clean_sql_query(generated_text)

        print(f"Generated SQL Query: {cleaned_query}")  # Debugging output
        return cleaned_query
    except Exception as e:
        print(f"Error generating SQL query: {e}")  # More detailed error logging
        return "Error generating SQL query: {}".format(e)

def execute_sql_query(sql_query):
    try:
        # Execute the SQL query
        conn = connection_pool.getconn()
        cur = conn.cursor()
        print(f"Executing SQL query: {sql_query}")  # Debugging output
        cur.execute(sql_query)
        column_names = [desc[0] for desc in cur.description] if cur.description else []
        result = cur.fetchall() if cur.description else []
        print(f"Column Names: {column_names}")  # Debugging output
        print(f"Query Result: {result}")  # Debugging output

        if not result:
            return "No rows selected", None, None
        else:
            row_count = len(result)
            return column_names, result, row_count
    except psycopg2.Error as e:
        print(f"Error executing SQL query: {e}")
        return "Error executing SQL query: {}".format(e), None, None