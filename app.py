from flask import Flask, render_template, redirect
import scrape

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

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

@app.route("/scrape")
def scraper():
    mars_data = scrape.scrape()
    db.mars.drop()
    db.mars.insert(mars_data)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
