from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars"
mongo = PyMongo(app)

@app.route("/")
def index():
    # grab one item and render
    listings = mongo.db.red_planet.find_one()
    
    return render_template("index.html", listings=listings)


@app.route("/scrape")
def scrape():
   
    #create collection in database
    red_planet = mongo.db.red_planet
    #load table with data from scraper function
    red_planet_data = scrape_mars.scrape()
    red_planet.update({}, red_planet_data, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
