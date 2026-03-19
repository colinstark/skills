---
name: design-1pager
description: This skill helps you write Design One-Pager.
license: MIT
metadata:
  author: Colin Stark
  version: "1.0.0"
  triggers: design one-pager, one-pager
---

# Design One-Pager generator
This is skill is there to help designers write clear, intentional one-pagers before jumping into solutioning.

- Is this internal to the design org, or product work? 
- Is this collaborative with other designers or solo?
- Who are the stakeholders? Ask for names
- Who are the partners of this project? What team? Designers involved, Engineers involved, who's the PM? Ask for Names)
- What's the user story/stories? What problem are you solving, and for who?
- Let the user describe the problem or the current situations, ask some questions if unclear
- Is there existing research?
- Suggest what metrics this should touch. What should increase? What should decrease? What should not be affected as a side effect? Ask if you can't come up with some
- Propose and validate the metrics with the user
- Iterate on potential solutions with the user, be proactive but ask for confirmation
- 
## Related skill
- problem-definition

## Result
You should return a nicely formatted one-pager with the following structure
0. Project title
1. Stakeholders & Partners
2. Problem statement
3. User stories ("As a __, I want to __, so I can __")
4. Research
5. Potential Solutions
6. Metrics (Increase/Decrease/Keep)
7. Links & References (empty, to be filled later)
