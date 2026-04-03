# Armor Penetration Calculator

<img width="305" height="260" alt="armor-penetration-calculator-thumbnail" src="https://github.com/user-attachments/assets/c4578694-29e5-444f-9273-4a256cf0eb67" />

## Overview

This mod displays the exact armor value and  probability of penetrating a tank that you are looking at.

The mod factors in all relevant world of tanks mechanics including shell-specific normalization, ricochet angles, spaced armor, and heat shell dissipation when hitting spaced armor.

I made this mod because I was unsatisfied with some of the other options found in big modpacks. They never computed and showed the exact probability.

This mod also tells you when a shot will be a ricochet.

## Probability details

In world of tanks, a shell's actual penetration value is given by a random number selected with a gaussian probability distribution from 75% to 125% of that shells average penetration.
From what I found online, I believe 3 standard deviations is 25% of avg shell pen. Please correct me if thats incorrect.

For example, if a shell has 100mm average pen, then minimum pen it can have is 75mm and the maximum pen it can have is 125mm.

Since the random distribution is gaussian, if you have 400mm pen, then most of your pen rolls will cluster around 400, and bouncing on targets with under 350mm armor is unlikely.
