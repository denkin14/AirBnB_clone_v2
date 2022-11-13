#!/usr/bin/python3
""" Flask app that display all
    states on route /cities_by_states
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def states():
    """Returns list of cities per state"""
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def tear_down(td):
    """close session when application context in popped"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
