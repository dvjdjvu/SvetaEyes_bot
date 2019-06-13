#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sys
sys.path.append('../token')

import telebot
import mongo
import SvetaEyesToken

class SvetaEyes():
    
    def __init__(self, _mongo):
        self.bot = telebot.TeleBot(SvetaEyesToken.token)
        
        self.mongo = _mongo
        
        self.keyboardStart = telebot.types.ReplyKeyboardMarkup()
        self.keyboardStart.row('Подключиться', 'Не подключаться')
        
        @self.bot.message_handler(commands=['start'])
        def get_start(message):
            if not self.mongo.coll.find({"id": message.chat.id}).count() :
                
                self.bot.send_message(message.chat.id, 'Привет, ты подключился ко мне.')
            
                self.mongo.coll.save({'id': message.chat.id, 'first_name': message.from_user.first_name, 'last_name': message.from_user.last_name})
            
                print(message.chat.id, message.from_user.first_name, message.from_user.last_name)
            else :
                self.bot.send_message(message.chat.id, 'Привет, ты уже подключен ко мне.')
            
        @self.bot.message_handler(commands=['stop'])
        def get_start(message):
            self.bot.send_message(message.chat.id, 'Привет, ты отключился от меня.')
            self.mongo.coll.remove({"id": message.chat.id})
        
        @self.bot.message_handler(content_types=['text'])
        def get_text(message):
            if self.mongo.coll.find({"id": message.chat.id}).count() :
                for men in self.mongo.coll.find({"id": message.chat.id}):
                    self.bot.send_message(message.from_user.id, "Привет ", men["name"])
            else :
                self.bot.send_message(message.from_user.id, "Ты ко мне не подключен, напиши /start")
    
    def __del__(self):
        pass
    
    def run(self):
        self.bot.polling(none_stop=True, interval=0)
    
    
    
            
            