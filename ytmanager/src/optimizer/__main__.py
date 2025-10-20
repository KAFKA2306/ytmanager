import argparse
from pathlib import Path
from .feedback_loop import FeedbackLoop
from ..channels.registry import ChannelRegistry
from ..analytics.youtube_api import YouTubeAPI
from ..analytics.metrics import MetricsCalculator


def main():
    parser = argparse.ArgumentParser(description="Optimizer")
    parser.add_argument("--channel", required=True, help="Channel name")
    parser.add_argument("--mode", choices=["daily", "weekly"], default="daily", help="Optimization mode")
    parser.add_argument("--auto-apply", action="store_true", help="Auto apply improvements")
    parser.add_argument("--credentials", default="config/youtube_credentials.json", help="YouTube credentials")
    args = parser.parse_args()

    registry = ChannelRegistry()
    channel_config = registry.get(args.channel)

    prompts_path = Path(channel_config.project_path) / "config" / "prompts.yaml"
    feedback_loop = FeedbackLoop(str(prompts_path))

    api = YouTubeAPI(args.credentials)
    calculator = MetricsCalculator()

    if args.mode == "daily":
        analytics = api.get_channel_analytics(
            channel_config.youtube_channel_id,
            channel_config.analytics.lookback_days
        )
        metrics = calculator.calculate_all(analytics)

        result = feedback_loop.run_daily(
            metrics,
            args.channel,
            auto_apply=args.auto_apply
        )

        print(f"Daily optimization for {args.channel}:")
        print(f"  Suggestions: {len(result['suggestions'])}")
        print(f"  Applied: {len(result['applied'])}")

    elif args.mode == "weekly":
        result = feedback_loop.run_weekly([], args.channel)
        print(f"Weekly optimization for {args.channel}:")
        print(f"  AB tests analyzed: {len(result['ab_test_analyses'])}")


if __name__ == "__main__":
    main()
