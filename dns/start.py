import threading
import psycopg2
import socket
import signal
import dotenv
import enum
import sys
import os
import re

dotenv.load_dotenv()

SERVER_BACKLOG_MAX_CONNECTIONS = 5
SERVER_RECV_BUFFER_SIZE = 4096

active_threads = []
shutdown_event = threading.Event()

class Templates(enum.Enum):
    ADD = "INSERT INTO computers (email, domain, ip) VALUES (%s, %s, %s);"
    REMOVE = "DELETE FROM computers WHERE domain = %s;"
    GET_ALL = "SELECT * FROM computers;"


def get_connection():
    return psycopg2.connect(**{
        "dbname" : os.getenv("db_name"),
        "user" : os.getenv("db_user"),
        "password" : os.getenv("db_password"),
        "host" : os.getenv("db_host"),
        "port" : os.getenv("db_port")
    })


def validate_computer_details(email, domain, ip):
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise ValueError("Invalid email format")

    if not re.match(r"^[a-z]+$", domain):
        raise ValueError("Domain must contain only lowercase letters")

    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4}$", ip):
        raise ValueError("IP must be in the format x.x.x.x:xxxx")


def add_computer(email, domain, ip):
    validate_computer_details(email, domain, ip)
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(Templates.ADD.value, (email, domain, ip))
            conn.commit()
    except Exception as e:
            print(f"Error occurred during add_computer(): {e}")
            conn.rollback()
    finally:
        conn.close()


def remove_computer(domain):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(Templates.REMOVE.value, (domain,))
            conn.commit()
    except Exception as e:
        print(f"Error occurred during remove_computer(): {e}")
        conn.rollback()
    finally:
        conn.close()


def get_all_computers():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(Templates.GET_ALL.value)
            computers = cur.fetchall()
            return computers
    except Exception as e:
        print(f"Error occurred during get_all_computers(): {e}")
        return []
    finally:
        conn.close()


def handle_packet(packet):
    print(packet)
    return b"Dummy response"


def receive_response(client_socket):
    response = b""

    while True:
        part = client_socket.recv(SERVER_RECV_BUFFER_SIZE)
        response += part

        # there is no more data OR all data has been recieved already
        if len(part) < SERVER_RECV_BUFFER_SIZE:
            break

    return response


def handle_connection(client_socket):
    try:
        while not shutdown_event.is_set():
            request = receive_response(client_socket)

            # nothing has been received
            if not request:
                break

            response = handle_packet(request)
            client_socket.send(response)
    finally:
        client_socket.close()


def handle_signal(sig, frame):
    print("\nShutting down server gracefully...")

    # signal all threads to close and wait for all threads to finish
    shutdown_event.set()
    for thread in active_threads:
        thread.join()

    sys.exit(0)


def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, int(port)))
    server.listen(SERVER_BACKLOG_MAX_CONNECTIONS)

    print(f"BreadNet Domain Name Server is listening on -- {host}:{port}")

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    try:
        while not shutdown_event.is_set():
            try:
                client_sock, addr = server.accept()

            # socket was closed by the signal handler
            except OSError:
                break

            print(f"Accepted connection from -- {addr}")

            client_thread = threading.Thread(
                target=handle_connection,
                args=(client_sock,)
            )
            client_thread.start()
            active_threads.append(client_thread)
    finally:
        server.close()

        for thread in active_threads:
            thread.join()

        print("Server closed.")


if __name__ == "__main__":
    start_server(
        os.getenv("dns_host"),
        os.getenv("dns_port")
    )
