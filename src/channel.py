import json
import os
from googleapiclient.discovery import build

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey = api_key)


class Channel:
    """ Класс для ютуб-канала """


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.youtube = self.get_service().channels().list(id = self.channel_id, part = 'snippet,statistics').execute()
        self.title = self.youtube['items'][0]['snippet']['title']
        self.description = self.youtube["items"][0]["snippet"]["description"]
        self.url = self.youtube["items"][0]["snippet"]["thumbnails"]["high"]["url"]
        self.subscriber_count = int(self.youtube["items"][0]["statistics"]["subscriberCount"])
        self.video_count = self.youtube["items"][0]["statistics"]["videoCount"]
        self.view_count = self.youtube["items"][0]["statistics"]["viewCount"]
        self.data = {"title": self.title, "description": self.description,
"url": self.url,"subscriber_count": self.subscriber_count,
"video_count": self.video_count,"view_count": self.view_count}


    def __str__(self):
        return f"{self.title} ({self.url})"


    def __add__(self, other):
        return (self.subscriber_count + other.subscriber_count)


    def __sub__(self, other):
        return (self.subscriber_count - other.subscriber_count)


    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count


    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count


    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count


    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count


    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id = self.channel_id,
part = 'snippet,statistics').execute()
        print(json.dumps(channel, indent = 2, ensure_ascii = False))

    @classmethod
    def get_service(cls):
        """
        класс-метод, возвращающий объект для работы с YouTube API
        """
        api_key = os.getenv('API_key')
        return build("youtube", "v3", developerKey = api_key)


    def to_json(self, filename):
        """
        метод, сохраняющий в файл значения атрибутов экземпляра `Channel`
        """
        with open(filename, "w") as file:
            json.dump(self.youtube, file, indent = 2, ensure_ascii = False)

