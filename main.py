import logging
import json
from tinydb import TinyDB, Query
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
import amazon
import classes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    keyboard = [[InlineKeyboardButton("Add product 🎁", callback_data='1'),
                 InlineKeyboardButton("More info 📚", callback_data='2')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        'Welcome to Amazon Price Checker. Start adding your first product and we will notify you once it drops to your desired price.', reply_markup=reply_markup)

    return 0


def button(bot, update):
    query = update.callback_query
    logger.info('Query data: %s', query.data)
    if query.data == '1':
        bot.send_message(chat_id=query.message.chat_id,
                         text="Nice! Send us the link of an Amazon product you want to track. 📉")
    else:
        return help(bot, update)

    return


def add(bot, update, args):
    query = update.callback_query
    logger.info('Query data: %s', args[0])
    if "https://www.amazon.es/" in args[0]:
        chat_id = update.message.chat_id
        newItem = classes.item(chat_id, args[0])
        addToDB(newItem)
        bot.send_message(chat_id, text="Product '{}' added! Actual price is {}€".format(
            amazon.getName(args[0]).strip(), amazon.checkPrice(args[0])))
    else:
        logger.info('Nope')

    return


def setPrice(bot, update, args):
    query = update.callback_query
    logger.info('setPrice query data: %s', args[0])

    return


def addToDB(item):
    db = TinyDB('db.json')
    table = db.table('items')
    table.insert({'item': item.getURL(), 'user': item.getUser(),
                  'price': item.getPrice()})
    logger.info('DB: %s', table.all())


def help(bot, update):
    query = update.callback_query
    bot.send_message(chat_id=query.message.chat_id,
                     text="Use /start to test this bot.")


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater("KEY")

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            0: [CallbackQueryHandler(button)],
        },
        fallbacks=[CommandHandler('start', start)]
    )

    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('add', add, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler(
        'setPrice', setPrice, pass_args=True))
    updater.dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__


if __name__ == '__main__':
    main()
