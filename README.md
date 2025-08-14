# Anonymous Chat Telegram Bot

This is a Python-based Telegram bot that facilitates anonymous chats between users, supports private chat links, and provides admin functionalities. Built using the `python-telegram-bot` library, it includes features like user management, required channel membership, and message broadcasting.

## Features
- Anonymous chat pairing for random user connections.
- Private chat links for direct chats with specific users.
- Display name customization for users (up to 20 characters).
- Admin panel for managing bot statistics, users, and required channels.
- Support for broadcasting messages (text, photos, documents) to all users.
- SQLite database for storing user data, chat sessions, and required channels.
- Mandatory channel membership check before accessing the bot.
- Support for sending text, photos, documents, and stickers in chats.

## Requirements
- Python 3.7+
- `python-telegram-bot` library (`pip install python-telegram-bot`)
- `sqlite3` (included with Python standard library)

## Setup
1. Replace `'TOKEN'` in the code with your Telegram Bot API token obtained from [BotFather](https://t.me/BotFather).
2. Update the `ADMINS` list with the Telegram user IDs of administrators.
3. Install dependencies using `pip install -r requirements.txt` (create a `requirements.txt` with `python-telegram-bot`).
4. Run the bot with `python bot.py`.

## Usage
- Start the bot with `/start` to access the main menu.
- Join required channels (if any) to unlock bot features.
- Use "شروع چت ناشناس 🎭" to start an anonymous chat with a random user.
- Use "تغییر نام ✏️" to set a custom display name.
- Use "لینک دعوت 🔗" to generate a private chat link.
- Admins can access the admin panel with "پنل مدیریت 👨‍💻" to view stats, manage users, broadcast messages, or configure required channels.
- Use `/cancel` to end an active chat.

## Database Structure
- `users`: Stores user details (user_id, username, first_name, last_name, display_name, join_date).
- `chats`: Tracks chat sessions (chat_id, user1_id, user2_id, start_time, end_time, via_link).
- `required_channels`: Stores mandatory channel usernames for membership checks.

## Logging
- Console logs are enabled to track bot activities, such as chat initiations, terminations, and errors.

## Code Structure
- `add_user`, `get_user`, `update_display_name`: Manage user data in the database.
- `start_chat`, `end_chat`: Handle chat session creation and termination.
- `check_channels_membership`, `add_required_channel`, `remove_required_channel`: Manage mandatory channel subscriptions.
- `show_main_menu`, `show_admin_panel`: Display user and admin interfaces.
- `handle_start`, `start_anonymous_chat`, `handle_private_link`: Manage bot commands and chat logic.
- `handle_messages`: Forward messages (text, photos, documents, stickers) between chat partners.
- Admin functions: Handle broadcasting, user stats, and channel management.

## License
MIT License

---

# ربات چت ناشناس تلگرام

این یک ربات تلگرامی مبتنی بر پایتون است که امکان چت ناشناس بین کاربران، لینک‌های چت خصوصی و قابلیت‌های مدیریتی را فراهم می‌کند. این ربات با استفاده از کتابخانه `python-telegram-bot` ساخته شده و شامل ویژگی‌هایی مانند مدیریت کاربران، بررسی عضویت در کانال‌های اجباری و ارسال پیام همگانی است.

## ویژگی‌ها
- جفت‌سازی چت ناشناس برای اتصال تصادفی کاربران.
- لینک‌های چت خصوصی برای گفت‌وگو با کاربران خاص.
- امکان تغییر نام نمایشی کاربران (حداکثر 20 کاراکتر).
- پنل مدیریت برای مشاهده آمار ربات، مدیریت کاربران و کانال‌های اجباری.
- پشتیبانی از ارسال پیام همگانی (متن، عکس، فایل) به همه کاربران.
- پایگاه داده SQLite برای ذخیره اطلاعات کاربران، جلسات چت و کانال‌های اجباری.
- بررسی عضویت در کانال‌های اجباری قبل از دسترسی به ربات.
- پشتیبانی از ارسال متن، عکس، فایل و استیکر در چت‌ها.

## پیش‌نیازها
- پایتون نسخه 3.7 یا بالاتر
- کتابخانه `python-telegram-bot` (نصب با `pip install python-telegram-bot`)
- `sqlite3` (موجود در کتابخانه استاندارد پایتون)

## راه‌اندازی
1. مقدار `'TOKEN'` در کد را با توکن API ربات تلگرام که از [BotFather](https://t.me/BotFather) دریافت کرده‌اید جایگزین کنید.
2. لیست `ADMINS` را با آیدی‌های کاربری تلگرام مدیران به‌روزرسانی کنید.
3. وابستگی‌ها را با استفاده از `pip install -r requirements.txt` نصب کنید (فایل `requirements.txt` را با درج `python-telegram-bot` ایجاد کنید).
4. ربات را با اجرای `python bot.py` راه‌اندازی کنید.

## استفاده
- با دستور `/start` ربات را شروع کنید تا به منوی اصلی دسترسی پیدا کنید.
- در کانال‌های اجباری (در صورت وجود) عضو شوید تا قابلیت‌های ربات فعال شود.
- از گزینه "شروع چت ناشناس 🎭" برای شروع چت با یک کاربر تصادفی استفاده کنید.
- از گزینه "تغییر نام ✏️" برای تنظیم نام نمایشی دلخواه استفاده کنید.
- از گزینه "لینک دعوت 🔗" برای ایجاد لینک چت خصوصی استفاده کنید.
- مدیران می‌توانند با گزینه "پنل مدیریت 👨‍💻" به آمار، مدیریت کاربران، ارسال پیام همگانی و تنظیم کانال‌های اجباری دسترسی پیدا کنند.
- از دستور `/cancel` برای پایان دادن به چت فعال استفاده کنید.

## ساختار پایگاه داده
- `users`: ذخیره اطلاعات کاربران (شناسه، نام کاربری، نام، نام خانوادگی، نام نمایشی، تاریخ عضویت).
- `chats`: رصد جلسات چت (شناسه چت، شناسه کاربر 1، شناسه کاربر 2، زمان شروع، زمان پایان، از طریق لینک).
- `required_channels`: ذخیره نام کاربری کانال‌های اجباری برای بررسی عضویت.

## لاگ‌ها
- لاگ‌های کنسول برای رصد فعالیت‌های ربات مانند شروع چت، پایان چت و خطاها فعال هستند.

## ساختار کد
- `add_user`، `get_user`، `update_display_name`: مدیریت داده‌های کاربران در پایگاه داده.
- `start_chat`، `end_chat`: مدیریت ایجاد و پایان جلسات چت.
- `check_channels_membership`، `add_required_channel`، `remove_required_channel`: مدیریت عضویت در کانال‌های اجباری.
- `show_main_menu`، `show_admin_panel`: نمایش رابط کاربری و پنل مدیریت.
- `handle_start`، `start_anonymous_chat`، `handle_private_link`: مدیریت دستورات ربات و منطق چت.
- `handle_messages`: ارسال پیام‌ها (متن، عکس، فایل، استیکر) بین شرکای چت.
- توابع مدیریتی: مدیریت ارسال همگانی، آمار کاربران و کانال‌ها.

## مجوز
مجوز MIT

---

# Telegram匿名聊天机器人

这是一个基于Python的Telegram机器人，支持用户之间的匿名聊天、私人聊天链接以及管理员功能。使用`python-telegram-bot`库构建，包含用户管理、强制频道成员检查和消息广播等功能。

## 功能
- 随机用户连接的匿名聊天配对。
- 私人聊天链接，用于与特定用户直接聊天。
- 用户可自定义显示名称（最多20个字符）。
- 管理员面板，用于管理机器人统计数据、用户和强制频道。
- 支持向所有用户广播消息（文本、图片、文件）。
- 使用SQLite数据库存储用户数据、聊天会话和强制频道。
- 在访问机器人之前检查强制频道成员资格。
- 支持在聊天中发送文本、图片、文件和贴纸。

## 要求
- Python 3.7或更高版本
- `python-telegram-bot`库（使用`pip install python-telegram-bot`安装）
- `sqlite3`（Python标准库中包含）

## 设置
1. 将代码中的`'TOKEN'`替换为从[BotFather](https://t.me/BotFather)获取的Telegram机器人API令牌。
2. 更新`ADMINS`列表，添加管理员的Telegram用户ID。
3. 使用`pip install -r requirements.txt`安装依赖项（创建一个包含`python-telegram-bot`的`requirements.txt`文件）。
4. 使用`python bot.py`运行机器人。

## 使用
- 使用`/start`命令启动机器人以访问主菜单。
- 加入强制频道（如果有）以解锁机器人功能。
- 使用“شOLED开始匿名聊天🎭”选项与随机用户开始匿名聊天。
- 使用“更改名称✏️”选项设置自定义显示名称。
- 使用“邀请链接🔗”选项生成私人聊天链接。
- 管理员可以使用“管理面板👨‍💻”选项查看统计数据、管理用户、广播消息或配置强制频道。
- 使用`/cancel`命令结束活跃聊天。

## 数据库结构
- `users`：存储用户信息（用户ID、用户名、名字、姓氏、显示名称、加入日期）。
- `chats`：跟踪聊天会话（聊天ID、用户1 ID、用户2 ID、开始时间、结束时间、通过链接）。
- `required_channels`：存储强制频道的用户名以进行成员检查。

## 日志
- 启用控制台日志以跟踪机器人活动，例如聊天开始、结束和错误。

## 代码结构
- `add_user`、`get_user`、`update_display_name`：管理数据库中的用户数据。
- `start_chat`、`end_chat`：处理聊天会话的创建和终止。
- `check_channels_membership`、`add_required_channel`、`remove_required_channel`：管理强制频道订阅。
- `show_main_menu`、`show_admin_panel`：显示用户和管理员界面。
- `handle_start`、`start_anonymous_chat`、`handle_private_link`：管理机器人命令和聊天逻辑。
- `handle_messages`：在聊天伙伴之间转发消息（文本、图片、文件、贴纸）。
- 管理员功能：处理广播、用户统计和频道管理。

## 许可证
MIT许可证