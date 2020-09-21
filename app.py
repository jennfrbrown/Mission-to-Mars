#Use flask to render a template
from flask import Flask, render_template
#Use pymongo to interact with our Mongo database
from flask_pymongo import PyMongo
#use the scraping code, convert from Jupyter notebook to Python
import scraping

app = Flask(__name__)

#Use flask_pymongo to set up mongo connection
#App will connect to Mongo using a URI, a uniform resource identifier similiar to a URL
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index1.html", mars=mars)

#Defines the route that Flask will be using
@app.route("/scrape")
#Define it
def scrape():
    #Assign a new variable that points to our Mongo database:
    mars = mongo.db.mars
    #Create a new variable to hold the newly scraped data
    mars_data = scraping.scrape_all()
    #update the database using .update(query_parameter, data, options)
    mars.update({}, mars_data, upsert=True)
    #Add a message to let us know that the scraping was successful
    return "Scraping Successful!"

if __name__ == "__main__":
    app.run()
