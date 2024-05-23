import cv2
import datetime

face_cascade = cv2.CascadeClassifier('files/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('files/haarcascade_eye.xml')

def video_predict(file):
    # Capture
    cap = cv2.VideoCapture(file)

    # Recording
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    output_video_path = f'output_{datetime.date.today()}.mp4' 
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 10, (frame_width, frame_height))

    scale_factor = 1.1
    min_neighbours_for_faces = 5
    min_neighbours_for_eyes = 5
    min_size_w = 240
    min_size_h = 240
    min_size_w_eye = 60
    min_size_h_eye = 60

    # Stream data
    total_frames = 0

    while True:
        ret, img = cap.read()
        if ret == False:
            break
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,scaleFactor=scale_factor,minNeighbors=min_neighbours_for_faces,minSize=(min_size_w,min_size_h),flags=cv2.CASCADE_SCALE_IMAGE)

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            # Frames
            total_frames += 1
            cv2.putText(img, f"Frames: {total_frames}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

            out.write(img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    return output_video_path