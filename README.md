# DeepSnakeUSA
Using computer vision to identify venomous snakes from the U.S.A.

# DISCLAIMER
Do not rely on this repo to identify venomous snakes! It is not accurate enough (yet) for real-world application!
Do not handle snakes that you cannot identify!
And please - be kind to snakes!

## Purpose:
Given an image of snake from the USA, identify whether it is likely to be a coral snake (highly venomous, no antivenom available), pit viper (highly venomous, antivenom available), or harmless (mild or no venom, not considered dangerous to humans). 

## Description:
The DeepSnakeUSA.ipynb notebook demonstrates the training of the model. I use transfer learning and the resnet50 model. The pretrained model is >100MB, so I need to find a workaround to upload it here. For single-image prediction, I'm using a web app written with Flask (app.py). Just testing it locally so far. 


## To Do:
Deployment using docker + AWS lamba / Now
