import os

def main():
    if os.path.exists("./.env"):
        print("./.env exists already")
        return

    keys = [
        "host",
        "user",
        "password",
        "dbname",
        "port"
    ]

    with open("./.env", "w") as env:
        for key in keys:
            env.write(f"{key}=\n")

    print("./.env file has been created with empty fields")


if __name__ == "__main__":
    main()
