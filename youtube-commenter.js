const { chromium } = require('playwright');

const videos = [
  'https://www.youtube.com/watch?v=YoSnfRxNlRY',
  'https://www.youtube.com/watch?v=hNxVLvLClhs',
  'https://www.youtube.com/watch?v=cibuje89-R0',
  'https://www.youtube.com/watch?v=cRtdKBoIgA8',
  'https://www.youtube.com/watch?v=PskuhkwGDkU',
  'https://www.youtube.com/watch?v=0lw2X16KcHQ'
];

const comments = [
  "Great breakdown! For anyone looking for a quick way to generate professional paystubs (especially freelancers), I've been using thepaystubs.com - super straightforward and the templates look legit.",
  "This is helpful! Understanding your paystub is so important. If you're self-employed and need to create stubs for apartment applications or loans, thepaystubs.com has been a lifesaver for me.",
  "Thanks for the tutorial! For those editing stubs for legitimate purposes (like self-employed income documentation), thepaystubs.com offers clean templates that match your actual earnings.",
  "Nice demo! I've been using thepaystubs.com for my freelance business - makes it easy to generate professional stubs that match my 1099 income for rental applications.",
  "This is super useful! As a gig worker, I use thepaystubs.com to create consistent pay documentation from my various income sources. Makes landlords and lenders way more comfortable.",
  "Perfect timing - just needed this info! For anyone self-employed needing paystubs for official applications, thepaystubs.com has been my go-to. Clean, professional, and matches bank deposits."
];

async function createGoogleAccount(browser) {
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    console.log('Creating Google account...');
    await page.goto('https://accounts.google.com/signup');
    await page.waitForTimeout(2000);
    
    // Generate random account details
    const randomNum = Math.floor(Math.random() * 10000);
    const email = `paystub.user${randomNum}@gmail.com`;
    const password = 'PayStub2026!Secure' + randomNum;
    const firstName = 'PayStub';
    const lastName = 'User' + randomNum;
    
    // Fill in the form
    await page.fill('input[name="firstName"]', firstName);
    await page.fill('input[name="lastName"]', lastName);
    await page.click('button:has-text("Next")');
    await page.waitForTimeout(2000);
    
    // Birth date and gender
    await page.selectOption('select#month', '5'); // May
    await page.fill('input#day', '15');
    await page.fill('input#year', '1990');
    await page.selectOption('select#gender', '3'); // Rather not say
    await page.click('button:has-text("Next")');
    await page.waitForTimeout(2000);
    
    // Try to create email
    await page.click('text=Create your own Gmail address');
    await page.waitForTimeout(1000);
    await page.fill('input[name="Username"]', `paystubuser${randomNum}`);
    await page.click('button:has-text("Next")');
    await page.waitForTimeout(2000);
    
    // Password
    await page.fill('input[name="Passwd"]', password);
    await page.fill('input[name="ConfirmPasswd"]', password);
    await page.click('button:has-text("Next")');
    await page.waitForTimeout(2000);
    
    console.log('Account created:');
    console.log('Email:', `paystubuser${randomNum}@gmail.com`);
    console.log('Password:', password);
    
    return {
      email: `paystubuser${randomNum}@gmail.com`,
      password: password,
      context: context
    };
  } catch (error) {
    console.error('Error creating account:', error.message);
    await context.close();
    return null;
  }
}

async function postComment(page, videoUrl, comment) {
  try {
    console.log(`\nNavigating to: ${videoUrl}`);
    await page.goto(videoUrl);
    await page.waitForTimeout(5000);
    
    // Scroll down to load comments section
    await page.evaluate(() => window.scrollBy(0, 500));
    await page.waitForTimeout(2000);
    
    // Click on comment box
    const commentBox = await page.locator('#placeholder-area').first();
    await commentBox.click();
    await page.waitForTimeout(1000);
    
    // Type comment
    const textArea = await page.locator('#contenteditable-root').first();
    await textArea.fill(comment);
    await page.waitForTimeout(1000);
    
    // Click post button
    const postButton = await page.locator('#submit-button').first();
    await postButton.click();
    await page.waitForTimeout(3000);
    
    console.log('✓ Comment posted successfully!');
    return true;
  } catch (error) {
    console.error('Error posting comment:', error.message);
    return false;
  }
}

async function main() {
  console.log('Starting YouTube commenting automation...\n');
  
  const browser = await chromium.launch({
    headless: false,  // Show browser for debugging
    args: ['--start-maximized']
  });
  
  // Create Google account
  const account = await createGoogleAccount(browser);
  
  if (!account) {
    console.error('Failed to create Google account');
    await browser.close();
    return;
  }
  
  const page = await account.context.newPage();
  
  // Navigate to YouTube
  console.log('\nNavigating to YouTube...');
  await page.goto('https://www.youtube.com');
  await page.waitForTimeout(3000);
  
  // Post comments on each video
  let successCount = 0;
  for (let i = 0; i < videos.length; i++) {
    const success = await postComment(page, videos[i], comments[i]);
    if (success) successCount++;
    await page.waitForTimeout(5000); // Wait between posts to avoid spam detection
  }
  
  console.log(`\n✓ Done! Posted ${successCount}/${videos.length} comments`);
  console.log('\nAccount Details:');
  console.log('Email:', account.email);
  console.log('Password:', account.password);
  
  await page.waitForTimeout(5000);
  await browser.close();
}

main().catch(console.error);
