def policy_decision(injection_detected, entities):

    if injection_detected:
        return "BLOCK"

    if len(entities) > 0:
        return "MASK"

    return "ALLOW"