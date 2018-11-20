import requests
from enum import Enum

class SessionType(Enum):
    Tuning = 'tuning_session'
    Random = 'randomly_generate'
    NoTuning = 'no_tuning_session'

def create_new_user():
    URL = 'http://0.0.0.0:8000/signup'
    payload = {
        'csrfmiddlewaretoken': 'sodRmGxyAUUow3FX5uk2K7N2HxSZqEpsS5YbVQRHLp6LSGmjxXxmyIfGmrj2Qzc0',
        'username': 'suafeng1',
        'email': 'suafeng@gmail.com',
        'password1': 'abcd123',
        'password2': 'abcd123',
        'submit': 'submit-value'
    }

    session = requests.session()
    r = requests.post(URL, data=payload)
    return session

def create_new_project():
    URL = 'http://0.0.0.0:8000/projects/new/'
    payload = {
        'name': 'os tuning',
        'description': ''
    }
    r = requests.post(URL, data=payload)

def create_new_session(session_type=SessionType.Random):
    URL = 'http://0.0.0.0:8000/projects/1/sessions/new/'
    payload = {
        'name': 'session 1',
        'description': '',
        'dbms': '10',
        'tuning_session': session_type.value,
        'target_objective': '99th_lat_ms'
    }
    r = requests.post(URL, data=payload)

def get_upload_code():
    URL = 'http://0.0.0.0:8000/projects/1/sessions/1/'
    text_content = requests.get(URL).text

create_new_user()
