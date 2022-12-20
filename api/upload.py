import base64
from io import BytesIO
from pprint import pprint

import numpy as np
from PIL import Image
from ariadne import convert_kwargs_to_snake_case

from face_swaps.face_swap import swap_faces


@convert_kwargs_to_snake_case
def resolve_upload_image(obj, info, image_1, image_2):
    print('starting resolve_upload_image')
    filename = image_1.filename
    mimetype = image_1.mimetype
    data = image_1.read()

    print('starting to swapping...')
    output = swap_faces(np.array(Image.open(image_1)),
                        np.array(Image.open(image_2)))

    image_io = BytesIO()
    res = Image.fromarray(output)
    res.save(image_io, 'JPEG')
    image_io.seek(0)

    pprint(image_io)

    data_base64 = base64.b64encode(image_io.read()).decode('utf-8')

    return {
        'filename': filename,
        'mimetype': mimetype,
        'data': data_base64,
    }
