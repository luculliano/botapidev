import pickle
from pathlib import Path

import aiofiles

path = Path(__file__).parent.joinpath("users_db.pkl")

UserProgress = dict[str, int | None]


async def save_user_progress(uid: int, progress: UserProgress) -> None:
    """updates dictionary in "users_db.pkl" file"""
    async with aiofiles.open(path, "rb+") as file:
        data = await file.read()
        users_db = pickle.loads(data)
        users_db.update({uid: progress})
        await file.seek(0)
        await file.write(pickle.dumps(users_db))


async def _init_db() -> dict:
    """creates "users_db.pkl" if it doesn't exist or loads existing"""
    if path.exists():
        async with aiofiles.open(path, "rb") as file:
            data = await file.read()
            users_db = pickle.loads(data)
            return users_db
    async with aiofiles.open(path, "wb") as file:
        await file.write(pickle.dumps({}))
    return {}
