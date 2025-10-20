import argparse
from .youtube_api import YouTubeAPI
from .metrics import MetricsCalculator
from ..channels.registry import ChannelRegistry


def main():
    parser = argparse.ArgumentParser(description="YouTube Analytics")
    parser.add_argument("--channel", required=True, help="Channel name")
    parser.add_argument("--credentials", default="config/youtube_credentials.json", help="YouTube credentials path")
    args = parser.parse_args()

    registry = ChannelRegistry()
    channel_config = registry.get(args.channel)

    api = YouTubeAPI(args.credentials)
    calculator = MetricsCalculator()

    analytics = api.get_channel_analytics(
        channel_config.youtube_channel_id,
        channel_config.analytics.lookback_days
    )

    metrics = calculator.calculate_all(analytics)

    print(f"Analytics for {args.channel}:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value}")


if __name__ == "__main__":
    main()
