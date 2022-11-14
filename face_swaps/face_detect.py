import os

import cv2

from face_swaps.face_swap import face_detector


def rect_to_bounding_box(face_rect):
    x = face_rect.left()
    y = face_rect.top()
    w = face_rect.right() - x
    h = face_rect.bottom() - y

    return x, y, w, h


def scale_rect(param, scale):
    (x, y, w, h) = param
    return int(x / scale), int(y / scale), int(w / scale), int(h / scale)


def face_marked(img):
    scale = 200 / min(img.shape[1], img.shape[0])
    thumb = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(thumb, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray, 1)

    for i, face_rect in enumerate(faces):
        (x, y, w, h) = scale_rect(rect_to_bounding_box(face_rect), scale)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return img


def face_marked2(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cascade_classifier_file = 'haarcascade_frontalface_alt2.xml'
    full_path = os.path.realpath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), './' + cascade_classifier_file))

    face_cascade = cv2.CascadeClassifier(cascade_classifier_file)
    face_cascade.load(full_path)
    faces = face_cascade.detectMultiScale(gray)
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return img
