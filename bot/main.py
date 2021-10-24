#!/usr/bin/python3
import requests
import telebot
from telebot import types
import datetime
import config
import os
import json
import random

url="http://212.109.192.158/pdfun/api/v1.0/get_code"
bot = telebot.TeleBot(config.token)
person = { "persons": [] }

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['command1'])
def send_command1(message):
    bot.reply_to(message,"Enter code!")
    msg = bot.send_message(message.chat.id,"Enter code, pls!")
    bot.register_next_step_handler(msg,check_code)

def check_code(msg):
    print(msg.text)
    r = requests.post(url, data={"code":msg.text})
    print(r.text)


bot.infinity_polling()