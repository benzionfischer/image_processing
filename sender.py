import io
import socket
import struct
import time
import cv2

# create socket and connect to receiver
client_socket = socket.socket()
client_socket.connect(('localhost', 5551))

# create video capture object
capture = cv2.VideoCapture(0)

# set camera resolution and framerate
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
capture.set(cv2.CAP_PROP_FPS, 24)

# wait for camera to warm up
time.sleep(2)

# capture frames and send to receiver
while True:
    # capture frame from camera
    ret, frame = capture.read()

    # encode frame as JPEG image
    _, buffer = cv2.imencode('.jpg', frame)

    # pack image data into network byte order and send to receiver
    data = struct.pack(">L", len(buffer)) + buffer.tobytes()
    client_socket.sendall(data)

    # wait for 0.1 seconds to limit framerate
    time.sleep(0.1)
