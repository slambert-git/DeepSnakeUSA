# DeepSnakeUSA
Using computer vision to identify venomous snakes from the U.S.A.

The app is currently deployed through AWS Elastic Beanstalk for demo purposes: 

# DISCLAIMER
Do not rely on this repo to identify venomous snakes in the real world! It is not accurate enough for real-world application (95% validation accuracy is "good" but not good enough for this purpose)!
Do not handle snakes that you cannot identify!
And please - be kind to all snakes!

## Purpose:
Given an image of snake from the USA, identify whether it is likely to be a coral snake (venomous, no antivenin available), pit viper (venomous, antivenin available), or 'harmless' (mild or no venom, not considered dangerous to humans). 

## Description:
The DeepSnakeUSA.ipynb notebook demonstrates the training of the model. I used transfer learning and the resnet50 model, implemented using the fastai library. The model and weights are found in `snakes-usa.pth` For single-image prediction, I'm using a web app written with Flask (`application.py`). I took .html templates from this repo: https://github.com/ferrygun/AIFlowers2. 
