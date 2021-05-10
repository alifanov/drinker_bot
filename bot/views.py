from telebot import TeleBot, types
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from .models import BotUser

bot = TeleBot(settings.TOKEN)


class UpdateBotView(APIView):
    def post(self, request, token):
        update = types.Update.de_json(request.data)
        bot.process_new_updates([update])
        return Response({'code': 200})


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user, _ = BotUser.objects.get_or_create(tg_id=call.from_user.id)
    if call.data == 'drinking_now':
        user.is_open_for_requests = True
        user.save()
        bot.send_message(call.message.chat.id, text='Оке, буду присылать запросы на выпить :)', parse_mode='HTML')

    if call.data == 'go_home':
        user.is_open_for_requests = False
        user.save()
        bot.send_message(call.message.chat.id, text='Оке, больше не буду присылать запросы на выпить :)', parse_mode='HTML')

    if call.data == 'want_to_drink':
        open_users = BotUser.objects.filter(is_open_for_requests=True)
        for u in open_users:
            keyboard = types.InlineKeyboardMarkup()
            key_ok = types.InlineKeyboardButton(text='Давай', callback_data=f'{u.tg_id}_ok')
            keyboard.add(key_ok)

            bot.send_message(u.tg_id, text=f'@{u.username} ищет с кем бы бухнуть', reply_markup=keyboard)

    if call.data.endswith('_ok'):
        requestor = BotUser.objects.get(tg_id=call.data.replace('_ok', ''))
        bot.send_message(requestor.tg_id, text=f'@{user.username} откликнулся на твой зов')


@bot.message_handler(commands=['start'])
def start_handler(message):
    text = 'Найди собутыльника :)'

    BotUser.objects.get_or_create(tg_id=message.from_user.id, defaults={
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'username': message.from_user.username
    })

    keyboard = types.InlineKeyboardMarkup()
    key_want_to_drink = types.InlineKeyboardButton(text='Хочу бухать', callback_data='want_to_drink')
    key_drinking_now = types.InlineKeyboardButton(text='Уже бухаю', callback_data='drinking_now')
    key_go_home = types.InlineKeyboardButton(text='Иду домой', callback_data='go_home')

    keyboard.add(key_want_to_drink)
    keyboard.add(key_drinking_now)
    keyboard.add(key_go_home)

    bot.send_message(message.chat.id, text=text, reply_markup=keyboard, parse_mode='HTML')


def set_webhook(url):
    bot.set_webhook(url=url + settings.TOKEN)
