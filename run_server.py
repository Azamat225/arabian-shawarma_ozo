#!/usr/bin/env python3
"""
🌯 Сервер для запуска приложения "Арабская шаурма" (PWA)
Запуск: python run_server.py
"""
import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path
import threading

PORT = 8029
HOST = "localhost"

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """Тихий обработчик: не спамит логами в консоль при каждом запросе"""
    def log_message(self, format, *args):
        pass

def open_browser():
    webbrowser.open(f"http://{HOST}:{PORT}")

def main():
    # Переходим в папку, где лежит этот скрипт
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)

    # Проверяем наличие главного файла
    if not Path("index.html").exists():
        print("❌ Ошибка: файл index.html не найден!")
        print("💡 Положите этот скрипт в папку с файлами приложения (рядом с index.html, manifest.json, sw.js)")
        sys.exit(1)

    # Разрешаем повторное использование порта (избегаем ошибки при быстром перезапуске)
    socketserver.TCPServer.allow_reuse_address = True

    try:
        with socketserver.TCPServer((HOST, PORT), QuietHandler) as httpd:
            print("\n🌯 " + "="*45)
            print(f"✅ Сервер запущен: \033[92mhttp://{HOST}:{PORT}\033[0m")
            print(f"📁 Папка проекта: {script_dir}")
            print("💡 Чтобы остановить сервер, нажмите Ctrl+C")
            print("="*45 + "\n")

            # Открываем браузер в отдельном потоке, чтобы сервер не блокировался
            threading.Thread(target=open_browser, daemon=True).start()

            # Запускаем бесконечное ожидание запросов
            httpd.serve_forever()
    except OSError as e:
        if e.errno in (98, 10048):  # 98 = Linux/Mac, 10048 = Windows
            print(f"❌ Порт {PORT} уже занят. Закройте другое приложение или измените переменную PORT в скрипте.")
        else:
            raise
    except KeyboardInterrupt:
        print("\n👋 Сервер остановлен. До встречи!")

if __name__ == "__main__":
    main()