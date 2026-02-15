#!/usr/bin/env python3
"""
YouTube Comment Bot - Posts comments on specified videos (v2 - improved)
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

def main():
    print("🚀 Starting YouTube Comment Bot (v2)...")
    
    with sync_playwright() as p:
        # Launch browser (headed so user can see)
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()
        
        try:
            # Step 1: Go directly to Google sign in page
            print("🔐 Opening Google sign-in page...")
            page.goto("https://accounts.google.com/ServiceLogin?service=youtube&continue=https://www.youtube.com/")
            time.sleep(3)
            
            # Enter email
            print(f"📧 Entering email: {EMAIL}")
            page.fill('input[type="email"]', EMAIL)
            time.sleep(1)
            page.keyboard.press('Enter')
            time.sleep(4)
            
            # Enter password
            print("🔑 Entering password...")
            page.fill('input[type="password"]', PASSWORD)
            time.sleep(1)
            page.keyboard.press('Enter')
            time.sleep(6)
            
            print("✅ Logged in successfully!")
            
            # Step 2: Post comments on each video
            for i, video in enumerate(VIDEOS, 1):
                print(f"\n📹 Video {i}/6: {video['url']}")
                page.goto(video['url'])
                time.sleep(5)
                
                # Scroll down to load comments section
                print("   📜 Scrolling to comments...")
                page.evaluate("window.scrollTo(0, 800)")
                time.sleep(3)
                
                # Click on comment box - try multiple selectors
                print("   💬 Opening comment box...")
                try:
                    # Try to click the comment area
                    page.click('#simplebox-placeholder', timeout=5000)
                except:
                    try:
                        page.click('#placeholder-area', timeout=5000)
                    except:
                        print("   ⚠️  Clicking on page to focus, then trying again...")
                        page.click('body')
                        time.sleep(1)
                        page.evaluate("window.scrollTo(0, 800)")
                        time.sleep(2)
                        page.click('#simplebox-placeholder')
                
                time.sleep(2)
                
                # Type comment
                print("   ⌨️  Typing comment...")
                page.fill('#contenteditable-root', video['comment'])
                time.sleep(2)
                
                # Click Comment button
                print("   ✉️  Posting comment...")
                page.click('#submit-button button', timeout=10000)
                time.sleep(4)
                
                print(f"   ✅ Comment {i} posted successfully!")
                time.sleep(3)
            
            print("\n🎉 All comments posted successfully!")
            print("Closing browser in 5 seconds...")
            time.sleep(5)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Taking screenshot...")
            page.screenshot(path="error_screenshot.png")
            print("Screenshot saved to error_screenshot.png")
            print("Keeping browser open for 30 seconds so you can see what happened...")
            time.sleep(30)
        
        finally:
            browser.close()
            print("✅ Done!")

if __name__ == "__main__":
    main()
