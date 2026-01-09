import telebot
from telebot import types
from flask import Flask
from threading import Thread
import time

# --- 1. СЕРВЕР ---
app = Flask('')
@app.route('/')
def home(): return "Бот Donat Almaz активен!"
def run_web(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run_web).start()

# --- 2. НАСТРОЙКИ ---
# ВСТАВЬ СЮДА НОВЫЙ ТОКЕН ИЗ BOTFATHER
TOKEN = '8547909884:AAHpxaFXE29_bmSRfAcwz0OGz1yfjCnfxp8'
ADMINS = [1657728225, 7955178618] 
LOG_CHANNEL = -1003638749260 
FEEDBACK_CHANNEL = -1002237937446 
WELCOME_PHOTO = "https://i.postimg.cc/mD3m8S0x/welcome.jpg"
CARD_NUMBER = "+992558888065" 
CARD_NAME = "Душанбе Сити"

bot = telebot.TeleBot(TOKEN)
user_data = {} 

texts = {
    'tj': {
        'welcome': "👋 **Ассалому алейкум!**\n\nБа боти **Donat Almaz** хуш омадед.",
        'main_menu': "⬇️ Яке аз бахшҳоро интихоб кунед:",
        'products': "🛒 Маҳсулотҳо",
        'support': "🆘 Дастгирӣ",
        'lang_btn': "🌐 Ивази забон",
        'choose_item': "📦 **Маҳсулотро интихоб кунед:**",
        'get_id': "🆔 **ID-и бозии худро нависед:**",
        'pay_text': "✅ **ID:** `{0}`\n\n💳 **МАБЛАҒРО ГУЗАРОНЕД:**\n🏦 **{1}**\n🔢 `{2}`\n\n📷 **ЧЕКРО ФИРИСТЕД!**",
        'wait_adm': "⏳ **Чеки шумо қабул шуд!**",
        'wait_5min': "⏳ **Лутфан 5 дақиқа мунтазир шавед.**\nФармоиши шумо дар ҳоли иҷрост!",
        'done': "✅ **Фармоиш иҷро шуд!**\nОтзыв нависед: https://t.me/otziv_am1r",
        'thanks_msg': "🙏 **Ташаккур барои интихоб!**",
        'rejected': "❌ **Фармоиш рад шуд.**",
        'support_text': "🆘 **Админҳо:**"
    },
    'ru': {
        'welcome': "👋 **Здравствуйте!**\n\nДобро пожаловать в **Donat Almaz**.",
        'main_menu': "⬇️ Выберите раздел:",
        'products': "🛒 Товары",
        'support': "🆘 Поддержка",
        'lang_btn': "🌐 Смена языка",
        'choose_item': "📦 **Выберите товар:**",
        'get_id': "🆔 **Напишите ваш игровой ID:**",
        'pay_text': "✅ **ID принят:** `{0}`\n\n💳 **ОПЛАТИТЕ НА КАРТУ:**\n🏦 **{1}**\n🔢 `{2}`\n\n📷 **ОТПРАВЬТЕ ЧЕК!**",
        'wait_adm': "⏳ **Ваш чек отправлен!**",
        'wait_5min': "⏳ **Пожалуйста, подождите 5 минут.**\nЗаказ выполняется!",
        'done': "✅ **Заказ выполнен!**\nНапишите отзыв: https://t.me/otziv_am1r",
        'thanks_msg': "🙏 **Спасибо, что выбрали нас!**",
        'rejected': "❌ **Заказ отклонен.**",
        'support_text': "🆘 **Наши администраторы:**"
    }
}

item_names = {
    "100": "💎 100+5 | 9.0 c.", "310": "💎 310+16 | 24.0 c.", "520": "💎 520+26 | 46.0 c.", 
    "1060": "💎 1060+53 | 90.0 c.", "2180": "💎 2180+109 | 180.0 c.",
    "week": "🎟 Ваучер неделя | 15.0 c.", "month": "🎟 Ваучер месяц | 90.0 c.",
    "evo3": "🎁 Ево 3 дня | 9.0 c.", "evo7": "🎁 Ево 7 дней | 12.0 c.", "evo30": "🎁 Ево 30 дней | 32.0 c."
}

def get_lang(uid): return user_data.get(uid, {}).get('lang', 'tj')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🇹🇯 Тоҷикӣ", callback_data="setlang_tj"),
               types.InlineKeyboardButton("🇷🇺 Русский", callback_data="setlang_ru"))
    bot.send_photo(message.chat.id, WELCOME_PHOTO, caption="Интихоби забон / Выбор языка:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("setlang_"))
def set_lang(call):
    lang = call.data.split("_")[1]
    user_data[call.from_user.id] = {'lang': lang}
    bot.delete_message(call.message.chat.id, call.message.message_id)
    main_menu(call.message.chat.id, texts[lang]['welcome'])

def main_menu(chat_id, text=None):
    lang = get_lang(chat_id)
    if not text: text = texts[lang]['main_menu']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(texts[lang]['products'], texts[lang]['support'])
    markup.add(texts[lang]['lang_btn'])
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text in ["🛒 Маҳсулотҳо", "🛒 Товары"])
def products(message):
    lang = get_lang(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for k, v in item_names.items():
        markup.add(types.InlineKeyboardButton(text=v, callback_data=f"buy_{k}"))
    bot.send_message(message.chat.id, texts[lang]['choose_item'], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def handle_buy(call):
    uid = call.from_user.id
    lang = get_lang(uid)
    item_key = call.data.replace("buy_", "")
    user_data[uid] = {'lang': lang, 'item': item_key}
    msg = bot.send_message(call.message.chat.id, texts[lang]['get_id'])
    bot.register_next_step_handler(msg, save_id)

def save_id(message):
    uid = message.from_user.id
    lang = get_lang(uid)
    if 'item' not in user_data[uid]: return
    user_data[uid]['game_id'] = message.text
    bot.send_message(uid, texts[lang]['pay_text'].format(message.text, CARD_NAME, CARD_NUMBER), parse_mode="Markdown")

@bot.message_handler(content_types=['photo', 'text'])
def handle_photo_and_text(message):
    uid = message.from_user.id
    lang = get_lang(uid)

    # Админ пересылает фото юзеру
    if uid in ADMINS and message.content_type == 'photo':
        msg = bot.reply_to(message, "Введите ID пользователя:")
        bot.register_next_step_handler(msg, send_photo_admin, message.photo[-1].file_id)
        return

    # Если юзер пишет отзыв
    if user_data.get(uid, {}).get('waiting_feedback'):
        user_info = f"👤 Отзыв от: @{message.from_user.username or 'User'} (ID: {uid})"
        if message.content_type == 'photo':
            bot.send_photo(FEEDBACK_CHANNEL, message.photo[-1].file_id, caption=f"{user_info}\n💬 {message.caption or ''}")
        else:
            bot.send_message(FEEDBACK_CHANNEL, f"{user_info}\n💬 {message.text}")
        bot.send_message(uid, texts[lang]['thanks_msg'])
        user_data[uid]['waiting_feedback'] = False
        return

    # Юзер прислал чек
    if message.content_type == 'photo' and 'item' in user_data.get(uid, {}):
        item_code = user_data[uid]['item']
        info = f"🔔 **НОВЫЙ ЧЕК!**\nID: `{uid}`\nID FF: `{user_data[uid]['game_id']}`\nПакет: {item_names[item_code]}"
        bot.send_message(uid, texts[lang]['wait_adm'])
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Тасдиқ", callback_data=f"adm_ok_{uid}"),
                   types.InlineKeyboardButton("❌ Рад", callback_data=f"adm_no_{uid}"))
        
        bot.send_photo(LOG_CHANNEL, message.photo[-1].file_id, caption=info)
        for adm in ADMINS:
            try: bot.send_photo(adm, message.photo[-1].file_id, caption=info, reply_markup=markup)
            except: pass
        user_data[uid].pop('item', None)

def send_photo_admin(message, photo_id):
    try:
        target_uid = int(message.text)
        lang = get_lang(target_uid)
        bot.send_photo(target_uid, photo_id, caption=texts[lang]['thanks_msg'])
        bot.send_message(message.chat.id, "✅ Фото успешно отправлено!")
    except: bot.send_message(message.chat.id, "❌ Ошибка в ID.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('adm_'))
def admin_action(call):
    act, _, uid = call.data.split('_')
    uid = int(uid)
    lang = get_lang(uid)
    if act == 'ok':
        bot.send_message(uid, texts[lang]['wait_5min'])
        if uid not in user_data: user_data[uid] = {'lang': lang}
        user_data[uid]['waiting_feedback'] = True 
        bot.send_message(uid, texts[lang]['done'])
    else:
        bot.send_message(uid, texts[lang]['rejected'])
    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                             caption=call.message.caption + f"\n\n🏁 Статус: {act.upper()}")

@bot.message_handler(func=lambda m: m.text in ["🆘 Дастгирӣ", "🆘 Поддержка"])
def support(message):
    lang = get_lang(message.chat.id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("👨‍💻 Admin 1", url="https://t.me/amirjanffx"),
               types.InlineKeyboardButton("👨‍💻 Admin 2", url="https://t.me/aminjanffx"))
    bot.send_message(message.chat.id, texts[lang]['support_text'], reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["🌐 Ивази забон", "🌐 Смена языка"])
def change_lang_btn(message): start(message)

if __name__ == "__main__":
    keep_alive()
    # Очистка очереди перед запуском
    bot.remove_webhook()
    time.sleep(1)
    bot.infinity_polling(skip_pending=True)
