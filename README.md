# GPU Power Limit vs. Performance-per-Watt Characterization

## Objective
Measure how the power limit of an AMD Radeon RX 9070 (GIGABYTE GAMING OC) affects
benchmark score, average board power, peak temperature and clock speed, with the
fan held at 100%, and find the setting with the best performance per watt.

**Why this matters.** Embedded and shipboard computers run in sealed,
space-limited enclosures with fixed power budgets and limited cooling, so
engineers care about performance per watt as much as raw speed. This project
tests a desktop GPU, not military hardware, but it measures the same trade-off:
how much performance is given up as a power cap is lowered, and how much power
and heat that saves.

## Hypothesis
I predict performance-per-watt (score ÷ average watts) will be highest at -20% 
because reducing the power limit improves energy efficiency by lowering power 
consumption while letting the GPU maintain most of its clock speed and performance. 
At higher power limits, the GPU uses more electricity for only small performance gains. 
I predict the score at -30% will be about 15% below stock, and the +10% setting will 
raise the score by about 2%. 