from django.db import models

# Create your models here.
class VehiclePedestrian(models.Model):
    road_id = models.IntegerField()
    road_name = models.CharField(max_length=255)
    vehicle_id = models.IntegerField()
    vehicle_num = models.CharField(max_length=255)
    vehicle_type = models.CharField(max_length=255)
    detection_time = models.DateTimeField()
    pedestrian_id = models.IntegerField()

    class Meta:
        managed = False  # Django가 이 테이블을 관리하지 않음을 명시
        db_table = 'vehicle_pedestrian_view'  # 뷰 이름을 테이블 이름으로 사용