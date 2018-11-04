#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 16:20:26 2018

@author: shea
"""

from flask import Flask, request, jsonify, redirect, url_for, render_template
import os
import fastai
from fastai import *
from fastai.vision import *
from PIL import Image


#Load model
fastai.defaults.device = torch.device('cpu')
path = "/"
tfms = get_transforms(max_zoom=1.1)
data = ImageDataBunch.single_from_classes(path, ['Coral','NotDangerous','PitViper'], tfms=tfms, size=299).normalize(imagenet_stats)
learn = create_cnn(data, models.resnet50)
learn.load('snakes-usa')




##App requirements / helper functions
from werkzeug import secure_filename
UPLOAD_FOLDER = path + 'uploads/'
ALLOWED_EXTENSIONS = ['jpg']


def predict(filename):
    #open image
    img = open_image(UPLOAD_FOLDER + filename)
    # do prediction
    pred_class,pred_idx,outputs = learn.predict(img)
    # return output
    label=pred_class
    return label      


#Flask App 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def template_init():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            label=predict(filename)   
        return render_template('results.html', label=label, imagesource='../uploads/' + filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
  app.run(port=8008)
