from pyzbar.pyzbar import decode
import requests
import telepot
import cv2
import numpy as np
import io

def get_barcode_info(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray_img)

    if len(barcodes) == 1:
        code = barcodes[0].data
        url = "https://it.openfoodfacts.org/api/v0/product/{}.json".format(code)
        data = requests.get(url).json()
        if data["status"] == 1:
            product = data["product"]
            brand = product["brands"]
            return "produttore: {}    nome: {}".format(product["brands"], product["product_name"])
        else:
            return "Prodotto non trovato!"
    else:
        return "Codice a barre non trovato!"


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'photo':
        raw_img = io.BytesIO()
        bot.download_file(msg['photo'][-1]['file_id'], raw_img)
        file_bytes = np.fromstring(raw_img.getvalue(), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        bot.sendMessage(chat_id, "Sto cercando...")
        data = get_barcode_info(img)
        bot.sendMessage(chat_id, data)
    else:
      bot.sendMessage(chat_id, "Inviami una foto contenente un codice a barre!")

TOKEN = '*** inserisci il tuo token qui  ***'

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)

print('Listening ...')

import time
while 1:
    time.sleep(10)
