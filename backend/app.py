"""Module containing main app for HBnB project"""
from services.Initializer.initializer import initialize_services
from services.Initializer.create_app import FlaskApp

app = FlaskApp().get_app()

initialize_services()

app.options = {
    'bind': '0.0.0.0:8000',
    'workers': 2,
    'threads': 2,
    'accesslog': '-',
    'access_log_format': '%(h)s - - [%(t)s] "%(r)s" %(s)s "%(f)s"',
}


@app.get('/')
def index():
    return "Hi!"
