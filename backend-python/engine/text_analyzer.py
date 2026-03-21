# engine/text_analyzer.py

def split_sentences(text: str):
    return [s.strip() for s in text.split('.') if s.strip()]


def contains_any(text: str, keywords: list):
    text_lower = text.lower()
    return any(k.lower() in text_lower for k in keywords)


def count_sentences_with(sentences: list, keywords: list):
    count = 0
    for s in sentences:
        for k in keywords:
            if k.lower() in s.lower():
                count += 1
                break
    return count


def count_occurrences(text: str, keywords: list):
    text_lower = text.lower()
    return sum(text_lower.count(k.lower()) for k in keywords)


def count_markers(text: str, markers: list):
    text_lower = text.lower()
    count = 0
    for m in markers:
        if m.lower() in text_lower:
            count += 1
    return count


def analyze_text(text: str, detection_rules: dict):
    text_lower = text.lower()
    sentences = split_sentences(text_lower)

    return {
        "total_sentences": len(sentences),

        "opinion_present":
            contains_any(text_lower, detection_rules.get("opinion_markers", [])),

        "explanation_count":
            count_sentences_with(
                sentences,
                detection_rules.get("explanation_markers", [])
            ),

        "example_count":
            count_sentences_with(
                sentences,
                detection_rules.get("example_markers", [])
            ),

        "personal_count":
            count_occurrences(
                text_lower,
                detection_rules.get("personal_pronouns", [])
            ),

        "advantage_count":
            count_markers(
                text_lower,
                detection_rules.get("advantage_markers", [])
            ),

        "disadvantage_count":
            count_markers(
                text_lower,
                detection_rules.get("disadvantage_markers", [])
            ),

        "problem_count":
            count_markers(
                text_lower,
                detection_rules.get("problem_markers", [])
            ),

        "solution_count":
            count_markers(
                text_lower,
                detection_rules.get("solution_markers", [])
            ),

        "cause_count":
            count_markers(
                text_lower,
                detection_rules.get("cause_markers", [])
            ),

        "effect_count":
            count_markers(
                text_lower,
                detection_rules.get("effect_markers", [])
            )
    }