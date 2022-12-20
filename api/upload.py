import base64
from pprint import pprint

from ariadne import convert_kwargs_to_snake_case


@convert_kwargs_to_snake_case
def resolve_upload_image(obj, info, image_1, image_2):
    filename = image_1.filename
    mimetype = image_1.mimetype
    data = image_1.read()

    data_base64 = base64.b64encode(data).decode('utf-8')

    return {
        'filename': filename,
        'mimetype': mimetype,
        'data': data_base64,
    }
