#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 16:20:26 2018

@author: shea
"""
#Import dependencies
from flask import Flask, request, jsonify, redirect, url_for, render_template
import os
import fastai
from fastai import *
from fastai.vision import *
from PIL import Image
from werkzeug import secure_filename

## Load the pretrained resnet model
defaults.device = torch.device('cpu')
tfms = get_transforms(max_zoom=1.1)
path="./"
data = ImageDataBunch.single_from_classes(path, ['Coral snake. No antivenin available.','Harmless. Mild or no venom, not known to be dangerous to humans.','Pit viper. Antivenin available.'], ds_tfms=tfms, size=299).normalize(imagenet_stats)
learn = create_cnn(data, models.resnet50)
learn.model.load_state_dict(torch.load("snakes-usa.pth", map_location="cpu"))

## App variables / helper functions
UPLOAD_FOLDER = path + 'uploads/'
ALLOWED_EXTENSIONS = ['jpg']


def predict(filename):
    # do prediction
    pred_class,pred_idx,outputs = learn.predict(img)
    # return output
    label=pred_class
    return label      


#Flask App 
application = Flask(__name__, template_folder=path + 'templates/')
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Render Initial Template
@application.route("/")
def template_init():
    return render_template('index.html')

# Function to check and upload file, perform prediction
@application.route('/', methods=['GET', 'POST'])
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
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
	    img = open_image(UPLOAD_FOLDER + filename)
            label=predict(filename)[0]   
            return render_template('results.html', label=label, imagesource='../uploads/' + filename)


# Function that will actually save uploaded file and assign its path to the variable "filename"
@application.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(application.config['UPLOAD_FOLDER'],
                              filename)

from werkzeug import SharedDataMiddleware
application.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
application.wsgi_app = SharedDataMiddleware(application.wsgi_app, {
    '/uploads':  application.config['UPLOAD_FOLDER']
})

# Run app if "serve" is passed as command-line argument ("python application.py serve")
if __name__ == '__main__':
    if "serve" in sys.argv:
        application.run(host='0.0.0.0')
