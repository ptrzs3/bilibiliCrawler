import requests
import urllib3
import json
import sys
from bili_download import download_by_id
import asyncio
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
interface = 'https://api.bilibili.com/x/web-interface/search/type'

try:
    keyword = sys.argv[1]
except IndexError:
    print("index error")
    exit(0)
video_dir = "videoSrc"
save_path = os.path.join(os.path.dirname(__file__), video_dir)
save_path = os.path.join(save_path, keyword)
for i in range(1):
    params = {
        'keyword': keyword,
        'search_type': 'video',
        'page': str(i+1),
        'order': 'click',
        'duration': '1'
    }
    f = requests.get(url=interface, verify=False, params=params).text
    contents = f.encode(encoding='utf-8')
    jsonObject = json.loads(contents)
    video_list = jsonObject['data']['result']
    print(len(video_list))
    it = iter(video_list)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for x in it:
        asyncio.get_event_loop().run_until_complete(download_by_id(x['bvid'], save_path))