# Dependencies

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions

# def predict(img_path):
def getPrediction(filename):
     model = tf.keras.models.load_model("//home/mac-aphid/Videos/4th-YEAR-PROJECT/waste-classification-model/final_model_weights.h5")
     img = load_img('/home/mac-aphid/Videos/4th-YEAR-PROJECT/waste-classification-model/static/'+filename, target_size=(180, 180))
     img = img_to_array(img)
     img = img / 255
     img = np.expand_dims(img,axis=0)
     #category = model.predict_classes(img)
     predictions = model.predict(img)
     category = int(np.argmax(predictions))
     answer = category
     #probability = model.predict_proba(img)
     probability = model.predict(img)
     probability_results = 0

     if answer == 1:
          answer = "Recyclable"
          probability_results = probability[0][1]
     else:
          answer = "Organic"
          probability_results = probability[0][0]

     answer = str(answer)
     probability_results=str(probability_results)

     values = [answer, probability_results, filename]
     return values[0], values[1], values[2]


