import io
from io import BufferedReader

import cv2
import numpy as np
from flask import Flask, request, send_file
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


@app.route("/")
def hello_world():
    """Example endpoint returning hello world
    ---
    parameters:
      - name: name
        in: query
        type: string
        required: true
    responses:
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


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/swap", methods=['POST'])
def swap():
    """Uploading 2 files and swapping faces in them
    ---
    parameters:
        - name: image1
          required: true
          in: formData
          type: file
        - name: image2
          required: true
          in: formData
          type: file
    responses:
        200:
            description: success response
    """
    if 'image1' not in request.files:
        return "No image1"
    if 'image2' not in request.files:
        return "No image2"
    image1 = request.files['image1']
    image2 = request.files['image2']

    if image1.filename == '':
        return "image1 is empty"
    if image2.filename == '':
        return "image2 is empty"

    if not (image1 and allowed_file(image1.filename)):
        return "image1 file format not supported"

    if not (image2 and allowed_file(image2.filename)):
        return "image2 file format not supported"

    image1bytes = np.fromfile(image1, np.uint8)

    return send_file(io.BytesIO(image1bytes), mimetype='image/png')
