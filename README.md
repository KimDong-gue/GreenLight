# GreenLight


### <b>야간 보행자를 보호하기 위한 스마트 AI 신호등</b>

<br><br>

## 1. Collaborator
- 강은지 (PM, Back-end, 데이터시각화)
- 김동신 (AI Modeling, Back-end)
- 정수연 (Front-end, 데이터 시각화)
- 노정환 (Back-end)
<br><br>

## 2. Tech
- Front-End
<br><br>
 ![image](https://github.com/user-attachments/assets/6b174715-1b5e-49c9-9489-337fe93c0c99)

  
- Back-End
<br><br>
     ![image](https://github.com/user-attachments/assets/dbf58f13-c831-40b1-99cb-a0c618f0d0d5)
    ![image](https://github.com/user-attachments/assets/654c9eec-a4b6-4c34-8499-448fb38e08dd)


  <br>

  - Edit Tool
  <br><br>
      <img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=flat-square&logo=Visual Studio Code&logoColor=white">&nbsp;
      <img src="https://img.shields.io/badge/Mysql Workbench-4479A1?style=flat-square&logo=Mysql&logoColor=white">&nbsp;

     <img src="https://img.shields.io/badge/Django-0A3711?style=flat-square&logo=Django&logoColor=green">&nbsp;
    
<br><br>

## 3. Project Management (23.11.03 ~ 23.12.14)
### 프로젝트 개발 방식
  - #### `Front-End`

    `Django Framework`를 활용하여 UI/UX 설계
    <br>
  - #### `Back-End`

    `RESTful API`를 통한 서버 통신, `MySQL`로 데이터베이스 설계.
    <br>
  - #### `AI Model`

    `Yolo v10n`을 이용하여, 사람과 자동차 객체 ID, 정확도, 속도 및 Tracking 기능 이용하여 탐지지
    
    <br>

## 4. 프로젝트 상세 내용
<div align='center'>
  
  |목차 & 기획 의도|
  |---|
  |![image](https://github.com/user-attachments/assets/f191045d-976a-4fee-86a8-3e3975382fcd)|
  <br>
  

  |사용한 Tech & AI Model|
  |---|
  |`Yolo v10 Nano`, `matplotlib`, `OpenCV`|
  <br>
 
  |Gantt Chart & Flow Chart|
  |---|
  |![image](https://github.com/user-attachments/assets/3a4c8ebc-34c0-49cc-ae1a-08c110346ed4)|
  |![image](https://github.com/KimDong-gue/Healthy-Mento/assets/116249934/449f5882-8d72-43cd-8855-6cf162d26e3c)|

  <br>
  

  <br>
  
  |시행 착오 / 개선 사항|
  |---|
  |<div align='center'>시행 착오</div>|
  |![image](https://github.com/user-attachments/assets/b2edb52f-4228-4e2c-a1a4-6a70efa5416c)|
  |- `Yolo v10 Nano` 모델링시, 동시에 검출된 객체가 ID값이 동일시되고, Tracking기능이 꼬이는 상황 발생|
| - time_diff(시간)이 0이 되어 ZeroDivisionError발생하는 것을 확인하고, 객체의 초기 감지시, 시간 값 저장을 보장하여 오류를 해결|
 |![image](https://github.com/user-attachments/assets/d3df2da6-2216-4ac9-bcb0-643e2cce4019) |
| 야간 시간대 조회 문제로 자정을 넘어가는 시간을 체크하는데 데이터를 가져오지 못하는 문제 발생 |
| start_time과 end_time을 특정 시간대를 설정하여 필터링하여 해결하였다. |


  <br>
  
  
</div>

