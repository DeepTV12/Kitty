import requests
import json
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def read_query_ids(filename="datas.txt"):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]

def display_logo():
    console.print(Panel.fit(
        "[bold cyan] ██████████                               ███████████ █████   █████ ████   ████████ [/]\n"
        "[bold cyan]░░███░░░░███                             ░█░░░███░░░█░░███   ░░███ ░░███  ███░░░░███[/]\n"
        "[bold cyan] ░███   ░░███  ██████   ██████  ████████ ░   ░███  ░  ░███    ░███  ░███ ░░░    ░███[/]\n"
        "[bold cyan] ░███    ░███ ███░░███ ███░░███░░███░░███    ░███     ░███    ░███  ░███    ███████[/]\n"
        "[bold cyan] ░███    ░███░███████ ░███████  ░███ ░███    ░███     ░░███   ███   ░███   ███░░░░[/]\n"
        "[bold cyan] ░███    ███ ░███░░░  ░███░░░   ░███ ░███    ░███      ░░░█████░    ░███  ███      █[/]\n"
        "[bold cyan] ██████████  ░░██████ ░░██████  ░███████     █████       ░░███      █████░██████████[/]\n"
        "[bold cyan]░░░░░░░░░░    ░░░░░░   ░░░░░░   ░███░░░     ░░░░░         ░░░      ░░░░░ ░░░░░░░░░░[/]\n"
        "\n[bold yellow]© DeepTV | Telegram: [blue]https://t.me/DeepTV12[/][/]"
    ))

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def watermark(text, status="INFO", color="white"):
    timestamp = get_time()
    return f"[{timestamp}] [{status}] [bold {color}]{text}[/] [dim]— DeepTV12[/]"

def login(query_id):
    url = "https://kitty-api.bfp72q.com/api/login/tg"
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://kitty-web.bfp72q.com",
        "referer": "https://kitty-web.bfp72q.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    data = {
        "init_data": query_id,
        "referrer": ""
    }
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    return response_data.get("data", {}).get("token", {}).get("token")

def get_eggs(token):
    url = "https://kitty-api.bfp72q.com/api/scene/info"
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://kitty-web.bfp72q.com",
        "referer": "https://kitty-web.bfp72q.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    data = {"token": token}
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    eggs = []
    for i in range(9):
        try:
            eggs.extend(response_data.get("data", [])[i].get("eggs", []))
        except (IndexError, AttributeError):
            continue
    return [egg.get("uid") for egg in eggs]

def claim_egg_reward(token, egg_uid):
    url = "https://kitty-api.bfp72q.com/api/scene/egg/reward"
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://kitty-web.bfp72q.com",
        "referer": "https://kitty-web.bfp72q.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    data = {"token": token, "egg_uid": egg_uid}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def main():
    query_ids = read_query_ids()
    for query_id in query_ids:
        token = login(query_id)
        console.print(watermark("logging in account with id : ", "INFO", "yellow"))
        if not token:
            console.print(watermark("Failed to retrieve token.", "ERROR", "red"))
            return
        console.print(watermark("Token retrived", "SUCCESS", "green"))
        console.print(watermark("Getting eggs.", "INFO", "yellow"))
        eggs = get_eggs(token)
        console.print(watermark("Selling eggs.", "INFO", "yellow"))
        if not eggs:
            console.print(watermark("No eggs found.", "INFO", "yellow"))
            return
        
        for egg_uid in eggs:
            reward_response = claim_egg_reward(token, egg_uid)
            console.print(watermark(f"Egg {egg_uid}: {reward_response}", "SUCCESS", "green"))
        time.sleep(5)

if __name__ == "__main__":
    while True:
        try:
            display_logo()
            main()
            console.print(watermark("Sleeping for 3 minutes...", "INFO", "yellow"))
            time.sleep(180)
        except Exception as e:
            console.print(watermark(f"An error occurred: {e}", "ERROR", "red"))
