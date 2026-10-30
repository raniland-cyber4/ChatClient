import socket
import threading
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

clients = {}

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()
pem_public_key = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

i = 0
color_list = [
    "cyan", "pink", "magenta", "hotpink", "deeppink",
    "yellow", "gold", "lime", "spring green", "chartreuse",
    "orange", "coral", "deep sky blue", "dodger blue",
    "royal blue", "medium orchid", "dark orchid", "violet", "turquoise"
]


def Client_Handle(conn, addr):
    print(f"{addr} connected.")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            clr, username, sender_suite = clients.get(conn, ("white", "admin", None))
            decrypted_msg = sender_suite.decrypt(data).decode('utf-8')
            msg_to_broadcast = f"{clr}|{username}: {decrypted_msg}"
            print(f"{msg_to_broadcast}")

            for client_conn, (c_clr, c_user, c_suite) in list(clients.items()):
                try:
                    enc_msg = c_suite.encrypt(msg_to_broadcast.encode('utf-8'))
                    client_conn.send(enc_msg)
                except Exception as e:
                    print(f"Error sending to {c_user}: {e}")

        except Exception as e:
            print(f"Connection error with {addr}: {e}")
            break

    print(f"{addr} disconnected.")
    if conn in clients:
        left_clr, left_user, _ = clients[conn]
        del clients[conn]

        leave_msg = f"{left_clr}|❌ {left_user} left the chat."
        for client_conn, (_, _, c_suite) in list(clients.items()):
            try:
                enc_leave = c_suite.encrypt(leave_msg.encode('utf-8'))
                client_conn.send(enc_leave)
            except:
                pass
    conn.close()


def start_server():
    global i
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 55555))
    server.listen()
    print("Server is listening on port 55555...")

    while True:
        try:
            conn, addr = server.accept()
            info = conn.recv(1024).decode('utf-8').strip()
            if " ץ " not in info:
                conn.close()
                continue

            username, passcode = info.split(" ץ ")
            signs = "!@#$%^&*?_"

            if len(passcode) < 6 or (not any(c.isupper() for c in passcode) and not any(c in signs for c in passcode)):
                conn.send("Access denied, incorrect password..".encode("utf-8"))
                conn.close()
                continue

            clr = color_list[i % len(color_list)]
            i += 1

            conn.send(f"Access Granted|{clr}|".encode("utf-8") + pem_public_key)

            enc_fernet_key = conn.recv(1024)
            client_fernet_key = private_key.decrypt(
                enc_fernet_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            client_suite = Fernet(client_fernet_key)
            clients[conn] = (clr, username, client_suite)

            join_msg = f"{clr}|⫗ {username} has joined the chat!"
            for client_conn, (_, _, c_suite) in list(clients.items()):
                try:
                    client_conn.send(c_suite.encrypt(join_msg.encode('utf-8')))
                except:
                    pass

            th = threading.Thread(target=Client_Handle, args=(conn, addr))
            th.daemon = True
            th.start()

        except Exception as e:
            print(f"Error accepting connection: {e}")


if __name__ == "__main__":
    start_server()