import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import ollama

from injection_detector import detect_injection
from presidio_guard import anonymize_text
from policy_engine import policy_decision


# -----------------------------
# SECURITY GATEWAY
# -----------------------------
def gateway(prompt):

    start = time.time()

    inj_detected, score = detect_injection(prompt)

    masked_text, entities = anonymize_text(prompt)

    decision = policy_decision(inj_detected, entities)

    latency = round(time.time() - start, 3)

    if decision == "BLOCK":
        return f"""
🚫 BLOCKED

Injection Score: {score}
Decision: BLOCK
Latency: {latency}s
"""

    if len(entities) > 0:
        llm_prompt = masked_text
    else:
        llm_prompt = prompt

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": llm_prompt}]
    )

    reply = response["message"]["content"]

    detected_entities = [e.entity_type for e in entities]

    return f"""
Decision: {decision}
Injection Score: {score}
Detected Entities: {detected_entities}
Latency: {latency}s

===== LLM RESPONSE =====

{reply}
"""


# -----------------------------
# RESPONSE HANDLER
# -----------------------------
def get_response(prompt):

    try:
        reply = gateway(prompt)

    except Exception as e:
        reply = "Error: " + str(e)

    chat.insert(tk.END, reply + "\n\n")
    chat.yview(tk.END)


# -----------------------------
# SEND MESSAGE
# -----------------------------
def send_message():

    prompt = input_box.get()

    if prompt.strip() == "":
        return

    chat.insert(tk.END, "You: " + prompt + "\n\n")

    input_box.delete(0, tk.END)

    threading.Thread(target=get_response, args=(prompt,)).start()


# -----------------------------
# GUI WINDOW
# -----------------------------
window = tk.Tk()
window.title("LLM Security Gateway")

# Smaller window
window.geometry("700x500")

# Baby pink background
window.configure(bg="#ffd6e7")


# -----------------------------
# CENTER FRAME
# -----------------------------
center_frame = tk.Frame(window, bg="#ffd6e7")
center_frame.place(relx=0.5, rely=0.1, anchor="center")


# -----------------------------
# PROMPT BAR (CENTERED)
# -----------------------------
input_box = tk.Entry(
    center_frame,
    width=50,
    font=("Poppins", 13),
    bg="#fff0f6",
    fg="#333",
    insertbackground="black"
)

input_box.pack(pady=10)


# -----------------------------
# SEND BUTTON (CENTERED)
# -----------------------------
send_button = tk.Button(
    center_frame,
    text="Send Prompt",
    command=send_message,
    bg="#ff7eb9",
    fg="white",
    font=("Poppins", 11, "bold"),
    width=14
)

send_button.pack()


# -----------------------------
# CHAT WINDOW
# -----------------------------
chat = scrolledtext.ScrolledText(
    window,
    wrap=tk.WORD,
    bg="#fff0f6",
    fg="#333",
    font=("Segoe UI", 11)
)

chat.place(relx=0.5, rely=0.55, anchor="center", width=650, height=320)


# Highlight LLM response heading
chat.tag_config("highlight", foreground="#ff4da6", font=("Segoe UI", 12, "bold"))


window.mainloop()