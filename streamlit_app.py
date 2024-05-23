# v 0.0.1
import streamlit as st
import cv2
import io
from util.prediction import video_predict

temp_file_to_save = './temp_file_1.mp4'
temp_file_result  = './temp_file_2.mp4'
output_file = './output_2024-05-23.mp4'

# func to save BytesIO on a drive
def write_bytesio_to_file(filename, bytesio):
    """
    Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet. 
    """
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.read())

def main():
    _author_ = "melike"
    st.title("Distraction Detection")
    st.markdown(
        """
        This project developed by %s
        """
        % _author_)
    
    with open(temp_file_to_save, "rb") as video_file:
        video_bytes = video_file.read()
        st.video(video_bytes)

    tab1, tab2, tab3 = st.tabs(["Upload a File", "Use Webcam", "..."])
    user_input = None

    with tab1:
        uploaded_file = st.file_uploader("Upload a file", type=["avi", "mp4", "jpg", "png", "gif"])
        generate_file_input = st.button("Detection from File")
            
    user_input = None

    if generate_file_input and uploaded_file is not None:
        user_input = io.BytesIO(uploaded_file.read())
        # save uploaded video to disk
        write_bytesio_to_file(temp_file_to_save, user_input)

    #if user_input:
        #st.session_state.user_input = user_input

    if user_input:
        #user_input = st.session_state.get("user_input", None)
        if user_input:
            with st.spinner("Generating Video..."):
                try:
                    #st.video(user_input)
                    video_path = video_predict(temp_file_to_save)
                    st.write(video_path)
                    video_file = open(video_path, 'rb')
                    video_bytes = video_file.read()
                    st.video(video_bytes)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()