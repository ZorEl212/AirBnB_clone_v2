#!/usr/bin/python3

"""
starts a Flask web application
"""


from flask import Flask, render_template, abort
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Close database connection after the request"""
    storage.close()


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states_list(id=None):
    """Fetch all states """
    all_states = storage.all('State')
    if id:
        key = "State." + id
        state = all_states.get(key)
        if not state:
            return abort(404)
        return render_template('9-states.html', state=state)
    else:
        all_states = sorted(list(all_states.values()), key=lambda x: x.name)
        return render_template('9-states.html', states_list=all_states)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
