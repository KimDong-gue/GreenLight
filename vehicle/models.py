from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator

from road.models import Road


class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True, verbose_name='차량 식별자')
    vehicle_num = models.CharField(
        max_length=20,
        verbose_name='차량 번호판',
        blank=True,
        validators=[RegexValidator(regex=r'^\d{2}[가-힣]\d{4}$', message='Invalid vehicle number')]
    )
    vehicle_type = models.CharField(max_length=20, verbose_name='차량 종류', blank=True)
    detection_time = models.DateTimeField(verbose_name='인식 시간', blank=True)
    road = models.ForeignKey(Road, on_delete=models.RESTRICT, verbose_name='도로 식별자', blank=True)

    class Meta:
        db_table = 'tb_vehicle'
        verbose_name = '차량'
        verbose_name_plural = '차량'

    def __str__(self):
        return self.vehicle_num
# Speed 모델
class Speed(models.Model):
    speed_id = models.AutoField(primary_key=True, verbose_name='속도 식별자')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.RESTRICT, verbose_name='차량 식별자')
    speed = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='차량 속도', default=0.0)
    speed_violation_yn = models.CharField(max_length=1, verbose_name='위반 여부', blank=True, default='N')
    road = models.ForeignKey(Road, on_delete=models.RESTRICT, verbose_name='도로 식별자', blank=True)
    speed_violation_img = models.CharField(max_length=1000, verbose_name='위반 이미지', blank=True)

    class Meta:
        db_table = 'tb_speed'
        verbose_name = '속도위반'
        verbose_name_plural = '속도위반'

    def __str__(self):
        return f'Speed {self.speed_id}'

# Signal 모델
class Signal(models.Model):
    signal_id = models.AutoField(primary_key=True, verbose_name='신호 식별자')
    road = models.ForeignKey(Road, on_delete=models.RESTRICT, verbose_name='도로 식별자')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.RESTRICT, verbose_name='차량 식별자')
    signal_violation_yn = models.CharField(max_length=1, verbose_name='신호 위반 여부', blank=True, default='N')
    signal_violation_img = models.CharField(max_length=1000, verbose_name='위반 이미지', blank=True)

    class Meta:
        db_table = 'tb_signal'
        verbose_name = '신호위반'
        verbose_name_plural = '신호위반'

    def __str__(self):
        return f'Signal {self.signal_id}'

# Speed와 Signal 항목을 저장하는 시그널 핸들러
@receiver(post_save, sender=Vehicle)
def create_speed_and_signal_entries(sender, instance, created, **kwargs):
    if created:
        # 기본 도로를 가정함, 실제 로직에 맞게 조정 필요
        default_road = Road.objects.first()  # 예시이므로 실제 로직으로 교체 필요
        Speed.objects.create(vehicle=instance, road=default_road, speed=0.0, speed_violation_yn='N')
        Signal.objects.create(vehicle=instance, road=default_road, signal_violation_yn='N')

# 시그널 핸들러 연결
post_save.connect(create_speed_and_signal_entries, sender=Vehicle)



