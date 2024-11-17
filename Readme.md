# Instructions
### Installation
1. `cd` into the project directory, and run `python -m venv env` in the terminal to setup a Python virtual environment.
2. Run `env/Scripts/Activate.ps1`  in the VScode terminal, in the project directory to activate the Python virtual environment.
3. Run `pip install -r requirements.txt` to install all required Python dependencies.

# How to run 
Run `python render_schedule.py --schedule=test/schedule_basic.json --overrides=test/overrides_basic_one.json --from='2023-11-17T17:00:00Z' --until='2023-12-01T17:00:00Z'`
See more tests below.

# Assumptions
This program assumes that the format of dates are given correctly.

# Optimisations
When applying overrides, two pointers (`shift_index` and `overrides_index`) are used to traverse the original schedule (size $n$) and overrides list (size $m$)  since both of them are ordered chronologically. This results in an improved time complexity of $O(n+m)$ instead of $O(n*m)$ (nested for loop of schedule and overrides), because we only traverse overrides list once.

# Tests
1. Empty schedule
    - Command: `haha`
    - Expected result: should return an empty schedule
2. Empty override
    - Command: `haha`
    - Expected result: should return a schedule with users at specified intervals
3. Overlapping overrides
    - Description: An override that overlaps 2 intervals
    - Command: `haha`
    - Expected result: should return an empty schedule
    - Explanation
4. Encompassing overrides
    - Description: An override that spans 3 intervals, completely including the middle one
5. Multiple overrides in one interval
6. Schedule with cycles
    - Command: `haha`
    - Expected result: should return an empty schedule
7. From date later than handover start date