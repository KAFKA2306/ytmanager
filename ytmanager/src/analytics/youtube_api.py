from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from typing import Dict, List


class YouTubeAPI:
    def __init__(self, credentials_path: str):
        self.credentials = Credentials.from_authorized_user_file(credentials_path)
        self.youtube = build("youtube", "v3", credentials=self.credentials)
        self.youtube_analytics = build("youtubeAnalytics", "v2", credentials=self.credentials)

    def get_channel_videos(self, channel_id: str, max_results: int = 50) -> List[Dict]:
        request = self.youtube.search().list(
            part="id,snippet",
            channelId=channel_id,
            maxResults=max_results,
            order="date",
            type="video"
        )
        response = request.execute()
        return response.get("items", [])

    def get_video_analytics(self, video_id: str, start_date: datetime, end_date: datetime) -> Dict:
        request = self.youtube_analytics.reports().query(
            ids=f"channel==MINE",
            startDate=start_date.strftime("%Y-%m-%d"),
            endDate=end_date.strftime("%Y-%m-%d"),
            metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,likes,comments,shares",
            dimensions="video",
            filters=f"video=={video_id}"
        )
        response = request.execute()
        return response

    def get_channel_analytics(self, channel_id: str, lookback_days: int = 7) -> Dict:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_days)
        request = self.youtube_analytics.reports().query(
            ids=f"channel=={channel_id}",
            startDate=start_date.strftime("%Y-%m-%d"),
            endDate=end_date.strftime("%Y-%m-%d"),
            metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,likes,comments,shares,subscribersGained,subscribersLost",
            dimensions="day"
        )
        response = request.execute()
        return response
