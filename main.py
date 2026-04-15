import asyncio
import random
from datetime import datetime

from telethon import TelegramClient, events

from config import API_ID, API_HASH, DAILY_LIMIT, KEYWORDS
from sheets import already_contacted, save_user, mark_replied
from utils import generate_message

# ✅ MUST match your file name: fear.session
client = TelegramClient('fear', API_ID, API_HASH)

sent_today = 0


# 📩 Track replies
@client.on(events.NewMessage(incoming=True))
async def handle_reply(event):
    sender = await event.get_sender()

    if sender.bot:
        return

    print(f"Reply from {sender.first_name}")
    mark_replied(sender.id)


# 📢 Monitor groups
@client.on(events.NewMessage)
async def handler(event):
    global sent_today

    if sent_today >= DAILY_LIMIT:
        return

    if not event.is_group:
        return

    sender = await event.get_sender()
    message = event.raw_text.lower()

    if sender.bot or sender.is_self:
        return

    # Keyword match
    if not any(word in message for word in KEYWORDS):
        return

    # Skip duplicates
    if already_contacted(sender.id):
        return

    try:
        await asyncio.sleep(random.randint(20, 60))

        msg = generate_message(sender.first_name)

        await client.send_message(sender.id, msg)

        sent_today += 1
        print(f"✅ Sent DM to {sender.first_name}")

        save_user(sender, message)

        await asyncio.sleep(random.randint(90, 180))

    except Exception as e:
        print("❌ Error:", e)
        await asyncio.sleep(300)


# 🕒 Safety loop
async def safety_loop():
    global sent_today

    while True:
        now = datetime.now()

        if now.hour == 0:
            sent_today = 0

        if 2 <= now.hour <= 8:
            print("😴 Sleeping...")
            await asyncio.sleep(3600)
        else:
            await asyncio.sleep(300)


# ▶️ Start
async def main():
    # ❌ Do NOT use start() here
    # ✅ Use connect for server
    await client.connect()

    # ✅ Check if session exists
    if not await client.is_user_authorized():
        print("❌ Session not found. Run locally first.")
        return

    print("🚀 FEAR Automation Running...")

    asyncio.create_task(safety_loop())

    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())
