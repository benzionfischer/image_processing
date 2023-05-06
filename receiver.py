import io
import socket
import struct
import cv2
import numpy as np

# create socket and bind to port
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 5551))
server_socket.listen(0)

# accept client connection
connection = server_socket.accept()[0]

# create empty bytes buffer
data = b''

# receive frames and display them
while True:
    # read image size from network byte order
    size = connection.recv(struct.calcsize(">L"))

    # break if no more data is received
    if not size:
        break

    # unpack image size and read image data from socket
    size = struct.unpack(">L", size)[0]
    print("size: {}".format(size))
    data = connection.recv(size)

    # convert data to OpenCV image
    image = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    if image is None:
        continue
    # display image
    cv2.imshow('Receiver', image)
    if cv2.waitKey(1) == ord('q'):
        break

# cleanup
cv2.destroyAllWindows()
connection.close()
server_socket.close()
