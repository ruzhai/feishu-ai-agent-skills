---
name: date-calculator
description: "MANDATORY for ALL date/time/weekday/countdown questions. You MUST run the script via the exec tool BEFORE answering. Do NOT answer from your own knowledge."
when_to_use: "today, weekday, countdown, deadline, how many days, date calculation, what day, 今天, 星期几, 距离, 多少天"
always: true
---
# IMPORTANT: You MUST use the exec tool to run the script below. Do NOT answer date questions directly.

When the user asks anything about dates or weekdays, run the script via the **exec** tool and base your answer on its output. Never compute the date yourself.

## When to call this skill (MANDATORY)

Call this skill ONLY for date/time/weekday questions, such as:

- "今天是几号" / "今天星期几" / "what day is today"
- "距离 2026-12-31 还有多少天" / countdown to a deadline
- "两个日期之间相差几天" / days between two dates
- "X天后是几号" / add days to a date
- Any date/time/weekday calculation

## When NOT to call this skill

- Course/deep-learning/ML knowledge questions (use knowledge-base instead)
- Casual chat, greetings, or small talk

## Commands

| Command | What it does | Example |
|---|---|---|
| `today` | Today's date + weekday | `date_calc.py today` |
| `weekday` | Just the weekday | `date_calc.py weekday` |
| `countdown <YYYY-MM-DD>` | Days until a date | `date_calc.py countdown 2026-08-30` |
| `daysbetween <d1> <d2>` | Days between two dates | `date_calc.py daysbetween 2026-07-14 2026-08-30` |
| `add <YYYY-MM-DD> <days>` | Add days to a date | `date_calc.py add 2026-07-14 30` |
| `schedule <YYYY-MM-DD> <event>` | Reminder for an event | `date_calc.py schedule 2026-07-20 "Final Exam"` |

Aliases are also accepted (`day`, `dayofweek`, `week`, `dow`, `date`, `now`).

## Path to the script

The skill deploys under the gateway workspace, so at runtime the script lives at
`<openclaw-workspace>/skills/date-calculator/scripts/date_calc.py`. Use whatever
Python 3 interpreter the gateway has, and substitute the real skill directory for
`<SKILL_DIR>`:

```
python <SKILL_DIR>/scripts/date_calc.py today
python <SKILL_DIR>/scripts/date_calc.py countdown 2026-08-30
python <SKILL_DIR>/scripts/date_calc.py daysbetween 2026-07-14 2026-08-30
```

The `exec` tool needs the **absolute** path — that is the only reason the command
is spelled out in full here rather than as `python scripts/date_calc.py`.

NEVER answer date/weekday questions without running this script first.

## Response Format (MANDATORY)

When you reply after running the script, you MUST start your reply with this exact tag on its own line:

[Skill Tool: date-calculator]

Then continue with your answer based on the script output. Example:

[Skill Tool: date-calculator]
Today is Tuesday.

This tag tells the user that the answer came from the custom Skill tool, not from the model's own knowledge.