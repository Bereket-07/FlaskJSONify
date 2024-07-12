import os
from flask import request , Flask , jsonify, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import db , Question,Questionares,Choices,Answers
from services import get_users , get_by_questioner_id
from flask_session import Session

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

@app.route('/users', methods=['GET'])
def get_usersRoute():
    return get_users()

@app.route('/users/<int:user_id>', methods=['GET'])
def get_data_using_questioner_id(user_id):
    return get_by_questioner_id(user_id)


if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000)