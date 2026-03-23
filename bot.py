import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

roles = []
is_collecting = False


# دالة تتحقق إذا المستخدم مشرف في نفس الجروب
def is_admin(chat_id, user_id):
    try:
        admins = bot.get_chat_administrators(chat_id)
        for admin in admins:
            if admin.user.id == user_id:
                return True
        return False
    except:
        return False


# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً 👋\nالبوت شغال")


# بدء تسجيل الأدوار
@bot.message_handler(commands=['start_roles'])
def start_roles(message):
    global is_collecting

    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ هذا الأمر للمشرفين فقط")

    is_collecting = True
    bot.reply_to(message, "تم بدء تسجيل الأدوار 🎭")


# إيقاف التسجيل
@bot.message_handler(commands=['stop_roles'])
def stop_roles(message):
    global is_collecting

    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ هذا الأمر للمشرفين فقط")

    is_collecting = False
    bot.reply_to(message, "تم إيقاف التسجيل ⛔")


# مسح الأدوار
@bot.message_handler(commands=['clear_roles'])
def clear_roles(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ هذا الأمر للمشرفين فقط")

    roles.clear()
    bot.reply_to(message, "تم مسح الأدوار 🗑️")


# عرض الأدوار
@bot.message_handler(commands=['show_roles'])
def show_roles(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ هذا الأمر للمشرفين فقط")

    if not roles:
        bot.reply_to(message, "لا يوجد أدوار ❌")
    else:
        text = "📋 الأدوار:\n" + "\n".join(roles)
        bot.reply_to(message, text)


# تسجيل الأدوار
@bot.message_handler(func=lambda message: True)
def collect_roles(message):
    global is_collecting

    # فقط إذا التسجيل شغال
    if not is_collecting:
        return

    # فقط مشرفين
    if not is_admin(message.chat.id, message.from_user.id):
        return

    roles.append(message.text)
    bot.reply_to(message, f"تم حفظ الدور: {message.text}")


# تشغيل البوت
bot.infinity_polling()
