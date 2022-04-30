from ast import parse
import string
from urllib import response
from aiogram import Bot, Dispatcher, executor
from numpy import average, string_
import config
import logging
import sqlite
import Levenshtein as lev
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import copy
import math
from sqlite import sqlight
import asyncio
from contextlib import suppress
from aiogram import types
import aiogram.utils.exceptions
import aioschedule as schedule
import requests
import json
import concurrent.futures
import threading
import time
import parser

thread_local = threading.local()

db = sqlight('crypto_coins.db')

## This function returns list with all chat ids
def get_id():
    id = []
    response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(config.API_TOKEN))
    json_request = json.loads(response.text)
    response_info = json_request["result"]
    for i in range(len(response_info)):
        if response_info[i].get("message"):
            id.append(response_info[i]["message"]["chat"]["id"])
        else:
            id.append(response_info[i]["my_chat_member"]["chat"]["id"])
    id = list(dict.fromkeys(id))
    return id

def send_list():
    string = 'Daily morning report of 5 most popular tokens:\n'
    string_p = ''
    tickets = db.get_tickets()
    for ticket in tickets:
        ticket_real = ticket[0]
        all_info = db.get_all(ticket_real)
        arrow = ''
        if all_info[4] == '+':
            arrow = '↑'
        elif all_info[4] == '-':
            arrow = '↓'
        else:
            arrow = ''
        string_p = string_p + all_info[0] + " " + all_info[1] + ' ' + arrow + all_info[3] + '\n'
    string = string + string_p
    return string

async def send_everyone():
    list_id = get_id()
    for id in list_id:
        requests.post('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(config.API_TOKEN, str(id), str(send_list())))

async def sched():
    schedule.every().day.at("01:19").do(send_everyone)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(0.1) 

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task2 = loop.create_task(parser.parse_every())
    task1 = loop.create_task(sched())
    loop.run_forever()
