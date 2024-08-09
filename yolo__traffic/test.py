import time
from datetime import datetime

# 현재 시간을 초 단위로 반환
current_time_in_seconds = time.time()
print("Current time in seconds:", current_time_in_seconds)

# 초 단위를 읽기 쉬운 형식으로 변환
readable_time = datetime.fromtimestamp(current_time_in_seconds).strftime('%Y-%m-%d %H:%M:%S')
print("Readable time:", readable_time)

# 예시: a와 b를 설정하고 3초 차이를 확인하는 코드
a = time.time()
time.sleep(3)  # 3초 대기
b = time.time()

print("Time a:", a)
print("Time b:", b)
print("Difference in seconds:", b - a)

# a와 b의 읽기 쉬운 형식 출력
readable_time_a = datetime.fromtimestamp(a).strftime('%Y-%m-%d %H:%M:%S')
readable_time_b = datetime.fromtimestamp(b).strftime('%Y-%m-%d %H:%M:%S')
print("Readable Time a:", readable_time_a)
print("Readable Time b:", readable_time_b)