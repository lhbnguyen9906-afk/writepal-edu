# engine/error_prioritizer.py

def prioritize(errors: list, priority_list: list):
    for p in priority_list:
        if p in errors:
            return p

    return errors[0] if errors else "positive"