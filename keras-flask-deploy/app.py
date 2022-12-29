# Flask
from flask import Flask, request, render_template, jsonify

# TensorFlow and tf.keras
import tensorflow as tf
from keras.models import load_model

# Some utilites
import numpy as np
import cv2,os
from flask import Flask,request
from pytube import YouTube 


#################################################################

# Declare a flask app
app = Flask(__name__)

#################################################################

# Model saved with Keras model.save()
MODEL_PATH = "D:/Technocolabs Internship/keras-flask-deploy/models/U101_model.h5"
# Load your own trained model
model = load_model(MODEL_PATH, compile=False)
# model._make_predict_function()          
print('Start serving...')

#################################################################
def format_frames(frame, output_size):
    frame = tf.image.convert_image_dtype(frame, tf.float32)
    frame = tf.image.resize_with_pad(frame, *output_size)
    return frame
def frames_from_video_file(video_path, n_frames,  frame_step = 15):
    # Read each video frame by frame
    result = []
    output_size = (224,224)
    src = cv2.VideoCapture(video_path)  

    # ret is a boolean indicating whether read was successful, frame is the image itself
    ret, frame = src.read()
    result.append(format_frames(frame, output_size))

    for _ in range(n_frames - 1):
      for _ in range(frame_step):
        ret, frame = src.read()
      if ret:
        frame = format_frames(frame, output_size)
        result.append(frame)
      else:
        result.append(np.zeros_like(result[0]))
    src.release()
    result = np.array(result)[..., [2, 1, 0]]

    return result
#################################################################
def model_predict(data, model):
    sample_video = frames_from_video_file(data, n_frames = 10)
    sample_video=sample_video.reshape([1, 10, 224 ,224, 3])
    preds = model.predict(sample_video)
    return preds

################################################################
@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

##################################################################


@app.route('/handle_data', methods=['POST','GET'])
def handle_data():
    if request.method == 'POST':
        url = request.form['v_url']
        yt=YouTube(url)
        stream = yt.streams.first()
        stream.download('D:/Technocolabs Internship/keras-flask-deploy/static/downloads_videos')
        print("done")
        # result="Now You Can Click on Subumit to See Result :) "
        # return jsonify(result=result)
    return '', 204

##################################################################

@app.route('/predict', methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        dir="D:\Technocolabs Internship\keras-flask-deploy\static\downloads_videos"
        for video in os.listdir(dir):
            # Make prediction
            preds = model_predict(os.path.join(dir,video), model)
            names=['ApplyEyeMakeup',
            'ApplyLipstick',
            'Archery',
            'BabyCrawling',
            'BalanceBeam',
            'BandMarching',
            'BaseballPitch',
            'BasketballDunk',
            'Basketball',
            'BenchPress',
            'Biking',
            'Billiards',
            'BlowDryHair',
            'BlowingCandles',
            'BodyWeightSquats',
            'Bowling',
            'BoxingPunchingBag',
            'BoxingSpeedBag',
            'BreastStroke',
            'BrushingTeeth']
            # Process your result for human
            result=names[np.argmax(preds[0])]   
            os.remove(os.path.join(dir, video))
            # Serialize the result, you can add additional fields
            return jsonify(result=result)  #, probability=pred_proba
    return '', 204

#################################################################

if __name__ == '__main__':
    # serve app on localhost port 5000
    app.run(debug=True)
