from setuptools import setup

setup(name='tango_with_django_project',
	version='0.1',
	description='Web application about polls',
	url='https://github.com/javiexfiliana7/proyectoDAI-IV/',
	author='Javier Ruiz Cesar',
	author_email='javiexfiliana@gmail.com',
	license='GNU GPL',
	packages=['tango_with_django_project'],
	install_requires=['django','wheel','djangorestframework'],
	zip_safe=False)
