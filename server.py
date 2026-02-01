import socket, os, random, string, hashlib, json
from cryptography.fernet import Fernet

PORT = 7331
PASW = "file-transfer-bot!gn"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", PORT))
server.listen()

while True:
    conn, addr = server.accept()
    print("[*] Verbindung von: ", addr)

    ENC_KEY = conn.recv(44)
    fernet = Fernet(ENC_KEY)

    nonce = "".join(random.choice(string.ascii_letters) for _ in range(10))
    N_PASW = hashlib.sha256(f"{nonce}{PASW}".encode()).hexdigest()

    conn.send(fernet.encrypt( nonce.encode() ))
    U_PASW = fernet.decrypt( conn.recv(4096) )

    if U_PASW.decode() != N_PASW:
        print(addr[0], " Wrong hashed pasw")
        conn.close()
        continue
    
    DATA = {}
    for element in os.listdir("./dateien"):
        DATA[element] = open("./dateien/" + element, "rb").read().decode()
    
    DATA_STRING = json.dumps(DATA)
    ENC_DATA = fernet.encrypt(DATA_STRING.encode())

    length = len(ENC_DATA).to_bytes(6, "big")
    conn.sendall(length + ENC_DATA)

    conn.close()