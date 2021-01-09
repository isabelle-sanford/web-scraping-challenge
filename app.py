from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo 
import scrape_mars 

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

@app.route("/")
def home():
    # stuff
    # Find one record of data from the mongo database
    mars_record = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", data=mars_record)


@app.route("/scrape")
def scrape():

    mars_data = scrape_mars.scraper()

    print(mars_data)

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)


