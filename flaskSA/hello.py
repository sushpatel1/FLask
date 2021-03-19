# python imports
# third-party imports
# your own imports

from flask import Flask
from markupsafe import escape

from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"
