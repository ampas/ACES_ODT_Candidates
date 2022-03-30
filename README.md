# ACES ODT Candidates
 Prebaked LUTs of the ACES 2.0 ODT candidates from the [ACES Output Transforms Architecture Virtual Working Group](https://paper.dropbox.com/doc/Output-Transforms-Architecture-Virtual-Working-Group-HKNpj824NA0Z8tn7jiPS0)

This repo contains:
* a Nukescipt used to bake the LUTs.
* A dctl template to wrap them in a way Resolve will treat as a valid ACES ODT.
* A FilmLight Display Rendering Transforms intended for use in Baselight.

There is a HDR YouTube clip comparing these 3 versions [here](https://www.youtube.com/watch?v=s8f1MylJLN0). It should only be viewed on a HDR display, as SDR playback will be passing through YouTube's tonemapper, which dramatically effects the look.


# Overview

## Candidate A
This represents a minimal departure from the existing ACES 1.2 transforms.
Some minor colour tweaks collectively known as the RRT Sweeteners have been removed.
The c9 (SDR) and SSTS (HDR) tonescales have both been replaced with the Michaelis-Menten Spring Dual-Contrast (MMSDC) curve, still applied as a per channel RGB lookup in the AP1 rendering space. Mapping down to the final display gamut is a simple matrix, as used in the existing ACES Display Transforms.

## Candidate B
Is a mathematically minimal approach that tries to preserve hue, whilst leaving as many options open for the user as possible.
It applies the same MMSDC tonecurve in a way that preserves chart linear hue lines, allowing for improved SDR to HDR colour rendering. But leaves the final mapping down to the target display gamut to the user, allowing greater choice in the approach taken here.

## Candidate C
Is a more complex approach that pushes the scene-referred data into a perceptually driven colour appearance model, and does the tonemapping and explicit target display gamut compression in that space. Representation of light intensity is prioritised over saturation. And perceptual hue consistency is prioritised over absolute saturation. 


# Installation

## Filmlight Baselight

### 1. Adding the DRTs to Baselight:
- Copy all the files contained in `ACES2_0_Candidates_rev007` to `/vol/.support/etc/colourspaces`
- Restart Baselight
- You should see three new custom DRTs in `Scene Settings -> Format & Colour -> Display Rendering Transform`


## Davinci Resolve

### 1. Adding a Custom ACES IDT or ODT File:
- Navigate to the `ACES Transforms` folder in Resolve's application support folder.
    - MacOS: `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/ACES Transforms`
    - Windows: `C:\Users\<User>\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\ACES Transforms\IDT`
    - Linux: `~/.local/share/DaVinciResolve/ACES Transforms`
- Place your custom ACES DCTL files for Input Device Transforms (IDTs) in the IDT subfolder.
- Place your custom ACES DCTL files for Output Device Transforms (ODTs) in the ODT subfolder.
- Start Resolve.
