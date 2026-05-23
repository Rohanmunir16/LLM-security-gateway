from injection_detector import detect_injection
from presidio_guard import anonymize_text
from policy_engine import policy_decision
from latency import measure_latency


def gateway(prompt):

    # Injection detection
    (inj_result, inj_score), inj_latency = measure_latency(detect_injection, prompt)

    # Presidio analysis
    (masked_text, entities), pii_latency = measure_latency(anonymize_text, prompt)

    # Policy
    decision = policy_decision(inj_result, entities)

    print("\nInjection Score:", inj_score)
    print("PII Entities:", entities)
    print("Decision:", decision)

    print("Injection Latency:", inj_latency)
    print("PII Latency:", pii_latency)

    if decision == "BLOCK":
        return "Prompt blocked due to injection attack."

    elif decision == "MASK":
        return masked_text

    return prompt


while True:

    user_input = input("\nEnter prompt (type 'exit' to quit): ")

    if user_input.lower() in ["exit", "quit"]:
        print("Exiting Security Gateway...")
        break

    result = gateway(user_input)

    print("Output:", result)