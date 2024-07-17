from flask import Flask, render_template, request, redirect, url_for
import datetime
from pymongo import MongoClient
import os

app = Flask(__name__)

mongodb_username = os.environ.get('MONGODB_USERNAME')
mongodb_password = os.environ.get('MONGODB_PASSWORD')

print(f"MongoDB Username: {mongodb_username}")
print(f"MongoDB Password: {mongodb_password}")

mongodb_uri = f"mongodb+srv://{mongodb_username}:{mongodb_password}@cluster-1.wlgfddo.mongodb.net/?tls=true"

client = MongoClient(mongodb_uri)
app.db = client.microblog

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        entry_content = request.form.get("content")
        formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
        app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
        return redirect(url_for('index'))

    date_filter = request.args.get('date')
    if date_filter:
        entries = app.db.entries.find({"date": date_filter})
    else:
        entries = app.db.entries.find({}).sort("date" , -1)

    entries_with_date = [
        (
            entry["content"],
            entry["date"],
            datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
        )
        for entry in entries  # Use the filtered entries
    ]
    no_entries = len(entries_with_date) == 0

    return render_template("index.html", entries=entries_with_date, no_entries=no_entries)

if __name__ == '__main__':
    app.run(debug=False )
