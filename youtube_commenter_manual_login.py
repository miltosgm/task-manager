#!/usr/bin/env python3
"""
YouTube Comment Bot - Manual login, automated commenting
"""
from playwright.sync_api import sync_playwright
import time

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
    print("🚀 Starting YouTube Comment Bot (Manual Login Version)...")
    
    with sync_playwright() as p:
        # Launch browser with persistent context (saves cookies)
        user_data_dir = "./youtube_profile"
        browser = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            slow_mo=300
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        try:
            # Step 1: Open YouTube and wait for manual login
            print("\n📺 Opening YouTube...")
            print("=" * 60)
            page.goto("https://www.youtube.com")
            time.sleep(3)
            
            print("\n⏸️  PLEASE LOG IN MANUALLY NOW!")
            print("=" * 60)
            print("Email: enjandreas5@gmail.com")
            print("Password: Andreas@Enj_123")
            print("\n1. Click 'Sign in' button in the browser")
            print("2. Enter the email and password")
            print("3. Complete any verification if needed")
            print("4. When you see your profile pic in top right, press ENTER here...")
            print("=" * 60)
            
            input("\n👉 Press ENTER after you've logged in successfully...")
            
            print("\n✅ Great! Starting to post comments...")
            
            # Step 2: Post comments on each video
            for i, video in enumerate(VIDEOS, 1):
                print(f"\n📹 Video {i}/6: {video['url']}")
                page.goto(video['url'])
                time.sleep(5)
                
                # Scroll down to load comments section
                print("   📜 Scrolling to comments...")
                page.evaluate("window.scrollTo(0, 800)")
                time.sleep(3)
                
                # Click on comment box
                print("   💬 Opening comment box...")
                try:
                    page.click('#simplebox-placeholder', timeout=5000)
                except:
                    try:
                        page.click('#placeholder-area', timeout=5000)
                    except:
                        print("   ⚠️  Trying alternative method...")
                        page.evaluate("window.scrollTo(0, 800)")
                        time.sleep(2)
                        page.click('div#simple-box div#placeholder-area', timeout=10000)
                
                time.sleep(2)
                
                # Type comment in the focused contenteditable
                print("   ⌨️  Typing comment...")
                page.locator('#contenteditable-root').fill(video['comment'])
                time.sleep(2)
                
                # Click Comment button
                print("   ✉️  Posting comment...")
                try:
                    page.click('button#submit-button:has-text("Comment")', timeout=5000)
                except:
                    # Alternative selector
                    page.click('#submit-button button[aria-label="Comment"]', timeout=5000)
                
                time.sleep(4)
                
                print(f"   ✅ Comment {i} posted successfully!")
                time.sleep(3)
            
            print("\n" + "=" * 60)
            print("🎉 ALL COMMENTS POSTED SUCCESSFULLY!")
            print("=" * 60)
            print("\nClosing browser in 5 seconds...")
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user. Exiting...")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\nTaking screenshot...")
            try:
                page.screenshot(path="error_screenshot.png")
                print("Screenshot saved to error_screenshot.png")
            except:
                pass
            print("\nKeeping browser open for 30 seconds...")
            time.sleep(30)
        
        finally:
            browser.close()
            print("✅ Done!")

if __name__ == "__main__":
    main()
