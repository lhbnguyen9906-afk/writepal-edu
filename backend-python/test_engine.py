import json
from engine.text_analyzer import analyze_text
from engine.error_detector import detect_errors
from engine.error_prioritizer import prioritize


def load_unit_config(unit):
    with open(f"config/unit{unit}.json", "r", encoding="utf-8") as f:
        return json.load(f)


def test_text(unit, text):
    config = load_unit_config(unit)

    metrics = analyze_text(text, config["detection_rules"])
    errors = detect_errors(metrics, config)
    main_issue = prioritize(errors, config["error_priority"])

    result = {
        "unit": unit,
        "metrics": metrics,
        "main_issue": main_issue,
        "feedback": config["feedback_map"].get(main_issue, "No feedback available.")
    }

    print("\n=== RESULT ===")
    print(json.dumps(result, indent=2))


# ==========================
# TEST CASES HERE
# ==========================

if __name__ == "__main__":

    # Unit 1 test
    text1 = "I think online learning has many benefits because it is flexible. For example, students can study at home."
    test_text(1, text1)

    # Unit 2 test
    text2 = "I believe social media has advantages because it connects people. However, it also has disadvantages such as addiction."
    test_text(2, text2)