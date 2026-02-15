#!/bin/bash
# Post YouTube comments via browser control

VIDEOS=(
  "https://www.youtube.com/watch?v=YoSnfRxNlRY"
  "https://www.youtube.com/watch?v=hNxVLvLClhs"
  "https://www.youtube.com/watch?v=cibuje89-R0"
  "https://www.youtube.com/watch?v=cRtdKBoIgA8"
  "https://www.youtube.com/watch?v=PskuhkwGDkU"
  "https://www.youtube.com/watch?v=0lw2X16KcHQ"
)

COMMENTS=(
  "Great breakdown! For anyone looking for a quick way to generate professional paystubs (especially freelancers), I've been using thepaystubs.com - super straightforward and the templates look legit."
  "This is helpful! Understanding your paystub is so important. If you're self-employed and need to create stubs for apartment applications or loans, thepaystubs.com has been a lifesaver for me."
  "Thanks for the tutorial! For those editing stubs for legitimate purposes (like self-employed income documentation), thepaystubs.com offers clean templates that match your actual earnings."
  "Nice demo! I've been using thepaystubs.com for my freelance business - makes it easy to generate professional stubs that match my 1099 income for rental applications."
  "This is super useful! As a gig worker, I use thepaystubs.com to create consistent pay documentation from my various income sources. Makes landlords and lenders way more comfortable."
  "Perfect timing - just needed this info! For anyone self-employed needing paystubs for official applications, thepaystubs.com has been my go-to. Clean, professional, and matches bank deposits."
)

for i in {0..5}; do
  echo "===== Video $((i+1))/6 ====="
  echo "URL: ${VIDEOS[$i]}"
  echo "Comment: ${COMMENTS[$i]}"
  echo ""
done
