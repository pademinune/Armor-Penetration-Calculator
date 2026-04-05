# Armor Penetration Calculator

<img width="284" height="270" alt="m4-100%" src="https://github.com/user-attachments/assets/bb634f0c-cd3c-4324-bae8-8f33afb2cd0c" />
<img width="300" height="328" alt="m4-34%" src="https://github.com/user-attachments/assets/0ac9168a-ffb3-41e4-a923-fd96e7ee82dd" />
<img width="238" height="233" alt="m4-1%" src="https://github.com/user-attachments/assets/a48185c4-c4fe-46c5-9a62-b7ff40a48450" />

*Photos were taken with a 125mm pen shell*

## Overview

This mod displays the exact effective armor value and penetration probability of a tank you are aiming at.

The mod factors in all relevant World of Tanks mechanics including shell-specific normalization, ricochet angles, spaced armor, and HEAT shell dissipation through spaced armor.

I made this mod because I was unsatisfied with the options found in big modpacks: they never computed and displayed the exact probability.

This mod also tells you when a shot will ricochet.

## Installation

Since this mod relies on [GUIFlash](https://github.com/CH4MPi/GUIFlash), you will need two `.wotmod` files.

### Install using the zip file (Recommended)

1. Download `unzip-me.zip` from the [latest release](https://github.com/pademinune/Armor-Penetration-Calculator/releases).

2. Put the zip file in your `mods/x.x.x.x/` folder found in your local
World of Tanks installation folder.

3. Unzip and extract the two `.wotmod` files into that folder.

4. Launch World of Tanks and the labels will appear when looking at an enemy
tank.

### Install without the zip file

1. Download the [latest version](https://github.com/pademinune/Armor-Penetration-Calculator/releases) of `armor-calculator-x.x.x.wotmod` from releases.

2. Download `guiflash_x.x.x.wotmod` from releases.

3. Put both mods in your `mods/x.x.x.x/` folder found in your local World of Tanks
installation folder.

4. Launch World of Tanks and the labels will appear when looking at an enemy
tank.

## Incompatibilities
- Hitmarker mod found in ProMod

## Probability Details

In World of Tanks, a shell's actual penetration is sampled from a Gaussian distribution ranging from 75% to 125% of its average penetration value. The 25% deviation from the mean is treated as the 3-sigma point.

For example, a shell with 100mm average penetration can roll anywhere from 75mm to 125mm, with most rolls clustering near 100mm.

So if you have 400mm penetration, bouncing off targets with under 350mm effective armor is very unlikely.
