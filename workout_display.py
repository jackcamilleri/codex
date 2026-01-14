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


def update_display(date_label, workout_label):
    day_text, workout_text = render_text()
    date_label.configure(text=day_text)
    workout_label.configure(text=workout_text)
    date_label.after(60_000, update_display, date_label, workout_label)


def run_display(fullscreen):
    root = tk.Tk()
    root.title("Workout Schedule")
    root.configure(bg="#111111")
    root.attributes("-fullscreen", fullscreen)

    container = tk.Frame(root, bg="#111111")
    container.pack(expand=True)

    date_label = tk.Label(
        container,
        text="",
        font=("Helvetica", 36, "bold"),
        fg="#f5f5f5",
        bg="#111111",
    )
    date_label.pack(pady=(0, 20))

    workout_title = tk.Label(
        container,
        text="Today's Workout",
        font=("Helvetica", 24),
        fg="#a0a0a0",
        bg="#111111",
    )
    workout_title.pack()

    workout_label = tk.Label(
        container,
        text="",
        font=("Helvetica", 40, "bold"),
        fg="#4ade80",
        bg="#111111",
    )
    workout_label.pack(pady=(10, 0))

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

    if args.print_only:
        day_text, workout_text = render_text()
        print(day_text)
        print(workout_text)
        return 0

    run_display(args.fullscreen)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
