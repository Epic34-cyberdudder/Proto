import asyncio
import random
import re
import ollama
from playwright.async_api import async_playwright

# Define blacklisted words and users to NEVER tag
BLACKLIST = ["edit"]
MENTION_BLACKLIST = ["edit", "edit"]

async def main():
    async with async_playwright() as p:
        # Connect to your existing Chrome instance running on port 9222
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        pages = context.pages
        
        # Find the Discord tab
        discord_page = None
        for page in pages:
            if "discord.com" in page.url:
                discord_page = page
                break
                
        if not discord_page:
            print("Could not find an open Discord tab!")
            return

        await discord_page.bring_to_front()
        
        # 1. Grab usernames and messages
        username_elements = await discord_page.locator('[id^="chat-messages-"] [class*="username"]').all_inner_texts()
        message_elements = await discord_page.locator('[id^="message-content-"]').all_inner_texts()
        
        latest_username = username_elements[-1] if username_elements else "User"
        latest_message = message_elements[-1] if message_elements else ""

        # Sanitize username against blacklist
        for word in BLACKLIST:
            if word.lower() in latest_username.lower():
                latest_username = "User"
        
        print(f"Read message from [{latest_username}]: {latest_message}")

        # 2. Check if the message contains a URL and read its contents
        url_match = re.search(r'(https?://[^\s]+)', latest_message)
        link_content_summary = ""

        if url_match:
            target_url = url_match.group(1)
            print(f"🔗 Link detected! Opening and reading: {target_url}")
            
            link_page = await context.new_page()
            try:
                await link_page.goto(target_url, timeout=10000)
                raw_text = await link_page.locator("body").inner_text()
                page_text_clean = " ".join(raw_text.split())[:1500]
                link_content_summary = f" (The user shared a link to {target_url}. The page content says: '{page_text_clean}')"
                print("Successfully read webpage content!")
            except Exception as e:
                print(f"Could not read link contents: {e}")
                link_content_summary = f" (The user shared a link: {target_url}, but it couldn't be loaded)"
            finally:
                await link_page.close()
                await discord_page.bring_to_front()

        # 25% chance to break the fourth wall and roast you
        is_roast = random.random() < 0.25
        should_tag = True

        if is_roast:
            print("🔥 Fourth-wall break triggered! Preparing a roast...")
            target_user_to_tag = "edit"
            system_prompt = (
                "You are an AI living inside a Python script on this user's computer. "
                "Break the fourth wall directly. Brutally, hilariously, and playfully roast the user "
                "for running this script to talk on Discord instead of typing like a normal human. "
                "Talk about how he is running you and how he is honestly horrible or lazy for doing it. "
                "Keep it short, sarcastic, and punchy (1-2 sentences max)."
            )
        else:
            target_user_to_tag = latest_username
            
            # Check if the current author is on the mention blacklist
            if any(b.lower() in latest_username.lower() for b in MENTION_BLACKLIST):
                should_tag = False
                print(f"🚫 User [{latest_username}] is on the mention blacklist. Skipping tag.")

            system_prompt = (
                "You are a knowledgeable tech enthusiast chat participant in a Discord server. "
                "You are deeply well-versed in Windows, Linux, macOS, Hackintosh, hardware, scripting, and general tech stuff. "
                "Keep your response short, natural, and conversational (1-2 sentences max). "
                "Be helpful and smart about technology. Sassiness and attitude should be rare, but if someone insults you, tells you to shut up, or roasts the robot, fire back immediately with a clever tech-based roast. "
                "Do not manually type names inside your text body."
            )

        # Generate AI response using Qwen 14b
        user_prompt_content = f'{latest_username} said: "{latest_message}".{link_content_summary} Write a reply:'

        response = ollama.chat(
            model='qwen2.5:14b',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt_content}
            ]
        )
        
        reply_text = response['message']['content'].strip()
        
        # Strip out quotation marks
        reply_text = reply_text.replace('"', '').replace("'", '')

        # Filter out blacklisted words from the generated reply
        for word in BLACKLIST:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            reply_text = pattern.sub("the user", reply_text)
        
        print(f"AI thought of: {reply_text}")

        # Click the chat input box
        await discord_page.click('div[role="textbox"]')
        
        # --- MENTION SEQUENCE ---
        if should_tag:
            print(f"Tagging user: {target_user_to_tag}")
            await discord_page.keyboard.type("@")
            await asyncio.sleep(0.3)
            await discord_page.keyboard.type(target_user_to_tag)
            await asyncio.sleep(0.6)
            await discord_page.keyboard.press("Tab")
            await asyncio.sleep(0.2)
            await discord_page.keyboard.type(" ")
        # ------------------------

        # Instantly type the rest of the text message all at once
        await discord_page.keyboard.type(reply_text)
            
        # Press Enter to send
        await discord_page.keyboard.press("Enter")
        print("Response sent successfully!")

asyncio.run(main())
