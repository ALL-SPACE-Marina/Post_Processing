import pandas as pd
import numpy as np
import matplotlib.pyplot as plt;

plt.rcParams['font.size'] = 15
import os
import pip

plt.close('all')

# load
filePath = r'C:\Terminal_Testing\S-Type_Test\Rx_TLM\Single_Beam_RHCP'
Th_deg = 70.0
Ph_deg = 0.0
cal_freq = 19.5
meas_freq = 19.5
#ph_deg=0.0

dirScript = os.getcwd()
os.chdir(dirScript)
#dfFull = pd.read_excel(fileName + ".xlsx")
#print(dfFull)

dirScript = os.getcwd()

## Defs ##

def find_measFiles(path, fileString):
    global measFiles, files
    files = []
    for root, directories, file in os.walk(path):
        for file in file:
            if (file.endswith(".xlsx")) == True:
                print('True')
                files.append(os.path.join(root, file))
    measFiles = []
    print(files)
    for i in range(len(files)):
        print(files[i])
        if fileString in files[i]:
            measFiles.append(files[i])



def thetaphi_to_azel(theta, phi):
    global az, el

    theta = theta * np.pi / 180.0
    phi = phi * np.pi / 180.0

    sin_el = np.sin(phi) * np.sin(theta)
    tan_az = np.cos(phi) * np.tan(theta)
    el = np.arcsin(sin_el) * 180.0 / np.pi
    az = np.arctan(tan_az) * 180.0 / np.pi

    return az


def reduce_df(df):
    global dfPlot, beam, acu, columns, ph_deg1

    # load
    columns = df.columns.tolist()

    # reduce
    #df = df[(df["phi_deg"] == ph_deg)]
    df = df[(df["cal_freq_GHz"] == cal_freq)]
    df = df[(df["freq_GHz"] == meas_freq)]
    df = df[(df["entry_type"] == 'gain_at_requested_angle')]
    #df = df[(df["fpath_parent"] == fpath)]

    acu_test=np.array(df['acu_version'])
    beam_test=np.array(df['beam_no'])
    ph_deg_test = np.array(df['phi_deg'])
    acu=np.array(list(set(acu_test)))
    beam=np.array(list(set(beam_test)))
    ph_deg1=np.array(list(set(ph_deg_test)))
    print(acu)
    print(beam[1])
    print(ph_deg1)

    x = np.array(df['theta_deg'])
    y = np.array(df['Gain_dB'])

def plot__gainVstheta(df, test_beam, ph_deg):
    global dfPlot, x, y, columns

    # load
    columns = df.columns.tolist()

    # reduce
    df = df[(df["beam_no"] == test_beam)]
    df = df[(df["phi_deg"] == ph_deg)]
    df = df[(df["cal_freq_GHz"] == cal_freq)]
    df = df[(df["freq_GHz"] == meas_freq)]
    df = df[(df["entry_type"] == 'gain_at_requested_angle')]


    x = np.array(df['theta_deg'])
    y = np.array(df['Gain_dB'])


find_measFiles( filePath, 'ppk')
dfFull = pd.DataFrame()



dfFull = pd.concat(pd.read_excel(f) for f in measFiles)
print(dfFull)

reduce_df(dfFull)


labelLog = ['Cal_0dB_1sig_BA_0dB', 'Cal_0dB_2sig_BA_0dB', 'Cal_3dB_1sig_BA_0dB', 'Cal_3dB_2sig_BA_0dB',
            'Cal_m3dB_1sig_BA_0dB', 'Cal_m3dB_2sig_BA_0dB']



for j in range(len(ph_deg1)):
    ph_deg=ph_deg1[j]
    plt.figure(figsize=([7, 6]))
    for i in range(len(beam)):
        test_beam = beam[i]
        plot__gainVstheta(dfFull, test_beam, ph_deg)
        plt.plot(x, y, 's', markeredgecolor='k', markersize=10, label='Beam '+ str(test_beam))
        plt.xlabel('Theta [deg]');
        plt.ylabel('TLM gain [dB]\n(at req. angle)')
        plt.yticks(np.linspace(0, 100, num=51))
        plt.xticks(np.linspace(-100, 100, num=21))
        plt.xlim([-10, 80]);
        plt.ylim([50, 80]);  # plt.ylim([65, 75])
        #plt.set_yticks(np.linspace(10, 50, num=int((50-10) / 5 + 1)))
        plt.grid(True, which='major')
        plt.legend(loc='lower left')
        plt.title('SW: ' + str(acu[0]) + '\nFreq = ' + str(meas_freq) + ' GHz' + '\nTh=' + 'X' + ', Phi=' + str(ph_deg),
                  fontsize=15)
        plt.tight_layout()
        savePath = filePath + '\\' + 'Figures'
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        plt.savefig(savePath + '\\' + 'Pointing_angle_Ph_Cut_'+str(ph_deg),dpi=400)
    plt.close()


#
#
# def plot__gainVstheta(sb_mute, b1_theta, b1_phi, acu, freq, b2_phi, fpath):
#     global dfPlot, df, x, y, columns
#
#     # load
#     dirScript = os.getcwd()
#     os.chdir(dirScript)
#     df = pd.read_excel(fileName + ".xlsx")
#     columns = df.columns.tolist()
#
#     # reduce
#     # df = df[(df["pb_theta_deg"] == b1_theta)]
#     df = df[(df["phi_deg"] == Ph_deg)]
#     # df = df[(df["sb_mute"] == sb_mute)]
#     df = df[(df["theta_deg"] == Th_deg)]
#     df = df[(df["freq_GHz"] == df["cal_freq_GHz"])]
#     df = df[(df["entry_type"] == 'gain_at_requested_angle')]
#     df = df[(df["fpath_parent"] == fpath)]
#
#     x = np.array(df['freq_GHz'])
#     y = np.array(df['Gain_dB'])
#
#
# sb_mute = 'ON'
# labelLog = ['Cal_0dB_1sig_BA_0dB', 'Cal_0dB_2sig_BA_0dB', 'Cal_3dB_1sig_BA_0dB', 'Cal_3dB_2sig_BA_0dB',
#             'Cal_m3dB_1sig_BA_0dB', 'Cal_m3dB_2sig_BA_0dB']
# acu = '1.17.7'
# # acu = '1.17.67'
# freq = 19.5
# freq = 29.5
# b1_theta = 0.0
# b1_phi = 0.0
# b2_phi = 0.0
# plt.figure(figsize=([7, 6]))
# fpathLog = [
#     r'/mnt/nfs/data/groups/measurements/slc3/S2000/DVT/S-Type/RX_TLM-ES2c/QR440-0254-00045/Single_Beam/RHCP/B2/20230812/Cal_0dB_1sig_BA_0dB',
#     r'/mnt/nfs/data/groups/measurements/slc3/S2000/DVT/S-Type/RX_TLM-ES2c/QR440-0254-00045/Single_Beam/RHCP/B2/20230812/Cal_0dB_2sig_BA_0dB',
#     r'/mnt/nfs/data/groups/measurements/slc3/S2000/DVT/S-Type/RX_TLM-ES2c/QR440-0254-00045/Single_Beam/RHCP/B2/20230812/Cal_3dB_1sig_BA_0dB',
#     r'/mnt/nfs/data/groups/measurements/slc3/S2000/DVT/S-Type/RX_TLM-ES2c/QR440-0254-00045/Single_Beam/RHCP/B2/20230812/Cal_3dB_2sig_BA_0dB',
#     r'/mnt/nfs/data/groups/measurements/slc3/S2000/DVT/S-Type/RX_TLM-ES2c/QR440-0254-00045/Single_Beam/RHCP/B2/20230812/Cal_m3dB_1sig_BA_0dB',
#     r'/mnt/nfs/data/groups/measurements/slc3/S2000/DVT/S-Type/RX_TLM-ES2c/QR440-0254-00045/Single_Beam/RHCP/B2/20230812/Cal_m3dB_2sig_BA_0dB']
# for i in range(len(fpathLog)):
#     fpath = fpathLog[i]
#     plot__gainVstheta(sb_mute, b1_theta, b1_phi, acu, freq, b2_phi, fpath)
#     plt.plot(x, y, 's', markeredgecolor='k', markersize=10, label=labelLog[i])
#     plt.xlabel('freq [GHz]');
#     plt.ylabel('Beam 1 gain [dB]\n(at req. angle)')
#     plt.yticks(np.linspace(0, 100, num=21))
#     # plt.xticks(np.linspace(-100,100,num=21))
#     plt.xlim([20.0, 21.5]);
#     plt.ylim([30, 80]);  # plt.ylim([65, 75])
#     plt.grid('on')
#     plt.legend(loc='lower left')
#     plt.title('SW: ' + acu + '\nFreq = ' + ' X' + '\nb2: Th=' + str(Th_deg) + ', Phi=' + str(Ph_deg), fontsize=15)
#     plt.tight_layout()
#     plt.savefig(
#         r'C:\Users\mmarinova\Downloads\Testing\S2000\DVT\S-Type\Rx_TLM_ES2c\QR440-0254-00045\Single_Beam_B2_RHCP\SLC2_20230812\\' + 'Frequency_comparison',
#         dpi=400)
#
#     sb_mute = 'OFF'
#
