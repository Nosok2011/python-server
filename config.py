stop_hotkey = "ctrl+c"
addr = "0.0.0.0" # менять можно, но лучше не надо
port = 8000
sock_buff_size = 1024
http_codes = { # вообще не надо менять
    200: "200 OK",
    403: "403 Forbidden",
    404: "404 Not Found",
    500: "500 Internal Server Error"
}
get_header = lambda code: f"HTTP/1.1 {http_codes[code]}\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
get_header_encoded = lambda code: get_header(code).encode()
htdocs = "htdocs"
index = "index.html"