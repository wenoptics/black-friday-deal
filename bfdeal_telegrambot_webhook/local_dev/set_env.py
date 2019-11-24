import os

telegrambot_token, _, _ = open('../../secret.txt').readlines()+['']
os.environ['TELEBOT_TOKEN'] = telegrambot_token
