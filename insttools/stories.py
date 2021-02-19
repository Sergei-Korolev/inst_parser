import requests
import json


def get_json_with_story(profile_id, cookie):
    """Takes profile_id and cookie. Then writes .json with stories"""
    headers_for_stories = {
        'authority': 'i.instagram.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'accept': '*/*',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
        'x-ig-app-id': '936619743392459',
        'origin': 'https://www.instagram.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.instagram.com/',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': cookie
}

    params_for_stories = (('reel_ids', f'{profile_id}'),)
    response = requests.get('https://i.instagram.com/api/v1/feed/reels_media/',
                            headers=headers_for_stories,
                            params=params_for_stories)
    with open('jsons/story.json', 'w') as f:
            json.dump(response.json(), f, indent=2)


def parse_json_story():
    """Parses .json with stories and writes new .json with url of stories"""
    all_stories = []
    with open('jsons/story.json') as f:
        reels_media = json.load(f)
    for reels in reels_media['reels_media']:
        for item in reels['items']:
            if 'video_versions' in item:
                all_stories.append(item['video_versions'][-1]['url'])
            else:
                all_stories.append(item['image_versions2']['candidates'][0]['url'])
    with open('jsons/bin/all_stories.json', 'w') as f:
        json.dump(all_stories, f, indent=2)


def download_stories(folder_name):
    """Takes folder_name to download into it stories"""
    count_of_download_stories = 0
    with open('jsons/bin/all_stories.json') as f:
        all_stories = json.load(f)
    print('Trying to download stories')
    for url in all_stories:
        media = requests.get(url)
        name = url[url.rfind('/')+1:url.find('?')]
        with open(f'media/{folder_name}/stories/{name}', 'wb') as f:
            f.write(media.content)
        count_of_download_stories += 1
        print(f'Downloaded {count_of_download_stories}/{len(all_stories)}')
