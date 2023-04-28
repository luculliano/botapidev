"""This module contains vocabularies with answers and commands"""

VOCABULARY_EN = {
   "main": "{greet}, {name}!\nIt's a guess-bot powered by luculliano.\n"
            "I pick a number from 0 to 100.\n"
            "If you guess the number for 5 attempts "
            "I'll send you fun meme.\n\n"
            "Available commands:\n"
            "/game - to start game.\n"
            "/cancel - to cancel game.\n"
            "/stat - to show stat.\n"
            "/help - to show this message.\n\n",

    "game": {
        "success": "The number is picked. You have 5 attempts.",
        "error": "Command /game not available in game mode."
    },
    "cancel": {
        "success": "The game has been stopped.",
        "error": "Command /cancel is available in game mode only."
    },
    "stat": "",

    "other": "Not supported! Use /help for help.",

    "not_found": "User {cur_uid} doesn't exist. Use /start to log in.",

    "numbers": "Please, use numbers in game mode only."
}

VOCABULARY_COMMANDS_EN = {
    "/help": "to show help",
    "/game": "to start game",
    "/cancel": "to cancel game",
    "/stat": "to show stat"
}
