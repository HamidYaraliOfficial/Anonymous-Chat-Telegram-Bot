import telebot
from telebot import types
import sqlite3
from datetime import datetime

TOKEN = 'TOKEN'
ADMINS = [8272359057]  #عددی

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('anonchat.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users
             (user_id INTEGER PRIMARY KEY,
              username TEXT,
              first_name TEXT,
              last_name TEXT,
              display_name TEXT,
              join_date TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS chats
             (chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
              user1_id INTEGER,
              user2_id INTEGER,
              start_time TEXT,
              end_time TEXT,
              via_link INTEGER DEFAULT 0)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS required_channels
             (channel_id INTEGER PRIMARY KEY AUTOINCREMENT,
              channel_username TEXT UNIQUE)''')

conn.commit()

def add_user(user):
    cursor.execute('''INSERT OR IGNORE INTO users
                   (user_id, username, first_name, last_name, display_name, join_date)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                   (user.id, user.username, user.first_name, user.last_name,
                    user.first_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

def get_user(user_id):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    return cursor.fetchone()

def update_display_name(user_id, new_name):
    cursor.execute('UPDATE users SET display_name = ? WHERE user_id = ?', (new_name, user_id))
    conn.commit()

def is_user_in_chat(user_id):
    cursor.execute('''SELECT * FROM chats
                   WHERE (user1_id = ? OR user2_id = ?) AND end_time IS NULL''', (user_id, user_id))
    return cursor.fetchone() is not None

def start_chat(user1_id, user2_id, via_link=False):
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''INSERT INTO chats
                   (user1_id, user2_id, start_time, via_link)
                   VALUES (?, ?, ?, ?)''',
                   (user1_id, user2_id, start_time, 1 if via_link else 0))
    conn.commit()
    return cursor.lastrowid

def end_chat(chat_id):
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('UPDATE chats SET end_time = ? WHERE chat_id = ?', (end_time, chat_id))
    conn.commit()

def get_required_channels():
    cursor.execute('SELECT channel_username FROM required_channels')
    return [row[0] for row in cursor.fetchall()]

def add_required_channel(channel_username):
    try:
        cursor.execute('INSERT INTO required_channels (channel_username) VALUES (?)', (channel_username,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def remove_required_channel(channel_username):
    cursor.execute('DELETE FROM required_channels WHERE channel_username = ?', (channel_username,))
    conn.commit()
    return cursor.rowcount > 0

def check_channels_membership(user_id):
    required_channels = get_required_channels()
    if not required_channels:
        return True
        
    for channel in required_channels:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except:
            return False
    return True

def get_bot_stats():
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM chats')
    total_chats = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM chats WHERE end_time IS NULL')
    active_chats = cursor.fetchone()[0]
    
    return {
        'total_users': total_users,
        'total_chats': total_chats,
        'active_chats': active_chats
    }

waiting_users = []
active_pairs = {}

def show_main_menu(chat_id, is_admin=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('شروع چت ناشناس 🎭')
    btn2 = types.KeyboardButton('تغییر نام ✏️')
    btn3 = types.KeyboardButton('لینک دعوت 🔗')
    markup.add(btn1, btn2, btn3)
    
    if is_admin:
        btn_admin = types.KeyboardButton('پنل مدیریت 👨‍💻')
        markup.add(btn_admin)
    
    bot.send_message(chat_id, "به ربات چت ناشناس خوش آمدید!", reply_markup=markup)

@bot.message_handler(commands=['start', 'cancel'])
def handle_start(message):
    user = message.from_user
    add_user(user)
    
    if message.text == '/cancel':
        handle_cancel(message)
        return
    
    required_channels = get_required_channels()
    if required_channels and not check_channels_membership(user.id):
        show_channel_join_message(message.chat.id)
        return
    
    if len(message.text.split()) > 1:
        handle_private_link(message)
        return
    
    show_main_menu(message.chat.id, is_admin=(user.id in ADMINS))

def show_channel_join_message(chat_id):
    required_channels = get_required_channels()
    markup = types.InlineKeyboardMarkup()
    for channel in required_channels:
        markup.add(types.InlineKeyboardButton(
            text=f"عضویت در {channel}",
            url=f"https://t.me/{channel[1:]}"
        ))
    markup.add(types.InlineKeyboardButton(
        text="بررسی عضویت",
        callback_data="check_membership"
    ))
    bot.send_message(
        chat_id,
        "برای استفاده از ربات باید در کانال‌های زیر عضو شوید:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def check_membership(call):
    if check_channels_membership(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id, is_admin=(call.from_user.id in ADMINS))
    else:
        bot.answer_callback_query(call.id, "شما هنوز در همه کانال‌ها عضو نشده‌اید!")

def handle_cancel(message):
    user_id = message.from_user.id
    cursor.execute('''SELECT chat_id, user1_id, user2_id FROM chats
                   WHERE (user1_id = ? OR user2_id = ?) AND end_time IS NULL''',
                   (user_id, user_id))
    chat = cursor.fetchone()
    
    if chat:
        chat_id, user1_id, user2_id = chat
        partner_id = user1_id if user_id == user2_id else user2_id
        
        end_chat(chat_id)
        if user_id in active_pairs:
            del active_pairs[user_id]
        if partner_id in active_pairs:
            del active_pairs[partner_id]
        
        bot.send_message(user_id, "چت شما با موفقیت پایان یافت.")
        try:
            bot.send_message(partner_id, "کاربر مقابل چت را پایان داد.")
        except:
            pass
        
        show_main_menu(user_id, is_admin=(user_id in ADMINS))
        show_main_menu(partner_id, is_admin=(partner_id in ADMINS))
    else:
        bot.send_message(user_id, "شما در حال حاضر در چتی نیستید.")

@bot.message_handler(func=lambda message: message.text == 'شروع چت ناشناس 🎭')
def start_anonymous_chat(message):
    user_id = message.from_user.id
    
    if is_user_in_chat(user_id):
        bot.send_message(user_id, "شما هم اکنون در چت هستید! برای پایان چت از /cancel استفاده کنید.")
        return
    
    if user_id in waiting_users:
        bot.send_message(user_id, "شما در حال حاضر در لیست انتظار هستید.")
        return
    
    waiting_users.append(user_id)
    bot.send_message(user_id, "در حال جستجوی کاربر... لطفا صبر کنید.")
    
    if len(waiting_users) >= 2:
        user1 = waiting_users.pop(0)
        user2 = waiting_users.pop(0)
        
        chat_id = start_chat(user1, user2)
        active_pairs[user1] = (user2, chat_id)
        active_pairs[user2] = (user1, chat_id)
        
        bot.send_message(user1, "اتصال برقرار شد! شما با یک کاربر ناشناس چت می‌کنید.\nبرای پایان چت از /cancel استفاده کنید.")
        bot.send_message(user2, "اتصال برقرار شد! شما با یک کاربر ناشناس چت می‌کنید.\nبرای پایان چت از /cancel استفاده کنید.")

@bot.message_handler(func=lambda message: message.text == 'تغییر نام ✏️')
def set_display_name(message):
    msg = bot.send_message(message.chat.id, "لطفا نام نمایشی جدید خود را وارد کنید (حداکثر 20 کاراکتر):")
    bot.register_next_step_handler(msg, process_display_name)

def process_display_name(message):
    user_id = message.from_user.id
    new_name = message.text[:20]
    update_display_name(user_id, new_name)
    bot.send_message(message.chat.id, f"نام نمایشی شما به '{new_name}' تغییر یافت.")
    show_main_menu(message.chat.id, is_admin=(user_id in ADMINS))

@bot.message_handler(func=lambda message: message.text == 'لینک دعوت 🔗')
def generate_private_link(message):
    user_id = message.from_user.id
    bot.send_message(
        message.chat.id,
        f"لینک دعوت شما:\nhttps://t.me/{bot.get_me().username}?start=private_{user_id}\n\n"
        "این لینک را برای دوستان خود ارسال کنید تا مستقیماً با شما چت کنند."
    )

@bot.message_handler(func=lambda message: message.text == 'پنل مدیریت 👨‍💻')
def admin_panel_button(message):
    if message.from_user.id in ADMINS:
        show_admin_panel(message.chat.id)
    else:
        bot.send_message(message.chat.id, "⚠️ شما دسترسی به این بخش را ندارید!")

def show_admin_panel(chat_id):
    try:
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📊 آمار ربات", callback_data="admin_stats"),
            types.InlineKeyboardButton("👥 لیست کاربران", callback_data="admin_users"),
            types.InlineKeyboardButton("📢 ارسال همگانی", callback_data="admin_broadcast"),
            types.InlineKeyboardButton("📣 مدیریت کانال‌ها", callback_data="admin_channels")
        )
        bot.send_message(chat_id, "🔐 پنل مدیریت:", reply_markup=markup)
    except Exception as e:
        print(f"Error in admin_panel: {e}")
        bot.send_message(chat_id, "خطایی در نمایش پنل مدیریت رخ داد!")

def handle_private_link(message):
    user_id = message.from_user.id
    try:
        link_code = message.text.split()[1]
        
        if link_code.startswith('private_'):
            target_user_id = int(link_code.split('_')[1])
            target_user = get_user(target_user_id)
            
            if not target_user:
                bot.send_message(user_id, "کاربر مورد نظر یافت نشد!")
                return
            
            if is_user_in_chat(target_user_id):
                bot.send_message(user_id, "این کاربر هم اکنون در چت با شخص دیگری است.")
                return
            
            if user_id == target_user_id:
                bot.send_message(user_id, "شما نمی‌توانید با خودتان چت کنید!")
                return
            
            chat_id = start_chat(user_id, target_user_id, via_link=True)
            active_pairs[user_id] = (target_user_id, chat_id)
            active_pairs[target_user_id] = (user_id, chat_id)
            
            user_name = get_user(user_id)[4]
            target_name = target_user[4]
            
            bot.send_message(
                user_id,
                f"شما هم اکنون با {target_name} چت می‌کنید.\nبرای پایان چت از /cancel استفاده کنید."
            )
            bot.send_message(
                target_user_id,
                f"یک کاربر با لینک دعوت شما وارد چت شد!\nشما هم اکنون با {user_name} چت می‌کنید.\nبرای پایان چت از /cancel استفاده کنید."
            )
    except Exception as e:
        print(f"Error in handle_private_link: {e}")
        bot.send_message(user_id, "خطایی در برقراری ارتباط رخ داد!")

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'document', 'sticker'])
def handle_messages(message):
    user_id = message.from_user.id
    
    if user_id in active_pairs:
        partner_id, chat_id = active_pairs[user_id]
        
        cursor.execute('SELECT via_link FROM chats WHERE chat_id = ?', (chat_id,))
        via_link = cursor.fetchone()[0]
        
        try:
            if message.content_type == 'text':
                if via_link:
                    user_name = get_user(user_id)[4]
                    bot.send_message(partner_id, f"{user_name}: {message.text}")
                else:
                    bot.send_message(partner_id, message.text)
            elif message.content_type == 'photo':
                if via_link:
                    user_name = get_user(user_id)[4]
                    caption = f"{user_name}: {message.caption}" if message.caption else None
                    bot.send_photo(partner_id, message.photo[-1].file_id, caption=caption)
                else:
                    bot.send_photo(partner_id, message.photo[-1].file_id, caption=message.caption)
            elif message.content_type == 'document':
                if via_link:
                    user_name = get_user(user_id)[4]
                    caption = f"{user_name}: {message.caption}" if message.caption else None
                    bot.send_document(partner_id, message.document.file_id, caption=caption)
                else:
                    bot.send_document(partner_id, message.document.file_id, caption=message.caption)
            elif message.content_type == 'sticker':
                bot.send_sticker(partner_id, message.sticker.file_id)
        except:
            bot.send_message(user_id, "ارسال پیام ناموفق بود. ممکن است کاربر ربات را بلاک کرده باشد.")
            handle_cancel(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_'))
def handle_admin_actions(call):
    user_id = call.from_user.id
    if user_id not in ADMINS:
        return
    
    action = call.data.split('_')[1]
    
    if action == 'stats':
        stats = get_bot_stats()
        text = (
            "📊 آمار ربات:\n\n"
            f"👥 کاربران کل: {stats['total_users']}\n"
            f"💬 چت‌های کل: {stats['total_chats']}\n"
            f"🔛 چت‌های فعال: {stats['active_chats']}"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    
    elif action == 'users':
        cursor.execute('SELECT user_id, display_name, join_date FROM users ORDER BY join_date DESC LIMIT 50')
        users = cursor.fetchall()
        
        text = "آخرین کاربران:\n\n"
        for user in users:
            text += f"🆔 {user[0]} - {user[1]} - {user[2]}\n"
        
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    
    elif action == 'broadcast':
        msg = bot.send_message(user_id, "پیام همگانی خود را ارسال کنید:")
        bot.register_next_step_handler(msg, process_broadcast)
    
    elif action == 'channels':
        channels = get_required_channels()
        markup = types.InlineKeyboardMarkup()
        
        if channels:
            text = "کانال‌های اجباری فعلی:\n\n"
            for channel in channels:
                text += f"🔹 {channel}\n"
                markup.add(types.InlineKeyboardButton(
                    f"حذف {channel}",
                    callback_data=f"remove_channel_{channel}"
                ))
        else:
            text = "هیچ کانال اجباری تنظیم نشده است."
        
        markup.add(types.InlineKeyboardButton(
            "➕ افزودن کانال",
            callback_data="add_channel"
        ))
        markup.add(types.InlineKeyboardButton(
            "🔙 بازگشت",
            callback_data="admin_back"
        ))
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data == 'admin_back')
def admin_back(call):
    show_admin_panel(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('remove_channel_'))
def remove_channel(call):
    channel_username = call.data.split('_', 2)[2]
    if remove_required_channel(channel_username):
        bot.answer_callback_query(call.id, f"کانال {channel_username} حذف شد")
    else:
        bot.answer_callback_query(call.id, "خطا در حذف کانال")
    handle_admin_actions(call)

@bot.callback_query_handler(func=lambda call: call.data == 'add_channel')
def add_channel(call):
    msg = bot.send_message(call.from_user.id, "آیدی کانال را وارد کنید (مثال: @channel_name):")
    bot.register_next_step_handler(msg, process_new_channel)

def process_new_channel(message):
    if message.text.startswith('@'):
        if add_required_channel(message.text):
            bot.send_message(message.from_user.id, f"کانال {message.text} با موفقیت اضافه شد")
        else:
            bot.send_message(message.from_user.id, "این کانال قبلاً اضافه شده است")
    else:
        bot.send_message(message.from_user.id, "فرمت آیدی کانال نامعتبر است. باید با @ شروع شود")

def process_broadcast(message):
    if message.from_user.id not in ADMINS:
        return
    
    cursor.execute('SELECT user_id FROM users')
    users = cursor.fetchall()
    
    success = 0
    fail = 0
    
    for user in users:
        try:
            if message.content_type == 'text':
                bot.send_message(user[0], message.text)
            elif message.content_type == 'photo':
                bot.send_photo(user[0], message.photo[-1].file_id, caption=message.caption)
            elif message.content_type == 'document':
                bot.send_document(user[0], message.document.file_id, caption=message.caption)
            success += 1
        except:
            fail += 1
    
    bot.send_message(
        message.from_user.id,
        f"ارسال همگانی انجام شد:\n✅ موفق: {success}\n❌ ناموفق: {fail}"
    )

# راه‌اندازی ربات
print("Bot is running...")
bot.polling()