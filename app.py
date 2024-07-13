from flask import Flask, render_template, request, redirect, url_for
import datetime
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    client = MongoClient('localhost', 27017)
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
            return redirect(url_for('index'))

        date_filter = request.args.get('date')
        if date_filter:
            entries = app.db.entries.find({"date": date_filter})
        else:
            entries = app.db.entries.find({})

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
        app.run(debug=False , host='0.0.0.0' )

    return app
