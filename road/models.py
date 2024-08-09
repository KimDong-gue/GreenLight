from django.db import models

# Create your models here.
class Road(models.Model):
    road_id = models.AutoField(primary_key=True, verbose_name='도로 식별자',null=False,unique=True)
    road_name = models.CharField(max_length=50, verbose_name='도로 명', blank=True)
    speed_limit = models.IntegerField(verbose_name='제한 속도', blank=True)
    red_light = models.IntegerField(null=True, blank=True)


    class Meta:
        db_table = 'tb_road'
        verbose_name = '도로'
        verbose_name_plural = '도로'

    def __str__(self):
        return self.road_name