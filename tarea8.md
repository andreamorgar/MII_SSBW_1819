
Primero nos creamos las claves siguiendo los pasos (aquí)[https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-in-ubuntu-18-04]
~~~
$ sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
~~~

Después, en la carpeta del proyecto, creamos un directorio llamado `cert`
~~~
$ sudo cp /etc/ssl/certs/nginx-selfsigned.crt /home/andreamorgar/MII_SSBW_1819/proyecto/cert/
$ sudo cp /etc/ssl/private/nginx-selfsigned.key /home/andreamorgar/MII_SSBW_1819/proyecto/cert/
~~~

Además, creamos un directorio llamado `conf`, y dentro creamos el archivo de configuración de _nginx_, al que llamaremos `nginx.conf`, y tendrá el siguiente contenido. Este contenido es el que hemos copiado de la tarea de swad, solo que hay que modificar tres cosas:
- Añadir una llave al final del fichero
- Modificar en location, y añadir ejercicios,pelis y static
- Modificar "accounts" (ponía "accuonts")

~~~
server {
  listen 80 default_server;
  server_name _;

  # redirecciona todo a https
  return 301 https://$host$request_uri;
}

server {
  listen 443 ssl;
  server_name _;

  # la pareja de claves
  ssl_certificate /etc/ssl/private/nginx.crt;
  ssl_certificate_key /etc/ssl/private/nginx.key;
  keepalive_timeout   70;

  ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
  ssl_ciphers         AES128-SHA:AES256-SHA:RC4-SHA:DES-CBC3-SHA:RC4-MD5;
  ssl_session_cache   shared:SSL:10m;
  ssl_session_timeout 10m;

  location  ~ ^/(miapp|admin|accounts|ejercicios|pelis|static) {
		try_files $uri @proxy_to_app;
  }

  # proxy inverso
  location @proxy_to_app {
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	proxy_set_header Host $http_host;
	proxy_redirect off;
	proxy_pass   http://web:8000;
  }
}
~~~

Por último, modificamos el fichero `docker-compose.yml` con lo que pone en swad.


Para comprobar que funciona:
~~~
$ sudo docker-compose build
$ sudo docker-compose up
~~~

Al entrar a una página con el puerto 80 (no el 8000), redirecciona a https automáticamente (está especificado en el fichero de configuración). La primera vez nos pide que agreguemos un certificado, una vez sigamos los pasos, ya accederemos de forma segura. Las siguientes veces, saldrá ya directamente el candado junto a la barra de direcciones.
Además, si consultamos la terminal, podremos ver los logs de nginx funcionando cada vez que hagamos una consulta bajo el puerto 80. 
