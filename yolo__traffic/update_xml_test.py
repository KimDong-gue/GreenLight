import xml.etree.ElementTree as ET

file_path = r'yolo__traffic/event.xml'

def update_event_xml(event):
    # XML 파일 읽기
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # XML 선언 부분 제거
    if content.startswith('<?xml'):
        content = content.split('?>', 1)[1]

    # 가상의 루트 태그 추가
    wrapped_content = f"<root>{content}</root>"

    # 가상의 루트 태그가 추가된 내용을 파싱
    root = ET.fromstring(wrapped_content)

    # <event> 태그 내 내용 찾기 및 변경
    event_tag = root.find('event')
    if event_tag is not None:
        event_tag.text = str(event)



    # 변경된 내용을 다시 XML 문자열로 변환
    new_content = ET.tostring(root, encoding='unicode', method='xml')

    # 가상 루트 태그 제거
    new_content = new_content.replace('<root>', '').replace('</root>', '')

    # XML 선언 추가
    new_content = f'<?xml version="1.0" encoding="utf-8"?>{new_content}'

    # 변경된 내용 다시 파일에 저장
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

def test(event):
    update_event_xml(event)

# 테스트 실행
""" test(1, 10) """
