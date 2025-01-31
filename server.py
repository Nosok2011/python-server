from socket import create_server, gethostbyname_ex, gethostname
import config
from keyboard import add_hotkey
from threading import Thread
from os import kill, getpid, access, R_OK, listdir
from os.path import exists, isdir
from signal import SIGTERM
def stop_server():
    print("Остановка сервера")
    global stop
    stop = True
    kill(getpid(), SIGTERM)
def get_page(request):
    query = request.split(" ")[1]
    path = config.htdocs + query
    if not exists(path):
        return config.get_header_encoded(404) + open("service/404.html", encoding="UTF-8").read().replace("{query}", query).encode()
    if not access(path, R_OK):
        return config.get_header_encoded(403) + open("service/403.html", encoding="UTF-8").read().replace("{query}", query).encode()
    if not isdir(path):
        response = open(path, "rb").read()
    elif config.index in listdir(path):
        response = open(f"{path}{"" if query.endswith("/") else "/"}{config.index}", "rb").read()
    else:
        list_of_files = [f"<li><a href=\".{query}{"" if query.endswith("/") else "/"}{file}\">{file}</a></li>" for file in listdir(path)]
        response = open("service/list.html", encoding="UTF-8").read().replace("{dir}", query).replace("{files}", "".join(list_of_files)).encode()
    return config.get_header_encoded(200) + response
def handle_connection():
    while not stop:
        try:
            client, addr = server.accept()
            print(f"Новый запрос от {addr[0]}:{addr[1]}")
            data = client.recv(config.sock_buff_size).decode()
            if not data:
                continue
            print(data)
            content = get_page(data)
            client.sendall(content)
        except Exception as e:
            err_desc = f"{type(e).__name__}: {e}"
            print(err_desc)
            client.sendall(config.get_header_encoded(500) + open("service/500.html", encoding="UTF-8").read().replace("{err_desc}", err_desc).encode())
    server.close()
list_to_str = lambda a: "; ".join(a)
add_hotkey(config.stop_hotkey, stop_server)
print("Запуск сервера")
stop = False
server = create_server((config.addr, config.port))
host, alias, addr_list = gethostbyname_ex(gethostname())
print("Сервер запущен")
print(f"Для остановки нажать {config.stop_hotkey.upper()}")
print(f"Имя хоста: {host}")
print(f"Алиасы: {list_to_str(alias)}")
print(f"Адреса для доступа к серверу: {list_to_str([f"{addr}:{config.port}" for addr in addr_list])}")
handler = Thread(target=handle_connection)
handler.start()