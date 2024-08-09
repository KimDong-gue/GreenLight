from bs4 import BeautifulSoup
import threading
import time

file_path = 'yolo__traffic/event.xml'
current_signal = 0  # Initialize with a default signal state
signal_lock = threading.Lock()  # Lock for thread-safe signal updates

def update_event_xml(value):
    global current_signal
    print(f"Updating event XML to {value}")
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml-xml')

    event_tag = soup.find('event')
    if event_tag is not None:
        event_tag.string = str(value)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    with signal_lock:
        current_signal = value
    print(f"Event XML updated to {value}")

def control_traffic_light(value, duration=5):
    print(f"Controlling traffic light to {value} for {duration} seconds")
    with signal_lock:
        if current_signal != value:
            update_event_xml(value)
            time.sleep(duration)
            update_event_xml(0)
        else:
            print(f"Signal already at {value}, no change required.")
    print(f"Traffic light control completed for {value}")

def test(value):
    thread = threading.Thread(target=control_traffic_light, args=(value,))
    thread.daemon = True  # Allow thread to be killed when main program exits
    thread.start()