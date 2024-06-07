import psycopg2
import socket
import dotenv
import enum
import os
import re

class Templates(enum.Enum):
    ADD = "INSERT INTO computers (email, domain, ip) VALUES (%s, %s, %s);"
    REMOVE = "DELETE FROM computers WHERE domain = %s;"
    GET_ALL = "SELECT * FROM computers;"


def get_connection():
    dotenv.load_dotenv()
    return psycopg2.connect(**{
        "dbname" : os.getenv("dbname"),
        "user" : os.getenv("user"),
        "password" : os.getenv("password"),
        "host" : os.getenv("host"),
        "port" : os.getenv("port")
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
    with conn.cursor() as cur:
        cur.execute(Templates.ADD.value, (email, domain, ip))
        conn.commit()
    conn.close()


def remove_computer(domain):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(Templates.REMOVE.value, (domain,))
        conn.commit()
    conn.close()


def get_all_computers():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(Templates.GET_ALL.value)
        computers = cur.fetchall()
    conn.close()
    return computers


def main():
    pass


if __name__ == "__main__":
    main()
