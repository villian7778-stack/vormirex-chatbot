import os
import sys

# Ensure project root is on path so `backend` package can be imported when
# running this script directly.
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.chatbot import chatbot_reply


def run_scenario(name, messages, user_ids):
    print(f"\n--- Scenario: {name} ---\n")
    for i, msg in enumerate(messages):
        uid = user_ids[i] if i < len(user_ids) else user_ids[-1]
        resp = chatbot_reply(user_id=uid, user_message=msg)
        print(f"User (id={uid}): {msg}")
        print("Bot ->", resp)
        print()


# Conversation sequence from your report
msgs = [
    "hi",
    "akash 8788624502",
    "data science"
]

# 1) Persistent user_id (correct flow expected)
persistent_ids = ["user-123"] * len(msgs)

# 2) Non-persistent user_id (simulates frontend not sending same id)
nonpersistent_ids = ["user-a", "user-b", "user-c"]

run_scenario("Persistent user_id", msgs, persistent_ids)
run_scenario("Non-persistent user_id", msgs, nonpersistent_ids)

print("Simulation complete.")
