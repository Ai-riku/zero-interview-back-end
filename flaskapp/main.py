import streamlit as st
import numpy as np
import cv2
import config
import time
import os

from openai_util import prompt_to_text, transcribe
from av_util import video_capture_streamlit
from util import removeFile


def main():
    st.set_page_config(
        page_title="Zero Interview",
        page_icon="📺",
        initial_sidebar_state='collapsed'
    )

    st.header("Zero Interview 📺")

    def set_stage(stage):
        st.session_state.stage = stage

    if 'stage' not in st.session_state:
        st.session_state.stage = 0

    prompt_input = st.text_area("Job Description:",
                                placeholder="""Please enter
                                 the job description to
                                 generate appropriate
                                 inteview questions""")
    prompt = prompt_input
    if st.button("Generate Question") and prompt is not None:
        set_stage(1)

    if st.session_state.stage > 0:
        with st.spinner('Generating...'):
            st.subheader('Question:')
            final_prompt = """given the following job
             description, please ask an appropriate
             interview question: \n""" + prompt
            interview_question = prompt_to_text(final_prompt)
            st.markdown(interview_question)
        st.button('Video Answer:',
                  type="primary",
                  on_click=set_stage,
                  args=(2,))

    if st.session_state.stage > 1:
        st.subheader('Video Answer:')
        video_generator = video_capture_streamlit()
        image_container = st.empty()
        for lastFrame, frame in video_generator:
            if lastFrame:
                break
            np_frame = cv2.imdecode(
                np.frombuffer(frame, np.uint8),
                cv2.IMREAD_COLOR)
            image_container.image(np_frame, channels="BGR")

        with st.spinner('Transcribing...'):
            while not os.path.exists(config.AUDIO_PATH):
                time.sleep(1)
            try:
                transcription = transcribe(config.AUDIO_PATH)
                with open(config.TRANSCRIPT_PATH, 'w') as file:
                    file.write(transcription)
            except OSError as e:
                print('Access-error on file "'
                      + config.TRANSCRIPT_PATH
                      + 'or' + config.AUDIO_PATH
                      + '"! \n' + str(e))
            st.subheader('Transcription:')
            st.markdown(transcription)
            removeFile(config.TRANSCRIPT_PATH)
            st.button('Reset', type="primary", on_click=set_stage, args=(0,))


if __name__ == '__main__':
    main()
