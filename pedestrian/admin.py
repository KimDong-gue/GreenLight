from django.contrib import admin

from pedestrian.models import Pedestrian

# Register your models here.


class PedestrianAdmin(admin.ModelAdmin):
    list_display = ["pedestrian_id","road", "detection_time"]
admin.site.register(Pedestrian, PedestrianAdmin)
