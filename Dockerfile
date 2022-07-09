FROM ubuntu:focal

LABEL author="YuQuang" email="bbb233456@gmail.com"

# 複製網站檔案到pandian工作區
COPY . /pandian

# 系統更新
RUN apt update
# RUN apt -y upgrade

# 檢查缺漏
RUN apt -y --fix-missing install

# 安裝必要套件
RUN apt install -y libsasl2-dev python3-dev libldap2-dev libssl-dev libmysqlclient-dev python3-pip

# 檢查缺漏
RUN apt -y --fix-missing install

# 安裝python套件
RUN pip3 install django==3.1.14
RUN pip3 install wheel python-ldap django_auth_ldap django_werkzeug_debugger_runserver django_extensions channels mysqlclient pillow uwsgi daphne

# Port 80 443 8000
EXPOSE 80 443 8000

# 設定當前工作區為/pandian
WORKDIR /pandian

# 初始化資料庫部分
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# 伺服器開啟指令
# ENTRYPOINT [ "sh", "/pandian/run.sh" ]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:80"]