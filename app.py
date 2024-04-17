from flask import Flask, render_template, request, redirect, session, jsonify
import os

from werkzeug.utils import secure_filename
import redis
from redis.exceptions import RedisError
from uuid import uuid4
import json

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
if not app.secret_key:
    raise RuntimeError("Secret key not set in environment variables")

# Redis Configuration for session handling and data caching
try:
    redis_client = redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=os.getenv('REDIS_PORT', 6379),
        password=os.getenv('REDIS_PASSWORD'),
        ssl=os.getenv('REDIS_SSL', 'False').lower() in ['true', '1', 't'],
        decode_responses=True  # Automatically decode responses to Unicode, use it if you prefer not handling decoding manually
    )
except RedisError as e:
    print(f"Redis connection error: {e}")


@app.route('/results')
def results():
    session_id = get_session_id()
    students_info = get_data_from_cache(session_id)
    return render_template('results.html', students=students_info)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/team', methods=['GET'])
def team():
    return render_template('team.html')


@app.route('/vamp_test', methods=['GET', 'POST'])
def vamp_test():
    if request.method == 'POST':
        session_id = get_session_id()
        student_info = {
            'name': request.form['name'],
            'has_shadow': request.form.get('shadow') == 'True',
            'complexion': request.form['complexion'],
            'dislike_garlic': request.form.get('garlic') == 'True',
            'accent': request.form.get('accent') == 'True',
            'vampire_score': 0,
            'vampire_likelihood': 'low'
        }

        # Calculate vampire score and likelihood
        if not student_info['has_shadow']:
            student_info['vampire_score'] += 2
        if student_info['complexion'] == 'Pale':
            student_info['vampire_score'] += 1
        if student_info['dislike_garlic']:
            student_info['vampire_score'] += 1
        if student_info['accent']:
            student_info['vampire_score'] += 1

        # Determine vampire likelihood and map to numeric value
        likelihood = 'high' if student_info['vampire_score'] >= 3 else 'medium' if student_info['vampire_score'] == 2 else 'low'
        likelihood_mapping = {'low': 0.1, 'medium': 0.5, 'high': 0.9}
        student_info['vampire_likelihood'] = likelihood_mapping[likelihood]

        # Store student data in Redis using the function designed to handle list storage
        store_data_in_cache(student_info, session_id)

        return redirect('/results?session_id=' + session_id)
    return render_template('vamp_test.html')


# This function checks and clears the key if it exists and is of the wrong type
def clear_redis_key(key):
    try:
        type = redis_client.type(key)
        if type != 'none' and type != 'list':
            redis_client.delete(key)
            print(f"Cleared key {key} as it was of type {type}")
    except Exception as e:
        print(f"Error clearing Redis key {key}: {e}")

# Example of using the function before storing data
# clear_redis_key(session_id)


def store_data_in_cache(data, session_key):
    try:
        # Serialize data to a JSON string
        data_json = json.dumps(data)
        # Check and clear key if necessary
        clear_redis_key(session_key)
        # Append the serialized student data to the list of students under the session key
        redis_client.rpush(session_key, data_json)
        print(f"Storing data for session_key: {session_key} - Storage successful")
    except Exception as e:
        print(f"Error while storing data in cache for session_key {session_key}: {e}")


def get_data_from_cache(session_key):
    try:
        # Ensure the key is cleared if the type is wrong
        clear_redis_key(session_key)
        # Retrieve all student data from the list in Redis
        data_json_list = redis_client.lrange(session_key, 0, -1)
        students = [json.loads(data_json) for data_json in data_json_list if data_json]
        if students:
            print(f"Retrieving data for session_key: {session_key} - Data retrieval successful")
            return students
        else:
            print(f"Retrieving data for session_key: {session_key} - No data found in cache")
            return None
    except Exception as e:
        print(f"Error retrieving data from cache for session_key {session_key}: {e}")
        return None


def get_session_id():
    """Generate or retrieve a unique session ID."""
    if 'session_id' not in session:
        session['session_id'] = str(uuid4())
    return session['session_id']


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
