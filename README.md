# PropertyCheckSystem網站建置

![盤點圖片](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGIL0tDpFmqdgwYPSXBKMXYuRVfL3T0k-zRA&usqp=CAU)

1. [To-Do](#To-Do)
1. [套件](#套件)
1. [執行](#架設環境)
1. [開始部屬](#)

# 套件
### 後端環境
> channels
> Django
> Node.js (僅安裝tailwind)
> tailwind (透過npm安裝)

### 資料庫
> 10.5.9-MariaDB

### 前端環境
> Vue.JS 3.0.11

### 安裝MySQL or MariaDB
``` shell
# 安裝MySQL
sudo apt install mysql-server
sudo apt install mysql-client
sudo apt install libmysqlclient-dev
# 初始設定
sudo mysql_secure_installation
```
[Access denied問題](https://www.notion.so/MySQL-access-cf0e58a320eb4060b818d4f35a88e569)

### Debian需要的套件
``` shell
sudo apt install libsasl2-dev python-dev libldap2-dev libssl-dev libmysqlclient-dev
```

### python需要的套件
1. django
1. ldap
1. django_auth_ldap
1. django_werkzeug_debugger_runserver
1. django_extensions
1. channels
1. mysqlclient
1. pillow


# 執行
### 使用django內部伺服器執行
``` shell
# 首次執行需要先初始話資料庫
python manage.py makemigrations
python manage.py migration
# 創建SuperUser
python manage.py createsuperuser
# 執行伺服器監聽所有IP於80 port
python manage.py runserver 0.0.0.0:80
```