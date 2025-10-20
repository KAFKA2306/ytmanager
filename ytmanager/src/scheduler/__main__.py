import argparse
from .cron_manager import CronManager
from .series_manager import SeriesManager
from .queue import ExecutionQueue
from ..channels.registry import ChannelRegistry


def main():
    parser = argparse.ArgumentParser(description="Scheduler")
    parser.add_argument("--action", choices=["list", "run", "series", "queue"], required=True, help="Action")
    parser.add_argument("--channel", help="Channel name")
    parser.add_argument("--series-id", help="Series ID")
    args = parser.parse_args()

    cron = CronManager()
    series = SeriesManager()
    queue = ExecutionQueue()
    registry = ChannelRegistry()

    if args.action == "list":
        print("Scheduled channels:")
        for entry in cron.list():
            print(f"  {entry['channel']}: {entry['cron']} ({'enabled' if entry['enabled'] else 'disabled'})")

    elif args.action == "series":
        print("Active series:")
        for s in series.list_active():
            progress = len(s["episodes_produced"])
            total = s["total_episodes"]
            print(f"  {s['series_id']}: {s['title']} ({progress}/{total})")

    elif args.action == "queue":
        print("Execution queue:")
        for task in queue.list():
            print(f"  {task['task_id']}: {task['channel']} [{task['status']}]")

    elif args.action == "run":
        if not args.channel:
            print("--channel required for run action")
            return

        channel_config = registry.get(args.channel)
        print(f"Queueing {args.channel}...")

        task_id = queue.add(
            args.channel,
            f"uv run python -m src.main",
            priority=0
        )
        print(f"Task queued: {task_id}")


if __name__ == "__main__":
    main()
