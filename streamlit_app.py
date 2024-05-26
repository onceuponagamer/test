# v 0.0.1
import streamlit as st
import io
from util.prediction import video_predict
from util.prediction import convert_to_x264

temp_file_to_save = './temp_file_1.mp4'
temp_file_result  = './temp_file_2.mp4'
output_file = './output.mp4'

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

def show_video(filename):
    #st.write(filename)
    with open(filename, "rb") as video_file:
        video_bytes = video_file.read()
        st.video(video_bytes)

def click_button():
    convert_to_x264(temp_file_result, output_file)
    #video_predict(temp_file_to_save, temp_file_result)
    show_video(output_file)
    #convertedVideo = "./testh264.mp4"
    #subprocess.call(args=f"ffmpeg -y -i {temp_file_result} -c:v libx264 {convertedVideo}".split(" "))
    #subprocess.call(args=f"ffmpeg -y -c:v h264_v4l2m2m -i {temp_file_result} {convertedVideo}".split(" "))
    #ffmpeg -f s16le -ac 1 -ar 48000 -acodec pcm_s16le -i input.raw output.mp3

def main():
    _author_ = "melike"
    st.title("Distraction Detection")
    st.markdown(
        """
        This project developed by %s
        """
        % _author_)
    
    #with open(temp_file_to_save, "rb") as video_file:
    #    video_bytes = video_file.read()
    #    st.video(video_bytes)

    tab1, tab2, tab3 = st.tabs(["Upload a File", "Use Webcam", "..."])
    user_input = None

    with tab1:
        uploaded_file = st.file_uploader("Upload a file", type=["avi", "mp4", "mov"])
        generate_file_input = st.button("Detection from File")
        st.button('Convert video', on_click=click_button)
            
    user_input = None

    if generate_file_input and uploaded_file is not None:
        user_input = io.BytesIO(uploaded_file.read())
        # save uploaded video to disk
        write_bytesio_to_file(temp_file_to_save, user_input)
        #show_video(temp_file_to_save)

    #if user_input:
        #st.session_state.user_input = user_input
    #user_input = None
    if user_input:
        #user_input = st.session_state.get("user_input", None)
        if user_input:
            with st.spinner("Generating Video..."):
                try:
                    print(">>>>>> test")
                    #video_predict(temp_file_to_save, temp_file_result)
                    show_video(temp_file_to_save)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()