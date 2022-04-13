import aiohttp
import json
import asyncio
import atexit
import re
__session_pool = {}


@atexit.register
def __clean():
    loop = asyncio.get_event_loop()

    async def __clean_task():
        await __session_pool[loop].close()

    if loop.is_closed():
        loop.run_until_complete(__clean_task())
    else:
        loop.create_task(__clean_task())


async def request(method: str, url: str, params: dict = None):
    method = method.upper()
    DEFAULT_HEADERS = {
        "Referer": "https://www.bilibili.com",
        "User-Agent": "Mozilla/5.0"
    }
    headers = DEFAULT_HEADERS
    config = {
        "method": method,
        "url": url,
        "params": params,
        "headers": headers
    }
    session = get_session()

    async with session.request(**config) as resp:
        raw_data = await resp.text()
        resp_data = json.loads(raw_data)
        real_data = resp_data.get("data", None)
        if real_data is None:
            real_data = resp_data.get("result", None)
        return real_data


def get_session():
    loop = asyncio.get_event_loop()
    session = __session_pool.get(loop, None)
    if session is None:
        session = aiohttp.ClientSession(loop=loop)
        __session_pool[loop] = session
    return session


def filename_check(filename : str):
    pattern = re.compile(r'[^\u4e00-\u9fa5a-zA-Z0-9]')
    chinese = re.sub(pattern, '', filename)
    return chinese