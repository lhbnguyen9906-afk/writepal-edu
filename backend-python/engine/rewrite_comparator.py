"""Compare original vs rewrite. Here we perform a tiny heuristic comparison.
Returns a dict with score and notes.
"""

def compare_rewrites(original, rewrite):
    # Placeholder: if identical, score 0; else 1
    score = 0 if original == rewrite else 1
    notes = 'identical' if score == 0 else 'different'
    return {'score': score, 'notes': notes}
