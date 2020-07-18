import json
import requests

from bs4 import BeautifulSoup

def get_post_data(url):
  print('getting the post blocks')

  headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'
  }

  response = requests.get(url, headers=headers)

  if not response.ok:
    print(response.status_code)
    print(response.text)
    return None

  post = {
    'url': url
  }

  soup = BeautifulSoup(response.text, 'html.parser')

  print(soup.title.string)

  post['title'] = soup.find('h1', class_='story__title').text

  story = soup.find('div', class_='page-story__story')

  tags = set()

  for tag in story.find_all('a', class_='tags__tag'):
    if tag.string != None and tag.string != '[моё]':
      tags.add(tag.string)

  post['tags'] = list(tags)

  blocks = list()

  for block in story.find_all('div', class_='story-block'):
    if 'story-block_type_text' in block['class']:
      # print('text: ...')
      blocks.append({
        'type': 'text',
        'text': str(block)
      })
      continue
    if 'story-block_type_image' in block['class']:
      try:
        src = block.find('img')['data-large-image']
        print(f'image: {src}')
        blocks.append({
          'type': 'image',
          'src': src
        })
      except Exception as exception:
        print(exception)

      continue
    if 'story-block_type_video' in block['class']:
      src = block.find('div', class_='player')['data-source']
      # print(f'video {src}')
      blocks.append({
        'type': 'video',
        'src': src
      })
      continue

  if len(blocks) == 0:
    return None

  post['blocks'] = blocks

  # with open('post.json', 'w') as file:
  #   json.dump(post, file, ensure_ascii=False, indent=2, sort_keys=True)

  return post