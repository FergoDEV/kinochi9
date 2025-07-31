import telebot
from telebot import types

BOT_TOKEN = '7937933589:AAH5GPd6I0luGDUjLum1XYUFlZB9FDl5-KU'
ADMIN_ID = 7781534875 #gizning Telegram ID
PASSWORD = 'fergo123'  # Admin parol

bot = telebot.TeleBot(BOT_TOKEN)

kino_baza = {}  # {'code': file_id}
kanal_username = '@kinochi_uz1_n1'  # Majburiy kanal

admin_mode = {}

@bot.message_handler(commands=['start'])
def start(msg):
    user_id = msg.chat.id
    if kanal_username:
        try:
            status = bot.get_chat_member(kanal_username, user_id).status
            if status in ['left', 'kicked']:
                btn = types.InlineKeyboardMarkup()
                btn.add(types.InlineKeyboardButton("🔔 A'zo bo'lish", url=f'https://t.me/{kanal_username[1:]}'))
                bot.send_message(user_id, "Botdan foydalanish uchun kanalga a'zo bo'ling!", reply_markup=btn)
                return
        except:
            pass
    bot.send_message(user_id, "🎬 Kino kodini kiriting:")

@bot.message_handler(commands=['fergo'])
def admin_login(msg):
    if msg.chat.id == ADMIN_ID:
        bot.send_message(msg.chat.id, "🔐 Parolni kiriting:")
        admin_mode[msg.chat.id] = 'awaiting_password'

@bot.message_handler(func=lambda m: admin_mode.get(m.chat.id) == 'awaiting_password')
def check_pass(msg):
    if msg.text == PASSWORD:
        admin_mode[msg.chat.id] = 'admin_panel'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('🎞 Kino qo‘shish', '📢 Post yuborish', '📊 Statistika')
        bot.send_message(msg.chat.id, "Admin paneliga xush kelibsiz!", reply_markup=keyboard)
    else:
        bot.send_message(msg.chat.id, "❌ Noto‘g‘ri parol!")

@bot.message_handler(func=lambda m: admin_mode.get(m.chat.id) == 'admin_panel')
def admin_panel(msg):
    if msg.text == '🎞 Kino qo‘shish':
        bot.send_message(msg.chat.id, "➕ Kino kodini yozing:")
        admin_mode[msg.chat.id] = 'add_code'
    elif msg.text == '📢 Post yuborish':
        bot.send_message(msg.chat.id, "📝 Post matnini yuboring:")
        admin_mode[msg.chat.id] = 'new_post'
    elif msg.text == '📊 Statistika':
        bot.send_message(msg.chat.id, f"👤 Kino soni: {len(kino_baza)} ta")

@bot.message_handler(func=lambda m: admin_mode.get(m.chat.id) == 'add_code')
def get_code(msg):
    admin_mode[msg.chat.id] = {'step': 'awaiting_video', 'code': msg.text}
    bot.send_message(msg.chat.id, "🎥 Endi kinoni video/media sifatida yuboring:")

@bot.message_handler(content_types=['video', 'document'])
def get_kino(msg):
    if isinstance(admin_mode.get(msg.chat.id), dict) and admin_mode[msg.chat.id].get('step') == 'awaiting_video':
        code = admin_mode[msg.chat.id]['code']
        kino_baza[code] = msg.video.file_id if msg.content_type == 'video' else msg.document.file_id
        admin_mode[msg.chat.id] = 'admin_panel'
        bot.send_message(msg.chat.id, f"✅ Kino '{code}' qo‘shildi!")

@bot.message_handler(func=lambda m: admin_mode.get(m.chat.id) == 'new_post')
def post_yuborish(msg):
    try:
        bot.send_message(ADMIN_ID, "📢 Post yuborildi.")
        bot.send_message(ADMIN_ID, msg.text)
        admin_mode[msg.chat.id] = 'admin_panel'
    except Exception as e:
        bot.send_message(msg.chat.id, f"Xato: {e}")

@bot.message_handler(func=lambda m: True)
def user_kino_qidirish(msg):
    if msg.text in kino_baza:
        bot.send_video(msg.chat.id, kino_baza[msg.text])
    else:
        bot.send_message(msg.chat.id, "❌ Bunday kod topilmadi!")

# ... (barcha kodlaringizdan keyin)
print("Bot ishga tushdi...")
bot.remove_webhook()
bot.polling()