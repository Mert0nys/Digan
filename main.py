import telebot
import config
import messages

ADMINN1 = config.MAIN_ADMIN
bot = telebot.TeleBot(config.BOT_KEY)
user_queries = {}
admin_ids = [ADMINN1] 

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, messages.welcome_text)

@bot.message_handler(commands=['addadmin'])
def add_admin(message):
    if message.from_user.id in admin_ids:
        try:
            if len(message.text.split()) < 2:
                bot.reply_to(message, messages.get_new_id)
                return
            
            new_admin_id = int(message.text.split()[1])
            if new_admin_id not in admin_ids:
                admin_ids.append(new_admin_id)
                bot.send_message(new_admin_id, messages.new_admin_message)
                bot.reply_to(message, f"Пользователь с ID <U>{new_admin_id}</U> был добавлен как администратор.", parse_mode="HTML")
            else:
                bot.reply_to(message, messages.the_admin_exists)
        except (IndexError, ValueError):
            bot.reply_to(message, messages.valueError_or_indexError)
    else:
        bot.reply_to(message, messages.no_admin)

@bot.message_handler(func=lambda message: message.from_user.id not in admin_ids)
def handle_user_message(message):
    user_queries[message.from_user.id] = message.text
    bot.send_message(ADMINN1, f"Сообщение от {message.from_user.username}: {message.text}")
    bot.reply_to(message, messages.user_message)

@bot.message_handler(func=lambda message: message.from_user.id in admin_ids)
def handle_admin_response(message):
    if user_queries:
        user_id = next(iter(user_queries))
        try:
            bot.send_message(user_id, f"Ответ от админа {message.from_user.username}: {message.text}")
            bot.reply_to(message, f"Ответ отправлен пользователю {user_id}.")
            del user_queries[user_id]
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
    else:
        bot.reply_to(message, messages.no_messages)

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
