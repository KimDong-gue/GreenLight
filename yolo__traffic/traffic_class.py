from gtts import gTTS
from playsound import playsound # playsound 모듈로부터 playsound 불러오기
import os # os 라이브러리 불러오기



text = "위반차량 감지. 안전에 유의하세요"

# tts 객체 생성 및 저장
tts = gTTS(text=text, lang='ko')
tts.save("hi.mp3")

# 음성 파일 재생
playsound("hi.mp3")
def only_car():
    # 차량만 있는 경우
    # -> 점멸 신호 유지 
    return
    

def one_way():
    # 보행자가 "한 횡단보도"에 1인만 있는 경우
    # 보행자가 "한 횡단보도"에 2인 이상 있는 경우
    # -> 보행자가 건너는 방향과 같은 방향으로 이동하는 차량에 대해서만 초록불 나머지 횡단보도 및 도로는 빨간불 유지
    return


def all_way():
    # 보행자가 "여러 횡단보도"에 여러 보행자가 있는 경우 -> 이 경우 먼저 도착 및 다 인원 보행자에 대한 우선순위를 주지 않음
    # 전체 횡단보도 신호는 초록불, 도로는 빨간불 유지
    # 47초 경과 후, 차량에게도 초록불을 신호를 일정시간 부여 후, 점멸신호로 전환
    return

"""
def only_car():
    # 차량만 있는 경우
    # -> 점멸 신호 유지 
    flash_signal_for_cars()
    
def flash_signal_for_cars():
    # 점멸 신호를 차량에게 유지하는 로직
    set_flash_signal_for_cars()  # 예를 들어, LED 패널에 점멸 신호 출력 등의 동작을 수행




def one_way(num_pedestrians):
    # num_pedestrians: 한 횡단보도에 있는 보행자 수
    if num_pedestrians == 1:
        allow_signal_for_pedestrians()  # 보행자에게 신호를 줌
        green_signal_for_crossing_direction()  # 해당 방향의 차량에 초록불 신호를 줌
        red_signal_for_other_directions()  # 다른 방향에는 빨간불 신호를 줌
    elif num_pedestrians >= 2:
        allow_signal_for_pedestrians()  # 보행자에게 신호를 줌
        green_signal_for_crossing_direction()  # 해당 방향의 차량에 초록불 신호를 줌
        red_signal_for_other_directions()  # 다른 방향에는 빨간불 신호를 줌

def allow_signal_for_pedestrians():
    # 보행자에게 신호를 줄 때의 동작
    set_signal_for_pedestrians()  # 예를 들어, LED 패널에 보행자 신호 출력 등의 동작을 수행
    
def green_signal_for_crossing_direction():
    # 해당 방향의 차량에 초록불 신호를 줄 때의 동작
    set_green_signal_for_crossing_direction()  # 예를 들어, LED 패널에 초록불 신호 출력 등의 동작을 수행
    
def red_signal_for_other_directions():
    # 다른 방향에 빨간불 신호를 줄 때의 동작
    set_red_signal_for_other_directions()  # 예를 들어, LED 패널에 빨간불 신호 출력 등의 동작을 수행

    
def all_way():
    allow_signal_for_pedestrians()  # 보행자에게 신호를 줌
    green_signal_for_all_crosswalks()  # 모든 횡단보도에 초록불 신호를 줌
    red_signal_for_all_roads()  # 모든 도로에 빨간불 신호를 줌
    schedule_flash_signal_after_47_seconds()  # 47초 후 점멸신호로 전환을 스케줄링
    
def green_signal_for_all_crosswalks():
    # 모든 횡단보도에 초록불 신호를 줄 때의 동작
    set_green_signal_for_all_crosswalks()  # 예를 들어, LED 패널에 초록불 신호 출력 등의 동작을 수행
    
def red_signal_for_all_roads():
    # 모든 도로에 빨간불 신호를 줄 때의 동작
    set_red_signal_for_all_roads()  # 예를 들어, LED 패널에 빨간불 신호 출력 등의 동작을 수행
    
def schedule_flash_signal_after_47_seconds():
    # 47초 후 점멸신호로 전환을 스케줄링하는 동작
    schedule_flash_signal()  # 점멸신호로 전환을 스케줄링하는 코드를 추가





"""
