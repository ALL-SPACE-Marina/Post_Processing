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

filePath = r'C:\Users\mmarinova\Downloads\P7\P7_Tx_Raw_Data'
# savePath = r'C:\Users\mmarinova\Downloads\RFA_Rx_I1\RFA_Files\17G7-20G7'

tlmType = 'Tx'
normVal = 0
multiplier = 3
fileType = 'RFA_2'  # RFC or RFA file. The _2 is needed otherwise it picks all csv files and throws an error
mask = 'FM'
multiIt = 'False'

if normVal >= 0:
    offset = 'Offset_' + str(normVal) + 'dB_' + str(multiplier) + 'sig'
elif normVal < 0:
    offset = 'Offset_m' + str(abs(normVal)) + 'dB_' + str(multiplier) + 'sig'

if tlmType == 'Rx':
    f_set_Log = [17.7, 18.2, 18.7, 19.2, 19.7, 20.2, 20.7, 21.2]
    # f_set_Log = [17.7, 18.2, 18.7, 19.2, 19.7, 20.2, 20.7] #[17.7, 18.2, 18.7, 19.2, 19.7, 20.2, 20.7, 21.2]
    # f_set_Log = [21.2]
elif tlmType == 'Tx':
    f_set_Log = [27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0]
    # f_set_Log = [29.5]

def find__RFAfiles(path, f_set, fileType, filesRFAtest):
    #global filesRFA, filesRFAtest
    files = []
    for root, directories, file in os.walk(path):
        for file in file:
            if (file.endswith(".csv")):
                files.append(os.path.join(root, file))

    for beamChoice in range(2):
        beam = beamChoice + 1
        k = 0
        for i in range(len(files)):
            if multiIt==True:
                if fileType in files[i] and 'GHz_' + str(f_set) + '0_GHz' in files[i] and 'Beam' + str(beam) and 'teration_1' in files[i]:
                    # if 'RFA' in files[i] and 'both_' + str(f_set) + '_GHz' in files[i] and 'Beam'+str(beam) in files[i]:
                    if beam==1:
                        filesRFAtest.append([files[i]])
                        k=k+1
                    elif beam==2:
                        filesRFAtest[k].extend([files[i]])
                        k = k + 1
            else:
                if fileType in files[i] and 'GHz_' + str(f_set) + '0_GHz' in files[i] and 'Beam' + str(beam) in files[i]:

                    if beam==1:
                        filesRFAtest.append([files[i]])
                        k=k+1
                    elif beam==2:
                        filesRFAtest[k].extend([files[i]])
                        k = k + 1
                    #print(filesRFAtest)


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

for f_set in f_set_Log:
    filesRFA = list()
    filesRFC = list()
    find__RFAfiles(filePath, f_set, fileType,filesRFA)
    find__RFAfiles(filePath, f_set, 'RFC_2', filesRFC)

    global_std = np.empty(2)
    global_median = np.empty(2)
    global_minVal = np.empty(2)

    for beamChoice in range(2):

        minValLog = np.empty(len(filesRFA))
        stdLog = np.empty(len(filesRFA))
        medianLog = np.empty(len(filesRFA))
        print(f_set)
        print('Beam is   ', beamChoice+1)

        for j in range(len(filesRFA)):
            load__RFA(filesRFA[j][beamChoice])
            col = np.argmin(np.abs((f_measPoints - float(f_set)) ** 2)) * 2
            gain = meas_array[:, col]
            medianVal = np.median(gain);
            medianLog[j]=medianVal
            stdVal = np.std(gain);
            stdLog[j]=stdVal

            boardName = filesRFA[j][beamChoice].split('\\')[-1].split('_')[6];
            print(boardName);

        global_std[beamChoice] = np.mean(stdLog)

        global_median[beamChoice] = np.average(medianLog)

        global_minVal[beamChoice] = global_median[beamChoice] - global_std[beamChoice] * multiplier

    beamCorrMin= np.min(global_minVal)
    RFC_gain_Corr= global_minVal-beamCorrMin
    print('beamCorrMin is    ', beamCorrMin)
    print('GlobalMinVal is    ', global_minVal)
    print('RFC_Gain_Corr is    ', RFC_gain_Corr)

    for beamChoice in range(2):

        for j in range(len(filesRFA)):
            load__RFA(filesRFA[j][beamChoice])
            #print(filesRFA[j][beamChoice])

            RFA_meas_info = meas_info
            RFA_meas_array = meas_array
            RFA_f_measPoints = f_measPoints

            load__RFA(filesRFC[j][beamChoice])
            RFC_meas_info = meas_info
            RFC_meas_array = meas_array
            RFC_f_measPoints = f_measPoints

            RFA_gain_full = RFA_meas_array[:, ::2]
            RFA_phase_full = RFA_meas_array[:, 1:][:, ::2]

            RFC_gain_full = RFC_meas_array[:, ::2]
            RFC_phase_full = RFC_meas_array[:, 1:][:, ::2]

            col = np.argmin(np.abs((RFA_f_measPoints - float(f_set)) ** 2)) * 2
            RFA_gain = RFA_meas_array[:, col]
            RFC_gain = RFC_meas_array[:, col]

            if f_set==30.5:
                RFA_gain=RFA_gain-global_minVal[beamChoice]+normVal
            else:
                RFA_gain=RFA_gain-global_minVal[beamChoice]+normVal

            L1_att = np.mean(gain[0:152]);  # Hardcoded for Tx
            L2_att = np.mean(gain[152:304]);  # Hardcoded for Tx
            L3_att = np.mean(gain[304:456]);  # Hardcoded for Tx

            # print(f_set)
            # print(L1_att)
            # print(L2_att)
            # print(L3_att)

            scaleval = min(L1_att, L2_att, L3_att)

            L1_att = L1_att - scaleval
            L2_att = L2_att - scaleval
            L3_att = L3_att - scaleval

            # print(f_set)
            # print(L1_att)
            # print(L2_att)
            # print(L3_att)

            RFA_gain[0:152] = RFA_gain[0:152] - L1_att
            RFA_gain[152:304] = RFA_gain[152:304] - L2_att
            RFA_gain[304:456] = RFA_gain[304:456] - L3_att

            RFC_gain[0] = RFC_gain[0] + L1_att + RFC_gain_Corr[beamChoice]
            RFC_gain[1] = RFC_gain[1] + L1_att + RFC_gain_Corr[beamChoice]
            RFC_gain[2] = RFC_gain[2] + L2_att + RFC_gain_Corr[beamChoice]
            RFC_gain[3] = RFC_gain[3] + L2_att + RFC_gain_Corr[beamChoice]
            RFC_gain[4] = RFC_gain[4] + L3_att + RFC_gain_Corr[beamChoice]
            RFC_gain[5] = RFC_gain[5] + L3_att + RFC_gain_Corr[beamChoice]

            col1 = np.argmin(np.abs((RFA_f_measPoints - float(f_set)) ** 2))

            RFA_gain_full[:, col1] = RFA_gain

            RFC_gain_full[:, col1] = RFC_gain

            for k in range(RFA_gain_full.shape[0]):
                for l in range(RFA_gain_full.shape[1]):

                    if RFA_gain_full[k, l] <= 0:
                        RFA_gain_full[k, l] = 0

            RFA_meas_info_list = RFA_meas_info.copy()
            RFA_meas_array_corrected = RFA_meas_array.copy() * 0.0
            for m in range(RFA_gain_full.shape[1]):
                RFA_meas_array_corrected[:, 2 * m] = RFA_gain_full[:, m]
                RFA_meas_array_corrected[:, 2 * m + 1] = RFA_phase_full[:, m]
            for o in range(len(RFA_meas_array_corrected)):
                RFA_meas_info_list.append(list(RFA_meas_array_corrected[o, :]))

            RFA_savePath = filePath + '_post-processed_Test' + '\\' + offset + '\\Corrected_RFA'
            if not os.path.exists(RFA_savePath):
                os.makedirs(RFA_savePath)
                # write new file
            RFA_filename = filesRFA[j][beamChoice].split('\\')[-1]
            RFA_filename = RFA_filename.split('.csv')[-2]

            if f_set==30.5:
                #file = open(RFA_savePath + '\\' + RFA_filename + '_' + 'Offset' + '_' + mask + '.csv', 'w+', newline='')
                file = open(RFA_savePath + '\\' + RFA_filename + '_' + offset + '_' + mask + '.csv', 'w+', newline='')
            else:
                file = open(RFA_savePath + '\\' + RFA_filename + '_' + offset + '_' + mask + '.csv', 'w+', newline='')
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

            RFC_savePath = filePath + '_post-processed_Test' + '\\' + offset + '\\Corrected_RFC'
            if not os.path.exists(RFC_savePath):
                os.makedirs(RFC_savePath)
                # write new file
            RFC_filename = filesRFC[j][beamChoice].split('\\')[-1]
            RFC_filename = RFC_filename.split('.csv')[-2]

            if f_set==30.5:
                file = open(RFC_savePath + '\\' + RFC_filename + '_' + 'Offset' + '_' + mask + '.csv', 'w+', newline='')
            else:
                file = open(RFC_savePath + '\\' + RFC_filename + '_' + offset + '_' + mask + '.csv', 'w+', newline='')
            with file:
                write = csv.writer(file)
                write.writerows(RFC_meas_info_list)












