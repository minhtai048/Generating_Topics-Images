import os, sys
import time
import streamlit as st
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

# --------------------------------------------------------------------------------

API_HOST='localhost'
API_PORT=8000
API_BASE_URL='http://localhost:8000'
backend = "http://localhost:8501/predict"

# Session State variables:
state = st.session_state
if 'API_APP' not in state:
    state.API_APP = None
if 'API_STARTED' not in state:
    state.API_STARTED=False

# --------------------------------------------------------------------------------

def main():
    st.title('Welcome to Generating Topics App')

    # RUN LRP
    if not state.API_STARTED:
        st.write('To launch app click the button below.')
        if st.button('Launch'):

            import subprocess
            import threading

            def run(job):
                print (f"\nRunning job: {job}\n")
                proc = subprocess.Popen(job)
                proc.wait()
                return proc

            job = [f'{sys.executable}', os.path.join('.', 'bootstrapper.py'), API_HOST, str(API_PORT)]

            # server thread will remain active as long as streamlit thread is running, or is manually shutdown
            thread = threading.Thread(name='FastAPI-Bootstrapper', target=run, args=(job,), daemon=True)
            thread.start()

            time.sleep(1)

            # !! Start the LRP !!
            requests.get(f'{API_BASE_URL}/run')

            state.API_STARTED = True

            st.experimental_rerun()

    if state.API_STARTED:
        st.write(""" # Image Classification """)
        file = st.file_uploader("Upload the image to be generated topics", accept_multiple_files=False, type=["jpg", "png", "jpeg"])
        st.set_option('deprecation.showfileUploaderEncoding', False)
        #CURRENTLY WORKING WITH ONLY ONE IMAGE PER GENERATION
        
        if st.button('Generating Topics'):
            img = MultipartEncoder(fields={"file": ("filename", file, "image/jpg/png/jpeg")})
            result = requests.post(f'{API_BASE_URL}/predict', data = img, headers={"Content-Type": img.content_type})
            st.image(file, use_column_width=True)
            st.write("The generated topics are: ")    
            final_lst = result.json()
            
            #a trick for better display as a list
            element = ''
            for i in final_lst:
                element += "- " + i + "\n"
            st.markdown(element)


def sidebar():
    # ABOUT
    st.sidebar.header('About')
    st.sidebar.info('FastAPI Wrapper to run Generating Topics With Image!')


if __name__ == '__main__':
    main()
    sidebar()
