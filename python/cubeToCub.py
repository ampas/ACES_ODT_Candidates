
def cubeToCub(cubePath,cubPath):
    inputCubePath = cubePath
    ouputCubPath = cubPath

    # read the cube
    with open(inputCubePath) as f:
        lines = f.readlines()

    # header
    tlHeader = '''# Truelight Cube v2.1
    # iDims     3
    # oDims     3
    # width     65 65 65\n
    # Cube'''

    # footer
    tlFooter = '''\n# end\n'''


    LUTlines = lines[2:]
    LUTlines = [x.replace('\n','').split(' ') for x in LUTlines]
    LUTlines = [[float(i) for i in x] for x in LUTlines]
    LUTlines = [[str(i) for i in x] for x in LUTlines]

    ## remove decimal from 0.0 and 1.0
    for i, x in enumerate(LUTlines):
        for j, a in enumerate(x):
            if '0.0' == a:
                LUTlines[i][j] = '0'
            if '1.0' == a:
                LUTlines[i][j] = '1'

    # reconstruct the cube string
    stringLUTlines = []
    for line in LUTlines:
        stringLUTlines.append(' '.join(line))
    newLUTStringBlock = '\n'.join(stringLUTlines)

    # join it all up
    outputContents = tlHeader + '\n' + newLUTStringBlock + '\n' + tlFooter

    # check directory for outputCubPath exists, if not, create it
    if not os.path.exists(os.path.dirname(ouputCubPath)):
        os.makedirs(os.path.dirname(ouputCubPath))

    # write the file
    with open(ouputCubPath, 'w') as f:
        f.write(outputContents)


inputCubePath = '/Users/afry/GitHub/ACES_ODT_Candidates/DaVinci Resolve/ACES Transforms/ODT/ACES2.0 Candidates rev001/ACES2.0 CandidateA rev001 Rec709.cube'
ouputCubPath = inputCubePath.replace('.cube', '_truelight.cub')
cubeToCub(inputCubePath,ouputCubPath)