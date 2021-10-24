#!/usr/bin/python3
import telebot
from telebot import types

import requests
import json
import os

from telebot.apihelper import download_file

import support_function_bot

token = '1606920972:AAFC_ZFHY4aaYc54Q9KBAFbVvuMzhLpRdGM'

bot = telebot.TeleBot(token)

key_bufer = {}


def send_code_to_API(message):
    global key_bufer
    code = message.text
    if code.isdigit():
        code_request = requests.post('http://212.109.192.158//pdfun/api/v1.0/auth_from_code', json={'code': code})
        if code_request.json()['status'] == True:
            key_bufer[message.from_user.id] = code
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_go_into_start = types.KeyboardButton("To Start.")
            msg = bot.send_message(message.chat.id,"Connected!\nSend file.", reply_markup=keyboard)
            bot.register_next_step_handler(msg, take_file, "send")
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_go_into_start = types.KeyboardButton("To Start.")
            button_go_into_bot = types.KeyboardButton("Forward to site.")
            keyboard.add(button_go_into_bot ,button_go_into_start)
            bot.send_message(message.chat.id,"Wrong Code.", reply_markup=keyboard)    
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_go_into_start = types.KeyboardButton("To Start.")
        button_go_into_bot = types.KeyboardButton("Forward to site.")
        keyboard.add(button_go_into_bot ,button_go_into_start)
        bot.send_message(message.chat.id,"Numbers, pls.", reply_markup=keyboard)


def take_file(message, *args):
    for arg in args:
        type = arg
        print(type)
    if message.content_type == 'document':
        if message.document.mime_type == 'application/pdf':
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_name = message.document.file_name
            support_function_bot.safe_files(downloaded_file, file_name, message.from_user.id)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            if type == "send":
                button_go_into_start = types.KeyboardButton("Send files to site.")
                button_go_into_bot = types.KeyboardButton("Download file to site.")
            elif type == "merge":
                button_go_into_start = types.KeyboardButton("Send files for merge.")
                button_go_into_bot = types.KeyboardButton("Download file for merge.")
            keyboard.add(button_go_into_bot ,button_go_into_start)
            bot.send_message(message.chat.id,"What next?", reply_markup=keyboard)
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_go_into_start = types.KeyboardButton("To Start.")
            button_go_into_bot = types.KeyboardButton("Send files to site.")
            keyboard.add(button_go_into_bot ,button_go_into_start)
            bot.send_message(message.chat.id,"Need for PDF file.", reply_markup=keyboard)
        
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_go_into_start = types.KeyboardButton("To Start.")
        button_go_into_bot = types.KeyboardButton("Send files to site.")
        keyboard.add(button_go_into_bot ,button_go_into_start)
        bot.send_message(message.chat.id,"Need for PDF file.", reply_markup=keyboard)




@bot.message_handler(commands=['start'])
def start_message(message):
    start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_go_to_web = types.KeyboardButton("Send to site.")
    button_go_into_bot = types.KeyboardButton("Work in bot.")
    start_keyboard.add(button_go_to_web, button_go_into_bot)	
    bot.send_message(message.chat.id,"Welcome to KekistanPDF", reply_markup=start_keyboard)

@bot.message_handler(content_types='text')
def check_text(message):
    global key_bufer
    if message.text == 'Send to site.':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_go_into_start = types.KeyboardButton("To Start.")
        keyboard.add(button_go_into_start)	
        prev_message = bot.send_message(message.chat.id,"Input code from site:", reply_markup=keyboard)
        bot.register_next_step_handler(prev_message, send_code_to_API)
    elif message.text == "Work in bot.":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_merge = types.KeyboardButton("Merge PDFs")
        keyboard.add(button_merge)
        msg = bot.send_message(message.chat.id, "Choose function",reply_markup=keyboard)
        bot.register_next_step_handler(msg,funcs)
    elif message.text == 'Download file to site.':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_go_into_start = types.KeyboardButton("To Start.")
        msg = bot.send_message(message.chat.id,"Send file", reply_markup=keyboard)
        bot.register_next_step_handler(msg, take_file, "send")
    elif message.text == 'Download file for merge':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_go_into_start = types.KeyboardButton("To Start.")
        msg = bot.send_message(message.chat.id,"Send file", reply_markup=keyboard)
        bot.register_next_step_handler(msg, take_file, "merge")
    elif message.text == 'Send files to site.':
        print(key_bufer)
        user_files = os.listdir(f'user_files/{message.from_user.id}')
        support_function_bot.send_files_to_api(user_files, message.from_user.id, key_bufer[int(message.from_user.id)])
        start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_go_to_web = types.KeyboardButton("Send to site.")
        button_go_into_bot = types.KeyboardButton("Work in bot.")
        start_keyboard.add(button_go_to_web, button_go_into_bot)	
        bot.send_message(message.chat.id,"Succsessful send to site.", reply_markup=start_keyboard)
    elif message.text == 'Send files for merge.':
        print(key_bufer)
        user_files = os.listdir(f'user_files/{message.from_user.id}')
        support_function_bot.send_files_to_api_mer(user_files, message.from_user.id)
        start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_go_to_web = types.KeyboardButton("Send to site.")
        button_go_into_bot = types.KeyboardButton("Work in bot.")
        start_keyboard.add(button_go_to_web, button_go_into_bot)
        file = open('user_files/doc.pdf', 'rb')
        bot.send_document(message.chat.id, file)
        bot.send_message(message.chat.id,"Succsessful send to site.", reply_markup=start_keyboard)
        file.close()


def funcs(msg):
    if msg.text == "Merge PDFs":
        msg = bot.send_message(msg.chat.id, "Send files to merge")
        bot.register_next_step_handler(msg, take_file, "merge")


bot.infinity_polling()