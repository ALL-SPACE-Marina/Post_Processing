import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt; plt.rcParams['font.size'] = 12
import scipy
from scipy.stats import norm
import os
import glob
import copy
import csv
import json
import time
from pylab import *
plt.close('all')

#filePath = r'C:\Users\mmarinova\Downloads\2023-09-01_21-43-12_MCR3_Rig1_eval_QR00003_F-Type_SM_P1Opt_CT_BC'
filePath = r'C:\Users\mmarinova\Downloads\2023-09-26_20-05-23_MCR3_Rig2_eval_QR00002_G-type_CA12_SW1p19p101_nBC'
filename = r'Eval_Freq_min-max_G-Type'
#tlmType= ['S-Type', 'F-Type_SM_GOpt_CT_nBC', 'F-Type_TM_GOpt_CT_nBC', 'F-Type_TM_P1Opt_CT_BC', 'F-Type_SM_P1Opt_CT_BC']
tlmType= ['G-type_CA12_SW1p19p101_nBC']
termType='G-Type'
fqRange='Tx'

# for i in range(len(tlmType)):
#     filename = filename + '_' + tlmType[i]
#     if i < len(tlmType) - 1:
#         filename = filename + '_vs'

if fqRange=='Rx':
    f_set_list = [17.7, 18.2, 18.7, 19.2, 19.7, 20.2, 20.7, 21.2]
    plotXlimMin=17.7
    plotXlimMax=21.2
    plotYlimMin = 0
    plotYlimMax = 50
elif fqRange=='Tx':
    f_set_list = [27.50, 28.00, 28.50, 29.00, 29.50, 30.00, 30.50, 31.00]
    plotXlimMin = 27.5
    plotXlimMax = 31.0
    plotYlimMin = -20
    plotYlimMax = 30

chop = False
# file path
dirScript = os.getcwd()
# definitions
def find_measFiles(path, fileString, beam):
    global measFiles, files
    files = []
    for root, directories, file in os.walk(path):
        for file in file:
            if (file.endswith(".csv")) == True:
                files.append(os.path.join(root, file))
    measFiles = []
    for i in range(len(files)):
        if fileString in files[i] and 'eam' + str(beam) in files[i]:
            measFiles.append(files[i])
            

def load_measFiles(filePath):
    global meas_info, meas_array, meas_frequencies, meas_params, meas_array_gain, meas_array_phase
    meas_params = {}
    meas_info = []
    # meas_info, array and measurement frequencies
    with open(filePath, 'r') as file:
        filecontent = csv.reader(file, delimiter=',')
        time.sleep(0.10)
        for row in filecontent:
            meas_info.append(row)
        index_start = [index for index in range(len(meas_info)) if 'barcodes' in meas_info[index]][0] + 2
        meas_info = meas_info[0:index_start]
        meas_array = np.genfromtxt(filePath, delimiter=',', skip_header=index_start)
        meas_array_gain = meas_array[:,::2]
        meas_array_phase = meas_array[:,1:][:,::2]
        meas_frequencies = np.array(meas_info[index_start - 1])[::2].astype(float)    
        
    # meas_params
    for i in range(len(meas_info) - 1):
        if len(meas_info[i]) > 1:
            paramName = meas_info[i][0]

            if paramName[0:2] == '# ':
                paramName = paramName[2:]
            meas_params[paramName] = meas_info[i][1]

# colMap = ['b','orange','g','r','purple','brown','pink','grey']
# plt.figure(figsize=(7,4))          
for beamChoice in range(2):
    beamChoice = beamChoice+1
    plt.figure(figsize=(7,4))
    count = 0
    for f_set in f_set_list:
        # plt.figure(figsize=(7,4))
        print('GHz_'+ str(f_set))
        find_measFiles( filePath, 'OP_2', beamChoice)
        for measFile in measFiles:
            #print(measFile)


            chop=True
            load_measFiles(measFile)
            if float(meas_params['f_c']) == float(f_set):
                if chop == True:
                    locLeft = np.argmin((meas_frequencies-(float(f_set)-0.25))**2); locRight = np.argmin((meas_frequencies-(float(f_set)+0.25))**2)
                if chop == False:
                    locLeft = 0; locRight = len(meas_frequencies)-1
                fileN = measFile.split('\\')[-1]
                print(fileN)
                print(len(tlmType))
                measLabel = []
                for i in range(len(tlmType)):
                    print(i)
                    if tlmType[i] in fileN:
                        measLabel = tlmType[i]
                # if beamChoice == 1:
                #     plt.plot(meas_frequencies[locLeft:locRight+1], np.median(meas_array_gain, axis=0)[locLeft:locRight+1], color = colMap[count], linewidth = 5, label = str(f_set) + ' GHz')
                # if beamChoice == 2:
                #     plt.plot(meas_frequencies[locLeft:locRight+1], np.median(meas_array_gain, axis=0)[locLeft:locRight+1], color = colMap[count], linestyle = '--', linewidth = 5, label = str(f_set) + ' GHz')
                plt.plot(meas_frequencies[locLeft:locRight+1], np.median(meas_array_gain, axis=0)[locLeft:locRight+1], linewidth = 5, label = str(f_set))
                count = count + 1
                plt.fill_between(meas_frequencies[locLeft:locRight+1], np.min(meas_array_gain, axis=0)[locLeft:locRight+1], np.max(meas_array_gain, axis=0)[locLeft:locRight+1], alpha=0.2)#, label = '\n Port min/max')
                temp = meas_array_gain*1.0
                #plt.legend(loc='lower right')
                plt.legend(ncol=2, loc='lower right', fontsize=12)
        plt.xlabel('Frequency [GHz]'); plt.ylabel('S$_{21}$ (arb.) [dB]')
        plt.ylim([plotYlimMin,plotYlimMax]); plt.xlim([plotXlimMin, plotXlimMax]); #plt.xlim([min(f_set_list), max(f_set_list)])
        plt.yticks(np.linspace(plotYlimMin,plotYlimMax, num=int((abs(plotYlimMin)+abs(plotYlimMax))/5)+1))
        plt.grid('on')

        print(filename)
        plt.tight_layout()
        #plt.title(termType+'\nf_set = ' + str(f_set) + ' GHz, Beam ' + str(beamChoice))
        plt.title(termType+'\nBeam ' + str(beamChoice)+ ', f_set = ' + str(f_set) + ' GHz')

        print(filename)
        plt.savefig(filePath + '\\' + filename + '_Beam_' + str(beamChoice) + '.png',
                    dpi=400)
        #plt.savefig(filePath+ '\\'+filename + '_f_set_' + str(f_set) + 'GHz_Beam_' + str(beamChoice) + '.png', dpi=400)
        #plt.close()