import cv2
import dlib
import os.path

video_capture = cv2.VideoCapture(0)
face_detector = dlib.get_frontal_face_detector()

dir_path = os.path.dirname(os.path.realpath(__file__))
landmark_file_path = os.path.realpath(os.path.join(dir_path, './face_swaps/shape_predictor_68_face_landmarks.dat'))
predictor = dlib.shape_predictor(landmark_file_path)


def rect_to_bounding_box(face_rect):
    x = face_rect.left()
    y = face_rect.top()
    w = face_rect.right() - x
    h = face_rect.bottom() - y

    return x, y, w, h


def trace_face(frm):
    scale = 200 / min(frm.shape[0], frm.shape[1])
    thumb = cv2.resize(frm, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(thumb, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray, 1)

    for i, face_rect in enumerate(faces):
        (x, y, w, h) = rect_to_bounding_box(face_rect)
        cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return gray


while True:
    ret, frame = video_capture.read()
    face_trace_frame = trace_face(frame)
    cv2.imshow('Video', face_trace_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
