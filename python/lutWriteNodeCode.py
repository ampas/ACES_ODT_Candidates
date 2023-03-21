### This code is embedded in the nukescript, not accessed from here





import os
import shutil


masterNode = nuke.thisNode()


bakeLuts = nuke.thisNode().knob('bakeLUTs').value()


def cubeToCub(cubePath,cubPath):
    inputCubePath = cubePath
    ouputCubPath = cubPath

    # read the cube
    with open(inputCubePath) as f:
        lines = f.readlines()

    cubeSize = lines[1].split(' ')[1].replace('\n','')

    # header
    tlHeader = '''# Truelight Cube v2.1
    # iDims     3
    # oDims     3
    # width     CUBESIZE CUBESIZE CUBESIZE\n
    # Cube'''

    tlHeader = tlHeader.replace('CUBESIZE',cubeSize)

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





def bakeCandidateLUTfromNode(node,inverse=False):
    candidate = node.knob('candidate').value()
    revision = node.knob('revision').value()
    target = node.knob('target').value()





    nukeScriptDir = nuke.script_directory()
    print(nukeScriptDir)
    dctltemplatePath = os.path.join(nukeScriptDir,node.knob('dctlTemplate').evaluate())
    if inverse:
        dctltemplatePath = dctltemplatePath.replace('.dctl','_inverse.dctl')

    fltransformTemplatePath = os.path.join(nukeScriptDir,node.knob('fltransformTemplate').evaluate())
    # flSpacePath = os.path.join(nukeScriptDir,'resources/ACEScct_AP0.flspace')
    # print(flSpacePath)





    cubePath = os.path.join(nukeScriptDir,node.knob('cubePath').evaluate())
    cubePathClean = cubePath.replace('(','').replace(')','')
    ocioCubePath = os.path.join(nukeScriptDir,node.knob('ocioCubePath').evaluate())
    cubPath = os.path.join(nukeScriptDir,node.knob('cubPath').evaluate())

    if inverse:
        cubePath = cubePath.replace('.cube','_inverse.cube')
        cubePathClean = cubePathClean.replace('.cube','_inverse.cube')
        ocioCubePath = ocioCubePath.replace('.cube','_inverse.cube')
        cubPath = cubPath.replace('.cub','_inverse.cub')

    # replace LUT writer path with evaluated path
    node.knob('file').setValue(cubePath)





    # check cubePath exists, if not, create it
    if not os.path.exists(os.path.dirname(cubePath)):
        os.makedirs(os.path.dirname(cubePath))




    # check ocioCubePath exists, if not, create it
    if not os.path.exists(os.path.dirname(ocioCubePath)):
        os.makedirs(os.path.dirname(ocioCubePath))

    dctlPath = cubePath.replace('.cube','.dctl')
    if inverse:
        dctlPath = dctlPath.replace('/ODT/','/IDT/')

    # check dctlPath exists, if not, create it
    if not os.path.exists(os.path.dirname(dctlPath)):
        os.makedirs(os.path.dirname(dctlPath))

    cubeName = cubePath.split('/').pop(-1)
    cubeNameClean = cubeName.replace('(','').replace(')','')






    if bakeLuts == True:
        node.knob('generate').execute()
        # if cubeName does not match cubeNameClean copy cubeName to cubeNameClean
        if cubePath != cubePathClean:
            shutil.copy(cubePath,cubePathClean)


    # read contents of cube file
    with open(cubePathClean) as f:
        cubelines = f.readlines()



    ## write the dctl file
    with open(dctltemplatePath) as f:
        lines = f.readlines()
    newLines = [x.replace('replace.cube',cubeNameClean) for x in lines]
    # replace the string REPLACE_WITH_CUBE_DATA with the contents of cubelines
    newLines = [x.replace('REPLACE_WITH_CUBE_DATA',''.join(cubelines)) for x in newLines]

    with open(dctlPath, 'w') as f:
        f.write(''.join(newLines))





    # Baselight
    # convert cube to cub
    cubeToCub(cubePath,cubPath)

    # copy cubePath to ocioCubePath
    shutil.copy(cubePath,ocioCubePath)

    # # remove original cube if it isnt the same as the clean version
    # if cubePathClean != cubePath:
    #     # delete cubeName
        # os.remove(cubePath)
    if os.path.exists(cubePath):
        os.remove(cubePath)
    if os.path.exists(cubePathClean):
        os.remove(cubePathClean)





    ## write the fltransform
    if target == 'Rec709':
        if  inverse == False:
            fltransformPath = cubPath.replace('.cub','.fltransform')
            cubeToken = os.path.basename(cubPath.replace('_Rec709','').replace('.cub',''))
            with open(fltransformTemplatePath) as f:
                lines = f.readlines()
            newLines = [x.replace('replaceTransformName','ACES 2.0 Candidate'+ candidate + ' rev'+revision) for x in lines]
            newLines = [x.replace('replaceForward',cubeToken) for x in newLines]
            # newLines = [x.replace('replaceForward_Rec2100',os.path.basename(cubPath).replace('Rec709','Rec2100').replace('.cub','')) for x in newLines]
            with open(fltransformPath, 'w') as f:
                f.write(''.join(newLines))





    # check ACEScct_AP0.flspace exists, if not, copy it
    for flspace in ['/ACEScct_AP0.flspace','/ACEScct_APS4.flspace']:
        flSpaceSourcePath = os.path.join(nukeScriptDir,'resources' + flspace)
        flSpaceDestPath = os.path.dirname(cubPath) + flspace
        if not os.path.exists(flSpaceDestPath):
            shutil.copy(flSpaceSourcePath,flSpaceDestPath)





def createOCIOconfigs(revision):
    nukeScriptDir = nuke.script_directory()
    revision = nuke.thisNode().knob('revision').value()
    ocioTemplateDir = os.path.join(nukeScriptDir,'resources/')
    newOcioTemplateDir = os.path.join(nukeScriptDir,'OCIO/')
    ocioConfigTemplates = [x for x in os.listdir(ocioTemplateDir) if x.endswith('.ocio')]
    ocioConfigTemplatePaths = [os.path.join(ocioTemplateDir,x) for x in ocioConfigTemplates]


    activeViewDicts = []
    activeViewDicts.append({'name':'All','values':[
        'ACES 1.2 - Rec.709',
        'ACES 1.2 - Rec2100',
        'ACES 1.2 - Rec2100 (Rec709 sim)',
        'ACES 1.2 - DisplayP3 (Rec.709 Limited)',
        'ACES 1.2 - DisplayP3 (P3D65 1000nit Limited)',
        'ACES 2.0 Candidate CAMDRT revXXX - Rec.709',
        'ACES 2.0 Candidate CAMDRT revXXX - P3D65',
        'ACES 2.0 Candidate CAMDRT revXXX - P3D65 (Rec709 sim)',
        'ACES 2.0 Candidate CAMDRT revXXX - Rec.2100 (Rec709 sim)',
        'ACES 2.0 Candidate CAMDRT revXXX - Rec.2100 (P3D65 540nit Limited)',
        'ACES 2.0 Candidate CAMDRT revXXX - Rec.2100 (P3D65 1000nit Limited)',
        'ACES 2.0 Candidate CAMDRT revXXX - DisplayP3 (Rec.709 Limited)',
        'ACES 2.0 Candidate CAMDRT revXXX - DisplayP3 (P3D65 Limited)',
        'ACES 2.0 Candidate CAMDRT revXXX - DisplayP3 (P3D65 540nit Limited)',
        'ACES 2.0 Candidate CAMDRT revXXX - DisplayP3 (P3D65 1000nit Limited)',
        ]})

    activeViewDicts.append({'name':'DisplayP3','values':[
        'ACES 1.2 - DisplayP3 (Rec.709 Limited)',
        'ACES 1.2 - DisplayP3 (P3D65 1000nit Limited)',
        'ACES 2.0 Candidate CAMDRT revXXX - DisplayP3 (Rec.709 Limited)',
        'ACES 2.0 Candidate CAMDRT revXXX - DisplayP3 (P3D65 Limited)',
        'ACES 2.0 Candidate CAMDRT revXXX - DisplayP3 (P3D65 540nit Limited)',
        'ACES 2.0 Candidate CAMDRT revXXX - DisplayP3 (P3D65 1000nit Limited)',
        ]})

    activeViewDicts.append({'name':'Limited','values':[
        'ACES 1.2 - Rec.709',
        'ACES 1.2 - Rec2100',
        'ACES 1.2 - Rec2100 (Rec709 sim)',
        'ACES 2.0 Candidate CAMDRT revXXX - Rec.709',
        'ACES 2.0 Candidate CAMDRT revXXX - P3D65',
        'ACES 2.0 Candidate CAMDRT revXXX - P3D65 (Rec709 sim)',
        'ACES 2.0 Candidate CAMDRT revXXX - Rec.2100 (Rec709 sim)',
        'ACES 2.0 Candidate CAMDRT revXXX - Rec.2100 (P3D65 540nit Limited)',
        'ACES 2.0 Candidate CAMDRT revXXX - Rec.2100 (P3D65 1000nit Limited)',
        ]})


    for config in ocioConfigTemplatePaths:
        for activeViewDict in activeViewDicts:

            configName = config.split('/').pop(-1)
            newConfigName = configName.replace('revXXX','rev'+revision).replace('TEMPLATE',activeViewDict['name'])
            newConfigPath = os.path.join(newOcioTemplateDir,newConfigName)
            with open(config) as f:
                lines = f.readlines()
            activeViewsStrings = [ x.replace('revXXX','rev'+revision) for x in  activeViewDict['values']]
            activeViews = ','.join(activeViewsStrings)
            newLines = [x.replace('revXXX','rev'+revision).replace('ACTIVEVIEWSPLACEHOLDER',activeViews) for x in lines]
            with open(newConfigPath, 'w') as f:
                f.write(''.join(newLines))




ODTWrites = []
for node in nuke.allNodes():
    if 'Write_ResolveACES_ODT_LUT' in node.name():
        ODTWrites.append(node)




for ODTWriteNode in ODTWrites:
    masterNode.knob('inverseMode').setValue(False)
    bakeCandidateLUTfromNode(ODTWriteNode)
    masterNode.knob('inverseMode').setValue(True)
    bakeCandidateLUTfromNode(ODTWriteNode, inverse=True)

## flip flag back to nukescript makes more sense when opened afterwards
masterNode.knob('inverseMode').setValue(False)

# createOCIOconfigs(revision)
createOCIOconfigs(nuke.thisNode().knob('revision').getValue())