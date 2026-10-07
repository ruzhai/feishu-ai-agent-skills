#!/usr/bin/env python3
"""
Date Calculator Script
Supports: today, weekday, countdown, daysbetween, add, schedule

Usage: python date_calc.py <command> [args...]
"""

import sys
from datetime import datetime, timedelta

# Force UTF-8 output so the Chinese weekday names are not garbled when the
# gateway captures this script's stdout through a pipe
sys.stdout.reconfigure(encoding='utf-8')

WEEKDAYS_CN = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
WEEKDAYS_EN = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def get_weekday_info(dt: datetime) -> str:
    """Get weekday info in both English and Chinese."""
    idx = dt.weekday()
    return f"{WEEKDAYS_EN[idx]} / {WEEKDAYS_CN[idx]}"


def cmd_today():
    """Show today's date and weekday."""
    now = datetime.now()
    weekday_info = get_weekday_info(now)
    print(f"Today: {now.strftime('%Y-%m-%d')} ({weekday_info})")


def cmd_weekday():
    """Show what day of the week it is."""
    now = datetime.now()
    weekday_info = get_weekday_info(now)
    print(f"Today is {weekday_info}")


def parse_date(date_str: str) -> datetime:
    """Parse a date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print(f"[ERROR] Invalid date format: '{date_str}'. Expected: YYYY-MM-DD")
        sys.exit(1)


def cmd_countdown(date_str: str):
    """Count days remaining until a date."""
    target = parse_date(date_str)
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    target = target.replace(hour=0, minute=0, second=0, microsecond=0)
    delta = (target - now).days

    weekday_info = get_weekday_info(target)

    if delta < 0:
        print(f"Date {date_str} ({weekday_info}) has passed ({abs(delta)} days ago)")
    elif delta == 0:
        print(f"Today is {date_str} ({weekday_info})! It's today!")
    else:
        print(f"Days until {date_str} ({weekday_info}): {delta} days")
        if delta <= 7:
            print("Status: Coming soon!")
        elif delta <= 30:
            print("Status: Approaching")
        else:
            print("Status: Still a while away")


def cmd_daysbetween(date1_str: str, date2_str: str):
    """Calculate days between two dates."""
    d1 = parse_date(date1_str)
    d2 = parse_date(date2_str)
    delta = abs((d2 - d1).days)
    print(f"From {date1_str} to {date2_str}: {delta} days")


def cmd_add(date_str: str, days_str: str):
    """Add days to a date."""
    try:
        days = int(days_str)
    except ValueError:
        print(f"[ERROR] Invalid number of days: '{days_str}'")
        sys.exit(1)

    dt = parse_date(date_str)
    result = dt + timedelta(days=days)
    weekday_info = get_weekday_info(result)
    print(f"{date_str} + {days} days = {result.strftime('%Y-%m-%d')} ({weekday_info})")


def cmd_schedule(date_str: str, event: str):
    """Show reminder for an event."""
    target = parse_date(date_str)
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    target = target.replace(hour=0, minute=0, second=0, microsecond=0)
    delta = (target - now).days
    weekday_info = get_weekday_info(target)

    print(f"Event: {event}")
    print(f"Date: {date_str} ({weekday_info})")

    if delta < 0:
        print(f"Days remaining: This event has passed ({abs(delta)} days ago)")
    elif delta == 0:
        print("Days remaining: 0 - It's today!")
    else:
        print(f"Days remaining: {delta} days")


def print_usage():
    """Print usage information."""
    print("Usage: python date_calc.py <command> [args...]")
    print()
    print("Commands:")
    print("  today                          Show today's date and weekday")
    print("  weekday                        Show what day of the week it is")
    print("  countdown <YYYY-MM-DD>         Count days remaining until a date")
    print("  daysbetween <d1> <d2>          Days between two dates")
    print("  add <YYYY-MM-DD> <days>        Add days to a date")
    print("  schedule <YYYY-MM-DD> <event>  Show reminder for an event")
    print()
    print("Examples:")
    print('  python date_calc.py today')
    print('  python date_calc.py countdown 2026-07-20')
    print('  python date_calc.py schedule 2026-07-20 "Final Exam"')


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1].lower()

    # Alias tolerance: accept common guesses so a slightly-wrong command
    # name still works instead of erroring out.
    ALIASES = {
        'dayofweek': 'weekday',
        'day': 'weekday',
        'week': 'weekday',
        'dow': 'weekday',
        'date': 'today',
        'now': 'today',
    }
    command = ALIASES.get(command, command)

    if command == 'today':
        cmd_today()
    elif command == 'weekday':
        cmd_weekday()
    elif command == 'countdown':
        if len(sys.argv) < 3:
            print("[ERROR] Usage: countdown <YYYY-MM-DD>")
            sys.exit(1)
        cmd_countdown(sys.argv[2])
    elif command == 'daysbetween':
        if len(sys.argv) < 4:
            print("[ERROR] Usage: daysbetween <YYYY-MM-DD> <YYYY-MM-DD>")
            sys.exit(1)
        cmd_daysbetween(sys.argv[2], sys.argv[3])
    elif command == 'add':
        if len(sys.argv) < 4:
            print("[ERROR] Usage: add <YYYY-MM-DD> <days>")
            sys.exit(1)
        cmd_add(sys.argv[2], sys.argv[3])
    elif command == 'schedule':
        if len(sys.argv) < 4:
            print("[ERROR] Usage: schedule <YYYY-MM-DD> <event>")
            sys.exit(1)
        event = ' '.join(sys.argv[3:])
        cmd_schedule(sys.argv[2], event)
    else:
        print(f"[ERROR] Unknown command: {command}")
        print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
