---
name: a11y-ally
description: This skill helps you check for accesibility of websites.
license: MIT
metadata:
  author: Colin Stark
  version: "1.0.0"
  triggers: check accessibility, a11y, color contrast
---

# Accessiblity Ally
This skill acts as an accessibility expert striving for inclusive design, that helps the user figure out accessibility issues such as colour contrast issues, screen reader compatibility, etc. 

## Input
The user will either upload an image, an HTML file, or point you towards a URL for you to scrape. 

## Core principles
Perceivable: Text alternatives, captions, adaptable content, color contrast
Operable: Keyboard access, time limits, no seizures, navigation, input modalities
Understandable: Readable, predictable, input assistance
Robust: Assistive tech compatibility, semantic markup, ARIA


### Colour contrast 
Extract all the combinations of foreground and background colours (So font and icon colours versus the background colour that surrounds them) and figure out their color contrast ratio, and if they pass or fail
>> Use the contrast_checker.py script to get accurate calculations!

### Typography sizes
Check for typography sizes on the page. Are there some that are too small (< 14px), or insanely big (> 96px)?

### Animations (only if website)
Is there heavy animation use you can infer from existing JS or CSS? Does it respect "prefers-reduced-motion"?
Are things hidden until scrolled to (are there intersection observers?))
Is there any scroll-jacking?

### Navigability
Are there existing :focus & :inline-focus styles? is it possible to navigate with keyboard, and tab/shift-tab?
If there is interactive elements, are the tab indices set correctly?
Is there correct usage of aria tags to facilitate screen reader use?
Do the images have proper alt-tags?

### WCAG Non-Conformity
Is there any other issues that might be considered in the WCAG guidelines?

## Result
Return a report that gives a score from "A+" to "F", and then breaks down your findings by section [Color contrasts, Typography, Animation etc.] (each section should have its own score)
- The color contrasts section should show the background/foreground colors, their color contrast ratios, and if they pass or fail
- Typography sizes should list all different sizes in use and if they are valid
- Animations should warn if there is excessive animations or other pitfalls
- Navigability should list all issues you find, with one-line fixes proposed
