#! /usr/bin/env python

import sys
import cv2

from face_swaps.face_swap import swap_faces


if __name__ == '__main__':

    # Make sure OpenCV is version 3.0 or above
    (major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')

    if int(major_ver) < 3:
        print >> sys.stderr, 'ERROR: Script needs OpenCV 3.0 or higher'
        sys.exit(1)

    print(sys.argv)
    # Read images
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]

    img1 = cv2.imread(filename1)
    img2 = cv2.imread(filename2)

    output = swap_faces(img1, img2)

    cv2.imwrite('result.jpg', output)

    cv2.imshow("Face Swapped", output)
    cv2.waitKey(0)

    cv2.destroyAllWindows()
