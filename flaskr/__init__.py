from flask import Flask
from flask_bootstrap import Bootstrap
import sys

app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)

print("Starting Flask")
sys.stdout.flush()

from flaskr import views