from flask import Flask, render_template, request
from api import generate_sql_query, execute_sql_query
import time

app = Flask(__name__)

# Print a startup message
print("Starting Flask app...")
@app.route('/', methods=['GET', 'POST'])
def index():
    sql_query = None
    result = None
    error = None
    processing_time = None
    row_count = None
    natural_language_query = ''
    column_names = None

    # Indicate we are handling a request
    print("Handling request...")

    if request.method == 'POST':
        action = request.form['action']
        start_time = time.time()

        if action == 'Generate Query':
            natural_language_query = request.form.get('query', '').strip()
            sql_query = generate_sql_query(natural_language_query)
            if sql_query.startswith("Please"):
                error = sql_query
                sql_query = None
        elif action == 'Execute Query':
            sql_query = request.form.get('sql_query', '').strip()
            natural_language_query = request.form.get('query', '').strip()
            column_names, result, row_count = execute_sql_query(sql_query)
            if column_names is None and result is None:
                error = "Error executing the SQL query."
            elif result is None:
                error = "No rows selected."
            else:
                result = (column_names, result)
        processing_time = f"{time.time() - start_time:.2f} seconds"

    return render_template(
        'index.html',
        sql_query=sql_query,
        result=result,
        error=error,
        processing_time=processing_time,
        natural_language_query=natural_language_query,
        row_count=row_count
    )

if __name__ == '__main__':
    app.run(debug=True)
