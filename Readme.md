# Instructions
### Installation
1. `cd` into the project directory, and run `python -m venv env` in the terminal to setup a Python virtual environment.
2. Run `env/Scripts/Activate.ps1`  in the VScode terminal, in the project directory to activate the Python virtual environment.
3. Run `pip install -r requirements.txt` to install all required Python dependencies.

### How to run 
Run `python render_schedule.py --schedule=test/schedule_basic.json --overrides=test/overrides_basic_one.json --from='2023-11-17T17:00:00Z' --until='2023-12-01T17:00:00Z'`
Output will be printed in console and also written as a JSON file to the `output` folder as `output.json`.
See more tests below.

# Assumptions
- The format of dates are given correctly.
- No overlapping between overrides (at any one point, only one person is scheduled)

# Optimisations
When applying overrides, two pointers (`shift_index` and `overrides_index`) are used to traverse the original schedule (size $n$) and overrides list (size $m$)  since both of them are ordered chronologically. This results in an improved time complexity of $O(n+m)$ instead of $O(n*m)$ (nested for loop of schedule and overrides), because we only traverse overrides list once.

# Tests
1. Empty schedule
    - Command: `python render_schedule.py --schedule=test/schedule_empty.json --overrides=test/overrides_basic_one.json --from='2023-11-17T17:00:00Z' --until='2023-12-01T17:00:00Z'`
    - Expected result: should return an empty schedule
    - Actual result: **PASS**
2. Empty override
    - Command: `python render_schedule.py --schedule=test/schedule_basic_one.json --overrides=test/overrides_empty.json --from='2023-11-17T17:00:00Z' --until='2023-12-02T17:00:00Z'`
    - Expected result: should return a schedule with users at specified intervals
    - Actual result: **PASS**
3. Multiple overrides (with cycled users)
    - Command: `python render_schedule.py --schedule=test/schedule_basic_two.json --overrides=test/overrides_basic_multiple.json --from='2023-11-17T17:00:00Z' --until='2023-12-02T17:00:00Z'`
    - Expected result: should return a schedule with all overrides applied
    - Actual result: **PASS**
4. Overlapping overrides
    - Description: An override that overlaps 2 intervals
    - Command: `python render_schedule.py --schedule=test/schedule_basic_one.json --overrides=test/overrides_overlapping.json --from='2023-11-17T17:00:00Z' --until='2023-12-01T17:00:00Z'`
    - Expected result: should return a schedule with all overrides correctly applied
    - Actual result: **PASS**
5. Encompassing overrides
    - Description: An override that spans 3 intervals, completely including the middle one
    - Command: `python render_schedule.py --schedule=test/schedule_short_handover.json --overrides=test/overrides_cover_three.json --from='2023-11-18T00:00:00Z' --until='2023-11-23T00:00:00Z'`
    - Expected result: The middle user's shift should not be in the final schedule since it's covered by the override entirely
    - Actual result: **PASS**
6. Multiple overrides in one user's interval
    - Command: `python render_schedule.py --schedule=test/schedule_basic_one.json --overrides=test/overrides_multiple_same_user.json --from='2023-11-17T17:00:00Z' --until='2023-12-01T17:00:00Z'`
    - Expected result: should return a schedule where all overrides are applied
    - Actual result: **PASS**
7. Override entire range
    - Description: one user overrides the entire range of from to until date
    - Command: `python render_schedule.py --schedule=test/schedule_basic_one.json --overrides=test/overrides_entire_range.json --from='2023-11-17T17:00:00Z' --until='2023-12-01T17:00:00Z'`
    - Expected result: should return a schedule with only that override user covering the entire range
    - Actual result: **PASS**
8. Cutoff overrides that exceed date range
   - Command: `python render_schedule.py --schedule=test/schedule_basic_one.json --overrides=test/overrides_out_of_range.json --from='2023-11-17T17:00:00Z' --until='2023-12-01T17:00:00Z'`
   - Expected result: Last override is cut off till until time
   - Actual result: **PASS**
9. Schedule with cycles
    - Description: Small handover interval days to check if users are cycled through
    - Command: `python render_schedule.py --schedule=test/schedule_short_handover.json --overrides=test/overrides_empty.json --from='2023-11-17T17:00:00Z' --until='2023-12-02T17:00:00Z'`
    - Expected result: should return a schedule where users are cycled
    - Actual result: **PASS**
10. From date and Until date cuts off schedule
    - Command: `python render_schedule.py --schedule=test/schedule_basic_two.json --overrides=test/overrides_empty.json --from='2023-11-18T17:00:00Z' --until='2023-12-02T05:00:00Z'`
    - Expected result: The first start time and the last end time should be the from and until time respectively, while the intervals are still obeyed
    - Actual result: **PASS**