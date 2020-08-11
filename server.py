from flaskr import app
import os

port = int(os.getenv('PORT', 8080))
host = os.getenv('IP', '0.0.0.0')
app.run(host=host, port=port, debug=True)

