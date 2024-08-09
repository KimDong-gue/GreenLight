import pygame
import time
import torch
import cv2
import numpy as np

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen = pygame.display.set_mode((300, 500))
pygame.display.set_caption("Traffic Light Simulation")

# 색상 정의
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

class TrafficLight:
    def __init__(self, screen):
        self.screen = screen
        self.state = "RED"  # 초기 신호등 상태는 빨간불
        self.pedestrian_detected = False  # 보행자 감지 여부
        self.car_detected = False  # 자동차 감지 여부
        self.last_change_time = time.time()  # 마지막 신호 변경 시간
        self.flash_state = False  # 점멸 신호등 상태

    def update(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_change_time

        if self.pedestrian_detected or self.car_detected:
            if self.state == "GREEN" and elapsed_time >= 4:
                self.state = "RED"
                self.last_change_time = current_time
            elif self.state == "RED" and elapsed_time >= 2:
                self.state = "YELLOW"
                self.last_change_time = current_time
            elif self.state == "YELLOW" and elapsed_time >= 2:
                self.state = "GREEN"
                self.last_change_time = current_time
            self.flash_state = False  # 보행자나 자동차가 감지되면 점멸 상태 해제
        else:
            # 보행자가 감지되지 않으면 점멸 신호등 상태로 변경
            if self.state == "YELLOW" and elapsed_time >= 0.5:  # 점멸 주기 조절 (예: 0.5초)
                self.flash_state = not self.flash_state
                self.last_change_time = current_time
            elif self.state != "YELLOW" and elapsed_time >= 5:
                if self.state == "RED":
                    self.state = "GREEN"
                elif self.state == "GREEN":
                    self.state = "YELLOW"
                self.last_change_time = current_time
            elif self.state == "YELLOW" and elapsed_time >= 2:
                self.state = "RED"
                self.last_change_time = current_time

    def draw(self):
        self.screen.fill(BLACK)

        # 빨간불 그리기
        if self.state == "RED":
            pygame.draw.circle(self.screen, RED, (150, 150), 50)
        else:
            pygame.draw.circle(self.screen, BLACK, (150, 150), 50)

        # 노란불 그리기
        if self.state == "YELLOW":
            if self.flash_state and not self.pedestrian_detected:  # 깜박이는 노란불 효과
                pygame.draw.circle(self.screen, YELLOW, (150, 250), 50)
            else:
                pygame.draw.circle(self.screen, BLACK, (150, 250), 50)  # 원을 검은색으로 그려서 노란색 원을 숨김
        else:
            pygame.draw.circle(self.screen, BLACK, (150, 250), 50)

        # 초록불 그리기
        if self.state == "GREEN":
            pygame.draw.circle(self.screen, GREEN, (150, 350), 50)
        else:
            pygame.draw.circle(self.screen, BLACK, (150, 350), 50)

        pygame.display.flip()

# 신호등 인스턴스 생성
traffic_light = TrafficLight(screen)

# YOLO v5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# 카메라 캡처 설정 (노트북의 내장 카메라 사용)
cap = cv2.VideoCapture(0)

def detect_objects(frame):
    results = model(frame)
    df = results.pandas().xyxy[0]
    pedestrian_detected = False
    car_detected = False
    for i in range(len(df)):
        label = df['name'][i]
        x1, y1, x2, y2 = int(df['xmin'][i]), int(df['ymin'][i]), int(df['xmax'][i]), int(df['ymax'][i])
        if label == 'person':
            pedestrian_detected = True
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, 'person', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        elif label == 'car':
            car_detected = True
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, 'car', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return pedestrian_detected, car_detected

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    pedestrian_detected, car_detected = detect_objects(frame)
    traffic_light.pedestrian_detected = pedestrian_detected
    traffic_light.car_detected = car_detected
    
    traffic_light.update()  # 신호등 상태 업데이트
    traffic_light.draw()    # 화면에 신호등 그리기
    
    # 카메라 영상 출력
    cv2.imshow('Camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    time.sleep(0.1)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
