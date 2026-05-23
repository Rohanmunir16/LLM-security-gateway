from presidio_analyzer import PatternRecognizer, Pattern

phone_pattern = Pattern(name="phone", regex=r"\b03\d{9}\b", score=0.6)

api_pattern = Pattern(
    name="api_key",
    regex=r"sk-[a-zA-Z0-9]{20,}",
    score=0.7
)

internal_id_pattern = Pattern(
    name="internal_id",
    regex=r"EMP\d{4}",
    score=0.6
)

phone_recognizer = PatternRecognizer(
    supported_entity="PHONE_NUMBER",
    patterns=[phone_pattern]
)

api_recognizer = PatternRecognizer(
    supported_entity="API_KEY",
    patterns=[api_pattern]
)

internal_id_recognizer = PatternRecognizer(
    supported_entity="INTERNAL_ID",
    patterns=[internal_id_pattern]
)