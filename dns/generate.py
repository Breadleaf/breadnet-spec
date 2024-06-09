import os

def main():
    if os.path.exists("./.env"):
        print("./.env exists already")
        return

    keys = [
        ["Configure database information:"],
        "db_name",
        "db_user",
        "db_password",
        "db_host",
        "db_port",
        None,
        ["Configure domain name server information:"],
        "dns_host",
        "dns_port",
    ]

    with open("./.env", "w") as env:
        for key in keys:
            if key is None:
                env.write("\n")
                continue

            if isinstance(key, list):
                env.write(f"# {key[0]}\n")
                continue

            env.write(f"{key}=\n")

    print("./.env file has been created with empty fields")


if __name__ == "__main__":
    main()
