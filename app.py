from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras import models, layers
import os
from PIL import Image
# import cv2
import numpy as np

app = Flask(__name__)

from tensorflow.keras.models import load_model
model=load_model("finalprojectoldcode64.h5")

picFolder = os.path.join('static', 'pics')
app.config['UPLOAD_FOLDER'] = picFolder

@app.route('/')
def index():
	return render_template("index.html", data="hey")

def names(number):
    if number==0:
        return 'Its a tumor'
    else:
        return 'Its not a tumor'

@app.route("/prediction", methods=["POST"])
def prediction():
	img = request.files['img']
	img.save("static/pics/img.jpg")
	image = Image.open("static/pics/img.jpg")
	x = np.array(image.resize((64,64)))
	x = np.expand_dims(x,axis=0)
	res = (model.predict_on_batch(x))
	classification = np.where(res == np.amax(res))[1][0]
	# a=names(classification)
	a=str(res[0][classification]*100) + '% Confidence ' + names(classification)

	pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'img.jpg')

	return render_template("prediction.html", data=a, user_image=pic1)


if __name__ == "__main__":
	app.run(debug=True)
