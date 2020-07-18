import json
import os
import sys

from pikabu.dirty import publish_post, get_image_source, get_video_block
from pikabu.pikabu import get_post_data

domain = sys.argv[1]
url = sys.argv[2]
print(f'domain: {domain}, url: {url}')

post_data = get_post_data(url)

if len(post_data) > 0:
  print(publish_post(domain, post_data))