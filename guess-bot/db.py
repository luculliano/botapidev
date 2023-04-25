import pickle
from pathlib import Path

path = Path(__file__).parent.joinpath("users_db.pql")

UserProgress = dict[str, int | None]


def save_user_progress(uid: int, progress: UserProgress) -> None:
    with open(path, "rb+") as file:
        users_db = pickle.load(file)
        users_db.update({uid: progress})
        file.seek(0)
        pickle.dump(users_db, file)


def init_db() -> dict:
    if path.exists():
        with open(path, "rb") as file:
            users_db = pickle.load(file)
            return users_db
    with open(path, "wb") as file:
        pickle.dump({}, file)
    return {}
