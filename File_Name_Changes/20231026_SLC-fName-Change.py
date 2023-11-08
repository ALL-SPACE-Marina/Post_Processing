import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import pickle

# inputs
filePath = r'G:\measurements\TLM_Meas\DVT_G-Type_1p5\Tx_TLM\Comparisons\SLC3\B_to_B_Comparison\Raw_Data\G-Type_1p5_B2'
#savePath = r'G:\measurements\TLM_Meas\DVT_G-Type_1p5\Tx_TLM\Comparisons\SLC3\TLM_Type_Comp_att_high\Raw_Data\F-Type_name_change'

# definitions
def find__measFiles(filePath, fileString):
    global measFiles
    files = []
    for root, directories, file in os.walk(filePath):
        for file in file:
            if (file.endswith(".csv")) == True:
                files.append(os.path.join(root, file))
    measFiles = []
    for i in range(len(files)):
        if fileString in files[i]:
            measFiles.append(files[i])

find__measFiles(filePath, 'SB1')
for measFile in measFiles:
    fName = measFile.split('\\')[-1]
    #print(fName)
    components = fName.split('_')
    print(components)
    comp8 = components[8]
    #print(comp7)
    comp8 = comp8.replace("TLMPB", "TLMB")
    comp8 = comp8.replace("Ph", ".0Ph")
    #comp8 = comp8 + '.0'
    comp8 = comp8.replace("MFalse", ".0")
    fNameNew = components[0] + '_' + components[1] + '_' + components[2] + '_' + components[3] + '_' + components[4] + '_' + components[5] + '_' + components[6] + '_' + components[7] + '_' +comp8 + '_' + components[10] + '_' + components[11] + '_' + components[12] + '_' + components[13]+ '_' + components[14]+ '_' + components[15]+ '_' + components[16]+ '_' + components[17]
    measFileNew = filePath + '\\' + fNameNew
    #print(measFileNew)

    # write new file
    os.rename(measFile, measFileNew)
