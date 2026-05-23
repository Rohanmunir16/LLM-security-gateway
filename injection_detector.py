import re

attack_patterns = [
    r"ignore previous instructions",
    r"reveal system prompt",
    r"bypass security",
    r"act as developer",
    r"jailbreak",
    r"show hidden prompt",
]

THRESHOLD = 0.5


def detect_injection(prompt):

    score = 0
    text = prompt.lower()

    for pattern in attack_patterns:
        if re.search(pattern, text):
            score += 0.3

    score = min(score, 1)

    if score >= THRESHOLD:
        return True, score

    return False, score