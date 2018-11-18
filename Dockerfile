FROM python:3.6-alpine
RUN mkdir -p /opt/app
WORKDIR /opt/app
ADD requirements.txt /opt/app/
RUN pip install -r requirements.txt
ADD . /opt/app

# Define working directory.
WORKDIR /opt/app

# Define default command.
ENTRYPOINT ["python"]
CMD ["app.py"]