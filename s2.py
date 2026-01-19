from instagrapi import Client

cl = Client()
cl.login("niazi_tere_proffs_hai", "niazigayhai")

threads = cl.direct_threads()

for t in threads:
    print("-------------")
    print("Thread title:", t.thread_title)
    print("Thread ID:", t.id)
    print("Users:", [u.username for u in t.users])
