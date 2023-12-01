from flask import Flask, render_template, request
import datetime 
import sys
import os
print(sys.path)
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog
 
    @app.route("/", methods=["GET", "POST"])
    def home():
        print([e for e in app.db.entries.find({})])
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content":entry_content, "date":formatted_date})

            entries_with_date = [
                (
                    entry["content"],
                    entry["date"],
                    datetime.datetime.strptime(entry["date"],"%Y-%m-%d").strftime("%b %d")
                )
                for entry in app.db.entries.find({})
            ]
                # entries.append((entry_content, formatted_date))
            return render_template("index.html", entries=entries_with_date or [])
        
        if request.method == "GET":
            return render_template("index.html", entries=[])
    return app