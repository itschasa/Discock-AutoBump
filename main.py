import httpx, time

# only change this if you want bright to get mad at you
timeout = 1800

# login stuff for discock
email = ""
password = ""

# post id
# found in url of post:
# https://discock.app/d/(post id)-(title)
postid = ""


def login(email, pswd, proxied, session, csrf):
    hdrs = {
        "accept": '*/*',
        "accept-encoding": 'gzip, deflate, br',
        "accept-language": 'en-US,en;q=0.9',
        "content-type": 'application/json; charset=UTF-8',
        "cookie": f'__proxied={proxied}; flarum_session={session}',
        "origin": 'https://discock.app',
        "referer": 'https://discock.app/',
        "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": '?0',
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": 'empty',
        "sec-fetch-mode": 'cors',
        "sec-fetch-site": 'same-origin',
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'x-csrf-token': csrf
    }
    
    r = httpx.post("https://discock.app/login", headers=hdrs,
        json={
            "identification": email,
            "password": pswd,
            "remember": True
        },
        cookies = {
            "__proxied": proxied
        }
    )
    open("test", "w").write(r.text)

    print(r.status_code)
    if r.status_code == 200:
        return r.cookies['flarum_remember'], r.cookies['flarum_session'], r.headers['x-csrf-token']



def fetch_proxied_cookie():
    hdrs = {
        "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        "accept-encoding": 'gzip, deflate, br',
        "accept-language": 'en-US,en;q=0.9',
        "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": '?0',
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": 'empty',
        "sec-fetch-mode": 'navigate',
        "sec-fetch-site": 'none',
        "sec-fetch-user": '?1',
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = httpx.get("https://discock.app", follow_redirects=False, headers=hdrs)
    print(r.status_code)
    print(r.cookies)
    if r.status_code == 307:
        proxied = r.cookies['__proxied']
        return proxied

def fetch_session(proxied):
    hdrs = {
        "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        "accept-encoding": 'gzip, deflate, br',
        "accept-language": 'en-US,en;q=0.9',
        "cookie": f"__proxied={proxied}",
        "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": '?0',
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": 'empty',
        "sec-fetch-mode": 'navigate',
        "sec-fetch-site": 'none',
        "sec-fetch-user": '?1',
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = httpx.get("https://discock.app", follow_redirects=False, headers=hdrs)
    print(r.status_code)
    print(r.cookies)
    if r.status_code == 200:
        session = r.cookies['flarum_session']
        return session, r.headers['x-csrf-token']
    

def bump(post_id, remember, session, proxied, csrf):
    payload = {
        "data": {
            "type": "posts",
            "attributes": {
                "content": "auto-bump!"
            },
            "relationships": {
                "discussion": {
                    "data": {
                    "type": "discussions",
                    "id": post_id
                }
                }
            }
        }
    }

    hdrs = {
        "accept": '*/*',
        "accept-encoding": 'gzip, deflate, br',
        "accept-language": 'en-US,en;q=0.9',
        "content-type": 'application/json; charset=UTF-8',
        "cookie": f'flarum_remember={remember}; __proxied={proxied}; flarum_session={session}',
        "origin": 'https://discock.app',
        "referer": 'https://discock.app/d/82-a-guide-to-use-the-forum/2',
        "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": '?0',
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": 'empty',
        "sec-fetch-mode": 'cors',
        "sec-fetch-site": 'same-origin',
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'x-csrf-token': csrf
    }

    r = httpx.post("https://discock.app/api/posts", headers=hdrs, json=payload)
    print(r.text)
    print(r.status_code)
    if r.status_code == 201:
        print("auto bumped!")
    else:
        print(f"failed to auto-bump")


while True:
    proxied = fetch_proxied_cookie()
    session, csrf = fetch_session(proxied)
    remember, session,csrf = login(email, password, proxied, session, csrf)
    bump(postid, remember, session, proxied, csrf
    time.sleep(timeout)
