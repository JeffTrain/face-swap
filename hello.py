from flask import Flask
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/")
def hello_world():
    """Example endpoint returning hello world
    ---
    :parameters:
      - name: name
        in: query
        type: string
        required: true
    :responses:
      200:
        description: A single user item
        schema:
          id: User
          properties:
            username:
              type: string
              description: The name of the user
              default: 'admin'
    """
    return "<p>Hello, World!</p>"
