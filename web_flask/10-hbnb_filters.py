#!/usr/bin/python3

"""
starts a Flask web application
"""


from flask import Flask, render_template, abort
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity

app = Flask(__name__, static_folder='static')



@app.teardown_appcontext
def teardown_db(exception):
    """Close database connection after the request"""
    storage.close()

@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """Fetch all states and amenities"""
    all_states = storage.all(State).values()
    all_amenities = storage.all(Amenity).values()
    return render_template('10-hbnb_filters.html', states=all_states,
                           amenities=all_amenities)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")