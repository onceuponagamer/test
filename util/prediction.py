import cv2
import subprocess
#import datetime

face_cascade = cv2.CascadeClassifier('files/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('files/haarcascade_eye.xml')

def video_predict(file, output_video_path):
    # Capture
    cap = cv2.VideoCapture(file)

    # Recording
    #frame_width = int(cap.get(3))
    #frame_height = int(cap.get(4))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_fps = cap.get(cv2.CAP_PROP_FPS)

    #output_video_path = f'output_{datetime.date.today()}.mp4' 
    #out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 10, (frame_width, frame_height))
    fourcc_mp4 = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc_mp4, frame_fps, (frame_width, frame_height),isColor = False)

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

    cap.release()
    out.release()

    convertedVideo = "./h264.mp4"
    subprocess.call(args=f"ffmpeg -y -i {output_video_path} -c:v libx264 {convertedVideo}".split(" "))

    return convertedVideo