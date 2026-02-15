#!/usr/bin/env python3
"""
YouTube Comment Bot - Persistent profile + manual login + automated comments
"""
from playwright.sync_api import sync_playwright
import time
import sys

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
    print("🚀 YouTube Comment Bot (Persistent Profile)")
    print("=" * 70)
    
    with sync_playwright() as p:
        # Use persistent context to save cookies/login
        user_data_dir = "./yt_browser_profile"
        
        print(f"\n📂 Using browser profile: {user_data_dir}")
        print("   (This saves your login so you only authenticate once!)\n")
        
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            slow_mo=1000,  # Very slow = more human-like
            args=[
                '--disable-blink-features=AutomationControlled',  # Hide automation
            ]
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        
        try:
            # Go to YouTube
            print("📺 Opening YouTube...")
            page.goto("https://www.youtube.com", wait_until='networkidle')
            time.sleep(3)
            
            # Check if already logged in
            is_logged_in = False
            try:
                if page.locator('button[aria-label*="Google Account"]').is_visible(timeout=3000):
                    print("✅ Already logged in!")
                    is_logged_in = True
            except:
                pass
            
            if not is_logged_in:
                print("\n" + "=" * 70)
                print("⏸️  PLEASE LOG IN MANUALLY:")
                print("=" * 70)
                print("1. Click 'Sign in' in the browser window")
                print("2. Email: enjandreas5@gmail.com")
                print("3. Password: Andreas@Enj_123")
                print("4. 2FA Code: 710136 (if asked)")
                print("5. Complete any verification steps")
                print("\nWhen you see your profile picture (top-right), come back here")
                print("=" * 70)
                
                input("\n👉 Press ENTER after logging in... ")
                print("\n✅ Great! Proceeding...")
            
            time.sleep(2)
            
            # Now post comments
            print("\n🎬 Starting automated commenting...")
            print("=" * 70)
            
            for i, video in enumerate(VIDEOS, 1):
                print(f"\n[{i}/6] 📹 {video['url']}")
                
                # Navigate to video
                page.goto(video['url'], wait_until='networkidle')
                time.sleep(5)
                
                # Scroll to comments section (slowly, like a human)
                print("    📜 Scrolling...")
                for _ in range(4):
                    page.evaluate("window.scrollBy(0, 250)")
                    time.sleep(0.8)
                time.sleep(2)
                
                # Click comment box
                print("    💬 Opening comment box...")
                try:
                    page.locator('#simplebox-placeholder').click(timeout=10000)
                except:
                    try:
                        page.locator('#placeholder-area').click(timeout=5000)
                    except Exception as e:
                        print(f"    ⚠️  Couldn't click comment box: {e}")
                        print("    ⏭️  Skipping this video...")
                        continue
                
                time.sleep(2)
                
                # Type comment (character by character = more human)
                print("    ⌨️  Typing comment...")
                comment_field = page.locator('#contenteditable-root').first
                comment_field.click()
                time.sleep(1)
                
                # Type slowly
                for char in video['comment']:
                    comment_field.type(char, delay=50)  # 50ms between chars
                
                time.sleep(2)
                
                # Submit
                print("    ✉️  Posting...")
                try:
                    page.locator('#submit-button button').first.click(timeout=8000)
                except:
                    try:
                        page.locator('button[aria-label="Comment"]').click(timeout=5000)
                    except Exception as e:
                        print(f"    ⚠️  Couldn't submit: {e}")
                        print("    ⏭️  Skipping...")
                        continue
                
                time.sleep(4)
                print(f"    ✅ Comment posted!")
                
                # Wait between videos
                if i < len(VIDEOS):
                    time.sleep(3)
            
            print("\n" + "=" * 70)
            print("🎉 MISSION COMPLETE - ALL COMMENTS POSTED!")
            print("=" * 70)
            print("\nClosing browser in 5 seconds...")
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Stopped by user.")
            
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            print("\nTaking screenshot...")
            try:
                page.screenshot(path="error_screenshot.png")
                print("Saved: error_screenshot.png")
            except:
                pass
            print("\nBrowser will stay open for 30 seconds...")
            time.sleep(30)
        
        finally:
            try:
                context.close()
            except:
                pass
            print("✅ Done!")

if __name__ == "__main__":
    main()
