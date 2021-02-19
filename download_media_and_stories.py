import os
import json
import requests
import glob
import config


from bs4 import BeautifulSoup
from insttools import media, stories, login


def jsons_foldes():
    """Creates folders for download data files"""
    if not os.path.exists('jsons'):
        os.makedirs('jsons')
    if not os.path.exists('jsons/bin'):
        os.makedirs('jsons/bin')
    if not os.path.exists('media'):
        os.makedirs('media')
    files = glob.glob('jsons/*.json')
    if files:
        for f in files:
            os.remove(f)
    if not os.path.exists('jsons/bin/profiles_id.json'):
        with open('jsons/bin/profiles_id.json', 'w') as f:
            json.dump({}, f)


def get_id(PROFILE, headers):
    """Parse instagram.com/PROFILE page and returns PROFILE id"""
    with open('jsons/bin/profiles_id.json') as f:
        profiles_id = json.load(f)
    if config.PROFILE in profiles_id:
        print(f'{config.PROFILE} -', profiles_id[f'{config.PROFILE}'])
        return profiles_id[f'{config.PROFILE}']
    url = 'http://www.instagram.com/' + config.PROFILE + '/'
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    script = soup.find_all('script', type="text/javascript")[3]
    #print(script)
    data = str(script)
    profile_id = data[data.find('[{"logging_page_id":"profilePage_') +
                 len('[{"logging_page_id":"profilePage_'):data.find('","show_suggested_profiles"')]
    try:
        profiles_id[f'{config.PROFILE}'] = int(profile_id)
    except:
        print('Try to update cookies or check nickname(PROFILE)')
        exit()
    print(f'{config.PROFILE} -', profile_id)
    with open('jsons/bin/profiles_id.json', 'w') as f:
        json.dump(profiles_id, f, indent=2)
    return int(profile_id)


def makedirs(PROFILE):
    """Creates folders with PROFILE name and return folder_name"""
    symbols = r'/:*?\<>"|+!@%.'
    folder_name = config.PROFILE
    for s in symbols:
        while s in folder_name:
            folder_name = config.PROFILE.replace(s, '_')
    if not os.path.exists(f'media/{folder_name}'):
        os.makedirs(f'media/{folder_name}')
    if not os.path.exists(f'media/{folder_name}/stories'):
        os.makedirs(f'media/{folder_name}/stories')
    return folder_name


def main():
    try:
        jsons_foldes()

        if config.NEW_COOKIE:
            login.write_cookies_json(config.USERNAME, config.PASSWORD)

        cookie, x_csrftoken = login.get_cookies()
        headers = {
            'authority': 'www.instagram.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'dnt': '1',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'x-csrftoken': x_csrftoken,
            'x-ig-app-id': '936619743392459',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'https://www.instagram.com/{config.PROFILE}/',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': cookie,
        }

        profile_id = get_id(config.PROFILE, headers)
        folder_name = makedirs(config.PROFILE)

        if config.MEDIA_DOWNLOAD:
            media.get_json(profile_id, config.BATCH_SIZE, headers)
            media.parse_jsons_files()
            media.download_media(folder_name)

        if config.STORIES_DOWNLOAD:
            stories.get_json_with_story(profile_id, cookie)
            stories.parse_json_story()
            stories.download_stories(folder_name)

        print('Done')

    except Exception as e:
        print(e)
        print('Something wrong')
    
    


if __name__ == '__main__':
    main()
