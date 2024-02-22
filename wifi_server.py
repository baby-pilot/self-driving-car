import socket
import subprocess

def get_local_ip_address():
    try:
        ip_address = subprocess.check_output(["hostname", "-I"]).decode("utf-8").split()[0]
        return ip_address
    except subprocess.CalledProcessError:
        print("Error retrieving IP address.")
        return None
    
HOST = get_local_ip_address() or "192.168.0.15" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'server at {HOST} listening on port {PORT}...')

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                print(data)     
                client.sendall(data) # Echo back to client
    except: 
        print("Closing socket")
        client.close()
        s.close()    