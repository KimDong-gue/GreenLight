from django.contrib import admin

from vehicle.models import Signal, Speed, Vehicle

# Register your models here.

class VehicleAdmin(admin.ModelAdmin):
    list_display = ["vehicle_id", "vehicle_num","vehicle_type","detection_time"]
admin.site.register(Vehicle, VehicleAdmin)


class SpeedAdmin(admin.ModelAdmin):
    list_display = ["speed_id","vehicle","road","speed","speed_violation_yn"]
admin.site.register(Speed, SpeedAdmin)

class SignalAdmin(admin.ModelAdmin):
    list_display = ["signal_id", "vehicle","road","signal_violation_yn"]
admin.site.register(Signal, SignalAdmin)