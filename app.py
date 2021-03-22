from flask import Flask, render_template, redirect

#import our scrape.py 
import scrape

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

#connect to mongo database
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db

# Set route
@app.route('/')
def index():
    # Store the entire team collection in a list
    data = list(db.mars.find())

    # Return the template with the teams list passed in
    return render_template('index.html', data=data[0])

#page visited by button
@app.route("/scrape")
def scraper():
    #run scrape function
    mars_data = scrape.scrape()

    #load result into MongaDB
    db.mars.drop()
    db.mars.insert(mars_data)

    #redirect to home
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
