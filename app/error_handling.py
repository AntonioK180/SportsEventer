from app import app
from flask import render_template


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html")
