# Instructions
### Installation
1. `cd` into the project directory, and run `python -m venv env` in the terminal to setup a Python virtual environment.
2. Run `env/Scripts/Activate.ps1`  in the VScode terminal, in the project directory to activate the Python virtual environment.
3. Run `pip install -r requirements.txt` to install all required Python dependencies.

# How to run 
Run `python render_schedule.py --schedule=test/schedule1.json --overrides=test/overrides1.json --from='2023-11-17T17:00:00Z' --until='2023-12-01T17:00:00Z'`

# Tests
1. Empty schedule
  - Command: `haha`
  - Expected result: should return an empty schedule
2. Empty override
    - Command: `haha`
    - Expected result: should return a schedule with users at specified intervals
3. Overlapping overrides
    - Description:
    - Command: `haha`
    - Expected result: should return an empty schedule
4. Schedule with cycles
    - Command: `haha`
    - Expected result: should return an empty schedule