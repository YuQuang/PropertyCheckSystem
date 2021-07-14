FROM ubuntu:focal

LABEL author="YuQuang" email="bbb233456@gmail.com"

COPY . /pandian
# COPY ./index /pandian/index 
# COPY ./static /pandian/static
# COPY ./static_file /pandian/static_file
# COPY ./templates /pandian/templates
# COPY ./Web /pandian/Web
# COPY ./manage.py /pandian

RUN apt update
RUN apt -y upgrade
RUN apt install -y libsasl2-dev python-dev libldap2-dev libssl-dev libmysqlclient-dev
RUN apt -y --fix-missing install
RUN apt install -y python3-pip
RUN apt -y --fix-missing install
RUN pip3 install wheel django python-ldap django_auth_ldap django_werkzeug_debugger_runserver django_extensions channels mysqlclient pillow 

EXPOSE 80

WORKDIR /pandian


RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
ENTRYPOINT [ "python3", "manage.py", "runserver" ]
CMD [ "0.0.0.0:80" ]