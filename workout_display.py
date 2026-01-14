#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
import tkinter as tk

CYCLE = [
    "Legs and abs",
    "Chest and triceps",
    "Back and biceps",
    "Shoulders and abs",
    "Cardio",
]

STATE_FILE = Path(__file__).with_name("workout_state.json")


def load_state():
    if not STATE_FILE.exists():
        return {"last_workout": CYCLE[-1]}
    with STATE_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_state(state):
    with STATE_FILE.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
        handle.write("\n")


def next_workout(last_workout):
    if last_workout not in CYCLE:
        return CYCLE[0]
    index = CYCLE.index(last_workout)
    return CYCLE[(index + 1) % len(CYCLE)]


def render_text():
    today = datetime.now()
    day_label = today.strftime("%A, %B %d, %Y")
    last_workout = load_state().get("last_workout", CYCLE[-1])
    planned = next_workout(last_workout)
    return day_label, planned


def workout_icon(workout_name):
    icons = {
        "Legs and abs": "🦵🧘",
        "Chest and triceps": "🏋️💪",
        "Back and biceps": "🧗💪",
        "Shoulders and abs": "🏋️‍♂️🧘",
        "Cardio": "🏃❤️",
    }
    return icons.get(workout_name, "💪")


def update_display(date_label, workout_label):
    day_text, workout_text = render_text()
    date_label.configure(text=day_text)
    workout_label.configure(text=workout_text)
    workout_label.icon_label.configure(text=workout_icon(workout_text))
    date_label.after(60_000, update_display, date_label, workout_label)


def run_display(fullscreen):
    root = tk.Tk()
    root.title("Workout Schedule")
    root.configure(bg="#111111")
    root.attributes("-fullscreen", fullscreen)

    container = tk.Frame(root, bg="#111111")
    container.pack(fill="both", expand=True, padx=40, pady=30)

    date_label = tk.Label(
        container,
        text="",
        font=("Helvetica", 30, "bold"),
        fg="#f5f5f5",
        bg="#111111",
    )
    date_label.pack(pady=(0, 30))

    content = tk.Frame(container, bg="#111111")
    content.pack(fill="both", expand=True)

    left_column = tk.Frame(content, bg="#111111")
    left_column.pack(side="left", fill="both", expand=True, anchor="w")

    right_column = tk.Frame(content, bg="#111111")
    right_column.pack(side="right", fill="both", expand=True, anchor="e")

    workout_title = tk.Label(
        left_column,
        text="Today's Workout",
        font=("Helvetica", 22),
        fg="#a0a0a0",
        bg="#111111",
        anchor="w",
        justify="left",
    )
    workout_title.pack(anchor="w")

    workout_row = tk.Frame(left_column, bg="#111111")
    workout_row.pack(anchor="w", pady=(12, 0))

    workout_icon_label = tk.Label(
        workout_row,
        text="",
        font=("Helvetica", 40),
        fg="#facc15",
        bg="#111111",
    )
    workout_icon_label.pack(side="left")

    workout_label = tk.Label(
        workout_row,
        text="",
        font=("Helvetica", 38, "bold"),
        fg="#4ade80",
        bg="#111111",
        anchor="w",
        justify="left",
    )
    workout_label.pack(side="left", padx=(14, 0))
    workout_label.icon_label = workout_icon_label

    metrics_title = tk.Label(
        right_column,
        text="Fitness Metrics",
        font=("Helvetica", 20),
        fg="#a0a0a0",
        bg="#111111",
        anchor="e",
        justify="right",
    )
    metrics_title.pack(anchor="e")

    metrics_hint = tk.Label(
        right_column,
        text="Sleep, recovery, and other stats\ncoming soon",
        font=("Helvetica", 18),
        fg="#64748b",
        bg="#111111",
        anchor="e",
        justify="right",
    )
    metrics_hint.pack(anchor="e", pady=(12, 0))

    update_display(date_label, workout_label)
    root.bind("<Escape>", lambda event: root.destroy())
    root.mainloop()


def set_last_workout(last_workout):
    state = load_state()
    state["last_workout"] = last_workout
    save_state(state)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Display a workout schedule based on the last completed workout."
    )
    parser.add_argument(
        "--set-last",
        metavar="WORKOUT",
        help="Set the last completed workout (e.g. 'Chest and triceps').",
    )
    parser.add_argument(
        "--fullscreen",
        action="store_true",
        help="Run the display in fullscreen mode.",
    )
    parser.add_argument(
        "--print",
        dest="print_only",
        action="store_true",
        help="Print today's date and planned workout without launching the UI.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])

    if args.set_last:
        set_last_workout(args.set_last)
        if not args.print_only:
            return 0

    if args.print_only:
        day_text, workout_text = render_text()
        print(day_text)
        print(workout_text)
        return 0

    run_display(args.fullscreen)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
