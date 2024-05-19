"""An entry point"""
from bot import bot


if __name__ == '__main__':
    try:
        bot.infinity_polling()
    except Exception as e:
        print(e)
