#!/usr/bin/python3
""" Flask app that display all
    states on route /state_list
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states():
    """Returns list of state"""
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def tear_down(td):
    """close session when application context in popped"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
