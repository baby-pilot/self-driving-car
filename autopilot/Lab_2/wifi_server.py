import socket
import picar_4wd as fc
import threading
import subprocess
import json
#from picamera import PiCamera
import time
import io
import struct
import numpy as np
import cv2 as cv

def get_local_ip_address():
    try:
        ip_address = subprocess.check_output(["hostname", "-I"]).decode("utf-8").split()[0]
        return ip_address
    except subprocess.CalledProcessError:
        print("Error retrieving IP address.")
        return None
    
HOST = get_local_ip_address() or "192.168.0.15" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
POWER = 10            # Power of motors

'''
Send metrics sends
car's battery state,
current speed, and cpu temp
to the client
'''
def get_metrics():
    print("sending metrics...")
    metrics = {}
    # get battery state
    metrics['battery'] = fc.power_read()
    # get speed
    metrics['speed'] = fc.speed_val()
    # get cpu temp
    metrics['cpu_temp'] = fc.cpu_temperature()
    return metrics


def handle_client(client, client_info):
    try:
        command = client.recv(1024).decode('utf-8').strip()
        if command == "start_camera":
            threading.Thread(target=send_camera_feed, args=(client, client_info)).start()
        else:
            while True:
                if not command:
                    break
                print(f"Received command from {client_info}: {command}")
                if command == "start_forward":
                    # Start moving forward
                    fc.forward(POWER)
                elif command == "start_reverse":
                    fc.backward(POWER)
                elif command == "start_left":
                    fc.turn_left(POWER)
                elif command == "start_right":
                    fc.turn_right(POWER)
                elif command == "stop_car":
                    # Stop moving forward
                    fc.stop()
                    break
                elif command == "get_metrics":
                    metrics = get_metrics()
                    client.sendall(json.dumps(metrics).encode())
                    break
                else:
                    print("Invalid command received: ", command)
                    break
    except Exception as e:
        print(f"Error handling client {client_info}: {e}")
    finally:
        client.close()

def send_camera_feed(client, client_info):
    try:
        # Create a stream for the camera to capture frames
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Cannot receive frame. Exiting...")
                break
            
            # Send the size of the data followed by the data itself
            size = len(frame)
            client.sendall(struct.pack('<L', size) + frame)

            time.sleep(0.1)  # Adjust the interval based on your needs

    except Exception as e:
        print(f"Error sending camera feed to {client_info}: {e}")
    finally:
        client.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    try:
        while True:
            client, client_info = s.accept()
            print(f"Connection from {client_info}")
            # Receive the message from the client
            # message = client.recv(1024).decode('utf-8').strip()

            # if message == "get_metrics":
            #     threading.Thread(target=send_metrics, args=(client, client_info)).start()
            # else:
            threading.Thread(target=handle_client, args=(client, client_info)).start()
            threading.Thread(target=send_camera_feed, args=(client, client_info)).start()
    except KeyboardInterrupt:
        # Handle Ctrl+C for a graceful shutdown
        print("Server shutting down.")
    except Exception as e:
        # Handle specific exceptions based on your requirements
        print(f"Exception: {e}")
    finally:
        s.close()

############## unused #################
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     client, clientInfo = s.accept()
#     try:
#         while 1:
#             client, clientInfo = s.accept()
#             print("server recv from: ", clientInfo)
#             data = client.recv(1024)      # receive 1024 Bytes of message in binary format
#             if data != b"":
#                 # match action
#                 print(data)
#                 client.sendall(data) # Echo back to client
#     except:
#         print("Closing socket")
#         client.close()
#         s.close()