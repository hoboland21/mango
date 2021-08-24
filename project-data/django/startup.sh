if [ ! -d "mango" ] ;then
/usr/local/bin/python /usr/local/bin/django-admin  startproject mango
fi
cd mango
./manage.py makemigrations --noinput
./manage.py  migrate

./manage.py runserver 0.0.0.0:8200



#cd /usr/src/app/stweb
#uwsgi --ini   uwsgi.ini 
