from astera.services.database.db_utils import connect_to_db


def create_user(username: str):

    try:
        connect = connect_to_db()
        if connect is None:
            return None
        with connect.cursor() as cur:
            cur.execute("INSERT INTO users(user_name) VALUES(%s)", (username,))
            connect.commit()
    except Exception as e:
        if connect:
            print(f"Error to insert username to DB {e}")
            connect.rollback()
    finally:
        if connect:
            connect.close()


if __name__ == "__main__":

    create_user("Jhon")
    create_user("Adam")
    create_user("Jhon")
