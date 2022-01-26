# ACES ODT Candidates
 Prebaked LUTs of the ACES 2.0 ODT candidates from the VWG

This repo contains a Nukescipt used to bake the LUTs, A dctl template to wrap them in a way Resolve will treat as a valid ACES ODT. And FilmLight Display Rendering Transforms intended for use in Baselight.


# Filmlight Baselight

## 1. Adding the DRTs to Baselight:
- copy all the files contained in `ACES2_0_Candidates_rev001` to `/vol/.support/etc/colourspaces`
- restart Baselight
- You should see three new custom DRTs in `Scene Settings -> Format & Colour -> Display Rendering Transform`




# Davinci Resolve

## 1. Adding a Custom ACES IDT or ODT File:
- Navigate to the "ACES Transforms" folder in Resolve's main application support folder.
    - MacOS: "~/Library/Application Support/Blackmagic Design/DaVinci Resolve/ACES Transforms"   double check folders again
    - Windows: "%AppData%\Blackmagic Design\\DaVinci Resolve\\Support\\ACES Transforms"
    - Linux: "~/.local/share/DaVinciResolve/ACES Transforms"
- Place your custom ACES DCTL files for Input Device Transforms (IDTs) in the IDT subfolder.
- Place your custom ACES DCTL files for Output Device Transforms (ODTs) in the ODT subfolder.
- Start Resolve.
