import pandas as pd
import numpy as np
import matplotlib.pyplot as plt; plt.rcParams['font.size'] = 15
import os
import pip
plt.close('all')

# load
fileName = r'G:\measurements\TLM_Meas\DVT_I-Type\Rx_TLM\Comparisons\SLC2\F_vs_G_vs_I\PP_Data\ppk_data'
savePath=r'G:\measurements\TLM_Meas\DVT_I-Type\Rx_TLM\Comparisons\SLC2\F_vs_G_vs_I\PP_Data\Partial'
Th_deg_list=[0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0]
Ph_deg=0.0

TLM_Type='Rx'

if TLM_Type=='Rx':
    cal_freq_list = [17.7, 18.2, 18.7, 19.2, 19.7, 20.2, 20.7, 21.2]
    meas_freq_list = [17.7, 18.2, 18.7, 19.2, 19.7, 20.2, 20.7, 21.2]
    f_min=17.2
    f_max=21.7
    y_min_scan=40
    y_max_scan=90
elif TLM_Type=='Tx':
    cal_freq_list=[27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0]
    meas_freq_list=[27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0]
    f_min = 27.0
    f_max = 31.5
    y_min_scan =20
    y_max_scan =70

# labelLog = ['QR00057_F-Type', 'QR00012_G-Type', 'QR00002_G-Type', 'QR00034_G-Type_1p5', 'QR00060_G-Type_1p5']
# fpathLog = [r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_G-Type_1p5/Tx_TLM/Comparisons/SLC3/TLM_Type_Comp_att0/Raw_Data/QR00057_F-Type',
#             r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_G-Type_1p5/Tx_TLM/Comparisons/SLC3/TLM_Type_Comp_att0/Raw_Data/QR00012_G-Type',
#             r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_G-Type_1p5/Tx_TLM/Comparisons/SLC3/TLM_Type_Comp_att0/Raw_Data/QR00002_G-Type',
#             r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_G-Type_1p5/Tx_TLM/Comparisons/SLC3/TLM_Type_Comp_att0/Raw_Data/QR00034_G-Type_1p5',
#             r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_G-Type_1p5/Tx_TLM/Comparisons/SLC3/TLM_Type_Comp_att0/Raw_Data/QR00060_G-Type_1p5']

labelLog = ['QR00045_F-Type', 'QR00020_G-Type', 'QR00081_I-Type'] #'QR00002_I-Type', 'QR00011_I-Type',
fpathLog = [r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_I-Type/Rx_TLM/Comparisons/SLC2/F_vs_G_vs_I/Raw_Data/QR00045_F-Type',
            r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_I-Type/Rx_TLM/Comparisons/SLC2/F_vs_G_vs_I/Raw_Data/QR00020_G-Type',
            #r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_I-Type/Rx_TLM/Comparisons/SLC2/F_vs_G_vs_I/Raw_Data/QR00002_I-Type',
            #r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_I-Type/Rx_TLM/Comparisons/SLC2/F_vs_G_vs_I/Raw_Data/QR00011_I-Type',
            r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_I-Type/Rx_TLM/Comparisons/SLC2/F_vs_G_vs_I/Raw_Data/QR00081_I-Type']



dirScript = os.getcwd()
os.chdir(dirScript)
dfFull = pd.read_excel(fileName + ".xlsx")
markerList=['s', 'o', '^', 'D', 'X', 'p', '*', 'H']

## Defs ##

def thetaphi_to_azel(theta, phi):
    global az, el
    
    theta = theta*np.pi/180.0
    phi = phi*np.pi/180.0
    
    sin_el = np.sin(phi) * np.sin(theta)
    tan_az = np.cos(phi) * np.tan(theta)
    el = np.arcsin(sin_el) * 180.0/np.pi
    az = np.arctan(tan_az) * 180.0/np.pi
     
    return az

def plot__gainVstheta(fpath, cal_freq, meas_freq):
    global dfPlot, df, x, y, columns, acu

    # load
    dirScript = os.getcwd()
    os.chdir(dirScript)
    df = pd.read_excel(fileName + ".xlsx")
    columns = df.columns.tolist()

    #reduce

    df = df[(df["phi_deg"] == 0)]
    df = df[(df["cal_freq_GHz"] == cal_freq)]
    df = df[(df["freq_GHz"] == meas_freq)]
    df = df[(df["entry_type"] == 'gain_at_requested_angle')]
    df = df[(df["fpath_parent"] == fpath)]
    acu=np.array(df['acu_version'])[0]
    print(acu)

    x = np.array(df['theta_deg'])
    y = np.array(df['Gain_dB'])

def plot__gainVsfreq(fpath,Th_deg):
    global dfPlot, df, x, y, columns, phi_meas_freq

    # load
    dirScript = os.getcwd()
    os.chdir(dirScript)
    df = pd.read_excel(fileName + ".xlsx")
    columns = df.columns.tolist()

    #reduce
    # df = df[(df["pb_theta_deg"] == b1_theta)]
    df = df[(df["phi_deg"] == Ph_deg)]
    # df = df[(df["sb_mute"] == sb_mute)]
    df = df[(df["theta_deg"] == Th_deg)]
    df = df[(df["freq_GHz"] == df["cal_freq_GHz"])]
    df = df[(df["entry_type"] == 'gain_at_requested_angle')]
    df = df[(df["fpath_parent"] == fpath)]

    phi_meas_freq = np.array(df['pa_phi_deg'])
    print(phi_meas_freq)
    x = np.array(df['freq_GHz'])
    y = np.array(df['Gain_dB'])




for k in range(len(cal_freq_list)):
    plt.figure(figsize=([7,6]))

    for i in range(len(fpathLog)):
        fpath = fpathLog[i]
        plot__gainVstheta(fpath, cal_freq_list[k], meas_freq_list[k])
        plt.plot(x, y, markerList[i], markeredgecolor='k', markersize=10, label = labelLog[i])
        plt.xlabel('Theta [deg]'); plt.ylabel('Beam 1 gain [dB]\n(at req. angle)')
        plt.yticks(np.linspace(0,100,num=21))
        plt.xticks(np.linspace(-100,100,num=21))
        plt.xlim([-10,80]); plt.ylim([y_min_scan,y_max_scan]);# plt.ylim([65, 75])
        plt.grid('on')
        plt.legend(loc='lower left')
        plt.title('SW: ' + acu + '\nFreq = ' + str(meas_freq_list[k]) + ' GHz' + '\nb1: Th=' + 'X' + ', Phi=' + str(Ph_deg), fontsize=15)
        plt.tight_layout()
        plt.savefig(savePath+'\\' + 'Pointing_angle_Phi_' + str(Ph_deg) + 'Freq_' + str(meas_freq_list[k])+'GHz.png', dpi=400)
    plt.close('all')
    
    
    





for p in range(len(Th_deg_list)):

    for i in range(len(fpathLog)):
        fpath = fpathLog[i]
        plot__gainVsfreq(fpath, Th_deg_list[p])
        plt.plot(x, y, markerList[i], markeredgecolor='k', markersize=10, label = labelLog[i])
        plt.xlabel('freq [GHz]'); plt.ylabel('Beam 1 gain [dB]\n(at req. angle)')
        plt.yticks(np.linspace(0,100,num=21))
        #plt.xticks(np.linspace(-100,100,num=21))
        plt.xlim([f_min,f_max]); plt.ylim([y_min_scan,y_max_scan]);# plt.ylim([65, 75])
        plt.grid('on')
        plt.legend(loc='lower left')
        plt.title('SW: ' + acu + '\nFreq = ' + ' X' + '\nb1: Th=' + str(Th_deg_list[p]) + ', Phi=' + str(Ph_deg), fontsize=15)
        plt.tight_layout()
        plt.savefig(savePath + '\\' +  'Frequency_comparison_Th_'+ str(Th_deg_list[p]) + '_Phi_' + str(Ph_deg)+'.png', dpi=400)
    plt.close('all')
    
#sb_mute = 'OFF'
    
