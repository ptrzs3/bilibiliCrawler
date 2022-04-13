from utils import request
from utils import filename_check


class BiliBili:
    def __init__(self, bvid: str = None):
        self.__bvid = bvid
        self.__aid = self.bvid2aid()

    def bvid2aid(self):
        table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        tr = {}
        for i in range(58):
            tr[table[i]] = i
        s = [11, 10, 3, 8, 4, 6]
        xor = 177451812
        add = 8728348608

        def dec(x):
            r = 0
            for i in range(6):
                r = tr[x[s[i]]] * 58 ** i
            return (r - add) ^ xor

        return dec(self.__bvid)

    async def get_video_info(self):
        info = await self.get_video_detail()
        cid = info["pages"][0]["cid"]
        url = "https://api.bilibili.com/x/player/playurl"
        params = {
            "avid": self.__aid,
            "cid": cid,
            "qn": "120",
            "otype": "json",
            "fnval": 16,
            "fourk": 1
        }
        avUrl = await request("GET", url, params=params)

        video_info = list()

        video_url = avUrl["dash"]["video"][0]['baseUrl']
        audio_url = avUrl["dash"]["audio"][0]['baseUrl']
        title = info["title"]
        title = filename_check(title)

        video_info.append(title)
        video_info.append(video_url)
        video_info.append(audio_url)
        return video_info

    async def get_video_detail(self):
        url = "https://api.bilibili.com/x/web-interface/view"
        params = {
            "aid": self.__aid
        }
        response = await request("GET", url, params=params)
        return response