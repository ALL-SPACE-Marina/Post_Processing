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

filePath = r'C:\Users\mmarinova\Downloads\HFSS_P3_v6_LUT_RC_FM_3dB_RFA_RFC'
# savePath = r'C:\Users\mmarinova\Downloads\RFA_Rx_I1\RFA_Files\17G7-20G7'

tlmType = 'Tx'
normVal = 0
multiplier = 1
fileType = 'RFA_2'  # RFC or RFA file. The _2 is needed otherwise it picks all csv files and throws an error
multiIt = 'False'
mask = 'FM_m3dB'

if tlmType == 'Rx':
    f_set_Log = [17.7, 18.2, 18.7, 19.2, 19.7, 20.2, 20.7, 21.2]
    # f_set_Log = [17.7, 18.2, 18.7, 19.2, 19.7, 20.2, 20.7] #[17.7, 18.2, 18.7, 19.2, 19.7, 20.2, 20.7, 21.2]
    # f_set_Log = [21.2]
elif tlmType == 'Tx':
    f_set_Log = [27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0]
    # f_set_Log = [29.5]

for beamChoice in range(2):
    beam = beamChoice + 1


    def find__RFAfiles(path, f_set, beam, fileType,filesRFA):
        #global filesRFA
        files = []
        for root, directories, file in os.walk(path):
            for file in file:
                if (file.endswith(".csv")):
                    files.append(os.path.join(root, file))

        for i in range(len(files)):
            if multiIt==True:
                if fileType in files[i] and 'GHz_' + str(f_set) + '0_GHz' in files[i] and 'Beam' + str(beam) in files[i] and 'teration_1' in files[i]:
                    # if 'RFA' in files[i] and 'both_' + str(f_set) + '_GHz' in files[i] and 'Beam'+str(beam) in files[i]:
                    filesRFA.append(files[i])
            else:
                if fileType in files[i] and 'GHz_' + str(f_set) + '0_GHz' in files[i] and 'Beam' + str(beam) in files[i]:
                    # if 'RFA' in files[i] and 'both_' + str(f_set) + '_GHz' in files[i] and 'Beam'+str(beam) in files[i]:
                    filesRFA.append(files[i])


    def analyse__RFAparams(filesRFA, RFAparamDict, fileName ):
        #global RFAparamDict, fileName

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
        filesRFA = []
        filesRFC =[]
        RFAparamDict = {}
        RFCparamDict = {}
        RFA_fileName=[]
        RFC_fileName = []

        find__RFAfiles(filePath, f_set, beam, fileType, filesRFA)
        analyse__RFAparams(filesRFA, RFAparamDict,RFA_fileName)

        find__RFAfiles(filePath, f_set, beam, 'RFC_2',filesRFC)
        analyse__RFAparams(filesRFC,RFCparamDict,RFC_fileName)


        ## Collate values and find global offsets
        minValLog = []
        stdLog = []
        medianLog = []
        badPortsLog = []
        boardLog = []
        for j in range(len(filesRFA)):

            load__RFA(filesRFA[j])
            RFA_meas_info = meas_info
            RFA_meas_array = meas_array
            RFA_f_measPoints = f_measPoints

            load__RFA(filesRFC[j])
            RFC_meas_info = meas_info
            RFC_meas_array = meas_array
            RFC_f_measPoints = f_measPoints
            col = np.argmin(np.abs((RFA_f_measPoints - float(f_set)) ** 2)) * 2
            RFA_gain = RFA_meas_array[:, col]
            RFC_gain = RFC_meas_array[:,col]

            RFA_gain_full = RFA_meas_array[:, ::2]
            RFA_phase_full = RFA_meas_array[:, 1:][:, ::2]

            RFC_gain_full = RFC_meas_array[:, ::2]
            RFC_phase_full = RFC_meas_array[:, 1:][:, ::2]

            L1_att = np.mean(RFA_gain[0:152]);
            L2_att = np.mean(RFA_gain[152:304]);
            L3_att = np.mean(RFA_gain[304:456]);
            print(f_set)
            print(L1_att)
            print(L2_att)
            print(L3_att)
            scaleval=min(L1_att, L2_att, L3_att)
            print(scaleval)
            L1_att = L1_att-scaleval
            L2_att = L2_att-scaleval
            L3_att = L3_att-scaleval

            RFA_gain[0:152]=RFA_gain[0:152]-L1_att
            RFA_gain[152:304] = RFA_gain[152:304] - L2_att
            RFA_gain[304:456] = RFA_gain[304:456] - L3_att

            RFC_gain[0] = RFC_gain[0] + L1_att
            RFC_gain[1] = RFC_gain[1] + L1_att
            RFC_gain[2] = RFC_gain[2] + L2_att
            RFC_gain[3] = RFC_gain[3] + L2_att
            RFC_gain[4] = RFC_gain[4] + L3_att
            RFC_gain[5] = RFC_gain[5] + L3_att

            col1 = np.argmin(np.abs((RFA_f_measPoints - float(f_set)) ** 2))

            RFA_gain_full[:, col1] = RFA_gain

            RFC_gain_full[:, col1] = RFC_gain

            for k in range(RFA_gain_full.shape[0]):
                for l in range(RFA_gain_full.shape[1]):

                    if RFA_gain_full[k, l] <= 0:
                        RFA_gain_full[k, l] = 0

            # merge back
            RFA_meas_info_list = RFA_meas_info.copy()
            RFA_meas_array_corrected = RFA_meas_array.copy() * 0.0
            for m in range(RFA_gain_full.shape[1]):
                RFA_meas_array_corrected[:, 2 * m] = RFA_gain_full[:, m]
                RFA_meas_array_corrected[:, 2 * m + 1] = RFA_phase_full[:, m]
            for o in range(len(RFA_meas_array_corrected)):
                RFA_meas_info_list.append(list(RFA_meas_array_corrected[o, :]))

            RFA_savePath = filePath + '_post-processed' + '\\Corrected_RFA'
            if not os.path.exists(RFA_savePath):
                os.makedirs(RFA_savePath)
                # write new file
            RFA_filename = filesRFA[j].split('\\')[-1]
            RFA_filename = RFA_filename.split('.csv')[-2]

            file = open(RFA_savePath + '\\' + RFA_filename + '_Offset' + mask +'.csv', 'w+', newline='')
            with file:
                write = csv.writer(file)
                write.writerows(RFA_meas_info_list)

            RFC_meas_info_list = RFC_meas_info.copy()
            RFC_meas_array_corrected = RFC_meas_array.copy() * 0.0
            for m in range(RFC_gain_full.shape[1]):
                RFC_meas_array_corrected[:, 2 * m] = RFC_gain_full[:, m]
                RFC_meas_array_corrected[:, 2 * m + 1] = RFC_phase_full[:, m]
            for o in range(len(RFC_meas_array_corrected)):
                RFC_meas_info_list.append(list(RFC_meas_array_corrected[o, :]))

            RFC_savePath = filePath + '_post-processed' + '\\Corrected_RFC'
            if not os.path.exists(RFC_savePath):
                os.makedirs(RFC_savePath)
                # write new file
            RFC_filename = filesRFC[j].split('\\')[-1]
            RFC_filename = RFC_filename.split('.csv')[-2]

            file = open(RFC_savePath + '\\' + RFC_filename + '_Offset' + mask + '.csv', 'w+', newline='')
            with file:
                write = csv.writer(file)
                write.writerows(RFC_meas_info_list)












