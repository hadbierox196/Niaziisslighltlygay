from instagrapi import Client
import time
import os

# ================= CONFIG =================
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

TARGET_USERNAME = os.getenv("TARGET_USERNAME")
THREAD_ID = os.getenv("THREAD_ID")
REPLY_TEXT = os.getenv("REPLY_TEXT", "👍")
CHECK_DELAY = int(os.getenv("CHECK_DELAY", 20))
SESSION_FILE = "session.json"
# ==========================================

def login_client():
    cl = Client()

    if os.path.exists(SESSION_FILE):
        cl.load_settings(SESSION_FILE)
        cl.login(None, None)
    else:
        cl.login(IG_USERNAME, IG_PASSWORD)
        cl.dump_settings(SESSION_FILE)

    return cl

def main():
    cl = login_client()
    target_user_id = cl.user_id_from_username(TARGET_USERNAME)
    replied_ids = set()
    print("Bot started. Monitoring messages...")

    while True:
        try:
            thread = cl.direct_thread(THREAD_ID)
            for msg in reversed(thread.messages):
                if msg.id in replied_ids:
                    continue
                if (
                    msg.user_id == target_user_id
                    and not msg.is_sent_by_viewer
                    and msg.item_type == "text"
                ):
                    cl.direct_send(
                        text=REPLY_TEXT,
                        thread_ids=[THREAD_ID]
                    )
                    replied_ids.add(msg.id)
                    print("Replied to message:", msg.id)
            time.sleep(CHECK_DELAY)
        except Exception as e:
            print("Error:", e)
            time.sleep(60)

if __name__ == "__main__":
    main()
