import time
import serial
import threading
from queue import Queue

from lc29h.utils.checksum import compute_checksum


class SerialComm:
    def __init__(self, port="/dev/ttyAMA0", baudrate=115200, timeout=3):
        self.stream = serial.Serial(port, baudrate, timeout=timeout)
        self.data_queue = Queue()
        self.file_path = "output_data.bin"
        self.running = True

    def send_command(self, command: bytes):
        print(f"Sending: {command}")
        self.stream.write(command)
        time.sleep(1)  # Adjust sleep time as needed
        return self.receive_ack(command)

    def receive_ack(self, command: bytes):
        command_id = command.split(b",")[0][1:]  # Extract command ID from the command
        while False:
            # TODO: implement the answer not only ack
            ack = self.stream.read_until(b"\r\n")
            print(f"Received: {ack}")
            if ack.startswith(b"$PAIR001"):
                parts = ack.split(b",")
                if len(parts) >= 3 and parts[1] == command_id:
                    result = int(parts[2].split(b"*")[0])
                    return result
            time.sleep(0.1)  # Sleep briefly before checking again

    def read_stream(self, time_limit=None):
        start_time = time.time()
        while self.running:
            if time_limit and (time.time() - start_time) > time_limit:
                print("Time limit reached. Stopping the stream reading.")
                self.running = False
                break
            if self.stream.in_waiting > 0:
                data = self.stream.read(64)  # Read a fixed number of bytes (e.g., 64 bytes)
                self.data_queue.put(data)

    def process_data(self):
        with open(self.file_path, "wb") as binary_file:
            while self.running:
                try:
                    data = self.data_queue.get()
                    binary_file.write(data)  # Write the binary data to file
                    binary_file.flush()  # Ensure data is written immediately
                    print(data)
                    # Uncomment and adjust the following lines if RTCMReader is available
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

    def start(self, time_limit=None):
        self.running = True
        threading.Thread(target=self.process_data, daemon=True).start()
        self.read_stream(time_limit)

    def stop(self):
        self.running = False
        self.stream.close()


def send_initial_commands(comm: SerialComm):
    commands = [
        b"$PAIR432,1",
    ]
    for command in commands:
        chksum = compute_checksum(command)
        command += f"*{chksum}\r\n".encode()
        print(f"Sending command: {command}")
        result = comm.send_command(command)
        if result == 0:
            print(f"Command {command} executed successfully.")
        elif result == 1:
            print(f"Command {command} is waiting for process.")
        else:
            print(f"Command {command} failed with result code {result}.")


def main():
    comm = SerialComm()
    try:
        send_initial_commands(comm)
        # Start the communication with a time limit of 1 hour (3600 seconds)
        comm.start(time_limit=3600)
    except KeyboardInterrupt:
        comm.stop()


if __name__ == "__main__":
    main()
