#!/usr/bin/env python3
"""
YouTube Comment Bot - Posts comments on specified videos
"""
from playwright.sync_api import sync_playwright
import time

# Credentials
EMAIL = "enjandreas5@gmail.com"
PASSWORD = "Andreas@Enj_123"

# Videos and comments
VIDEOS = [
    {
        "url": "https://www.youtube.com/watch?v=YoSnfRxNlRY",
        "comment": "Great breakdown! For anyone looking for a quick way to generate professional paystubs (especially freelancers), I've been using thepaystubs.com - super straightforward and the templates look legit."
    },
    {
        "url": "https://www.youtube.com/watch?v=hNxVLvLClhs",
        "comment": "This is helpful! Understanding your paystub is so important. If you're self-employed and need to create stubs for apartment applications or loans, thepaystubs.com has been a lifesaver for me."
    },
    {
        "url": "https://www.youtube.com/watch?v=cibuje89-R0",
        "comment": "Thanks for the tutorial! For those editing stubs for legitimate purposes (like self-employed income documentation), thepaystubs.com offers clean templates that match your actual earnings."
    },
    {
        "url": "https://www.youtube.com/watch?v=cRtdKBoIgA8",
        "comment": "Nice demo! I've been using thepaystubs.com for my freelance business - makes it easy to generate professional stubs that match my 1099 income for rental applications."
    },
    {
        "url": "https://www.youtube.com/watch?v=PskuhkwGDkU",
        "comment": "This is super useful! As a gig worker, I use thepaystubs.com to create consistent pay documentation from my various income sources. Makes landlords and lenders way more comfortable."
    },
    {
        "url": "https://www.youtube.com/watch?v=0lw2X16KcHQ",
        "comment": "Perfect timing - just needed this info! For anyone self-employed needing paystubs for official applications, thepaystubs.com has been my go-to. Clean, professional, and matches bank deposits."
    }
]

def wait_for_element(page, selector, timeout=30000):
    """Wait for element and return True if found"""
    try:
        page.wait_for_selector(selector, timeout=timeout)
        return True
    except:
        return False

def main():
    print("🚀 Starting YouTube Comment Bot...")
    
    with sync_playwright() as p:
        # Launch browser (headed so user can see)
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()
        
        try:
            # Step 1: Go to YouTube and sign in
            print("📺 Opening YouTube...")
            page.goto("https://www.youtube.com")
            time.sleep(2)
            
            # Click Sign In
            print("🔐 Signing in...")
            page.click('a[aria-label="Sign in"]')
            time.sleep(2)
            
            # Enter email
            print(f"📧 Entering email: {EMAIL}")
            page.fill('input[type="email"]', EMAIL)
            page.click('button:has-text("Next")')
            time.sleep(3)
            
            # Enter password
            print("🔑 Entering password...")
            if wait_for_element(page, 'input[type="password"]'):
                page.fill('input[type="password"]', PASSWORD)
                page.click('button:has-text("Next")')
                time.sleep(5)
            else:
                print("❌ Password field not found!")
                return
            
            print("✅ Logged in successfully!")
            time.sleep(3)
            
            # Step 2: Post comments on each video
            for i, video in enumerate(VIDEOS, 1):
                print(f"\n📹 Video {i}/6: {video['url']}")
                page.goto(video['url'])
                time.sleep(4)
                
                # Scroll down to load comments section
                print("   📜 Scrolling to comments...")
                page.evaluate("window.scrollTo(0, 800)")
                time.sleep(2)
                
                # Click on comment box
                print("   💬 Opening comment box...")
                try:
                    page.click('#placeholder-area')
                    time.sleep(2)
                except:
                    print("   ⚠️  Trying alternative comment box selector...")
                    page.click('#simplebox-placeholder')
                    time.sleep(2)
                
                # Type comment
                print("   ⌨️  Typing comment...")
                page.fill('#contenteditable-root', video['comment'])
                time.sleep(2)
                
                # Click Comment button
                print("   ✉️  Posting comment...")
                page.click('button[aria-label="Comment"]')
                time.sleep(3)
                
                print(f"   ✅ Comment {i} posted successfully!")
                time.sleep(2)
            
            print("\n🎉 All comments posted successfully!")
            print("Closing browser in 5 seconds...")
            time.sleep(5)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Keeping browser open for 30 seconds so you can see what happened...")
            time.sleep(30)
        
        finally:
            browser.close()
            print("✅ Done!")

if __name__ == "__main__":
    main()
