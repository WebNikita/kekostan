#!/usr/bin/python3
import telebot
from telebot import types

import requests
import json
import os

token = '1606920972:AAFC_ZFHY4aaYc54Q9KBAFbVvuMzhLpRdGM'
url2="http://212.109.192.158/pdfun/api/v1.0/merge_files"

bot = telebot.TeleBot(token)


def send_code_to_API(message):
    code = message.text
    if code.isdigit():
        code_request = requests.post('http://212.109.192.158//pdfun/api/v1.0/auth_from_code', json={'code': code})
        if code_request.json()['status'] == True:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_go_into_start = types.KeyboardButton("Начало")
            msg = bot.send_message(message.chat.id,"Успех! Загрузите файл", reply_markup=keyboard)
            bot.register_next_step_handler(msg, take_file)
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_go_into_start = types.KeyboardButton("Начало")
            button_go_into_bot = types.KeyboardButton("Продолжить на сайте")
            keyboard.add(button_go_into_bot ,button_go_into_start)
            bot.send_message(message.chat.id,"Вы ввели не тот код!", reply_markup=keyboard)    
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_go_into_start = types.KeyboardButton("Начало")
        button_go_into_bot = types.KeyboardButton("Продолжить на сайте")
        keyboard.add(button_go_into_bot ,button_go_into_start)
        bot.send_message(message.chat.id,"Вы ввели что то не то - нужны цифры", reply_markup=keyboard)


def take_file(message):
    if message.content_type == 'document':
        if message.document.mime_type == 'application/pdf':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_go_into_start = types.KeyboardButton("Конец загрузки")
            button_go_into_bot = types.KeyboardButton("Загрузить ещё файл")
            keyboard.add(button_go_into_bot ,button_go_into_start)
            bot.send_message(message.chat.id,"Что делаем?", reply_markup=keyboard)
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_go_into_start = types.KeyboardButton("Начало")
            button_go_into_bot = types.KeyboardButton("Продолжить на сайте")
            keyboard.add(button_go_into_bot ,button_go_into_start)
            bot.send_message(message.chat.id,"Нужно загрузить pdf файл", reply_markup=keyboard)
        
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_go_into_start = types.KeyboardButton("Начало")
        button_go_into_bot = types.KeyboardButton("Продолжить на сайте")
        keyboard.add(button_go_into_bot ,button_go_into_start)
        bot.send_message(message.chat.id,"Нужно загрузить pdf файл", reply_markup=keyboard)




@bot.message_handler(commands=['start'])
def start_message(message):
    start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_go_to_web = types.KeyboardButton("Продолжить на сайте")
    button_go_into_bot = types.KeyboardButton("Хочу в боте")
    start_keyboard.add(button_go_to_web, button_go_into_bot)	
    bot.send_message(message.chat.id,"Добро пожаловать в бота для конвертации PDF", reply_markup=start_keyboard)

@bot.message_handler(content_types='text')
def check_text(message):
    if message.text == 'Продолжить на сайте':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_go_into_start = types.KeyboardButton("Начало")
        keyboard.add(button_go_into_start)	
        prev_message = bot.send_message(message.chat.id,"Введите код с сайта:", reply_markup=keyboard)
        bot.register_next_step_handler(prev_message, send_code_to_API)
    elif message.text == "Хочу в боте":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_merge = types.KeyboardButton("Merge PDFs")
        keyboard.add(button_merge)
        msg = bot.send_message(message.chat.id, "Choose function",reply_markup=keyboard)
        bot.register_next_step_handler(msg,funcs)
    elif message.text == 'Загрузить ещё файл':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_go_into_start = types.KeyboardButton("Начало")
        msg = bot.send_message(message.chat.id,"Загрузите файл", reply_markup=keyboard)
        bot.register_next_step_handler(msg, take_file)
    elif message.text == 'Конец загрузки':
        start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_go_to_web = types.KeyboardButton("Продолжить на сайте")
        button_go_into_bot = types.KeyboardButton("Хочу в боте")
        start_keyboard.add(button_go_to_web, button_go_into_bot)	
        bot.send_message(message.chat.id,"Файлы успешно отправлены на сайт", reply_markup=start_keyboard)

def funcs(msg):
    if msg.text == "Merge PDFs":
        msg = bot.send_message(msg.chat.id, "Send files to merge")
        bot.register_next_step_handler(msg, sendm)

def sendm(msg):
    if(msg.content_type == "document" and msg.document.mime_type == "application/pdf"):
        while msg.document:
            print(msg.document.file_name)
            msg = bot.send_message(msg.chat.id,"Another")
            # path = msg.document.file_id
            # myfile = requests.get(path)
            # file = { "file":open(f"./user_files/document{i}.pdf", 'wb').write(myfile.content)}
            # requests.post(url2,file)
        msg = bot.send_message(msg.chat.id,"DONE")

bot.infinity_polling()