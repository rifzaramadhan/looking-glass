from flask import Flask

app = Flask(__name__)
app.secret_key = '5ur4b4y4'

from app import routes
from app import command