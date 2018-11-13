FROM python:3.6-slim-stretch
RUN apt update
RUN apt install -y python3-dev gcc
RUN pip3 install pip --upgrade

#These files/folders are needed to run the app
ADD requirements.txt requirements.txt
ADD templates templates/
ADD uploads uploads/
ADD application.py application.py
ADD snakes-usa.pth snakes-usa.pth

# Install pytorch, fastai, and flask
RUN pip3 install torch_nightly -f https://download.pytorch.org/whl/nightly/cpu/torch_nightly.html
RUN pip3 install -r requirements.txt

# Run app once to trigger resnet download
RUN python3 application.py

# Expose port
EXPOSE 5000

# Start server
CMD ["python3", "application.py", "serve"]
