import cv2
import time
import paho.mqtt.client as mqtt
import base64

MQTT_SERVER = "10.11.12.173"
IMAGE_W = 640
IMAGE_H = 480

cap = cv2.VideoCapture('/dev/video0')  # 使用你提供的设备路径

# 记录起始时间
start_time = time.time()

# Initialize the MQTT client
client = mqtt.Client()
client.connect(MQTT_SERVER, 1883, 60)

try:
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            # Convert the frame to JPEG
            ret, jpeg = cv2.imencode('.jpg', frame)

            if not ret:
                raise Exception('Could not encode image!')

            b64_string = base64.b64encode(jpeg.tobytes()).decode('utf-8')

            # Publish the encoded string via MQTT
            client.publish("robot/camera/image_raw", b64_string)
            print("sent a image to mqtt server")

            # 如果录制了10秒钟，就跳出循环
            if time.time() - start_time > 10:
                break
        else:
            break
except KeyboardInterrupt:
    print("KeyboardInterrupt")
finally:
    # 完成后释放所有内容
    cap.release()
    cv2.destroyAllWindows()
    print("已完成录像")
