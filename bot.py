import telebot
from telebot import types
from flask import Flask
from threading import Thread

# --- 1. СЕРВЕР ---
app = Flask('')
@app.route('/')
def home(): return "Бот Donat Almaz работает!"
def run_web(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run_web).start()

# --- 2. НАСТРОЙКИ ---
TOKEN = '8547909884:AAEf2zP72A_TSP2zYlW0bAH6fkAah0wRY0g'
# Список ID админов
ADMINS = [1657728225, 7955178618] 
LOG_CHANNEL = -1003638749260 
FEEDBACK_CHANNEL = -1002237937446 

CARD_NUMBER = "+992558888065" 
CARD_NAME = "Душанбе Сити"

bot = telebot.TeleBot(TOKEN)
user_data = {} 

# Тексты
texts = {
    'tj': {
        'welcome': "👋 **Ассалому алейкум!**\nБа боти расмии **Donat Almaz** хуш омадед.",
        'main_menu': "⬇️ Лутфан яке аз бахшҳоро интихоб кунед:",
        'products': "🛒 Маҳсулотҳо",
        'support': "🆘 Дастгирӣ",
        'lang_btn': "🌐 Ивази забон",
        'choose_item': "📦 **Рӯйхати маҳсулотҳо:**",
        'get_id': "🆔 **ID-и бозии худро нависед:**",
        'pay_text': "✅ **ID қабул шуд:** `{0}`\n\n💳 **МАБЛАҒРО ГУЗАРОНЕД:**\n🏦 **{1}**\n🔢 `{2}`\n\n📷 **СКРИНШОТИ ЧЕКРО ФИРИСТЕД!**",
        'wait_adm': "⏳ **Чеки шумо ба админҳо фиристода шуд!**",
        'wait_5min': "⏳ **Лутфан 5 дақиқа мунтазир шавед.**\nФармоиши шумо дар ҳоли иҷрост!",
        'done': "✅ **Табрик! Фармоиши шумо иҷро шуд.**\n\nАлмосҳо гузаронида шуданд. Лутфан отзыви худро нависед: https://t.me/otziv_am1r",
        'thanks_msg': "🙏 **Ташаккур, ки моро интихоб кардед!**\nХурсандем, ки ба мо муроҷиат кардед.",
        'rejected': "❌ **Бубахшед, фармоиши шумо рад карда шуд.**",
        'support_text': "🆘 Агар саволе дошта бошед, ба админҳо муроҷиат кунед:"
    },
    'ru': {
        'welcome': "👋 **Здравствуйте!**\nДобро пожаловать в бот **Donat Almaz**.",
        'main_menu': "⬇️ Пожалуйста, выберите раздел:",
        'products': "🛒 Товары",
        'support': "🆘 Поддержка",
        'lang_btn': "🌐 Смена языка",
        'choose_item': "📦 **Список товаров:**",
        'get_id': "🆔 **Напишите ваш игровой ID:**",
        'pay_text': "✅ **ID принят:** `{0}`\n\n💳 **ОПЛАТИТЕ НА КАРТУ:**\n🏦 **{1}**\n🔢 `{2}`\n\n📷 **ОТПРАВЬТЕ СКРИНШОТ ЧЕКА!**",
        'wait_adm': "⏳ **Ваш чек отправлен администраторам!**",
        'wait_5min': "⏳ **Пожалуйста, подождите 5 минут.**\nВаш заказ выполняется!",
        'done': "✅ **Поздравляем! Ваш заказ выполнен.**\n\nАлмазы зачислены. Пожалуйста, напишите ваш отзыв здесь: https://t.me/otziv_am1r",
        'thanks_msg': "🙏 **Спасибо, что выбрали нас!**\nМы рады, что вы к нам обратились.",
        'rejected': "❌ **Извините, ваш заказ отклонен.**",
        'support_text': "🆘 Если у вас есть вопросы, напишите администраторам:"
    }
}

item_names = {
    "tj": {
        "100": "💎 100+5 | 9.0 c.", "310": "💎 310+16 | 24.0 c.", "520": "💎 520+26 | 46.0 c.", 
        "1060": "💎 1060+53 | 90.0 c.", "2180": "💎 2180+109 | 180.0 c.",
        "week": "🎟 Ваучер ҳафта | 15.0 c.", "month": "🎟 Ваучер моҳ | 90.0 c.",
        "evo3": "🎁 Ево 3 рӯз | 9.0 c.", "evo7": "🎁 Ево 7 рӯз | 12.0 c.", "evo30": "🎁 Ево 30 рӯз | 32.0 c."
    },
    "ru": {
        "100": "💎 100+5 | 9.0 c.", "310": "💎 310+16 | 24.0 c.", "520": "💎 520+26 | 46.0 c.", 
        "1060": "💎 1060+53 | 90.0 c.", "2180": "💎 2180+109 | 180.0 c.",
        "week": "🎟 Ваучер неделя | 15.0 c.", "month": "🎟 Ваучер месяц | 90.0 c.",
        "evo3": "🎁 Ево 3 дня | 9.0 c.", "evo7": "🎁 Ево 7 дней | 12.0 c.", "evo30": "🎁 Ево 30 дней | 32.0 c."
    }
}

def get_lang(uid): return user_data.get(uid, {}).get('lang', 'tj')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🇹🇯 Тоҷикӣ", callback_data="setlang_tj"),
               types.InlineKeyboardButton("🇷🇺 Русский", callback_data="setlang_ru"))
    bot.send_message(message.chat.id, "Забонро интихоб кунед / Выберите язык:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("setlang_"))
def set_lang(call):
    lang = call.data.split("_")[1]
    user_data[call.from_user.id] = {'lang': lang}
    bot.delete_message(call.message.chat.id, call.message.message_id)
    main_menu(call.message.chat.id)

def main_menu(chat_id):
    lang = get_lang(chat_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(texts[lang]['products'], texts[lang]['support'])
    markup.add(texts[lang]['lang_btn'])
    bot.send_message(chat_id, texts[lang]['main_menu'], reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text in ["🛒 Маҳсулотҳо", "🛒 Товары"])
def show_p(message):
    lang = get_lang(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for k, v in item_names[lang].items():
        markup.add(types.InlineKeyboardButton(text=v, callback_data=f"buy_{k}"))
    bot.send_message(message.chat.id, texts[lang]['choose_item'], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def item_sel(call):
    uid = call.from_user.id
    lang = get_lang(uid)
    item_key = call.data.replace("buy_", "")
    user_data[uid] = {'lang': lang, 'item': item_key}
    msg = bot.send_message(call.message.chat.id, texts[lang]['get_id'])
    bot.register_next_step_handler(msg, save_id)

def save_id(message):
    uid = message.from_user.id
    lang = get_lang(uid)
    user_data[uid]['game_id'] = message.text
    bot.send_message(uid, texts[lang]['pay_text'].format(message.text, CARD_NAME, CARD_NUMBER), parse_mode="Markdown")

@bot.message_handler(content_types=['photo', 'text'])
def handle_all(message):
    uid = message.from_user.id
    lang = get_lang(uid)

    if uid in ADMINS and message.content_type == 'photo':
        msg = bot.reply_to(message, "Введите ID пользователя для отправки этого фото:")
        bot.register_next_step_handler(msg, send_photo_to_user, message.photo[-1].file_id)
        return

    if user_data.get(uid, {}).get('waiting_feedback'):
        user_info = f"👤 Отзыв: @{message.from_user.username or 'User'} (ID: {uid})"
        if message.content_type == 'photo':
            bot.send_photo(FEEDBACK_CHANNEL, message.photo[-1].file_id, caption=f"{user_info}\n💬 {message.caption or ''}")
        else:
            bot.send_message(FEEDBACK_CHANNEL, f"{user_info}\n💬 {message.text}")
        bot.send_message(uid, texts[lang]['thanks_msg'])
        user_data[uid]['waiting_feedback'] = False
        return

    if message.content_type == 'photo' and 'item' in user_data.get(uid, {}):
        item_code = user_data[uid]['item']
        info = f"🔔 **ЧЕК!**\nЮзер: @{message.from_user.username}\nID: `{uid}`\nID FF: `{user_data[uid]['game_id']}`\nПакет: {item_names['tj'][item_code]}"
        bot.send_message(uid, texts[lang]['wait_adm'])
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Тасдиқ", callback_data=f"adm_ok_{uid}"),
                   types.InlineKeyboardButton("❌ Рад", callback_data=f"adm_no_{uid}"))
        bot.send_photo(LOG_CHANNEL, message.photo[-1].file_id, caption=info)
        for adm in ADMINS:
            try: bot.send_photo(adm, message.photo[-1].file_id, caption=info, reply_markup=markup)
            except: pass
        user_data[uid].pop('item', None)

def send_photo_to_user(message, photo_id):
    try:
        target_uid = int(message.text)
        lang = get_lang(target_uid)
        bot.send_photo(target_uid, photo_id, caption=texts[lang]['thanks_msg'])
        bot.send_message(message.chat.id, "✅ Отправлено!")
    except: bot.send_message(message.chat.id, "❌ Ошибка ID.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('adm_'))
def admin_buttons(call):
    act, _, uid = call.data.split('_')
    uid = int(uid)
    lang = get_lang(uid)
    if act == 'ok':
        bot.send_message(uid, texts[lang]['wait_5min'])
        if uid not in user_data: user_data[uid] = {'lang': lang}
        user_data[uid]['waiting_feedback'] = True 
        bot.send_message(uid, texts[lang]['done'])
    else: bot.send_message(uid, texts[lang]['rejected'])
    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                             caption=call.message.caption + f"\n\n🏁 Статус: {act}")

@bot.message_handler(func=lambda m: m.text in ["🌐 Ивази забон", "🌐 Смена языка"])
def lang_change(message): start(message)

@bot.message_handler(func=lambda m: m.text in ["🆘 Дастгирӣ", "🆘 Поддержка"])
def support(message):
    lang = get_lang(message.chat.id)
    markup = types.InlineKeyboardMarkup()
    # Кнопки двух админов
    markup.add(types.InlineKeyboardButton("👨‍💻 Admin 1", url="https://t.me/amirjanffx"),
               types.InlineKeyboardButton("👨‍💻 Admin 2", url="https://t.me/aminjanffx"))
    bot.send_message(message.chat.id, texts[lang]['support_text'], reply_markup=markup)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
