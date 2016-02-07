###Creación de la instancia ec2

Para ello hemos seguido los siguientes pasos:

- Nos dirigimos al menú principal de ec2:

![i1](http://i63.tinypic.com/2nl8mew.png)

- Una vez  hemos seleccionado crear la instancia, seleccionamos el sistema operativo.
![i2](http://i64.tinypic.com/2zpk009.png)

- Seguimos los pasos indicando las características de nuestra máquina virtual hasta crear nuestra instancia
![i8](http://i65.tinypic.com/29djuyc.png)

- En el proceso de la creación de la instancia hemos descargado un archivo con extensión .pem que nos permetirá hacer la clave ssh, para ello es necesario añadirlo:

![i9](http://i67.tinypic.com/23sde6x.png)

- En nuestro fabfile tenemos para descargarnos nuestro Docker, a mi me ha dado problemas y consultando por internet me he dado cuenta de que lo tenía que ejecutar sin la caché y de esta manera se descarga solo. La siguiente imagen muestra el docker ejecutándose con la opción anteriormente mencionada:
![i10](http://i64.tinypic.com/ev896r.png)

###Dar servicio web con mi Docker

Para que la aplicación web que está contenida en el docker pueda ser servida es necesario realizar los siguientes pasos:

- Obtener la IP de mi docker (eth0)
![i11](http://i66.tinypic.com/2wc3cwp.png)

- Ejecutamos la aplicación contenida en el docker (python manage.py runserver 0.0.0.0:80) y en la instancia de ec2 introducimos una regla en la tabla NAT la cual conducirá las peticiones realizadas a la máquina a nuestro docker para que puedan ser atendidas por la aplicación.

![i12](http://i67.tinypic.com/f0ahcy.png)

Mi aplicación desplegada es la siguiente:

![i13](http://i67.tinypic.com/ip4cc6.png)
