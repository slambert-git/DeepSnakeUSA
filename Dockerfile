#thanks to: https://github.com/simonw/cougar-or-not/blob/master/Dockerfile

FROM python:3.6-slim-stretch

RUN apt update
RUN apt install -y python3-dev gcc

# Install pytorch and fastai
RUN pip install torch_nightly -f https://download.pytorch.org/whl/nightly/cpu/torch_nightly.html
RUN pip install fastai

ADD app.py app.py
ADD usa-snakes.pth usa-snakes.pth

# Install Flask and gunicorn
RUN pip install flask gunicorn

# Run it once to trigger resnet download
RUN python app.py

EXPOSE 8008

# Start the server
CMD ["python", "app.py", "serve"]
