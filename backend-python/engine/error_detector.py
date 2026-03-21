# engine/error_detector.py

def detect_errors(metrics: dict, config: dict):
    errors = []
    constraints = config.get("constraints", {})

    # Opinion
    if constraints.get("require_opinion") and not metrics["opinion_present"]:
        errors.append("opinion_missing")

    # Advantage
    if constraints.get("require_advantage") and metrics["advantage_count"] == 0:
        errors.append("no_advantage")

    # Disadvantage
    if constraints.get("require_disadvantage") and metrics["disadvantage_count"] == 0:
        errors.append("no_disadvantage")

    # Problem
    if constraints.get("require_problem") and metrics["problem_count"] == 0:
        errors.append("no_problem")

    # Solution
    if constraints.get("require_solution") and metrics["solution_count"] == 0:
        errors.append("no_solution")

    # Cause
    if constraints.get("require_cause") and metrics["cause_count"] == 0:
        errors.append("no_cause")

    # Effect
    if constraints.get("require_effect") and metrics["effect_count"] == 0:
        errors.append("no_effect")

    # Explanation sentences
    if metrics["explanation_count"] < constraints.get("min_explanation_sentences", 0):
        errors.append("no_explanation")

    # Example sentences
    if metrics["example_count"] < constraints.get("min_example_sentences", 0):
        errors.append("no_example")

    if not errors:
        errors.append("positive")

    return errors