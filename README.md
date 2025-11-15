
# Building for windows

```
pyinstaller main.py --noconfirm --onedir --add-data "assets;assets" --add-data "index.html;." --add-data "config.json;." --add-data "icon.ico;." --add-data "lib/windows/amd64/libpv_recorder.dll;pvrecorder/lib/windows/amd64/" --icon ./icon.ico --name AvatarApp --windowed   
```