import bilibili
import aiohttp
import os


async def download_by_id(video_id, save_path):
    v = bilibili.BiliBili(bvid=video_id)
    video_info = await v.get_video_info()
    title = video_info[0]
    video_file_name = title +'.mp4'
    video_file_name = os.path.join(save_path, video_file_name)
    if not os.path.exists(video_file_name):
        video_url = video_info[1]
        audio_url = video_info[2]
        HEADERS = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.bilibili.com/"
        }
        async with aiohttp.ClientSession() as sess:
            async with sess.get(video_url, headers=HEADERS) as resp:
                length = resp.headers.get('content-length')
                with open('video_temp.m4s', 'wb') as f:
                    process = 0
                    while True:
                        chunk = await resp.content.read(1024)
                        if not chunk:
                            break

                        process = len(chunk)
                        print(f'下载进度 {process} / {length}')
                        f.write(chunk)

            async with sess.get(audio_url, headers=HEADERS) as resp:
                length = resp.headers.get('content-length')

                with open('audio_temp.m4s', 'wb') as f:
                    process = 0
                    while True:
                        chunk = await resp.content.read(1024)
                        if not chunk:
                            break

                        process = len(chunk)
                        print(f'下载进度 {process} / {length}')
                        f.write(chunk)

            print('混流中')
            os.system('ffmpeg -i video_temp.m4s -i audio_temp.m4s -vcodec copy -acodec copy \"%s\"' % video_file_name)

            os.remove('video_temp.m4s')
            os.remove('audio_temp.m4s')

            print('下载完成%s' % video_file_name)
    else:
        print("exists")