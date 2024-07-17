import os
from flask import render_template, request , Flask , jsonify, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import db , Question,Questionares,Choices,Answers
from services import get_users , get_by_questioner_id
from flask_session import Session
from main import process_data, chat_with_groq

# load environment variables
load_dotenv()
# initialize flask app
app = Flask(__name__)
# Configure server-side session
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set a secret key for session management
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
# set a secret key for session management
app.config['SECRET_KEY']=os.getenv("FLASK_SECRET_KEY","default_secret_key")

# database configuration

db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'analytics')
}

# Example usage (for Flask SQLAlchemy setup)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# Initilize SQLAlchemy

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_usersRoute():
    return get_users()

@app.route('/users/<int:user_id>', methods=['GET'])
def get_data_using_questioner_id(user_id):
    return get_by_questioner_id(user_id)
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    # Assuming you have some way to get the user_id, e.g., from session or request
    user_id = 1
    processed_data = process_data(user_id)
    if not processed_data:
        return jsonify({"error": "Failed to fetch data"}), 400
    
    chat_response = chat_with_groq(processed_data, user_message)
    return jsonify({"response": chat_response})
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000)