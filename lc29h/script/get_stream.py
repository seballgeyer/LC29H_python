import time
import threading
import serial


stream = serial.Serial("/dev/ttyAMA0", 115200, timeout=3)

data = "Initial data"
buffer = 50
# while data:
#     try:
print("-")
# data=self.socket.recv(buffer)
# # self.out.buffer.write(data)
query = b"$PAIR432,1*22\r\n"
print("send:", query)
stream.write(query)
query = b"$PAIR062,-1,0*12\r\n"
diseable = [
    b"$PAIR062,0,0*3E\r\n",
    b"$PAIR062,1,0*3F\r\n",
    b"$PAIR062,2,0*3C\r\n",
    b"$PAIR062,3,0*3D\r\n",
    b"$PAIR062,4,0*3A\r\n",
    b"$PAIR062,5,0*3B\r\n",
    b"$PAIR062,6,0*38\r\n",
    b"$PAIR062,7,0*39\r\n",
    b"$PAIR062,8,0*36\r\n",
]
for i in diseable:
    print(i)
    stream.write(i)
    time.sleep(1)
query = b"$PAIR066,1,0,0,0,0,0*3B\r\n"
stream.write(query)
# d = stream.readlines()
# print(d)
# query = b"$PAIR432,0*22\r\n"
# print('send:', query)
# stream.write(query)
# d = stream.readlines()
# print(d)
# while True:
#     received_data = stream.read()              #read serial port
#     # time.sleep(0.03)
#     data_left = stream.inWaiting()             #check for remaining byte
#     received_data += stream.read(data_left)
#     print (received_data)                   #print received data
#     print("\n")
# ser.write(received_data)
# (raw_data, parsed_data) = nmr.read()
# print(raw_data)
# if bytes("GNGGA",'ascii') in raw_data :
#     print(raw_data)
stream.close()


# Function to handle decoding and printing in a separate thread
def process_data(data_queue, file_path):
    with open(file_path, "wb") as binary_file:
        while True:
            if not data_queue.empty():
                try:
                    data = data_queue.get()
                    binary_file.write(data)  # Write the binary data to file
                    binary_file.flush()  # Ensure data is written immediately
                    print(data)
                    # try:
                    #     msg = RTCMReader.parse(data, validate=1)
                    #     print(msg)
                    # except Exception as e:
                    #     msg = RTCMReader.parse(data, validate=0)
                    #     print("*", e)
                    #     print(msg)
                    #     print("===")

                except Exception as e:
                    print(f"Error writing to file: {e}")
                    pass


# Initialize the serial connection
ser = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3)

# Use a queue to pass data between threads
from queue import Queue

data_queue = Queue()

# Start a separate thread for decoding and printing
file_path = "output_data.bin"  # Path to the binary file
thread = threading.Thread(target=process_data, args=(data_queue, file_path))
thread.daemon = True
thread.start()
if 0 == 1:
    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)  # Read all available data
            data_queue.put(data)  # Put the data into the queue for processing

while True:
    if ser.in_waiting > 0:
        data = ser.read(64)  # Read a fixed number of bytes (e.g., 64 bytes)
        data_queue.put(data)

exit(0)
# except:
#     pass
