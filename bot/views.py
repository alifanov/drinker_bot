from telebot import TeleBot, types
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.utils.timezone import now, timedelta
from .models import BotUser, Match, Log

bot = TeleBot(settings.TOKEN)


class UpdateBotView(APIView):
    def post(self, request, token):
        update = types.Update.de_json(request.data)
        Log.objects.create(data=request.data)
        bot.process_new_updates([update])
        return Response({'code': 200})


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: types.CallbackQuery):
    user, _ = BotUser.objects.get_or_create(tg_id=call.from_user.id)
    bot.answer_callback_query(call.id)
    if call.data == 'drinking_now':
        user.open_for_requests_until = now() + timedelta(hours=2)
        user.save()
        bot.send_message(call.from_user.id, text='Оке, буду присылать запросы на выпить в ближайшие пару часов :)', parse_mode='HTML')

    if call.data == 'go_home':
        user.open_for_requests_until = None
        user.save()
        bot.send_message(call.from_user.id, text='Оке, больше не буду присылать запросы на выпить :)',
                         parse_mode='HTML')

    if call.data == 'want_to_drink':
        user.open_for_requests_until = None
        user.save()

        open_users = BotUser.objects.filter(open_for_requests_until__gte=now())
        if open_users.count() == 0:
            bot.send_message(user.tg_id, text='Пока никто не бухает :( Можешь стать первым хостом %)')
        else:
            bot.send_message(user.tg_id, text=f'Ща спрошу у {open_users.count()} людей')

        for u in open_users:
            keyboard = types.InlineKeyboardMarkup()
            key_ok = types.InlineKeyboardButton(text='Давай', callback_data=f'{user.tg_id}_ok')
            keyboard.add(key_ok)

            bot.send_message(u.tg_id, text=f'@{user.get_username()} ищет, с кем бы бухнуть', reply_markup=keyboard)

    if call.data.endswith('_ok'):
        requester = BotUser.objects.get(tg_id=call.data.replace('_ok', ''))
        bot.send_message(requester.tg_id, text=f'@{user.get_username()} откликается на твой зов')

        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        key_send_geo = types.KeyboardButton(text='Отправить местоположение', request_location=True)
        keyboard.add(key_send_geo)

        bot.send_message(user.tg_id, text=f'Отправь @{requester.get_username()}, где ты сейчас', reply_markup=keyboard)
        Match.objects.create(
            requester_tg_id=requester.tg_id,
            responder_tg_id=user.tg_id
        )


@bot.message_handler(content_types=['location'])
def send_location_handler(message):
    match = Match.objects.filter(responder_tg_id=message.from_user.id).last()
    bot.send_location(match.requester_tg_id, message.location.latitude, message.location.longitude)


@bot.message_handler(commands=['start'])
def start_handler(message):
    text = 'Найди собутыльника :)'

    user, _ = BotUser.objects.get_or_create(tg_id=message.from_user.id, defaults={
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
