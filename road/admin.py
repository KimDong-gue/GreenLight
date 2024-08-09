from django.contrib import admin

from road.models import Road

# Register your models here.


class RoadAdmin(admin.ModelAdmin):
    list_display = ["road_id","road_name","speed_limit"]
admin.site.register(Road, RoadAdmin)
