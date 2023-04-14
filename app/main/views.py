from flask import redirect, request, url_for

from app.main import main

@main.route("/")
def index():
    return 'hello!'