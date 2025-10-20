from typing import Dict


class MetricsCalculator:
    @staticmethod
    def calculate_ctr(impressions: int, clicks: int) -> float:
        return clicks / impressions if impressions > 0 else 0.0

    @staticmethod
    def calculate_engagement_rate(views: int, likes: int, comments: int, shares: int) -> float:
        return (likes + comments + shares) / views if views > 0 else 0.0

    @staticmethod
    def calculate_watch_time_minutes(estimated_minutes_watched: int) -> int:
        return estimated_minutes_watched

    @staticmethod
    def calculate_average_view_duration_seconds(average_view_duration: float) -> float:
        return average_view_duration

    @staticmethod
    def calculate_retention_rate(average_view_percentage: float) -> float:
        return average_view_percentage / 100.0

    def calculate_all(self, analytics_data: Dict) -> Dict:
        metrics = {}
        rows = analytics_data.get("rows", [])
        if not rows:
            return metrics

        for row in rows:
            views = row[1]
            estimated_minutes_watched = row[2]
            average_view_duration = row[3]
            average_view_percentage = row[4]
            likes = row[5]
            comments = row[6]
            shares = row[7]

            metrics["watch_time"] = self.calculate_watch_time_minutes(estimated_minutes_watched)
            metrics["average_view_duration"] = self.calculate_average_view_duration_seconds(average_view_duration)
            metrics["engagement_rate"] = self.calculate_engagement_rate(views, likes, comments, shares)
            metrics["retention_rate"] = self.calculate_retention_rate(average_view_percentage)

        return metrics
