# Simple Streamlit + FastAPI Integration For Generating Topics
A minimal Streamlit app showing how to launch and stop a FastAPI process on demand. The FastAPI `/run` route simulates a long-running process which is launched on a separate thread. 

Ensure the required packages are installed:

```bash
pip install -r requirements.txt
```

To run the app:

```bash
streamlit run app.py
```

The port for interfact is 8000

In the fastapi_wrapper.py the used port is 8501 if your device port is busy then change to another port in the CORS_ALLOW_ORIGINS
