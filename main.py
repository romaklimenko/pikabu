import asyncio
import json
import os

from pikabu.chat import get_message_urls
from pikabu.db import can_publish, save
from pikabu.dirty import publish_post, get_image_source, get_video_block
from pikabu.pikabu import get_post_data

async def main():
  urls = await get_message_urls(os.environ['TELEGRAM_CHANNEL_NAME'])
  for url in urls:
    if '/story/' in url:
      continue
    if can_publish(url):
      print(f'URL: {url}')
      try:
        save(url)
        post_data = get_post_data(url)
        if post_data != None:
          print(publish_post(post_data))
      except Exception as e:
        print(e)
      break

  # src = 'https://cs9.pikabu.ru/post_img/2020/05/16/5/1589608996140783793.png'
  # block = get_image_source(src)
  # print(block)

  # src = 'https://www.youtube.com/watch?v=aYz_BBSrr8w'
  # block = get_video_block(src)

  # print(block)

  # post = get_post_data('https://pikabu.ru/story/zabludilis_7446074')
  # publish_post(post)

  # with open('post.json', 'w') as file:
  #   json.dump(blocks, file, ensure_ascii=False, indent=2, sort_keys=True)

asyncio.get_event_loop().run_until_complete(main())
