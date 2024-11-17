# Instructions
### Installation
1. `cd` into the project directory, and run `python -m venv env` in the terminal to setup a Python virtual environment.
2. Run `env/Scripts/Activate.ps1`  in the Vscode terminal, in the project directory. 

Run `python render_schedule.py --schedule=test/schedule1.json --overrides=test/overrides1.json --from='2023-11-17T17:00:00Z' --until='2023-12-01T17:00:00Z'`

Tests:
1. Empty schedule

2. Empty override
3. Overlapping overrides
4. 