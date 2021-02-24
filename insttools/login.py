import json


from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def write_cookies_json(username, password):
    '''Takes username and password to write cookies'''
    data = {}
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(5)
    try:
        browser.get('https://www.instagram.com')

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)

        sleep(2)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)

        sleep(3)

        try:
            browser.get(f'https://www.instagram.com/{username}/')

        except Exception as ex:
            print(ex)
            browser.close()
            browser.quit()

        cookies = list(browser.get_cookies())

        browser.close()
        browser.quit()

    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()

    for cookie in cookies:
        data[cookie['name']] = cookie['value']

    with open('jsons/bin/cookies.json', 'w') as f:
        json.dump(data, f, indent=2)


def get_cookies():
    """Generate cookies for requests.
    Return tuple: (cookie for headers, csrftoken)

    """
    cookie = ''
    with open('jsons/bin/cookies.json') as f:
        cookies = json.load(f)
    for i in cookies:
        cookie += f'{i}={cookies[i]}; '
    return cookie, cookies['csrftoken']
