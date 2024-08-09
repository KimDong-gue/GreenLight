from django.db import models

from road.models import Road

# Create your models here.
class Pedestrian(models.Model):
    pedestrian_id = models.AutoField(primary_key=True, verbose_name='보행자 식별자')
    road = models.ForeignKey(Road, on_delete=models.RESTRICT, verbose_name='도로 식별자', blank=True)
    detection_time = models.DateTimeField(verbose_name='인식 시간')
    box_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='바운딩박스 아이디')

    class Meta:
        db_table = 'tb_pedestrian'
        verbose_name = '보행자'
        verbose_name_plural = '보행자'

    def __str__(self):
        return f'Pedestrian {self.pedestrian_id}'