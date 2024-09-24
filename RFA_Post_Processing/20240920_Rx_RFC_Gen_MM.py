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

filePath = r'C:\Users\mmarinova\Downloads\P6\P6_Rx_Raw_Data'
# savePath = r'C:\Users\mmarinova\Downloads\RFA_Rx_I1\RFA_Files\17G7-20G7'

tlmType = 'Rx'
normVal = 5
multiplier = 1
fileType = 'RFA_2'  # RFC or RFA file. The _2 is needed otherwise it picks all csv files and throws an error
mask = 'HFSS'
multiIt = 'False'

RFC_offset=[5, 5, 5, 5, 5, 5, 5, 5]

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


for i in range(len(f_set_Log)):
    f_set=f_set_Log[i]

    filesRFA = list()
    find__RFAfiles(filePath, f_set, fileType,filesRFA)
    #find__RFAfiles(filePath, f_set, 'RFC_2', filesRFC)

    if RFC_offset[i] >= 0:
        offset = 'Offset_' + str(RFC_offset[i]) + 'dB'
    elif RFC_offset[i] < 0:
        offset = 'Offset_m' + str(abs(RFC_offset[i])) + 'dB'

    for beamChoice in range(2):

        for j in range(len(filesRFA)):
            load__RFA(filesRFA[j][beamChoice])
            #print(filesRFA[j][beamChoice])

            RFA_meas_info = meas_info
            RFA_meas_array = meas_array
            RFA_f_measPoints = f_measPoints
            NumColumn=len(RFA_meas_array[1])

            RFC_meas_array=np.zeros([6,NumColumn])
            RFC_meas_info = RFA_meas_info
            RFC_meas_info[0][0]=RFC_meas_info[0][0].replace('RFA','RFC')
            RFC_f_measPoints = f_measPoints

            RFC_gain_full = RFC_meas_array[:, ::2]
            RFC_phase_full = RFC_meas_array[:, 1:][:, ::2]

            col = np.argmin(np.abs((RFA_f_measPoints - float(f_set)) ** 2)) * 2
            RFC_gain = RFC_meas_array[:, col]

            RFC_gain[0] = RFC_gain[0] + RFC_offset[i]
            RFC_gain[1] = RFC_gain[1] + RFC_offset[i]
            RFC_gain[2] = RFC_gain[2] + RFC_offset[i]
            RFC_gain[3] = RFC_gain[3] + RFC_offset[i]
            RFC_gain[4] = RFC_gain[4] + RFC_offset[i]
            RFC_gain[5] = RFC_gain[5] + RFC_offset[i]

            col1 = np.argmin(np.abs((RFA_f_measPoints - float(f_set)) ** 2))

            RFC_gain_full[:, col1] = RFC_gain

            RFA_savePath = filePath + '_post-processed_Test1\\Corrected_RFA_test1'
            if not os.path.exists(RFA_savePath):
                os.makedirs(RFA_savePath)
                # write new file
            RFA_filename = filesRFA[j][beamChoice].split('\\')[-1]
            RFA_filename = RFA_filename.split('.csv')[-2]

            file = open(RFA_savePath + '\\' + RFA_filename + '_' + offset + '_' + mask + '.csv', 'w+', newline='')
            with file:
                write = csv.writer(file)
                write.writerows(RFA_meas_info)

            RFC_meas_info_list = RFC_meas_info.copy()
            RFC_meas_array_corrected = RFC_meas_array.copy() * 0.0
            for m in range(RFC_gain_full.shape[1]):
                RFC_meas_array_corrected[:, 2 * m] = RFC_gain_full[:, m]
                RFC_meas_array_corrected[:, 2 * m + 1] = RFC_phase_full[:, m]
            for o in range(len(RFC_meas_array_corrected)):
                RFC_meas_info_list.append(list(RFC_meas_array_corrected[o, :]))

            RFC_savePath = filePath + '_post-processed_Test1\\Corrected_RFC_test1'
            if not os.path.exists(RFC_savePath):
                os.makedirs(RFC_savePath)
                # write new file
            RFC_filename = filesRFA[j][beamChoice].split('\\')[-1]
            RFC_filename = RFC_filename.split('.csv')[-2]
            RFC_filename=RFC_filename.replace('RFA','RFC')

            file = open(RFC_savePath + '\\' + RFC_filename + '_' + offset + '_' + mask + '.csv', 'w+', newline='')
            with file:
                write = csv.writer(file)
                write.writerows(RFC_meas_info_list)












