from datetime import datetime, timedelta
from io import BytesIO
from urllib.parse import unquote

import numpy as np
from PIL import Image, ImageDraw
from ariadne import load_schema_from_path, graphql_sync, snake_case_fallback_resolvers, ObjectType, \
    combine_multipart_data, upload_scalar
from ariadne.constants import PLAYGROUND_HTML
from ariadne.contrib.federation import make_federated_schema
from flasgger import Swagger
from flask import Flask, request, send_file, jsonify, json
from flask_cors import CORS

from api.greeting import greeting_resolver
from api.video import video_resolver, getVideoSrc, get_video_src_and_set_cache, cache_job
from api.upload import resolve_upload_image
from cache.cache import cache
from face_swaps.face_swap import swap_faces, readLandmarkPoints
from apscheduler.schedulers.background import BackgroundScheduler


query = ObjectType("Query")
query.set_field('greeting', greeting_resolver)
query.set_field('video', video_resolver)

mutation = ObjectType("Mutation")
mutation.set_field("uploadImage", resolve_upload_image)
mutation.set_field("setVideoSrcCache", get_video_src_and_set_cache)

type_defs = load_schema_from_path("schema.graphql")

schema = make_federated_schema(
    type_defs, snake_case_fallback_resolvers, query, mutation, upload_scalar
)

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    if request.content_type.startswith("multipart/form-data"):
        data = combine_multipart_data(
            json.loads(request.form.get("operations")),
            json.loads(request.form.get("map")),
            dict(request.files)
        )
    else:
        data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code


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


@app.route("/landmark", methods=['POST'])
def landmark():
    """Upload a photo and get its face landmarks
    ---
    parameters:
        - name: image
          required: true
          in: formData
          type: file
    responses:
        200:
            description: success response
    """
    if 'image' not in request.files:
        return "No image"

    image = request.files['image']

    if image.filename == '':
        return "image is empty"

    return readLandmarkPoints(np.array(Image.open(image)))


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


@app.after_request
def apply_caching(response):
    then = datetime.now() + timedelta(weeks=54)

    response.headers.add('Expires', then.strftime("%a, %d %b %Y %H:%M:%S GMT"))
    response.headers.add('Cache-Control', 'public,max-age=%d,s-maxage=%d' % (int(60 * 60 * 24 * 365), int(60 * 60 * 24 * 365)))
    return response


cache.init_app(app)


scheduler = BackgroundScheduler()
job = scheduler.add_job(func=cache_job, trigger="interval", hours=3)
scheduler.start()


if __name__ == '__main__':
    src = getVideoSrc()
    cache.set('video_src', src)
    app.run(host='0.0.0.0', port=5000, debug=True)
