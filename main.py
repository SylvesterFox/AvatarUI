# This Python file uses the following encoding: utf-8
import sys
import os
import pvrecorder as pvr
import asyncio
import json
import websockets
from aiohttp import web
import threading
import time
import random

from PySide6.QtWidgets import QApplication, QWidget, QColorDialog
from ui_form import Ui_Widget

STATE = {
    "avatar": "assets/default",
    "device": 0,
    "sensitivity": 50,
    "background": "#00ff00",
    "emotion": 0,
    "eyes": 0
}

WS_CLIENTS = set()
CONFIG_FILE = "config.json"

def save_config():
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(STATE, f, ensure_ascii=False, indent=4)

def load_config():
    global STATE
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                STATE.update(loaded)
            print("[CONFIG] Loaded config.json")
        except Exception as e:
            print("[CONFIG] Failed to load config:", e)

# -----------------------------------------------------------
#     WEBSOCKET SERVER (для OBS)
# -----------------------------------------------------------
async def broadcast(msg: dict):
    if not WS_CLIENTS:
        return
    
    dead = []
    for ws in list(WS_CLIENTS):
        try:
            await ws.send(json.dumps(msg))
        except Exception as e:
            print(f"WS send failed: {e}")
            dead.append(ws)
    
    for ws in dead:
        try:
            WS_CLIENTS.remove(ws)
            await ws.close()
        except:
            pass


async def ws_handler(ws):
    WS_CLIENTS.add(ws)
    print("[WS] connect")

    # отправляем текущее состояние
    await ws.send(json.dumps(STATE))

    try:
        async for message in ws:
            pass  # OBS ничего не отправляет
    finally:
        WS_CLIENTS.remove(ws)
        print("[WS] disconnect")

# -----------------------------------------------------------
#     HTTP SERVER (отдаёт OBS HTML)
# -----------------------------------------------------------
async def handle_index(request):
    return web.FileResponse("index.html")


async def http_server():
    app = web.Application()
    app.router.add_get("/", handle_index)
    app.router.add_get("/index.html", handle_index)
    app.router.add_static("/assets", "assets")

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", 5500)
    print("[HTTP] Running on http://localhost:5500")
    await site.start()


async def ws_server():
    print("[WS] Running on ws://localhost:8765")
    async with websockets.serve(ws_handler, "0.0.0.0", 8765,  ping_interval=None, ping_timeout=None):
        await asyncio.Future()  # не завершаться

# -----------------------------------------------------------
#     AUDIO PROCESSOR (эмоции + глаза)
# -----------------------------------------------------------
async def audio_loop():
    recorder = pvr.PvRecorder(device_index=STATE["device"], frame_length=1024)
    recorder.start()
    print("[Audio] Running")

    eyes_stage = 0
    last_blink = time.time()

    while True:
        try:
            frame = recorder.read()

            # ---------------- AMPLITUDE ----------------
            minimal = min(frame)
            maximum = max(frame)
            amplitude = maximum - minimal

            # ---------------- EMOTION LOGIC ------------
            sens = STATE["sensitivity"]
            emotion = 0

            if amplitude > sens * 20: emotion = 1
            if amplitude > sens * 40: emotion = 2
            if amplitude > sens * 60: emotion = 3
            if amplitude > sens * 80: emotion = 4
            if amplitude > sens * 120: emotion = 5

            STATE["emotion"] = emotion

            # ---------------- BLINK --------------------
            if time.time() - last_blink > random.randint(2, 5):
                eyes_stage = 1
                last_blink = time.time()

            if eyes_stage > 0:
                eyes_stage += 1
                if eyes_stage > 7:
                    eyes_stage = 0

            STATE["eyes"] = eyes_stage

            await broadcast({"emotion": emotion, "eyes": eyes_stage})
        except Exception as e:
            print("audio_loop error:", e)

        await asyncio.sleep(0.033)


# -----------------------------------------------------------
#     СТАРТ ВСЕХ СЕРВЕРОВ В ПОТОКЕ
# -----------------------------------------------------------
def start_asyncio_servers():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.create_task(http_server())
    loop.create_task(ws_server())
    loop.create_task(audio_loop())

    loop.run_forever()



class MainApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.setWindowTitle("webst")

        self.obs_link = self.ui.lineEdit
        self.avatar_box = self.ui.comboBox
        self.mic_box = self.ui.comboBox_2
        self.apply_btn = self.ui.pushButton_2
        self.color_btn = self.ui.colorPick
        self.sens_slider = self.ui.horizontalSlider
        self.color_hex = self.ui.colorHex


        self.color_btn.clicked.connect(self.choose_color)
        self.apply_btn.clicked.connect(self.apply_settings)

        self.ui.frameColor.setStyleSheet("background-color: #000000;")
        self.ui.lineEdit.setReadOnly(True)
        self.obs_link.setText("http://loaclhost:5500/")

        self.load_avaters()

        self.load_microphoes()


    # ================================================================
    #   ВЫБОР ЦВЕТА ФОНА
    # ================================================================

    def choose_color(self):
        color = QColorDialog.getColor(parent=self, title="Выбрать цвет")
        if color.isValid():
            self.ui.colorHex.setText(f"{color.name()}")
            self.ui.frameColor.setStyleSheet(f"background-color: {color.name()};")

    # ================================================================
    #   ЗАГРУЗКА АВАТАРОВ
    # ================================================================
    def load_avaters(self):
        self.ui.comboBox.clear()
        for folder in os.listdir("assets"):
            if os.path.isdir(f"assets/{folder}"):
                self.ui.comboBox.addItem(folder)

    # ================================================================
    #   ЗАГРУЗКА МИКРОФОНОВ
    # ================================================================
    
    def load_microphoes(self):
        self.mic_box.clear()
        devices = pvr.PvRecorder.get_available_devices()
        for d in devices:
            self.mic_box.addItem(d)
    
    def apply_settings(self):
        avatar = self.avatar_box.currentText()
        mic_index = self.mic_box.currentIndex()
        sensitivity = self.sens_slider.value()
        color = self.color_hex.text()

        STATE["avatar"] = f"assets/{avatar}"
        STATE["device"] = mic_index
        STATE["background"] = color
        STATE["sensitivity"] = sensitivity

        save_config()
        print("[CONFIG] Saved")

    def apply_loaded_config(self):
        # фон
        self.ui.colorHex.setText(STATE["background"])
        self.ui.frameColor.setStyleSheet(f"background-color: {STATE['background']};")

        # аватар
        avatar_folder = STATE["avatar"].replace("assets/", "")
        index = self.avatar_box.findText(avatar_folder)
        if index >= 0:
            self.avatar_box.setCurrentIndex(index)

        # микрофон
        if 0 <= STATE["device"] < self.mic_box.count():
            self.mic_box.setCurrentIndex(STATE["device"])

        # чувствительность
        self.sens_slider.setValue(STATE["sensitivity"])

if __name__ == "__main__":
    load_config()
    threading.Thread(target=start_asyncio_servers, daemon=True).start()
    app = QApplication(sys.argv)
    widget = MainApp()
    widget.apply_loaded_config()
    widget.show()
    sys.exit(app.exec())
