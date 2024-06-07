import psycopg2
import socket
import dotenv
import os

def get_connection() -> map:
    dotenv.load_dotenv()

    return psycopg2.connect(**{
        "dbname" : os.getenv("dbname"),
        "user" : os.getenv("user"),
        "password" : os.getenv("password"),
        "host" : os.getenv("host"),
        "port" : os.getenv("port")
    })


def main():
    conn = get_connection()
    cur = conn.cursor()


if __name__ == "__main__":
    main()
