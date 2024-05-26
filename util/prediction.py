import cv2
import subprocess
import numpy as np

from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image

face_cascade = cv2.CascadeClassifier('files/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('files/haarcascade_eye.xml')

"""
Class #0 = distracted
Class #1 = focused
"""

# convert opencv output video
def convert_to_x264(input_file, output_file):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-c:v', 'libx264',
        '-crf', '23',
        '-preset', 'medium',
        output_file
    ]
    result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    if result.returncode != 0:
        print("ffmpeg error:")
        print(result.stderr.decode())
    else:
        print("ffmpeg output:")
        print(result.stdout.decode())

# distraction predict
def video_predict(file, output_video_path):
    # Capture
    cap = cv2.VideoCapture(file)

    # Dummy ground truth labels
    cls_list = ['distracted', 'focused']

    emotion_id = -1
    accuracy_values = []
    frame_intervals = []

    # Recording
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc_mp4 = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc_mp4, frame_fps, (frame_width, frame_height)) #isColor = False

    scale_factor = 1.1
    min_neighbours_for_faces = 5
    min_neighbours_for_eyes = 5
    min_size_w = 240
    min_size_h = 240
    min_size_w_eye = 60
    min_size_h_eye = 60

    # load the trained model
    net = load_model('files/model-resnet50-final.h5')

    # Stream data
    total_frames = 0
    label_text = ''

    while True:
        ret, img = cap.read()
        if ret == False:
            break
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,scaleFactor=scale_factor,minNeighbors=min_neighbours_for_faces,minSize=(min_size_w,min_size_h),flags=cv2.CASCADE_SCALE_IMAGE)

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            
            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=scale_factor,minNeighbors=min_neighbours_for_eyes,minSize=(min_size_w_eye,min_size_w_eye))
            
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

                roi = roi_color[ey+2:ey+eh-2, ex+2:ex+ew-2]
                roi = cv2.resize(roi, (224, 224))
                roi = image.img_to_array(roi)
                roi = preprocess_input(roi)
                roi = np.expand_dims(roi, axis=0)
                
                pred = net.predict(roi)[0]
                top_inds = pred.argsort()[::-1][:5]

                label_text = cls_list[top_inds[0]]
                emotion_id = top_inds[0]

                for i in top_inds:
                    print('    {:.3f}  {}'.format(pred[i], cls_list[i]))

            cv2.putText(img, label_text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3, cv2.LINE_AA)

            # Frames
            total_frames += 1
            cv2.putText(img, f"Frames: {total_frames}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            out.write(img)

    cap.release()
    out.release()