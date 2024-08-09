import time
import numpy as np
import cv2
from ultralytics import YOLO
from sort import Sort
from django.utils import timezone
import pygame
import os
import random
import traceback
import sys

# Django settings initialization
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

# Django models import
from road.models import Road
from vehicle.models import Vehicle, Speed, Signal
from pedestrian.models import Pedestrian

# test2 module import (event function control)
from update_xml import test

# Initialize variables
results = {}
RoadB = {3, 4}
RoadC = {1, 2}
mot_tracker = Sort()
vehicles = [2, 3, 5, 7]  # Car, motorcycle, truck, bicycle
frame_nmr = 0
video_path = 'yolo__traffic/test/greenlight+.mp4'
output_dir = 'yolo__traffic/detected_images'
os.makedirs(output_dir, exist_ok=True)

# 한글 문자 리스트
KOREAN_CHARACTERS = ['가', '나', '다', '라', '마', '바', '사', '아', '자', '차', '카', '타', '파', '하']

def generate_vehicle_num():
    numbers = f'{random.randint(10, 99)}'
    korean_char = random.choice(KOREAN_CHARACTERS)
    serial = f'{random.randint(1000, 9999)}'
    return f'{numbers}{korean_char}{serial}'

def draw_border(img, top_left, bottom_right, color=(0, 255, 0), thickness=10, line_length_x=200, line_length_y=200):
    x1, y1 = top_left
    x2, y2 = bottom_right

    cv2.line(img, (x1, y1), (x1, y1 + line_length_y), color, thickness)
    cv2.line(img, (x1, y1), (x1 + line_length_x, y1), color, thickness)
    cv2.line(img, (x1, y2), (x1, y2 - line_length_y), color, thickness)
    cv2.line(img, (x1, y2), (x1 + line_length_x, y2), color, thickness)
    cv2.line(img, (x2, y1), (x2 - line_length_x, y1), color, thickness)
    cv2.line(img, (x2, y1), (x2, y1 + line_length_y), color, thickness)
    cv2.line(img, (x2, y2), (x2, y2 - line_length_y), color, thickness)
    cv2.line(img, (x2, y2), (x2 - line_length_x, y2), color, thickness)

    return img

def calculate_speed(previous_pos, current_pos, time_diff, pixel_to_meter_ratio):
    distance = np.linalg.norm(np.array(current_pos) - np.array(previous_pos))
    if time_diff > 0:
        speed_pixels_per_sec = distance / time_diff
        speed_kmh = speed_pixels_per_sec * pixel_to_meter_ratio * 3.6
    else:
        speed_kmh = 0
    return speed_kmh

def is_intersecting(box1, box2):
    x1, y1, x2, y2 = box1
    x1p, y1p, x2p, y2p = box2
    return not (x2 < x1p or x1 > x2p or y2 < y1p or y1 > y2p)

def main():
    cap = None
    try:
        model = YOLO("yolov10n.pt")
        plate_model = YOLO("yolo__traffic/license_plate_detector.pt")
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("Error opening video file.")
            return

        person_ids = {}  # Mapping of obj_id to person_id
        vehicle_ids = {}  # Mapping of obj_id to vehicle_id
        object_paths = {}  # Mapping of obj_id to list of positions
        object_times = {}  # Mapping of obj_id to last detection time
        frame_count = 0
        next_person_id = 1
        next_vehicle_id = 1
        saved_vehicle_ids = set()
        processed_license_plates = {}
        speed_kmh = 0  # Initialize speed_kmh to avoid UnboundLocalError

        road = Road.objects.get(road_id=2)
        mot_tracker = Sort()

        pixel_to_meter_ratio = 0.05  # Example conversion ratio

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("End of video or error reading frame.")
                break

            results = model.track(source=frame, persist=True, classes=[0, 2, 3, 5, 7])
            current_time = time.time()

            persons_detected = False
            cars_detected = False
            bicycle_detected = False
            motorcycle_detected = False
            bus_detected = False
            truck_detected = False

            vehicle_boxes = []
            vehicle_ids_for_boxes = []
            person_boxes = {}
            person_ids_for_boxes = {}
            motorcycle_boxes = []  # Track motorcycle boxes
            bus_boxes = []  # Track bus boxes

            for result in results:
                for box in result.boxes:
                    cls = box.cls[0]
                    conf = box.conf[0]
                    xyxy = box.xyxy[0]
                    obj_id = int(box.id[0]) if box.id is not None else None
                    if obj_id is None:
                        continue

                    label = model.names[int(cls)]
                    confidence = conf.item()

                    if label == 'person':
                        if not any(is_intersecting(xyxy, moto_box) for moto_box in motorcycle_boxes) and \
                            not any(is_intersecting(xyxy, bus_box) for bus_box in bus_boxes):
                            persons_detected = True
                            if obj_id not in person_ids:
                                person_ids[obj_id] = next_person_id
                                next_person_id += 1
                                Pedestrian.objects.create(
                                    road=Road.objects.get(road_id=2),
                                    detection_time=timezone.now(),
                                    box_id=obj_id
                                )
                                print("사람객체 저장")
                            person_id = person_ids[obj_id]
                            color = (0, 255, 0)  # Color for persons (Green)
                            cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), color, 2)
                            label_text = f'Person ID: {person_id}'
                            cv2.putText(frame, label_text, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                            confidence_text = f'Conf: {confidence:.2f}'
                            cv2.putText(frame, confidence_text, (int(xyxy[0]), int(xyxy[1]) - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

                    elif label in ['car', 'bicycle', 'motorcycle', 'bus', 'truck']:
                        if label == 'car':
                            cars_detected = True
                        elif label == 'bicycle':
                            bicycle_detected = True
                        elif label == 'motorcycle':
                            motorcycle_detected = True
                            motorcycle_boxes.append(xyxy)  # Track motorcycle boxes
                        elif label == 'bus':
                            bus_detected = True
                            bus_boxes.append(xyxy)  # Track bus boxes
                        elif label == 'truck':
                            truck_detected = True

                        if obj_id not in vehicle_ids:
                            vehicle_ids[obj_id] = next_vehicle_id
                            next_vehicle_id += 1
                            instance = Vehicle.objects.create(
                                vehicle_num=generate_vehicle_num(),
                                vehicle_type=label,
                                detection_time=timezone.now(),
                                road=Road.objects.get(road_id=2)
                            )
                            print("일반차량 DB저장 완료")

                        vehicle_id = vehicle_ids[obj_id]
                        color = (0, 0, 255)  # Color for vehicles (red)

                        vehicle_boxes.append(xyxy)
                        vehicle_ids_for_boxes.append(vehicle_id)

                        cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), color, 2)
                        label_text = f'{label} ID: {vehicle_id}'
                        cv2.putText(frame, label_text, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                        confidence_text = f'Conf: {confidence:.2f}'
                        cv2.putText(frame, confidence_text, (int(xyxy[0]), int(xyxy[1]) - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

                        if obj_id not in object_paths:
                            object_paths[obj_id] = []
                        object_paths[obj_id].append((int((xyxy[0] + xyxy[2]) / 2), int((xyxy[1] + xyxy[3]) / 2)))

                        if obj_id not in object_times:
                            object_times[obj_id] = current_time
                        else:
                            previous_time = object_times[obj_id]
                            object_times[obj_id] = current_time

                            time_diff = current_time - previous_time

                            if time_diff > 0 and label != 'person':
                                speed_kmh = calculate_speed(object_paths[obj_id][-2], object_paths[obj_id][-1], time_diff, pixel_to_meter_ratio)
                                cv2.putText(frame, f'Speed: {int(speed_kmh)} km/h', (int(xyxy[0]), int(xyxy[1]) - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

                                if speed_kmh >= 15:
                                    plate_results = plate_model(frame)

                                    for plate_result in plate_results:
                                        for box in plate_result.boxes:
                                            plate_xyxy = box.xyxy[0]
                                            plate_box = [int(plate_xyxy[0]), int(plate_xyxy[1]), int(plate_xyxy[2]), int(plate_xyxy[3])]
                                            for vehicle_box, vehicle_id in zip(vehicle_boxes, vehicle_ids_for_boxes):
                                                if is_intersecting(plate_box, vehicle_box):
                                                    if vehicle_id not in processed_license_plates:
                                                        plate_img = frame[int(plate_xyxy[1]):int(plate_xyxy[3]), int(plate_xyxy[0]):int(plate_xyxy[2])]
                                                        plate_image_path = os.path.join(output_dir, f'license_plate_{frame_count:04d}.jpg')
                                                        cv2.imwrite(plate_image_path, plate_img)
                                                        print(f"License plate image saved: {plate_image_path}")

                                                        cv2.imshow(f'License Plate - Frame {frame_count}', plate_img)
                                                        cv2.waitKey(1000)

                                                        processed_license_plates[vehicle_id] = plate_image_path
                                                        break

                        for i in range(1, len(object_paths[obj_id])):
                            cv2.line(frame, object_paths[obj_id][i - 1], object_paths[obj_id][i], color, 2)

            try:
                # Ensure 'instance' is defined before using it
                if 'instance' in locals():
                    if (cars_detected or bicycle_detected or motorcycle_detected or bus_detected or truck_detected) and not persons_detected:
                        test(0)
                        print("차량만 감지됨")
                        if speed_kmh >= 15:
                            Speed.objects.create(
                                vehicle=instance,
                                speed=speed_kmh,
                                road=Road.objects.get(road_id=2),
                                speed_violation_yn='Y',
                                speed_violation_img=None
                            )
                            Signal.objects.create(
                                vehicle=instance,
                                road=Road.objects.get(road_id=2),
                                signal_violation_yn='Y',
                                signal_violation_img=None
                            )
                            print("점멸시, 속도,신호위반 차량만 DB저장됨")
                    elif persons_detected and (cars_detected or bicycle_detected or motorcycle_detected or bus_detected or truck_detected): 
                        print("사람과 차량이 감지됨")
                        test(5)
                        person_time = time.time()
                        car_time = time.time()
                        if abs(car_time - person_time) <= 60:
                            if speed_kmh >= 5:
                                test(4)
                                road.red_light += 1
                                road.save()
                                detections = model(frame)[0]
                                detections_ = []
                                for detection in detections.boxes.data.tolist():
                                    print(f"Detection raw data: {detection}")  # Debug print
                                    if len(detection) >= 6:
                                        x1, y1, x2, y2, score, class_id = detection[:6]
                                        detections_.append([x1, y1, x2, y2, score, class_id])
                                    else:
                                        print(f"Unexpected detection format: {detection}")  # Debug print
                                detections_ = np.asarray(detections_)

                                if detections_.size > 0:
                                    track_ids = mot_tracker.update(detections_)
                                else:
                                    track_ids = mot_tracker.update(np.empty((0, 5)))

                                if instance and vehicle_id not in saved_vehicle_ids:
                                    output_path = os.path.join(output_dir, f'speeding_car_frame_{frame_count:04d}.jpg')
                                    cv2.imwrite(output_path, frame)
                                    saved_vehicle_ids.add(vehicle_id)
                                    pygame.mixer.init()
                                    try:
                                        pygame.mixer.music.load("hi.mp3")
                                    except pygame.error as e:
                                        print(f"Error loading MP3 file: {e}")
                                    pygame.mixer.music.play()
                                    while pygame.mixer.music.get_busy():
                                        pygame.time.Clock().tick(10)
                                    print("Speeding car image saved and sound played!")
                                    print(output_path)
                                    Speed.objects.create(
                                        vehicle=instance,
                                        speed=speed_kmh,
                                        road=Road.objects.get(road_id=2),
                                        speed_violation_yn='Y',
                                        speed_violation_img=None
                                    )

                                    Signal.objects.create(
                                        vehicle=instance,
                                        road=Road.objects.get(road_id=2),
                                        signal_violation_yn='Y',
                                        signal_violation_img=None
                                    )
                                    print("일반신호시, 신호, 과속 차량 DB 저장 완료")
                            else:
                                if instance:
                                    Speed.objects.create(
                                        vehicle=instance,
                                        speed=speed_kmh,
                                        road=Road.objects.get(road_id=2),
                                        speed_violation_yn='N',
                                        speed_violation_img=None
                                    )
                                    Signal.objects.create(
                                        vehicle=instance,
                                        road=Road.objects.get(road_id=2),
                                        signal_violation_yn='N',
                                        signal_violation_img=None
                                    )
                                    print("일반 차량 DB 저장 완료")
                else:
                    test(0)
            except Exception as e:
                print(f"Error during vehicle detection or processing: {e}")
                traceback.print_exc()

            frame_count += 1
            cv2.imshow('YOLO Object Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quitting...")
                break

    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()

    finally:
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()
        print("OpenCV windows destroyed.")

if __name__ == "__main__":
    main()
