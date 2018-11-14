import re

import requests

SID = ''

r = requests.get('http://www.yupoo.com/account/', allow_redirects=False, cookies={
    'sid': SID,
})

if r.status_code != 200:
    print('wrong SID')
    exit()

api_regex = re.search(r',apiKey: \'(.+)\',apiSecret:.+,user: {id: (\d+),username:', r.text)
if api_regex is None:
    print('no KEY and UID')
    exit()

API = api_regex.group(1)
UID = api_regex.group(2)


def get_photo_url(pid):
    r = requests.get('http://www.yupoo.com/api/rest/', params={
        'format': 'json',
        'api_key': API,
        'ypp': 1,
        'method': 'yupoo.photos.getInfo',
        'photo_id': pid,
    }, cookies={
        'sid': SID,
    })

    data = r.json()

    if data['stat'] == 'ok':
        photo = data['photo']
        url = 'http://photo.yupoo.com/' + \
              photo['bucket'] + '/' + photo['key'] + '/' + photo['secret'] + '.' + photo['originalformat']
        title = photo['title'] + '.' + photo['originalformat']
    else:
        print('# API stat:', data['stat'])
        url = title = ''

    return url, title


r = requests.get('http://www.yupoo.com/api/rest/', params={
    'format': 'json',
    'api_key': API,
    'ypp': 1,
    'method': 'yupoo.albums.getList',
    'user_id': UID,
}, cookies={
    'sid': SID,
})

data = r.json()

if data['stat'] == 'ok':
    for album in data['albums']:
        print('#', album['title'], album['photos'])

        r = requests.get('http://www.yupoo.com/api/rest/', params={
            'format': 'json',
            'api_key': API,
            'ypp': 1,
            'method': 'yupoo.albums.getPhotos',
            'album_id': album['id'],
        }, cookies={
            'sid': SID,
        })

        data = r.json()

        if data['stat'] == 'ok':
            for photo in data['album']['photos']:
                url, fn = get_photo_url(photo['id'])
                print(url)
                print('  out=' + album['title'] + '/' + fn)
        else:
            print('# API stat:', + data['stat'])

else:
    print('# API stat:', data['stat'])

