"""generate random bot name"""

from re import sub
from secrets import randbelow, choice

from faker import Faker

if __name__ == "__main__":
    botname = Faker().name()
    print(botname)
    print(f"{sub('[ .]', '', botname)}{randbelow(100)}{choice(('_bot', 'Bot'))}")
