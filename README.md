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

     <img src="https://img.shields.io/badge/Django-F05032?style=flat-square&logo=Django&logoColor=green">&nbsp;
    
<br><br>

## 3. Project Management (23.11.03 ~ 23.12.14)
### 프로젝트 개발 방식
  - #### `Front-End`

    `Figma`를 활용하여 UI/UX 설계
    <br>
  - #### `Back-End`

    `FastAPI`를 통한 서버 통신, `MySQL`로 데이터베이스 설계.
    <br>
  - #### `AI Model`

    `Python`의 `MediaPipe`와`Motion Transfer` 메인으로 사용자에게 운동에 대해 가이드를 제시하고,
    `Yolo v8`을 이용하여, 음식을 분류하여, 칼로리와 가지고 있는 음식을 기반으로 `Chat GPT`로 하루 식단을 가이드
    
    <br>

## 4. 프로젝트 상세 내용
<div align='center'>
  
  |목차 & 기획 의도|
  |---|
  |![image](https://github.com/KimDong-gue/Second_Team_Project/assets/116249934/0a5f30ca-b9bf-484c-90fd-d438b6b5f842)|
  <br>
  
  |사용한 Tech & AI Model|
  |---|
  |`Media Pipe`, `Motion Transfer`, `Yolo v8 Small`, `Chat GPT`|
  <br>
  
  |Gantt Chart & Flow Chart|
  |---|
  |![image](https://github.com/user-attachments/assets/3a4c8ebc-34c0-49cc-ae1a-08c110346ed4)
|
  |![image](https://github.com/KimDong-gue/Healthy-Mento/assets/116249934/449f5882-8d72-43cd-8855-6cf162d26e3c)|

  <br>
  

  <br>
  
  |시행 착오 / 개선 사항|
  |---|
  |<div align='center'>시행 착오</div>|
  |![image](https://github.com/KimDong-gue/Healthy-Mento/assets/116249934/8abcb693-79d5-466c-b2c4-b9c6624c5c8a)|
  |- `Yolo v8 Small` 모델링시, `Data InBalance` 문제 때문에, 데이터 증강을 수행 후, 어느정도의 `InBalance`를 해결하였습니다.
| - `MediaPipe`로 운동 자세를 검출할 때, 초기에 발생한 다양한 어려움들을 극복하기 위해 끊임없는 실험과 수정 작업이 필요했습니다. 이러한 경험을 통해 데이터 다양성, 후처리 기술의 활용, 적절한 임계값 설정, 모델의 업데이트에 대한 중요성을 깨달았습니다. 이러한 과정을 통해 프로젝트를 성공적으로 완료할 수 있었습니다. 
| - `Motion Transfer` 모델링시, 초기에 프로토타입을 빠르게 구현하고 사용자에게 시각적으로 효과를 보여주는 것이 목표였습니다. 그 후, 데모버젼을 구현하는데 성공하였습니다. 

  <br>
  
  |<div align='center'>참고 문헌</div>|
  |---|
  |https://github.com/Daniil-Osokin/lightweight-human-pose-estimation.pytorch|
  ||
  |https://github.com/AliaksandrSiarohin/first-order-model|
  ||
  |https://github.com/svip-lab/impersonator|
  ||
  |https://github.com/Wangt-CN/DisCo?tab=readme-ov-file|
  <br>
  
</div>

