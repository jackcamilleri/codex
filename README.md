# Workout Display for Raspberry Pi

A simple Python app that shows today's date and the next workout in your rotation. The app
reads the last completed workout from `workout_state.json`, then displays the next workout
in the cycle.

## Workout Cycle

1. Legs and abs
2. Chest and triceps
3. Back and biceps
4. Shoulders and abs
5. Cardio

## Requirements

- Python 3 with Tkinter (installed by default on Raspberry Pi OS).

## Usage

### Show the display

```bash
python3 workout_display.py --fullscreen
```

Press `Esc` to exit fullscreen.

### Update the last completed workout

```bash
python3 workout_display.py --set-last "Chest and triceps"
```

This updates the stored state and exits without starting the UI. Once updated,
the next workout will be shown the next time the screen refreshes (or when you
restart the app).

### Print today's workout to the terminal

```bash
python3 workout_display.py --print
```

## Updating from another device

If you want to update the schedule from your phone, run the `--set-last` command over SSH
or adjust `workout_state.json` directly. For example, from a phone SSH client:

```bash
ssh pi@raspberrypi.local "python3 /path/to/workout_display.py --set-last 'Back and biceps'"
```
