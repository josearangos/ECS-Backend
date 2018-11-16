FROM ubuntu:latest
RUN apt-get update

RUN apt-get install -y -q build-essential python-pip python-dev python-simplejson git
RUN pip install --upgrade pip
RUN pip install --upgrade virtualenv
RUN mkdir deployment
RUN git clone https://github.com/josearangos/ECS-Backend /deployment/
RUN virtualenv /deployment/env/
RUN /deployment/env/bin/pip install 'aniso8601==2.0.0'
RUN /deployment/env/bin/pip install 'click==6.7'
RUN /deployment/env/bin/pip install 'pymongo==3.5.1'
RUN /deployment/env/bin/pip install 'Flask==0.12.2'
RUN /deployment/env/bin/pip install 'Flask-RESTful==0.3.6'
RUN /deployment/env/bin/pip install 'itsdangerous==0.24'
RUN /deployment/env/bin/pip install 'Jinja2==2.10'
RUN /deployment/env/bin/pip install 'MarkupSafe==1.0'
RUN /deployment/env/bin/pip install 'pytz==2018.3'
RUN /deployment/env/bin/pip install 'six==1.11.0'
RUN /deployment/env/bin/pip install 'Werkzeug==0.14.1'
RUN /deployment/env/bin/pip install 'certifi==2018.1.18'
RUN /deployment/env/bin/pip install 'Flask-JWT'
RUN /deployment/env/bin/pip install 'Flask-Cors==3.0.2'
RUN /deployment/env/bin/pip install 'flask-jwt-extended'
RUN /deployment/env/bin/pip install 'gunicorn'
WORKDIR /deployment
CMD env/bin/python app.py