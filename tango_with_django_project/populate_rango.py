import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Bares, Tapas


def populate():


    b1_cat = add_tapa("Aceitunas")

    add_bar(tapa=b1_cat, nombre_bar="El vecino",
        direccion="Calle Gloria Mors")

    b2_cat = add_tapa("Jamn")

    add_bar(tapa=b2_cat, nombre_bar="Jimenez",
    direccion="Calle ")

    b3_cat = add_tapa("Queso")
    

    add_bar(tapa=b3_cat, nombre_bar="Florida",
    direccion="Calle Florida ")

    b4_cat = add_tapa("Hamburguesa")

    add_bar(tapa=b3_cat, nombre_bar="Pescador",
    direccion="Calle Flor ")
  

    # Print out what we have added to the user.
    for c in Bares.objects.all():
        for p in Tapas.objects.filter(nombre_tapa=c.tapa.nombre_tapa):
            print "- {0} - {1}".format(str(c), str(p))

def add_bar(tapa, nombre_bar,direccion,n_visitas=0):
    c = Bares.objects.get_or_create(tapa=tapa, nombre_bar=nombre_bar)[0]
    c.direccion=direccion
    c.n_visitas=n_visitas
    c.save()
    return c

def add_tapa(nombre_tapa, votos=0):
    p = Tapas.objects.get_or_create(nombre_tapa=nombre_tapa)[0]
    p.votos=votos
    p.save()
    return p



# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
