import requests
import json
import glob


from time import sleep


def get_json(profile_id, batch_size, headers):
    """Takes profile_id, batch_size and headers to
    write .json with all data of profile
    """
    index = 1
    after = None
    photo_in_progress = 0
    profile_id = profile_id
    all_media = 0
    while True:
        after_value = f',"after":"{after}"' if after else ''
        variables = f'{{"id":"{profile_id}","first":{str(batch_size)}{after_value}}}'
        params = {
            'query_hash': '003056d32c2554def87228bc3fd9668a',
            'variables': variables
        }
        response = requests.get('https://www.instagram.com/graphql/query/', headers=headers, params=params)
        if response.status_code == 200:
            print(f"{response.status_code} - good answer")
            data = response.json()
            with open(f'jsons/{index}.json', 'w') as f:
                json.dump(data, f, indent=2)
        else:
            print(f"{response.status_code} - bad answer")
            print('Close -_-')
            exit()
        with open(f'jsons/{index}.json', 'r') as f:
            data = json.load(f)
        all_media = data['data']['user']['edge_owner_to_timeline_media']['count']
        if not data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']:
            break
        after = data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        in_current_batch = len(data['data']['user']['edge_owner_to_timeline_media']['edges'])
        photo_in_progress += in_current_batch
        print(f'Processed {photo_in_progress}/{all_media}')
        sleep(4 if index % 10 != 0 else 8)
        index += 1
    print(f'Processed {all_media}/{all_media}')


def parse_jsons_files():
    """Parses .json with all data of profile and
    writes new .json with url of media

    """
    files = glob.glob('jsons/*.json')
    all_media = []
    for f in files:
        with open(f, 'r') as f:
            data = json.load(f)
            for edge in data['data']['user']['edge_owner_to_timeline_media']['edges']:
                if edge['node']['__typename'] == 'GraphImage':
                    all_media.append(edge['node']['display_url'])
                elif edge['node']['__typename'] == 'GraphSidecar':
                    for item in edge['node']['edge_sidecar_to_children']['edges']:
                        if item['node']['is_video']:
                            all_media.append(item['node']['video_url'])
                        else:
                            all_media.append(item['node']['display_url'])
                elif edge['node']['__typename'] == 'GraphVideo':
                    all_media.append(edge['node']['video_url'])
    with open('jsons/bin/all_media.json', 'w') as f:
        json.dump(all_media, f, indent=2)
    print('Got links of media')


def download_media(folder_name):
    """Takes folder_name to download into it media"""
    count_of_download_media = 0
    with open('jsons/bin/all_media.json') as f:
        data = json.load(f)
    print('Trying to download media')
    for media in data:
        item = requests.get(media)
        name = media[media.rfind('/') + 1:media.find('?')]
        with open(f'media/{folder_name}/{name}', 'wb') as d:
            d.write(item.content)
        count_of_download_media += 1
        print(f'Downloaded {count_of_download_media}/{len(data)}')
