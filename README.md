# Simple Streamlit + FastAPI Integration For Generating Topics
This streamlit app is used for demonstration of generating topics with movie poster which can be used for classifying topics and recommend other users in Recommender System.

## To test the app:

Ensure the required packages are installed:

```bash
pip install -r requirements.txt
```

To run the app:

```bash
streamlit run app.py
```

## To check the report:

Open .ipynb in the "building_model" folder.

## Notice

The port for interfact is 8000.

In the fastapi_wrapper.py the used port is 8501 if your device port is busy then change to another port in the CORS_ALLOW_ORIGINS.
