from django.contrib import admin
from rango.models import Bares, Tapas
from rango.models import UserProfile

# Add in this class to customized the Admin Interface
class TapaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('nombre_tapa',)}

admin.site.register(Bares)
admin.site.register(Tapas, TapaAdmin)
admin.site.register(UserProfile)
