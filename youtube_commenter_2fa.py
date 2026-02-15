#!/usr/bin/env python3
"""
YouTube Comment Bot - With 2FA support
"""
from playwright.sync_api import sync_playwright
import time

# Credentials
EMAIL = "enjandreas5@gmail.com"
PASSWORD = "Andreas@Enj_123"
VERIFICATION_CODE = "710136"

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
    print("🚀 Starting YouTube Comment Bot with 2FA...")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False, slow_mo=800)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()
        
        try:
            # Step 1: Go to Google sign in
            print("🔐 Opening Google sign-in...")
            page.goto("https://accounts.google.com/ServiceLogin?service=youtube&continue=https://www.youtube.com/")
            time.sleep(3)
            
            # Enter email
            print(f"📧 Entering email: {EMAIL}")
            page.fill('input[type="email"]', EMAIL)
            time.sleep(1)
            page.keyboard.press('Enter')
            time.sleep(5)
            
            # Enter password
            print("🔑 Entering password...")
            page.wait_for_selector('input[type="password"]', state='visible', timeout=10000)
            page.fill('input[type="password"]', PASSWORD)
            time.sleep(1)
            page.keyboard.press('Enter')
            time.sleep(6)
            
            # Check for 2FA prompt
            print("🔐 Checking for 2FA prompt...")
            try:
                # Look for verification code input
                verification_input = page.wait_for_selector('input[type="tel"]', timeout=5000)
                print(f"✅ Found 2FA prompt! Entering code: {VERIFICATION_CODE}")
                page.fill('input[type="tel"]', VERIFICATION_CODE)
                time.sleep(1)
                page.keyboard.press('Enter')
                time.sleep(5)
            except:
                print("ℹ️  No 2FA prompt detected, continuing...")
            
            # Handle any "Trust this device?" prompts
            try:
                if page.locator('text="Trust this device?"').is_visible(timeout=3000):
                    print("📱 Clicking 'Trust this device'...")
                    page.click('button:has-text("Continue")')
                    time.sleep(3)
            except:
                pass
            
            print("✅ Login complete! Starting comments...")
            time.sleep(3)
            
            # Step 2: Post comments on each video
            for i, video in enumerate(VIDEOS, 1):
                print(f"\n📹 Video {i}/6: {video['url']}")
                page.goto(video['url'])
                time.sleep(6)
                
                # Scroll to comments
                print("   📜 Scrolling to comments...")
                for scroll in range(3):
                    page.evaluate("window.scrollBy(0, 300)")
                    time.sleep(0.5)
                time.sleep(2)
                
                # Click comment box
                print("   💬 Clicking comment box...")
                try:
                    page.click('#simplebox-placeholder', timeout=8000)
                except:
                    try:
                        page.click('#placeholder-area', timeout=5000)
                    except:
                        print("   ⚠️  Trying click by coordinates...")
                        page.evaluate("window.scrollTo(0, 800)")
                        time.sleep(2)
                        page.click('#simplebox-placeholder')
                
                time.sleep(2)
                
                # Type comment
                print("   ⌨️  Typing comment...")
                comment_box = page.locator('#contenteditable-root')
                comment_box.click()
                time.sleep(1)
                comment_box.fill(video['comment'])
                time.sleep(2)
                
                # Submit
                print("   ✉️  Posting...")
                try:
                    page.click('#submit-button button', timeout=8000)
                except:
                    page.click('button[aria-label="Comment"]', timeout=5000)
                
                time.sleep(5)
                print(f"   ✅ Comment #{i} posted!")
                time.sleep(2)
            
            print("\n" + "="*60)
            print("🎉 ALL 6 COMMENTS POSTED SUCCESSFULLY!")
            print("="*60)
            print("\nClosing in 5 seconds...")
            time.sleep(5)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Taking screenshot...")
            try:
                page.screenshot(path="error_screenshot.png")
                print("Saved to error_screenshot.png")
            except:
                pass
            print("Browser staying open for 30s...")
            time.sleep(30)
        
        finally:
            try:
                browser.close()
            except:
                pass
            print("✅ Done!")

if __name__ == "__main__":
    main()
