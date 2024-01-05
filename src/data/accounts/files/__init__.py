import os, json

from ...database import path_accounts
from ....utils.dollar import get_value_dollar, ExchangeMonitor

path_text = f"{path_accounts}/files/text"

def create_file_text_in_database(user_id: int, monitors: list):
    user_file_path = os.path.join(path_text, f"u{user_id}.json")
    data = []

    os.makedirs(os.path.dirname(user_file_path), exist_ok=True)

    with open(user_file_path, "w") as f:
        for monitor in monitors:
            data.append(monitor)
        
        f.seek(0)
        f.write(json.dumps(data, indent=4))
        f.truncate()
        f.close()

def add_path_file_in_database(path: str, user_id: int):
    user_file_path = os.path.join(path_accounts, f"u{user_id}.json")
    with open(user_file_path, "r+") as f:
        data = json.load(f)
        data['user']['premium']['configuration']['path'] = path

        f.seek(0)
        f.write(json.dumps(data, indent=4))
        f.truncate()
        f.close()

def set_status_message(user_id: int, position: int, message: bool):
    user_file_path = os.path.join(path_accounts, f"u{user_id}.json")
    with open(user_file_path, "r+") as f:
        data = json.load(f)
        data['user']['premium']['configuration']['updated_hours'][position]['message'] = message

        f.seek(0)
        f.write(json.dumps(data, indent=4))
        f.truncate()
        f.close()