import datetime
from django.db import connection
from django.shortcuts import render
from django.db.models import Count, Avg
from django.db.models.functions import ExtractHour
import matplotlib.pyplot as plt
import io
import base64
import matplotlib.cm as cm
from matplotlib import font_manager, rc, rcParams
from pedestrian.models import Pedestrian
from vehicle.models import Speed, Vehicle
from .models import VehiclePedestrian
from road.models import Road


def index(request):
    return render(request, '../templates/includes/sidebar.html')

def admin(request):
    # 한글 폰트 설정
    font_path = "home/static/font/NanumBarunGothic.ttf"  # 시스템에 설치된 한글 폰트 경로
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)


    # GET 요청에서 날짜와 도로 정보 가져오기
    selected_date = request.GET.get('date')
    selected_road_id = request.GET.get('road_id')

    roads = Road.objects.all()


    data = VehiclePedestrian.objects.values('road_name').annotate(count=Count('pedestrian_id'))
    road_names = [entry['road_name'] for entry in data]
    counts = [entry['count'] for entry in data]
    wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
    colors = cm.Paired(range(len(road_names)))

    plt.figure(figsize=(4, 5), facecolor="#F0F2F5")
    plt.pie(counts, labels=road_names, autopct='%1.1f%%', colors=colors, startangle=100, wedgeprops=wedgeprops)
    plt.legend(road_names, title="도로이름",loc="best", shadow=True, ncol=1)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    a_graph = base64.b64encode(image_png).decode('utf-8')





    # 각 도로별 일반평균, 위반 평균, 안 위반 평균 속도 반환 시작
    if selected_road_id:
        with connection.cursor() as cursor:
                # 평균 속도 쿼리
                cursor.execute("""
                    SELECT AVG(speed)
                    FROM tb_speed
                    WHERE road_id = %s
                """, [selected_road_id])
                avg_speed_all = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT AVG(speed)
                    FROM tb_speed
                    WHERE speed_violation_yn = 'Y'
                    AND road_id = %s
                """, [selected_road_id])
                avg_speed_violation = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT AVG(speed)
                    FROM tb_speed
                    WHERE speed_violation_yn = 'N'
                    AND road_id = %s
                """, [selected_road_id])
                avg_speed_no_violation = cursor.fetchone()[0]
    else:
        avg_speed_all = avg_speed_violation = avg_speed_no_violation = None


    # 각 도로별 일반평균, 위반 평균, 안 위반 평균 속도 반환 끝

    # 그래프 데이터 초기화
    hours = [23, 0, 1, 2, 3, 4, 5]
    vehicle_counts = {hour: 0 for hour in hours}
    pedestrian_counts = {hour: 0 for hour in hours}

    if selected_date and selected_road_id:
        selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
        start_time = selected_date.replace(hour=23, minute=0, second=0)
        end_time = (selected_date + datetime.timedelta(days=1)).replace(hour=6, minute=0, second=0)

        # 차량 데이터 집계
        vehicle_data = Vehicle.objects.filter(
            road_id=selected_road_id,
            detection_time__range=(start_time, end_time)
        ).annotate(
            hour=ExtractHour('detection_time')
        ).values('hour').annotate(
            vehicle_count=Count('vehicle_id')
        ).order_by('hour')

        # 보행자 데이터 집계
        pedestrian_data = Pedestrian.objects.filter(
            road_id=selected_road_id,
            detection_time__range=(start_time, end_time)
        ).annotate(
            hour=ExtractHour('detection_time')
        ).values('hour').annotate(
            pedestrian_count=Count('pedestrian_id')
        ).order_by('hour')

        # 데이터 집계
        for entry in vehicle_data:
            hour = entry['hour']
            if hour == 23:
                vehicle_counts[23] = entry['vehicle_count']
            elif hour < 6:
                vehicle_counts[hour] = entry['vehicle_count']

        for entry in pedestrian_data:
            hour = entry['hour']
            if hour == 23:
                pedestrian_counts[23] = entry['pedestrian_count']
            elif hour < 6:
                pedestrian_counts[hour] = entry['pedestrian_count']

    # 차량 수 막대 그래프 생성
    plt.figure(figsize=(3, 5),facecolor="#F0F2F5")
    bar_width = 0.35
    index = range(len(hours))

    plt.bar(index, [vehicle_counts[hour] for hour in hours], bar_width, label='Vehicles', color='blue')
    plt.xlabel('Hour')
    plt.ylabel('Count')
    plt.xticks(index, ['23', '00', '01', '02', '03', '04', '05'])
    plt.legend()
    plt.grid(True)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    vehicle_graph = base64.b64encode(image_png).decode('utf-8')
    plt.clf()

    # 보행자 수 막대 그래프 생성
    plt.figure(figsize=(3,5),facecolor="#F0F2F5")
    plt.bar(index, [pedestrian_counts[hour] for hour in hours], bar_width, label='Pedestrians', color='red')
    plt.xlabel('Hour')
    plt.ylabel('Count')
    plt.xticks(index, ['23', '00', '01', '02', '03', '04', '05'])
    plt.legend()
    plt.grid(True)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    pedestrian_graph = base64.b64encode(image_png).decode('utf-8')






    return render(request, '../templates/includes/admin.html', {
        'roads': roads,
        'a_graph': a_graph,
        'vehicle_graph': vehicle_graph,
        'pedestrian_graph': pedestrian_graph,
        "avg_speed_all":avg_speed_all,
        "avg_speed_violation":avg_speed_violation,
        "avg_speed_no_violation":avg_speed_no_violation,
        "selected_date":selected_date,

    })