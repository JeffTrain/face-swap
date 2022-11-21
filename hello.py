from io import BytesIO
from urllib.parse import unquote

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from flask import Flask, request, send_file
from flasgger import Swagger

from face_swaps.face_swap import swap_faces

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

    print("starting to swapping!")
    output = swap_faces(np.array(Image.open(image1)),
                        np.array(Image.open(image2)))
    print("swapped!")

    image_io = BytesIO()
    res = Image.fromarray(output)
    res.save(image_io, 'JPEG')
    image_io.seek(0)

    return send_file(image_io, mimetype='image/png')


@app.route("/text2img", methods=['GET'])
def text2img():
    """Convert text to image
    ---
    parameters:
        - name: text
          required: true
          in: query
          type: string
    responses:
        200:
            description: success response
    """
    text = request.args.get('text')
    if text is None:
        return "No text"

    text = unquote(text).encode('utf-8')

    print("starting to convert!: ", text)

    im = Image.new('RGB', (1000, 30), color=(73, 109, 137))
    draw = ImageDraw.Draw(im)
    draw.text((10, 10), text, fill=(255, 255, 0))
    image_io = BytesIO()
    im.save(image_io, 'JPEG')
    image_io.seek(0)
    return send_file(image_io, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
