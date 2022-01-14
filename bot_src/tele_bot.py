import logging
from textwrap import dedent
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update


from edge import get_edge


def start_command(update: Update, context: CallbackContext):
    """
    Sends a welcome message to the user
    """

    welcome = dedent("""
    Hi, 
    
    I'm the xaspy bot (https://github.com/gnzng/xaspy). I use the XrayDB https://github.com/xraypy/XrayDB 
    
    Commands are (so far):
    /edge element edge -  uses xray_edges to return energies,fyield and jump ratio, takes element, specific lines and group of lines 

    
    """)

    update.message.reply_text(text=welcome, parse_mode='HTML', disable_web_page_preview=True)


def get_edge_command(update: Update, context: CallbackContext):
    """
    get edge(s) of element
    """
    get_edge(update, context)

def run(bot_token: str):
    """
    Starts the bot
    """

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start_command, run_async=True)

    get_edge_handler = CommandHandler('edge', get_edge_command, run_async=True)
    

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(get_edge_handler)

    job_queue = dispatcher.job_queue


    updater.start_polling()