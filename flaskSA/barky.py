from flask import (
     flash, g, redirect, render_template, request, url_for
)
from datetime import datetime, date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm import session


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmark.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Bookmarks(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   title = db.Column(db.String(100), nullable=False)
   url = db.Column(db.String(50), nullable=False)  
   notes = db.Column(db.String(200))
   date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


   def __init__(self, title, url, notes,date_added):
    self.title = title
    self.url = url
    self.notes = notes
    self.date_added = date_added


@app.route("/")
def index():
    bookmark = Bookmarks.query.all()
    app.logger.debug(bookmark)
    return render_template("index.html", bookmark=bookmark)


@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        Title = request.form["title"]
        Url = request.form["url"]
        Note = request.form["notes"]

        bookmark = Bookmarks(title=Title,url=Url,notes=Note,date_added=datetime.now())
        db.session.add(bookmark)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("create.html")

@app.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    x = Bookmarks.query.get_or_404(id) 
  
    if request.method == "POST":
       Title = request.form["title"]
       Url = request.form["url"]
       Note = request.form["notes"]
       error = None

       if error is not None:
            flash(error)
       else:  
        x.title = Title
        x.url = Url
        x.notes = Note
        db.session.commit()
       return redirect(url_for("index"))
  
    return render_template("update.html", bookmark=x)
    
@app.route("/delete/<int:id>", methods=("GET", "POST"))
def delete(id):
    if request.method == "POST":
     x = Bookmarks.query.get_or_404(id)   
     db.session.delete(x)   
     db.session.commit()
     return redirect("/")
    else:
       return redirect("/")  


if __name__ == "__main__":
    # if the database doesn't exist, create it an all associated entities
    db.drop_all()
    db.create_all()
    app.run(debug=True)
