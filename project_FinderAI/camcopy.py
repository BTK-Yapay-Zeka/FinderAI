import cv2
import numpy as np
import face_recognition
import asyncio
from telegram import Bot
import logging
import time
import os
from file_read import FileRead

BOT_TOKEN = 'your telegram bot token id'
CHAT_ID = 'your telegram id'

async def send_telegram_message(message):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

def telegram(name):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Başarılı. Zaman: {current_time}")
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_telegram_message(f"EŞLEŞME TESPİT EDİLDİ - {current_time} İD: {name}"))

fr = FileRead("aranan")

img_paths = fr.image_path_names
img_names = fr.image_names

name_list = []
encoding_list = []

def face_encoding(img_paths, img_names):
    for i, img in enumerate(img_paths):
        kisi = face_recognition.load_image_file(img)
        kisi_encoding = face_recognition.face_encodings(kisi)[0]

        encoding_list.append(kisi_encoding)
        name_list.append(img_names[i])

face_encoding(img_paths, img_names)

cap = cv2.VideoCapture(0)

fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Mevcut FPS: {fps}")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Görüntü alınamadı")
        break

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(encoding_list, face_encoding)
        name = "Temiz"

        if True in matches:
            matchedindex = matches.index(True)
            name = name_list[matchedindex]
            telegram(name)

            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filepath = os.path.join("bulundu", f"found_{timestamp}_{name}.jpg")
            cv2.imwrite(filepath, frame)

        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)

    cv2.imshow("Kamera", frame)

    if cv2.waitKey(2) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
