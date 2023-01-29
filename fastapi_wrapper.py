from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
import io


CORS_ALLOW_ORIGINS=['http://localhost, http://localhost:8501']

class FastAPI_Wrapper(FastAPI):
    
    def __init__(self):
        """
        Initializes a FastAPI instance.
        """
        print('Initializing FastAPI_Wrapper...')
        
        super().__init__()

        origins = CORS_ALLOW_ORIGINS

        self.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        genre_topics = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
                        'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror',
                        'Music', 'Musical', 'Mystery', 'N/A', 'News', 'Reality-TV', 'Romance',
                        'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']
        classes = pd.DataFrame(columns=[genre_topics])

        #converting multi-index to singe-index columns
        classes.columns = ['_'.join(map(str, x)) for x in classes.columns]
        classes = classes.columns
        
        def load_model():
            model=tf.keras.models.load_model('model/model_270123.h5')
            return model
        model=load_model()

        def upload_predict(upload_image, model):
            size = (224,224)
            img = ImageOps.fit(upload_image, size, Image.ANTIALIAS)
            img = image.img_to_array(img)
            img = img/255.0
            img_reshape = img.reshape(1,224,224,3)
            prediction = model.predict(img_reshape)
            return prediction
      
        @self.get("/run")
        async def run():
            import time
            from datetime import datetime
            import threading

            # !! RUN YOUR LONG-RUNNING PROCESS HERE !!
            def lrp_runner():
                while True:
                    time.sleep(1)
                    print(f'>>> Report @ {datetime.now()} <<<')

            threading.Thread(target=lrp_runner, daemon=True).start()
        
        @self.post("/predict")
        async def predict(file: UploadFile = File(...)):
            lst_contain_topics = []
            if file is not None:
                #LOADING IMAGE
                request_object_content = await file.read()
                load_img = Image.open(io.BytesIO(request_object_content))
                #-------------------------------------------------------
                predictions = upload_predict(load_img, model)
                topics = np.argsort(predictions[0])[:-6:-1]
                #take 5 most topics
                for i in range(5):
                    lst_contain_topics.append(classes[topics[i]])

                #fastapi doesn't work with numpy type -> change to list
                return lst_contain_topics