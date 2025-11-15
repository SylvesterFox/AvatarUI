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

from PySide6.QtWidgets import QApplication, QWidget, QColorDialog, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtGui import QCloseEvent
from ui_form import Ui_Widget


STATE = {
    "avatar": "assets/default",
    "device": 0,
    "sensitivity": 50,
    "background": "#00ff00",
    "face_frames": [],          
    "face_count": 0,
    "eyes_frames": [],
    "eyes_count": 0,  
}
ASYNC_LOOP = None
WS_CLIENTS = set()
CONFIG_FILE = None

# Store server references globally
HTTP_RUNNER = None
WS_SERVER = None
AUDIO_RECORDER = None


def resource_path(relative):
    """ Получение пути к ресурсу для PyInstaller и разработки """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.abspath("."), relative)


def load_avatar(path):
    faces = []
    eyes = []

    for f in sorted(os.listdir(path)):
        if f.startswith("face_") and f.endswith(".png"):
            faces.append(f)
        if f.startswith("eyes_") and f.endswith(".png"):
            eyes.append(f)

    STATE["avatar_path"] = path

    STATE["face_frames"] = faces
    STATE["face_count"] = len(faces)

    STATE["eyes_frames"] = eyes
    STATE["eyes_count"] = len(eyes)

    print("Loaded:", STATE["face_frames"], STATE["eyes_frames"])


def save_config():
    global CONFIG_FILE
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(STATE, f, ensure_ascii=False, indent=4)


def load_config():
    global STATE, CONFIG_FILE
    CONFIG_FILE = resource_path("config.json")
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
        WS_CLIENTS.discard(ws)
        print("[WS] disconnect")


# -----------------------------------------------------------
#     HTTP SERVER (отдаёт OBS HTML)
# -----------------------------------------------------------
async def handle_index(request):
    return web.FileResponse(resource_path("index.html"))


async def http_server():
    global HTTP_RUNNER
    app = web.Application()
    app.router.add_get("/", handle_index)
    app.router.add_get("/index.html", handle_index)
    app.router.add_static("/assets", resource_path("assets"))

    HTTP_RUNNER = web.AppRunner(app)
    await HTTP_RUNNER.setup()

    site = web.TCPSite(HTTP_RUNNER, "0.0.0.0", 5500)
    print("[HTTP] Running on http://localhost:5500")
    await site.start()


async def ws_server():
    global WS_SERVER
    print("[WS] Running on ws://localhost:8765")
    WS_SERVER = await websockets.serve(
        ws_handler, 
        "0.0.0.0", 
        8765, 
        ping_interval=None, 
        ping_timeout=None
    )
    await asyncio.Future()  # не завершаться


# -----------------------------------------------------------
#     AUDIO PROCESSOR (эмоции + глаза)
# -----------------------------------------------------------
async def audio_loop():
    global AUDIO_RECORDER
    AUDIO_RECORDER = pvr.PvRecorder(device_index=STATE["device"], frame_length=1024)
    AUDIO_RECORDER.start()
    print("[Audio] Running")

    eyes_stage = 0
    last_blink = time.time()

    try:
        while True:
            try:
                frame = AUDIO_RECORDER.read()

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
                if amplitude > sens * 140: emotion = 6

                STATE["emotion"] = emotion

                # ---------------- BLINK --------------------
                if time.time() - last_blink > random.randint(5, 10):
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
    finally:
        if AUDIO_RECORDER:
            try:
                AUDIO_RECORDER.stop()
                AUDIO_RECORDER.delete()
            except:
                pass


# -----------------------------------------------------------
#     СТАРТ ВСЕХ СЕРВЕРОВ В ПОТОКЕ
# -----------------------------------------------------------
def start_asyncio_servers():
    global ASYNC_LOOP
    ASYNC_LOOP = asyncio.new_event_loop()
    asyncio.set_event_loop(ASYNC_LOOP)

    ASYNC_LOOP.create_task(http_server())
    ASYNC_LOOP.create_task(ws_server())
    ASYNC_LOOP.create_task(audio_loop())

    try:
        ASYNC_LOOP.run_forever()
    except Exception as e:
        print("Async loop stopped:", e)


def stop_asyncio_servers():
    """Properly shutdown all async servers and tasks"""
    global ASYNC_LOOP, HTTP_RUNNER, WS_SERVER, AUDIO_RECORDER
    
    if ASYNC_LOOP is None:
        return

    async def cleanup():
        """Async cleanup function"""
        # Close all websocket clients
        for ws in list(WS_CLIENTS):
            try:
                await ws.close()
            except:
                pass
        WS_CLIENTS.clear()

        # Stop websocket server
        if WS_SERVER:
            WS_SERVER.close()
            await WS_SERVER.wait_closed()

        # Stop HTTP server
        if HTTP_RUNNER:
            await HTTP_RUNNER.cleanup()

        # Cancel all remaining tasks except current one
        tasks = [t for t in asyncio.all_tasks(ASYNC_LOOP) 
                 if not t.done() and t != asyncio.current_task()]
        for task in tasks:
            task.cancel()
        
        # Wait for all tasks to complete cancellation
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    # Schedule cleanup in the loop
    future = asyncio.run_coroutine_threadsafe(cleanup(), ASYNC_LOOP)
    
    try:
        future.result(timeout=5)  # Wait up to 5 seconds for cleanup
    except Exception as e:
        print(f"Cleanup error: {e}")
    finally:
        # Stop the loop
        ASYNC_LOOP.call_soon_threadsafe(ASYNC_LOOP.stop)
        
        # Wait a moment for loop to stop
        time.sleep(0.5)
        
        # Close the loop
        try:
            ASYNC_LOOP.close()
        except:
            pass


# -----------------------------------------------------------
#     GUI APPLICATION
# -----------------------------------------------------------
class MainApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.setWindowTitle("webst")

        # -----------------------------
        #   System Tray
        # -----------------------------
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon(resource_path("icon.ico")))
        self.tray.setVisible(True)

        # Меню трея
        tray_menu = QMenu()

        show_action = QAction("Открыть", self)
        show_action.triggered.connect(self.show_window)
        tray_menu.addAction(show_action)

        quit_action = QAction("Выход", self)
        quit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(quit_action)

        self.tray.setContextMenu(tray_menu)

        # Двойной клик по иконке — открыть окно
        self.tray.activated.connect(self.on_tray_activated)

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
        self.obs_link.setText("http://localhost:5500/")

        self.load_avaters()
        self.load_microphoes()

    def show_window(self):
        self.show()
        self.activateWindow()

    def exit_app(self):
        """Properly exit the application"""
        print("[APP] Shutting down...")
        self.tray.setVisible(False)
        
        # Stop async servers before quitting
        stop_asyncio_servers()
        
        QApplication.quit()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()
    
    def closeEvent(self, event: QCloseEvent):
        event.ignore()
        self.hide()
        self.tray.showMessage(
            "Avatar UI",
            "Приложение свернуто в трей",
            QSystemTrayIcon.Information,
            2000
        )

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
        assets_path = resource_path("assets")
        for folder in os.listdir(assets_path):
            folder_path = os.path.join(assets_path, folder)
            if os.path.isdir(folder_path):
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
        load_avatar(STATE["avatar"])

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