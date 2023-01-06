import os
from telegram.ext import *
from telegram import *


INPUT_TEXT = 0

def tipoSuelo(update, context):
    update.message.reply_text(
        text='Selecciona el tipo de suelo:',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='arenoso', callback_data='qr')],
            [InlineKeyboardButton(text='franco', callback_data='qr')],
            [InlineKeyboardButton(text='franco arenoso', callback_data='qr')],
            [InlineKeyboardButton(text='franco arcilloso', callback_data='qr')],
            [InlineKeyboardButton(text='arcilloso arenoso', callback_data='qr')],
            [InlineKeyboardButton(text='arcilloso', callback_data='qr')],
        ])
    )

def tipoCultivo(update, context):
    update.message.reply_text(
        text='Selecciona el tipo de cultivo:',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Ajo', callback_data='qr'), InlineKeyboardButton(text='Alfalfa', callback_data='qr'), InlineKeyboardButton(text='Almendro', callback_data='qr')],
            [InlineKeyboardButton(text='Arándano 1°año', callback_data='qr'), InlineKeyboardButton(text='Arándano 2°año', callback_data='qr'), InlineKeyboardButton(text='Arándano 3°año', callback_data='qr')],
            [InlineKeyboardButton(text='Arveja, fresca', callback_data='qr'), InlineKeyboardButton(text='Cebolla seca', callback_data='qr'), InlineKeyboardButton(text='Cebolla verde', callback_data='qr')],
            [InlineKeyboardButton(text='Ciruelo', callback_data='qr'), InlineKeyboardButton(text='Coliflor', callback_data='qr'), InlineKeyboardButton(text='Duraznero', callback_data='qr')],
            [InlineKeyboardButton(text='Espárragos', callback_data='qr'), InlineKeyboardButton(text='Frambuesa', callback_data='qr'), InlineKeyboardButton(text='Kiwi', callback_data='qr')],
            [InlineKeyboardButton(text='Maíz dulce', callback_data='qr'), InlineKeyboardButton(text='Maíz grano', callback_data='qr'), InlineKeyboardButton(text='Maní', callback_data='qr')],
            [InlineKeyboardButton(text='Manzano', callback_data='qr'), InlineKeyboardButton(text='Maravilla', callback_data='qr'), InlineKeyboardButton(text='Nectarino', callback_data='qr')],
            [InlineKeyboardButton(text='Nogal', callback_data='qr'), InlineKeyboardButton(text='Olivo', callback_data='qr'), InlineKeyboardButton(text='Palto', callback_data='qr')],
            [InlineKeyboardButton(text='Papa', callback_data='qr'), InlineKeyboardButton(text='Peral', callback_data='qr'), InlineKeyboardButton(text='Pimentón', callback_data='qr')],
            [InlineKeyboardButton(text='Poroto seco', callback_data='qr'), InlineKeyboardButton(text='Poroto verde', callback_data='qr'), InlineKeyboardButton(text='Pradera', callback_data='qr')],
            [InlineKeyboardButton(text='Remolacha', callback_data='qr'), InlineKeyboardButton(text='Sandia', callback_data='qr'), InlineKeyboardButton(text='Tabaco', callback_data='qr')],
            [InlineKeyboardButton(text='Tomate', callback_data='qr'), InlineKeyboardButton(text='Tngo', callback_data='qr'), InlineKeyboardButton(text='Vid', callback_data='qr')],
        ])
    )



def start(update, context):

    update.message.reply_text(
        text='Hola, bienvenido, qué deseas hacer?\n\nUsa /qr para generar un código qr.',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Generar qr', callback_data='qr')],
            [InlineKeyboardButton(text='Sobre el autor', url='https://lugodev.com')],
        ])
    )


def qr_command_handler(update, context):

    update.message.reply_text('Envíame el texto para generarte un código QR')

    return INPUT_TEXT


def qr_callback_handler(update, context):

    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Envíame el texto para generarte un código QR'
    )

    return INPUT_TEXT


def generate_qr(text):

    filename = text + '.jpg'
    print (filename)

    return filename

def input_text(update, context):

    text = update.message.text

    filename = generate_qr(text)

    chat = update.message.chat

    print("enviar imagen")

    return ConversationHandler.END


if __name__ == '__main__':

    updater = Updater(token='1946797475:AAGSHCt5sYhJI3QmitL6lvAxXEO8nX78cEc', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('tipoSuelo', tipoSuelo))
    dp.add_handler(CommandHandler('tipoCultivo', tipoCultivo))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('qr', qr_command_handler),
            CallbackQueryHandler(pattern='qr', callback=qr_callback_handler)
        ],

        states={
            INPUT_TEXT: [MessageHandler(Filters.text, input_text)]
        },

        fallbacks=[]
    ))

    updater.start_polling()
    updater.idle()