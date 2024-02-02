#!/usr/bin/python3

"""
starts a Flask web application
"""


from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Close database connection after the request"""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Fetch all states """
    all_states = storage.all('State')
    all_states = sorted(list(all_states.values()), key=lambda x: x.name)
    return render_template('7-states_list.html', states_list=all_states)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
