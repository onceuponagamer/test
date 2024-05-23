# v 0.0.1
import streamlit as st
import cv2
import io
from util.prediction import video_predict

#st.title('hello world!')

temp_file_to_save = './temp_file_1.mp4'
temp_file_result  = './temp_file_2.mp4'

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

    tab1, tab2, tab3 = st.tabs(["Upload a File", "Use Webcam", "..."])
    user_input = None

    with tab1:
        uploaded_file = st.file_uploader("Upload a file", type=["avi", "mp4", "jpg", "png", "gif"])
        generate_file_input = st.button("Detection from File")
            
    user_input = None

    if generate_file_input and uploaded_file is not None:
        #file_type = uploaded_file.type
        #st.write(file_type)
        user_input = io.BytesIO(uploaded_file.read())
        #st.write("filename:", uploaded_file.name)
        #st.write(user_input)
        # save uploaded video to disc
        write_bytesio_to_file(temp_file_to_save, user_input)

    #if user_input:
        #st.session_state.user_input = user_input

    if user_input:
        #user_input = st.session_state.get("user_input", None)
        if user_input:
            with st.spinner("Generating Video..."):
                try:
                    pass
                    #st.video(user_input)
                    #video_predict(temp_file_to_save)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()