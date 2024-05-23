# v 0.0.1
import streamlit as st
import cv2
from util.prediction import video_predict

#st.title('hello world!')

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
        file_type = uploaded_file.type
        #st.write(file_type)
        user_input = uploaded_file.read()
    
    if user_input:
        st.session_state.user_input = user_input

    if user_input:
        user_input = st.session_state.get("user_input", None)
        if user_input:
            with st.spinner("Generating Video..."):
                try:
                    #st.video(user_input)
                    video_predict(user_input)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()