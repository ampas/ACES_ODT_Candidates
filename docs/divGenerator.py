template = '''        <div class="juxtapose" data-startingposition="50%" data-showlabels="true"style="margin: 0 auto">>
            <img src="images/ACES_ODT_Candidate A rev008 - sRGB.XXXX.avif" data-label="A - SDR" />
            <img src="images/ACES_ODT_Candidate A rev008 - Rec.2100.XXXX.avif" data-label="A - HDR"  />
        </div>
        <div class="juxtapose" data-startingposition="50%" data-showlabels="true"style="margin: 0 auto">>
            <img src="images/ACES_ODT_Candidate C rev008 - sRGB.XXXX.avif" data-label="C - SDR" />
            <img src="images/ACES_ODT_Candidate C rev008 - Rec.2100.XXXX.avif" data-label="C - HDR"  />
        </div>'''


newDivs = []

for i in range(1,65):
    print(str(i).zfill(4))
    newDivs.append(template.replace('XXXX', str(i).zfill(4)))

for div in newDivs:
    print(div)