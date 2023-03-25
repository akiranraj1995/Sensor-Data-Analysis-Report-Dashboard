import streamlit as st
import time

# Define a function to read the contents of the output.txt file


def read_output_file():
    with open('/home/expert/Spyder/AgverseTech/Agverse_2ndWeek/Suvin Folder/Project/output/output.txt', 'r') as f:
        file_contents = f.read()
    return file_contents

# Define a Streamlit app that displays the contents of the output.txt file


def streamlit_app():
    st.title('Real-time Output')
    st.text('This app displays the contents of the output.txt file in real-time')
    st.write('')
    output_text = st.empty()
    while True:
        output_text.text(read_output_file())
        time.sleep(5)

# Run the Streamlit app


streamlit_app()
