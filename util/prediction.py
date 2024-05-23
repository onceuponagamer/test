import cv2

face_cascade = cv2.CascadeClassifier('files/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('files/haarcascade_eye.xml')

def video_predict(file):
    cap = cv2.VideoCapture(file)

    while True:
        ret, img = cap.read()
        if ret == False:
            break

        cv2.imshow('Distraction Detection', img)

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)