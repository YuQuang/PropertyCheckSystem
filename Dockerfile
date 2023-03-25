FROM ubuntu:focal
LABEL author="Roy.Xu" email="bbb233456@gmail.com"
COPY . /pandian

######################
# Install dependency
######################
RUN apt update
RUN apt install -y libsasl2-dev python3-dev libldap2-dev libssl-dev libmysqlclient-dev python3-pip
RUN apt -y --fix-missing install
###############################
# Install python dependency
###############################
RUN pip3 install django==3.2.13
RUN pip3 install wheel python-ldap django_auth_ldap django_werkzeug_debugger_runserver django_extensions channels mysqlclient pillow uwsgi daphne

EXPOSE 443
WORKDIR /pandian
CMD ["daphne", "-e", "ssl:443:privateKey=cert/cert.key:certKey=cert/cert.crt", "Web.asgi:application"]