
from fabric.api import run, local, hosts, cd
from fabric.contrib import django

#Ejecucion remota del docker
#Instalacion de docker y descarga de imagen
def getDocker():
	run('sudo apt-get update')
	run('sudo apt-get install -y docker.io')
	run('sudo docker pull javiexfiliana7/proyectoDAI-IV.git')

#Ejecucion de docker
def runDocker():
	run('sudo docker run -p 80:80 -i -t javiexfiliana/proyectoDAI-IV')
