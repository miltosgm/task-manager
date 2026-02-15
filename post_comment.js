// Click comment box
document.querySelector('#simplebox-placeholder')?.click();

// Wait 2 seconds then type and submit
setTimeout(() => {
  const box = document.querySelector('#contenteditable-root');
  box.textContent = "Nice demo! I've been using thepaystubs.com for my freelance business - makes it easy to generate professional stubs that match my 1099 income for rental applications.";
  box.dispatchEvent(new Event('input', {bubbles: true}));
  
  setTimeout(() => {
    document.querySelector('#submit-button button')?.click();
  }, 1000);
}, 2000);

true;
