import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode, RTCConfiguration
import cv2
import av
import numpy as np

from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

face_cascade = cv2.CascadeClassifier('files/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('files/haarcascade_eye.xml')

cls_list = ['distracted', 'focused']
#emotion_id = -1
label_text = ''

# load the trained model
net = load_model('files/model-resnet50-final.h5')

def process(img):
    global cls_list, label_text, net, face_cascade, eye_cascade

    scale_factor = 1.1
    min_neighbours_for_faces = 4
    min_neighbours_for_eyes = 4

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,scaleFactor=scale_factor,minNeighbors=min_neighbours_for_faces)
    print(f"faces: {len(faces)}")
        
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        print("face detected")
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=scale_factor,minNeighbors=min_neighbours_for_eyes)

        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            print("eyes detected")

            roi = roi_color[ey+2:ey+eh-2, ex+2:ex+ew-2]
            roi = cv2.resize(roi, (224, 224))
            roi = image.img_to_array(roi)
            roi = preprocess_input(roi)
            roi = np.expand_dims(roi, axis=0)

            try:    
                pred = net.predict(roi)[0]
                #print(pred)
                top_inds = pred.argsort()[::-1][:5]

                label_text = cls_list[top_inds[0]]
                #emotion_id = top_inds[0]

                for i in top_inds:
                    print('    {:.3f}  {}'.format(pred[i], cls_list[i]))

            except Exception as e:
                print(e)

        cv2.putText(img, label_text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3, cv2.LINE_AA)

    return img #cv2.flip(img, 1)

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.is_running = True

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        print("camera is running")
        img = process(img)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

def main():
    st.title("face eye detection")

    webrtc_ctx = webrtc_streamer(key="distraction-detection",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTC_CONFIGURATION, 
            media_stream_constraints={"video": True, "audio": False},
            video_processor_factory=VideoProcessor,
            async_processing=True)

if __name__ == "__main__":
    main()