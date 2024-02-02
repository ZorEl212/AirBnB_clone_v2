#!/usr/bin/python3

"""Create cities by cities route for the flask app"""


from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)

@app.teardown_request
def teardown_request(exception):
    """Close database connection after the request"""
    print("Teardown function executed!")
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Fetch all states """
    all_states = storage.all('State')
    all_states = sorted(list(all_states.values()), key=lambda x: x.name)
    return render_template('7-states_list.html', states_list=all_states)



@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """display the states and cities listed in alphabetical order"""
    states = storage.all("State").values()
    return render_template('8-cities_by_states.html', states=states)


if __name__ == "__main__":
    app.run(debug=True)
