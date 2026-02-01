import socket, hashlib, json, os
from cryptography.fernet import Fernet

IP = input("IP: ") or "127.0.0.1"
PORT = 7331

def recv_exact(sock:socket.socket, n:int) -> bytes:
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Socked closed")
        data += chunk
    return data

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

KEY = Fernet.generate_key()
fernet = Fernet(KEY)

client.send(KEY)

nonce = fernet.decrypt( client.recv(4096) )
PASW = "file-transfer-bot!gn"
FULL_PASW = hashlib.sha256(f"{nonce.decode()}{PASW}".encode()).hexdigest()

client.send(fernet.encrypt( FULL_PASW.encode() ))


length = int.from_bytes(recv_exact(client, 6), "big")
ENC_DATA = recv_exact(client, length)

DATA_STRING = fernet.decrypt(ENC_DATA)
DATA:dict = json.loads(DATA_STRING.decode())

if not os.path.exists("C:/gnillip") or not os.path.exists("/gnillip"):
    if os.name == "nt":
        os.mkdir("C:/gnillip")
    else:
        os.mkdir("/gnillip")

for name, inhalt in DATA.items():
    if os.name == "nt":
        with open("C:/gnillip/"+name, "wb") as data:
            data.write(inhalt.encode())
    
    else:
        with open("/gnillip/"+name, "wb") as data:
            data.write(inhalt.encode())