import os
import asyncio
import json

from datetime import date, datetime

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel

from telethon.tl.types import MessageMediaWebPage

class DateTimeEncoder(json.JSONEncoder):
  def default(self, o): # pylint: disable=E0202
    if isinstance(o, datetime):
      return o.isoformat()

    if isinstance(o, bytes):
      return list(o)

    return json.JSONEncoder.default(self, o)

async def get_message_urls(channel_name):
  api_id = os.environ['TELEGRAM_API_ID']
  api_hash = os.environ['TELEGRAM_API_HASH']

  client = TelegramClient('anon', api_id, api_hash)

  messages = list()
  urls = list()

  async with client:
    channel = await client.get_entity(f'https://t.me/{channel_name}')
    history = await client(GetHistoryRequest(
        peer=channel,
        offset_id=0,
        offset_date=None,
        add_offset=0,
        limit=10,
        max_id=0,
        min_id=0,
        hash=0
    ))

    if not history.messages:
      return
    else:
      for message in history.messages:
        if not message.media or not isinstance(message.media, MessageMediaWebPage):
          continue
        messages.append(message.to_dict())
        urls.append(message.media.webpage.url)

  # with open('messages.json', 'w') as file:
  #   json.dump(messages, file, ensure_ascii=False, indent=2, sort_keys=True, cls=DateTimeEncoder)

  return urls
