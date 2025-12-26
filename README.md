# PlainText-To-SQLQuery 🤖💾

A Python-based application that leverages Natural Language Processing (NLP) to convert plain English text into functional SQL queries. The application also runs the generated SQL query on the database, provided by the user and displays the resulted rows. This project uses a Flask web interface to make database interaction intuitive for non-technical users.

## 🚀 Features

Natural Language Processing: Converts plain text into SQL queries

Flask Web UI: Clean, browser-based interface

Backend API: Modular query-generation logic in api.py

## 🛠️ Installation & Setup

Follow these steps to run the project locally.

### 1️⃣ Clone the Repository
git clone https://github.com/rahulk-vk867/PlainText-To-SQLQuery.git

cd PlainText-To-SQLQuery

### 2️⃣ Create and Activate a Virtual Environment
Create virtual environment
python -m venv venv


Activate it (Windows):

.\venv\Scripts\activate


Activate it (Mac/Linux):

source venv/bin/activate

### 3️⃣ Install Dependencies
pip install -r requirements.txt

## ⚙️ Configuration (.env)

The application uses an .env file to store sensitive configuration.
Since .env is ignored by Git, you must create it manually.

Create a file named .env in the project root and add:

### Configuration for SQL Generator
API_KEY=your_actual_api_key_here

DATABASE_URL=your_database_path_or_url



⚠️ Replace the placeholder values with your actual credentials.

## 🏃 How to Run

Start the application:

python app.py


Open your browser and visit:

http://127.0.0.1:5000

📁 Project Structure
SQL PROJECT/

├── app.py              # Main Flask application

├── api.py              # Text-to-SQL processing logic

├── templates/index.html      # Frontend UI

├── requirements.txt    # Python dependencies

├── .gitignore          # Ignored files (env, cache, etc.)

🤝 Contributing

Feel free to fork this repository, submit pull requests, or report issues.
Contributions are always welcome! 🚀
