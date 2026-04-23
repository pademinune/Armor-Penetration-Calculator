# Armor Penetration Calculator

<img width="284" height="270" alt="m4-100%" src="https://github.com/user-attachments/assets/bb634f0c-cd3c-4324-bae8-8f33afb2cd0c" />
<img width="300" height="328" alt="m4-34%" src="https://github.com/user-attachments/assets/0ac9168a-ffb3-41e4-a923-fd96e7ee82dd" />
<img width="238" height="233" alt="m4-1%" src="https://github.com/user-attachments/assets/a48185c4-c4fe-46c5-9a62-b7ff40a48450" />

*Photos were taken with a 125mm pen AP shell*

## Overview

This mod displays the exact effective armor value and penetration probability of a tank you are aiming at.

> *How is this different from other effective armor mods found in modpacks?*

They don't compute and display the exact probability of penetrating.
You would have to estimate this in the moment based on your shell's 
penetration and their armor.
This wastes crucial time and is very innacurate (especially since the distribution
is not uniform).

> *What is the best way to use this mod?*

Sometimes in battles, it is better to save your shot rather than
taking a chance on an orange pen indicator.
If you try to pen when you have a 20% chance, you will likely bounce
and take a shot in return for nothing.
Instead, it may be better to save your shot for a few seconds until you get
a better opportunity.

Also, when aiming at a well armored tank, with this mod you can find the
optimal spot to shoot that will maximize your chance of penning.

### Features
- Displays the exact effective armor value following game mechanics
    - Shell-specific normalization
    - Ricochet angles
    - Gun caliber overmatching
    - Spaced armor
    - HEAT shell dissipation through spaced armor
- Computes and displays probability of penetration
- Tells you if a shot will be a ricochet
- Great performance since the mod uses the calculatons already done
by the game
- Customize the mod to your liking by changing the settings

### Config
There is a settings gui for the config you can edit in the garage.

You can also change the display settings (text size, color, position) using the config file found in `mods/configs/pademinune`.
To revert back to default settings, just delete the config file and when you restart the game, the default file will be created again.

\*It does not work with HE shells yet as they have different mechanics.

## Installation

1. Download `unzip-me.zip` from the [latest release](https://github.com/pademinune/Armor-Penetration-Calculator/releases).

2. Put the zip file in your `mods/x.x.x.x/` folder found in your local
World of Tanks installation folder.

3. Unzip and extract the `.wotmod` files into that folder.

4. Launch World of Tanks and the labels will appear when looking at an enemy
tank.

## Incompatibilities
- Hitmarker mod found in ProMod

## Probability Details

In World of Tanks, a shell's actual penetration is sampled from a Gaussian distribution ranging from 75% to 125% of its average penetration value. The 25% deviation from the mean is treated as the 3-sigma point.

For example, a shell with 100mm average penetration can roll anywhere from 75mm to 125mm, with most rolls clustering near 100mm.

So if you have 400mm penetration, bouncing off targets with under 350mm effective armor is very unlikely.
