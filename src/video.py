import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

class Video:

    def __init__(self, video_id):
        self.video_id = video_id
        self.video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                              id=video_id
                              ).execute()

        self.video_title: str = self.video_response['items'][0]['snippet']['title']
        self.url = self.video_response["items"][0]["snippet"]["thumbnails"]["high"]["url"]
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']


    def __str__(self):
        return f"{self.video_title}"


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
