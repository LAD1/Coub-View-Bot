from colorama import Fore
import threading
import httpx
import time
import os

proxies = []
total_views = 0
total_fails = 0
proxy_timeout = None

threads = 50 # increase or decrease the amount of threads
coub_id = "https://coub.com/view/2va486"

if "https://coub.com/view/" in coub_id:
    coub_id = coub_id.split("/")[-1]
    print(f"{Fore.CYAN}Using coub id: {coub_id}", Fore.GREEN)

def title():
    os.system(f'title "Total Views : {total_views} | Total Fails: {total_fails}"')

def get_proxy_format(proxy):
    if "@" in proxy:
        return proxy
    elif len(proxy.split(":")) == 2:
        return proxy
    else:
        if "." in proxy.split(":")[0]:
            return ":".join(proxy.split(":")[2:]) + "@" + ":".join(proxy.split(":")[:2])
        else:
            return ":".join(proxy.split(":")[:2]) + "@" + ":".join(proxy.split(":")[2:])

def get_proxy():
    if len(proxies) == 0:
        print("No Proxies", Fore.RED)
    raw = proxies[0]
    prx = get_proxy_format(proxies[0])
    proxy = "http://" + prx
    proxies.append(proxies[0])
    proxies.pop(0)
    print(f"{Fore.CYAN}Using proxy: {raw}", Fore.GREEN)
    return proxy

def main():
    global total_views
    global total_fails
    proxy = get_proxy()
    try:
        while True:
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
            r = httpx.post(f"https://coub.com/coubs/{coub_id}/increment_views?player=html5&type=site&platform=desktop",proxies=proxy, headers=headers, timeout=proxy_timeout)
            if r.status_code == 200:
                print(f"{Fore.CYAN}[X] {Fore.GREEN}Successfully added view: {Fore.YELLOW}{proxy}", Fore.GREEN)
                total_views += 1
                title()
            else:
                print(f"{Fore.CYAN}[X] {Fore.RED}Failed to add view: {Fore.YELLOW}{proxy}", Fore.RED)
                total_fails += 1
                title()
                main()
    except Exception as e:
        print(f"{Fore.CYAN}[X] {Fore.RED}Failed to add view: {Fore.YELLOW}{proxy}", Fore.RED)
        total_fails += 1
        title()
        main()

def refresh_proxies():
    global proxies
    r = httpx.get(f'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all')
    proxies = r.text.splitlines()
    print(f'{Fore.GREEN}Grabbed {len(proxies)} proxies!')
    time.sleep(1)
refresh_proxies()

for i in range(threads):
    thread = threading.Thread(target=main)
    thread.start()
