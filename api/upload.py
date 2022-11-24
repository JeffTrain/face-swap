from ariadne import convert_kwargs_to_snake_case


@convert_kwargs_to_snake_case
def resolve_upload_image(obj, info, image_1, image_2):
    return image_1

