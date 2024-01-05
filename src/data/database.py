import os, json
from dataclasses import asdict

from ..classes import User

path_accounts = f'{os.getcwd()}/src/data/accounts/'

def check_user_existence(user_id: int) -> bool:
    user_file_path = os.path.join(path_accounts, f"u{user_id}.json")
    return os.path.exists(user_file_path)

def create_user_in_database(user: User) -> None:
    user_file_path = os.path.join(path_accounts, f"u{user.id}.json")
    with open(user_file_path, "w") as f:
        data = asdict(user)

        f.seek(0)
        f.write(json.dumps(data, indent=4))
        f.truncate()
        f.close()

def set_notification_settings(user_id: int, isnotification: bool) -> None:
    user_file_path = os.path.join(path_accounts, f"u{user_id}.json")
    with open(user_file_path, "r+") as f:
        data = json.load(f)
        data['user']['premium']['notification'] = isnotification

        f.seek(0)
        f.write(json.dumps(data, indent=4))
        f.truncate()
        f.close()

def set_dollar_settings(user_id: int,
                         show_dollar: str = None,
                         path: str = None,
                         total_monitor: int = 0,
                         monitors: list = [],
                         updated_hours: list = []) -> None:
    user_file_path = os.path.join(path_accounts, f"u{user_id}.json")
    settings = {
        "show_dollar": show_dollar,
        "path": path,
        "total_monitors": total_monitor,
        "monitors": monitors,
        "updated_hours": updated_hours
    }

    with open(user_file_path, "r+") as f:
        data = json.load(f)
        if not data['user']['premium']['configuration']['path'] and not data['user']['premium']['configuration']['updated_hours']:
            data['user']['premium']['configuration'] = settings
        else:
            data['user']['premium']['configuration']['path'] = path
            data['user']['premium']['configuration']['show_dollar'] = show_dollar
            data['user']['premium']['configuration']['total_monitors'] = total_monitor
            data['user']['premium']['configuration']['monitors'] = monitors

        f.seek(0)
        f.write(json.dumps(data, indent=4))
        f.truncate()
        f.close()

def set_hours_settings(user_id: int, hours: list) -> None:
    user_file_path = os.path.join(path_accounts, f"u{user_id}.json")
    with open(user_file_path, "r+") as f:
        data = json.load(f)
        data['user']['premium']['configuration']['updated_hours'] = hours

        f.seek(0)
        f.write(json.dumps(data, indent=4))
        f.truncate()
        f.close()

def show_user_database(user_id: int) -> dict:
    user_file_path = os.path.join(path_accounts, f"u{user_id}.json")
    with open(user_file_path, "r") as f:
        data = json.load(f)
        f.close()
    return data