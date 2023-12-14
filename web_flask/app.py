#!/usr/bin/python3
""" flask web app """

from flask import Flask, render_template, url_for
from models import storage


app = Flask(__name__)


@app.route('/landing_page', strict_slashes=False)
def landing_page():
    """application landing page"""

    return render_template("landing_page.html")


@app.route('/MakeIt', strict_slashes=False)
def makeIt():
    return render_template("index.html")


@app.route('/home', strict_slashes=False)
def home():
    """ home page """
    jobs = [obj.to_dict() for obj in storage.all().values()]

    return render_template("home.html", jobs=jobs)

@app.route('/internships', strict_slashes=False)
def internship():
    """ only internships """
    internships = [obj.to_dict() for obj in storage.all("Intern").values()]

    return render_template("internship.html", internships=internships)

@app.route('/part_time', strict_slashes=False)
def casual():
    """ only casual jobs """
    part_time = [obj.to_dict() for obj in storage.all("Local").values()]

    return render_template("casual.html", part_time=part_time)

@app.route('/full_time', strict_slashes=False)
def officials():
    """ only full time jobs """
    full_time = [obj.to_dict() for obj in storage.all("Official").values()]

    return render_template("officials.html", full_time=full_time)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

