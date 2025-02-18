conda create --name lit_music_app
conda activate lit_music_app
uvicorn main:app --reload 


pip install sqlalchemy
pip install pymysql

# Run Docker Desktop
-------------
MySQL:
# Create a container called mymysql
docker run --name mymysql -e MYSQL_ROOT_PASSWORD=1214 -d mysql:latest
pip install pymysql
docker exec -it mymysql bash
mysql -u root -p1214 
(Iniciar el contenedor: docker start mymysql)
create database storedb;
show databases;

docker exec -it mymysql mysql -u root -p1214
------------

pip install cryptography

Para seguridad:
#pip install fastapi[all] pyjwt passlib[bcrypt]

pip install fastapi-users fastapi-users[jwt] python-jose[cryptography] passlib[bcrypt]