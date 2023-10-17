import pandas as pd
import numpy as np
import matplotlib.pyplot as plt; plt.rcParams['font.size'] = 15
import os
import pip
plt.close('all')

# load
fileName = r'C:\Terminal_Testing\G-Type_Test\SLC3_Tx_F-G_Comparison\ppk_data'
Th_deg=30.0
Ph_deg=0.0
cal_freq=29.5
meas_freq=29.5

dirScript = os.getcwd()
os.chdir(dirScript)
dfFull = pd.read_excel(fileName + ".xlsx")

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

def plot__gainVstheta(fpath):
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

    x = np.array(df['theta_deg'])
    y = np.array(df['Gain_dB'])



labelLog = ['F-Type_QR00057', 'G-Type_QR00012', 'G-Type_QR00017']

plt.figure(figsize=([7,6]))
fpathLog = [r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_G-Type/Tx_TLM/Comparisons/SLC3/Raw_Data/F-Type_QR00057',
            r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_G-Type/Tx_TLM/Comparisons/SLC3/Raw_Data/G-Type_QR00012',
            r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_G-Type/Tx_TLM/Comparisons/SLC3/Raw_Data/G-Type_QR00017']
for i in range(len(fpathLog)):
    fpath = fpathLog[i]
    plot__gainVstheta(fpath)
    plt.plot(x, y, 's', markeredgecolor='k', markersize=10, label = labelLog[i])
    plt.xlabel('Theta [deg]'); plt.ylabel('Beam 1 gain [dB]\n(at req. angle)')
    plt.yticks(np.linspace(0,100,num=51))
    plt.xticks(np.linspace(-100,100,num=21))
    plt.xlim([-10,80]); plt.ylim([30,70]);# plt.ylim([65, 75])
    plt.grid('on')
    plt.legend(loc='lower left')
    plt.title('SW: ' + acu + '\nFreq = ' + str(meas_freq) + ' GHz' + '\nb1: Th=' + 'X' + ', Phi=' + str(Ph_deg), fontsize=15)
    plt.tight_layout()
    plt.savefig(r'C:\Terminal_Testing\G-Type_Test\SLC3_Tx_F-G_Comparison'+'\\' + 'Pointing_angle_Phi_' + str(Ph_deg) + 'Freq_' + str(meas_freq)+'GHz.png', dpi=400)

    
    
    



def plot__gainVsfreq(fpath):
    global dfPlot, df, x, y, columns, phi_meas_freq

    # load
    dirScript = os.getcwd()
    os.chdir(dirScript)
    df = pd.read_excel(fileName + ".xlsx")
    columns = df.columns.tolist()

    #reduce
    # df = df[(df["pb_theta_deg"] == b1_theta)]
    #df = df[(df["phi_deg"] == Ph_deg)]
    # df = df[(df["sb_mute"] == sb_mute)]
    df = df[(df["theta_deg"] == Th_deg)]
    df = df[(df["freq_GHz"] == df["cal_freq_GHz"])]
    df = df[(df["entry_type"] == 'gain_at_requested_angle')]
    df = df[(df["fpath_parent"] == fpath)]

    phi_meas_freq = np.array(df['pa_phi_deg'])
    print(phi_meas_freq)
    x = np.array(df['freq_GHz'])
    y = np.array(df['Gain_dB'])

labelLog = ['F-Type_QR00057', 'G-Type_QR00012', 'G-Type_QR00017']

plt.figure(figsize=([7,6]))
fpathLog = [r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_G-Type/Tx_TLM/Comparisons/SLC3/Raw_Data/F-Type_QR00057',
            r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_G-Type/Tx_TLM/Comparisons/SLC3/Raw_Data/G-Type_QR00012',
            r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_G-Type/Tx_TLM/Comparisons/SLC3/Raw_Data/G-Type_QR00017']

for i in range(len(fpathLog)):
    fpath = fpathLog[i]
    plot__gainVsfreq(fpath)
    plt.plot(x, y, 's', markeredgecolor='k', markersize=10, label = labelLog[i])
    plt.xlabel('freq [GHz]'); plt.ylabel('Beam 1 gain [dB]\n(at req. angle)')
    plt.yticks(np.linspace(0,100,num=21))
    #plt.xticks(np.linspace(-100,100,num=21))
    plt.xlim([27.5,31.0]); plt.ylim([0,70]);# plt.ylim([65, 75])
    plt.grid('on')
    plt.legend(loc='lower left')
    plt.title('SW: ' + acu + '\nFreq = ' + ' X' + '\nb1: Th=' + str(Th_deg) + ', Phi=' + str(Ph_deg), fontsize=15)
    plt.tight_layout()
    plt.savefig(r'C:\Terminal_Testing\G-Type_Test\SLC3_Tx_F-G_Comparison' + '\\' +  'Frequency_comparison_Th_'+ str(Th_deg) + '_Phi_' + str(Ph_deg)+'.png', dpi=400)
    
    
    sb_mute = 'OFF'
    
