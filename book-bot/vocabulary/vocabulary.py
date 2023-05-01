"""This module contains vocabularies with answers and commands"""

VOCABULARY_RU: dict[str, str] = {
    "description": "Pet-проект, созданный с использованием aiogram3.x.\n"
                         "Исходный код: https://github.com/luculliano/botapidev",

    "/start": "<b>{greet}, {name}!</b>\nЭто бот, в котором Вы можете "
               "прочитать автобиографический роман Чарльза Буковски "
               "\"Xлеб с ветчиной.\"\n\nИспользуйте /help, чтобы открыть "
               "справочную информацию.",

    "/help": "<b>Справочная информация</b> 📕\n\nСписок доступных команд находится "
             "в <i>Menu</i> слева.\nЧтобы сохранить закладку - нажите на кнопку "
             "с номером страницы.\n\n<b>Приятного чтения!</b>",

    "/bookmarks": "Это список Ваших закладок",
    "edit_bookmark": "Страница добавлена в закладки!",
    "backward": "<<",
    "forward": ">>"
}

VOCABULARY_COMMANDS_RU = {
    "/start": "Запустить программу и вывести приветственное сообщение",
    "/help": "Открыть справочную информацию",
    "/continue": "Продолжить чтение",
    "/beginning": "Перейти в начало книги",
    "/bookmarks": "Открыть список закладок",
}