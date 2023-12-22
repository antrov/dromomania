import asyncio
import re
from collections import OrderedDict
from concurrent import futures

import client_pb2
import client_pb2_grpc
import grpc
from grpc_reflection.v1alpha import reflection
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, ContextTypes, MessageHandler,
                          filters)

rating_grades = OrderedDict([
    ("ok", "👍"),
    ("wpyte", "♥️"),
    ("meh", "💩"),
])
rating_buttons = [
    InlineKeyboardButton(
        value,
        callback_data=key) for key,
    value in rating_grades.items()]


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [rating_buttons]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        'https://media-cdn.tripadvisor.com/media/photo-s/0a/3f/bc/e9/some-view-at-summit-of.jpg',
        reply_markup=reply_markup,
        caption=r'''
*[Dom wolnostojący w Dobroniu](https://www.otodom.pl/pl/oferta/dom-wolnostojacy-w-dobroniu-ID4mKkJ)*
327 m2 \- 695K \- 2125 zł/m²
`3df5gk` \#latyfundia''',
        parse_mode="MarkdownV2")


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    print(update.callback_query.message.chat_id)
    query = update.callback_query
    rating = query.data
    symbol = rating_grades[rating]
    hash = re.findall(r'\`(\w*)\`', query.message.caption_markdown_v2)
    print(hash[0])
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See
    # https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    await query.edit_message_caption(caption=f"{query.message.caption_markdown_v2} \\#{rating} {symbol}", parse_mode="MarkdownV2")


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message.text)
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

app = ApplicationBuilder().token(
    "5738852320:AAFwaT_h0XEUC0il9eX5Ln9TV8F1Lh1neGE").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT, message))


class RouteGuideServicer(client_pb2_grpc.HelloServiceServicer):
    def SayHello(self, request, context):
        keyboard = [rating_buttons]
        reply_markup = InlineKeyboardMarkup(keyboard)

        asyncio.run(
            app.bot.send_photo(
                411400390,
                'https://media-cdn.tripadvisor.com/media/photo-s/0a/3f/bc/e9/some-view-at-summit-of.jpg',
                reply_markup=reply_markup,
                caption=r'''
*[Dom wolnostojący w Dobroniu](https://www.otodom.pl/pl/oferta/dom-wolnostojacy-w-dobroniu-ID4mKkJ)*
327 m2 \- 695K \- 2125 zł/m²
`3df5gk` \#latyfundia''',
                parse_mode="MarkdownV2"))
        return client_pb2.HelloResponse(reply="No siema")


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
client_pb2_grpc.add_HelloServiceServicer_to_server(
    RouteGuideServicer(), server)
# the reflection service will be aware of "Greeter" and "ServerReflection"
# services.
SERVICE_NAMES = (
    client_pb2.DESCRIPTOR.services_by_name['HelloService'].full_name,
    reflection.SERVICE_NAME,
)
reflection.enable_server_reflection(SERVICE_NAMES, server)
server.add_insecure_port("[::]:50051")
server.start()

app.run_polling()
