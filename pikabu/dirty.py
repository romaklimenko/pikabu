import json
import os
import requests

def get_headers():
  return {
      'X-Futuware-UID': os.environ['D3_UID'],
      'X-Futuware-SID': os.environ['D3_SID'],
      'Content-Type': 'application/json'
  }

def publish_post(domain, post_data):
  print('publishing the post')

  data = None

  if len(list(filter(lambda block: block['type'] == 'image' or block['type'] == 'video', post_data['blocks']))) > 1:
    data = data_article(post_data)
  else:
    data = data_link(post_data)

  print(data)

  draft_response = requests.post('https://d3.ru/api/drafts/', headers=get_headers(), json=data)

  draft = draft_response.json()

  draft_id = draft['id']

  response = requests.post(f'https://d3.ru/api/drafts/{draft_id}/publish/?domain_prefix={domain}', headers=get_headers())

  result = response.json()

  return result

def data_article(post_data):
  data = {
    'data': {
      'title': post_data['title'],
      'type': 'article',
      'blocks': [
        {
          'type': 'text',
          'text': post_data['url']
        }
      ]
    },
    'tags': post_data['tags']
  }

  for block in post_data['blocks']:
    if block['type'] == 'text':
      data['data']['blocks'].append({
        'type': 'text',
        'text': block['text']
      })
    elif block['type'] == 'image':
      data['data']['blocks'].append({
        'type': 'image',
        'align': 'center',
        'url': get_image_source(block['src'])
      })
    elif block['type'] == 'video' and not 'pikabu.ru/video' in block['src']:
      data['data']['blocks'].append(get_video_block(block['src']))

  return data

def data_link(post_data):
  data = {
        'data': {
            'type': 'link',
            'title': post_data['title']
        },
        'tags': post_data['tags']
    }

  for block in post_data['blocks']:
    if block['type'] == 'image' or block['type'] == 'video' and not 'link' in data['data']:
      if block['type'] == 'image':
        data['data']['link'] = {
          'url': post_data["url"]
        }
        data['data']['media'] = {
          'url': get_image_source(block['src'])
        }
      else:
        data['data']['link'] = {
          'url': block['src']
        }
    elif block['type'] == 'text' and not 'text' in data['data']:
      data['data']['text'] = block['text'] + f'\n{post_data["url"]}'

  if not 'text' in data['data']:
    data['data']['text'] = post_data["url"]

  return data

def get_image_source(src):
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': f'uid={os.environ["D3_UID"]}; sid={os.environ["D3_SID"]};'
  }

  data = {
    'url': src,
    'csrf_token': os.environ['D3_CSRF']
  }

  response = requests.post('https://d3.ru/ajax/urls/info/', headers=headers, data=data).json()

  if response['status'] == 'OK':
    return response['stored_location']
  else:
    return None

def get_video_block(src):
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': f'uid={os.environ["D3_UID"]}; sid={os.environ["D3_SID"]};'
  }

  data = {
    'url': src,
    'csrf_token': os.environ['D3_CSRF']
  }

  response = requests.post('https://d3.ru/ajax/urls/video/info/', headers=headers, data=data).json()

  return {
    'align': 'center',
    'type': 'embed',
    'url': response['url']['url'],
    'embed': {
      'provider': response['media_provider'],
      'id': response['media_provider_id']
    }
  }