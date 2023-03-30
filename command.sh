docker stop pandian
docker run -d --rm -p 8000:443 \
-e WEB_DB_ADDR=172.17.0.3 \
-e WEB_DB_NAME=MyWeb \
-v `pwd`/static/PropertyImage:/pandian/static/PropertyImage \
-v `pwd`/static_file/PropertyImage:/pandian/static_file/PropertyImage \
--name pandian \
yuquang/pandian:0.0.2