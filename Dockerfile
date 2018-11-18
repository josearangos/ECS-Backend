FROM python:3.6-alpine
RUN apk update && apk add git
RUN git clone https://github.com/josearangos/ECS-Backend.git /ECS-Backend/
RUN mkdir -p /opt/app
WORKDIR /opt/app
ADD requirements.txt /opt/app/
RUN pip install -r requirements.txt
RUN cp -R /ECS-Backend/* /opt/app

# Define working directory.
WORKDIR /opt/app

EXPOSE 5000

# Define default command.
ENTRYPOINT ["python"]
CMD ["app.py"]