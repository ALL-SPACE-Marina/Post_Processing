import numpy as np
import os
import json
import csv
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt;

plt.close('all')
import pickle

matplotlib.use('Agg')

filePath = r'C:\Users\mmarinova\Downloads\P2_Tx_20240612'
# savePath = r'C:\Users\mmarinova\Downloads\RFA_Rx_I1\RFA_Files\17G7-20G7'

tlmType = 'Tx'
L1_att=0
L2_att=3
L3_att=2

offset='L2_L3'

fileType = 'RFC_2'  # RFC or RFA file. The _2 is needed otherwise it picks all csv files and throws an error
zeroed = 'False'  # put to True if you want all amplitude values to be equalized to eqVal. Otherwise, put False. Will work for both RFC and RFA files
eqVal = 0

# if zeroed == 'True':
#     offset = 'HFSS_att_val_' + str(eqVal) + 'dB'
# elif normVal >= 0:
#     offset = 'HFSS_offset_' + str(normVal) + 'dB_' + str(multiplier) + 'sig'
# elif normVal < 0:
#     offset = 'HFSS_offset_m' + str(abs(normVal)) + 'dB_' + str(multiplier) + 'sig'

if tlmType == 'Rx':
    f_set_Log = [17.7, 18.2, 18.7, 19.2, 19.7, 20.2, 20.7, 21.2]
    # f_set_Log = [17.7, 18.2, 18.7, 19.2, 19.7, 20.2, 20.7] #[17.7, 18.2, 18.7, 19.2, 19.7, 20.2, 20.7, 21.2]
    # f_set_Log = [21.2]
elif tlmType == 'Tx':
    #f_set_Log = [27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0]
    f_set_Log = [29.5]

for beamChoice in range(2):
    beam = beamChoice + 1


    def find__RFAfiles(path, f_set, beam, fileType):
        global filesRFA
        files = []
        for root, directories, file in os.walk(path):
            for file in file:
                if (file.endswith(".csv")):
                    files.append(os.path.join(root, file))
        filesRFA = []
        for i in range(len(files)):
            if fileType in files[i] and 'GHz_' + str(f_set) + '0_GHz' in files[i] and 'Beam' + str(beam) in files[i]:
                # if 'RFA' in files[i] and 'both_' + str(f_set) + '_GHz' in files[i] and 'Beam'+str(beam) in files[i]:
                filesRFA.append(files[i])


    def analyse__RFAparams(filesRFA):
        global RFAparamDict, fileName
        RFAparamDict = {}
        log_fileName = []
        log_temperature = []
        log_f_set = []
        log_beam = []
        log_board = []
        for i in range(len(filesRFA)):
            fileName = filesRFA[i].split('\\')[-1]
            log_fileName.append(fileName)
            log_temperature.append(fileName.split('_')[-1][0:-5])
            log_f_set.append(fileName.split('_')[-3])
            log_beam.append(fileName.split('_')[9][-1])
            log_board.append(fileName.split('_')[4])
        RFAparamDict['fileNames'] = log_fileName
        RFAparamDict['temperatures'] = log_temperature
        RFAparamDict['f_sets'] = log_f_set
        RFAparamDict['beams'] = log_beam
        RFAparamDict['boards'] = log_board
        RFAparamDict['filePaths'] = filesRFA


    def load__RFA(filePath):
        global meas_info, meas_array, f_measPoints
        meas_info = []
        with open(filePath, 'r') as file:
            filecontent = csv.reader(file, delimiter=',')
            for row in filecontent:
                meas_info.append(row)
                header_offset = 29
            meas_info = meas_info[0:header_offset]
            meas_array = np.genfromtxt(filePath, delimiter=',', skip_header=header_offset)
            f_measPoints = np.array(meas_info[header_offset - 1])[::2].astype(float)


    ########## RUN ##########

    portFailDict = {}
    for f_set in f_set_Log:
        find__RFAfiles(filePath, f_set, beam, fileType)
        analyse__RFAparams(filesRFA)


        ## Open and edit RFA files
        for j in range(len(filesRFA)):

            load__RFA(filesRFA[j])
            gain = meas_array[:, ::2]
            phase = meas_array[:, 1:][:, ::2]
            print(len(gain))
            gain[0]=gain[0]+L1_att
            gain[1] = gain[1] + L1_att
            gain[2] = gain[2] + L2_att
            gain[3] = gain[3] + L2_att
            gain[4] = gain[4] + L3_att
            gain[5] = gain[5] + L3_att


            # merge back
            meas_info_list = meas_info.copy()
            meas_array_corrected = meas_array.copy() * 0.0
            for m in range(gain.shape[1]):
                meas_array_corrected[:, 2 * m] = gain[:, m]
                meas_array_corrected[:, 2 * m + 1] = phase[:, m]
            for o in range(len(meas_array_corrected)):
                meas_info_list.append(list(meas_array_corrected[o, :]))

            savePath = filePath + '_post-processed' + '\\' + offset
            if not os.path.exists(savePath):
                os.makedirs(savePath)
                # write new file
            RFAfilename = filesRFA[j].split('\\')[-1]
            RFAfilename = RFAfilename.split('.csv')[-2]

            file = open(savePath + '\\' + RFAfilename + '_' + offset + '.csv', 'w+', newline='')
            with file:
                write = csv.writer(file)
                write.writerows(meas_info_list)

        plt.close('all')










