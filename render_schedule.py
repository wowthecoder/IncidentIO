import json
import argparse
from datetime import datetime, timedelta
from dateutil import parser

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def apply_overrides(schedule, overrides, from_time, until_time):
    if not overrides:
        return schedule
    
    final_schedule = []
    shift_index, shift_count = 0, len(schedule)
    
    # Sort overrides by start time
    overrides = sorted(overrides, key=lambda x: parser.parse(x['start_at']))
    override_index, override_count = 0, len(overrides)
    
    while shift_index < shift_count:
        shift = schedule[shift_index]
        shift_start = parser.parse(shift['start_at'])
        shift_end = parser.parse(shift['end_at'])
        
        # Truncate shift based on from_time and until_time
        if shift_start < from_time:
            shift_start = from_time
        if shift_end > until_time:
            shift_end = until_time
        if shift_start >= shift_end:
            continue
        
        current_start = shift_start
        
        while override_index < override_count:
            override = overrides[override_index]
            override_start = parser.parse(override['start_at'])
            override_end = parser.parse(override['end_at'])

            # Cut off overrides that are outside of time range
            if override_start < from_time:
                override_start = from_time
            if override_end > until_time:
                override_end = until_time
            
            if override_end <= shift_start:
                # This override is completely before the shift, move to the next override
                override_index += 1
                continue

            if override_start >= shift_end:
                # This override is completely after the shift, break out of the loop
                break
            
            # Add the part of the shift before the override (if any)
            if current_start < override_start:
                final_schedule.append({
                    "user": shift['user'],
                    "start_at": current_start.isoformat(),
                    "end_at": override_start.isoformat()
                })

            # Add the overridden part of the shift   
            final_schedule.append({
                "user": override['user'],
                "start_at": override_start.isoformat(),
                "end_at": override_end.isoformat()
            })
            
            current_start = max(override_end, current_start)

            override_index += 1

            while override_end >= shift_end:
                shift_index += 1
                if shift_index >= shift_count:
                    break
                shift = schedule[shift_index]
                shift_end = parser.parse(shift['end_at'])
        
        # Add the part of the shift after the last override (if any)
        if shift_index >= shift_count:
            break
        shift = schedule[shift_index]
        shift_end = parser.parse(shift['end_at'])
        if current_start < shift_end:
            final_schedule.append({
                "user": shift['user'],
                "start_at": current_start.isoformat(),
                "end_at": shift_end.isoformat()
            })

        shift_index += 1
    
    return final_schedule

def generate_schedule(users, start_time, interval_days, from_time, until_time):
    # If there is no users, return empty schedule
    if not users:
        return []
    schedule = []
    current_time = start_time
    user_count = len(users)
    user_index = 0
    
    while current_time < until_time:
        end_time = current_time + timedelta(days=interval_days)
        if end_time > from_time:
            schedule.append({
                "user": users[user_index],
                "start_at": max(current_time, from_time).isoformat(),
                "end_at": min(end_time, until_time).isoformat()
            })
        current_time = end_time
        # Select next user
        user_index = (user_index + 1) % user_count
    
    return schedule

def main():
    # Parse command line arguments
    arg_parser = argparse.ArgumentParser(description='Render on-call schedule with overrides')
    arg_parser.add_argument('--schedule', required=True, help='Path to schedule JSON file')
    arg_parser.add_argument('--overrides', required=True, help='Path to overrides JSON file')
    arg_parser.add_argument('--from', dest='from_time', required=True, help='Start time for rendering schedule')
    arg_parser.add_argument('--until', dest='until_time', required=True, help='End time for rendering schedule')
    
    args = arg_parser.parse_args()
    
    # Load JSON inputs
    schedule_data = load_json(args.schedule)
    overrides_data = load_json(args.overrides)
    
    # Parse input times
    from_time = parser.parse(args.from_time)
    until_time = parser.parse(args.until_time)
    
    # Generate initial schedule
    users = schedule_data['users']
    handover_start_at = parser.parse(schedule_data['handover_start_at'])
    handover_interval_days = schedule_data['handover_interval_days']
    
    schedule = generate_schedule(users, handover_start_at, handover_interval_days, from_time, until_time)
    
    # Apply overrides and truncate based on from/until
    final_schedule = apply_overrides(schedule, overrides_data, from_time, until_time)
    
    # Output final schedule in JSON format
    print(json.dumps(final_schedule, indent=2))

    # Write output to file
    with open('output/output.json', 'w') as f:
        json.dump(final_schedule, f, indent=2)

if __name__ == "__main__":
    main()
