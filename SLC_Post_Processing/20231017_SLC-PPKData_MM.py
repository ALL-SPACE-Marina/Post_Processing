import pandas as pd
import numpy as np
import matplotlib.pyplot as plt; plt.rcParams['font.size'] = 15
import os
import pip
plt.close('all')

# load
fileName = r'G:\measurements\TLM_Meas\DVT_I-Type\Tx_TLM\QR00239\RHCP\B1\Cal_Investigation\SLC3\PP_Data\ppk_data'
savePath=r'G:\measurements\TLM_Meas\DVT_I-Type\Tx_TLM\QR00239\RHCP\B1\Cal_Investigation\SLC3\PP_Data'
Th_deg_list=[0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 55.0, 60.0, 65.0, 70.0]
Ph_deg=[0.0]#, 14.4, 28.8, 43.2, 57.6, 72.0, 86.4]

TLM_Type='Tx'
Pol='RHCP'

if TLM_Type=='Rx':
    cal_freq_list = [17.7, 18.2, 18.7, 19.2, 19.7, 20.2, 20.7, 21.2]
    meas_freq_list =[17.7, 18.2, 18.7, 19.2, 19.7, 20.2, 20.7, 21.2]
    f_min=17.2
    f_max=21.7
    y_min_scan=40
    y_max_scan=90
    y_min_scan_xpd = 0
    y_max_scan_xpd = 30
elif TLM_Type=='Tx':
    cal_freq_list=[27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0]
    meas_freq_list=[27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0]
    f_min = 27.0
    f_max = 31.5
    y_min_scan =20
    y_max_scan =80
    y_min_scan_xpd = 0
    y_max_scan_xpd = 30

# labelLog = ['QR00057_F-Type', 'QR00012_G-Type', 'QR00002_G-Type', 'QR00034_G-Type_1p5', 'QR00060_G-Type_1p5']
# fpathLog = [r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_G-Type_1p5/Tx_TLM/Comparisons/SLC3/TLM_Type_Comp_att0/Raw_Data/QR00057_F-Type',
#             r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_G-Type_1p5/Tx_TLM/Comparisons/SLC3/TLM_Type_Comp_att0/Raw_Data/QR00012_G-Type',
#             r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_G-Type_1p5/Tx_TLM/Comparisons/SLC3/TLM_Type_Comp_att0/Raw_Data/QR00002_G-Type',
#             r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_G-Type_1p5/Tx_TLM/Comparisons/SLC3/TLM_Type_Comp_att0/Raw_Data/QR00034_G-Type_1p5',
#             r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_G-Type_1p5/Tx_TLM/Comparisons/SLC3/TLM_Type_Comp_att0/Raw_Data/QR00060_G-Type_1p5']

labelLog = ['Cal_13mm', 'Cal_10mm', 'Cal_15mm', 'Cal_20mm']#, 'QR00011_I-Type',
fpathLog = [r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_I-Type/Tx_TLM/QR00239/RHCP/B1/Cal_Investigation/SLC3/Raw_Data/Ass_Cal',
            r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_I-Type/Tx_TLM/QR00239/RHCP/B1/Cal_Investigation/SLC3/Raw_Data/Ass_Cal_10mm',
            r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_I-Type/Tx_TLM/QR00239/RHCP/B1/Cal_Investigation/SLC3/Raw_Data/Ass_Cal_15mm',
            #r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_I-Type/Rx_TLM/Comparisons/SLC2/F_vs_G_vs_I/Raw_Data/QR00011_I-Type',
            r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_I-Type/Tx_TLM/QR00239/RHCP/B1/Cal_Investigation/SLC3/Raw_Data/Ass_Cal_20mm']

# labelLog = ['Aluminum', 'Plastic'] #'QR00002_I-Type', 'QR00011_I-Type',
# fpathLog = [r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_F-Type/Rx_TLM/QR440-0111-00005/RHCP/B1/Nest_Test/SLC2/Raw_Data/Aluminum',
#             #r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_I-Type/Rx_TLM/Comparisons/SLC2/F_vs_G_vs_I/Raw_Data/QR00020_G-Type',
#             #r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_I-Type/Rx_TLM/Comparisons/SLC2/F_vs_G_vs_I/Raw_Data/QR00002_I-Type',
#             #r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_I-Type/Rx_TLM/Comparisons/SLC2/F_vs_G_vs_I/Raw_Data/QR00011_I-Type',
#             r'/mnt/nfs/data/groups/measurements/TLM_Meas/DVT_F-Type/Rx_TLM/QR440-0111-00005/RHCP/B1/Nest_Test/SLC2/Raw_Data/Plastic']


dirScript = os.getcwd()
os.chdir(dirScript)
dfFull = pd.read_excel(fileName + ".xlsx")
markerList=['s', 'o', '^', 'D', 'X', 'p', '*', 'H']
colourMap = [['b','orange','g','r','purple','brown','magenta','grey'],
             ['c', 'peru', 'darkgreen', 'darksalmon', 'plum', 'chocolate', 'hotpink', 'k'],
             ['cornflowerblue', 'tan', 'greenyellow', 'darkred', 'blueviolet', 'rosybrown', 'mediumvioletred', 'darkslategrey'],
             ['deepskyblue', 'gold', 'olivedrab', 'crimson', 'indigo', 'sienna', 'orchid', 'silver']]

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

def plot__gainVstheta(fpath, cal_freq, meas_freq, phi_deg):
    global dfPlot, df, x, y, columns, acu, xpd_theta

    # load
    dirScript = os.getcwd()
    os.chdir(dirScript)
    df = pd.read_excel(fileName + ".xlsx")
    columns = df.columns.tolist()

    #reduce

    df = df[(df["phi_deg"] == phi_deg)]
    df = df[(df["cal_freq_GHz"] == cal_freq)]
    df = df[(df["freq_GHz"] == meas_freq)]
    df = df[(df["entry_type"] == 'gain_at_requested_angle')]
    df = df[(df["fpath_parent"] == fpath)]
    df = df[(df["lens_enabled"] == 'l1e_l2e_l3e')]
    acu=np.array(df['acu_version'])[0]
    print(acu)

    x = np.array(df['theta_deg'])
    y = np.array(df['Gain_dB'])
    xpd_theta=np.array(df['xpd_dB'])

def plot__gainVsfreq(fpath,Th_deg,Ph_degree):
    global dfPlot, df, x, y, columns, phi_meas_freq, xpd_freq

    # load
    dirScript = os.getcwd()
    os.chdir(dirScript)
    df = pd.read_excel(fileName + ".xlsx")
    columns = df.columns.tolist()

    #reduce
    # df = df[(df["pb_theta_deg"] == b1_theta)]
    df = df[(df["phi_deg"] == Ph_degree)]
    # df = df[(df["sb_mute"] == sb_mute)]
    df = df[(df["theta_deg"] == Th_deg)]
    df = df[(df["freq_GHz"] == df["cal_freq_GHz"])]
    df = df[(df["entry_type"] == 'gain_at_requested_angle')]
    df = df[(df["fpath_parent"] == fpath)]

    phi_meas_freq = np.array(df['pa_phi_deg'])
    x = np.array(df['freq_GHz'])
    y = np.array(df['Gain_dB'])
    xpd_freq=np.array(df['xpd_dB'])


def plot__mispointVsfreq(fpath,Th_deg,Ph_degree):
    global dfPlot, df, x, columns, phi_meas_freq, phi_mispoint, th_mispoint,acu

    # load
    dirScript = os.getcwd()
    os.chdir(dirScript)
    df = pd.read_excel(fileName + ".xlsx")
    columns = df.columns.tolist()

    #reduce
    df = df[(df["pa_phi_deg"] == Ph_degree)]
    df = df[(df["pa_theta_deg"] == Th_deg)]
    df = df[(df["freq_GHz"] == df["cal_freq_GHz"])]
    df = df[(df["fpath_parent"] == fpath)]
    df_request = df[(df["entry_type"] == 'gain_at_requested_angle')]
    df_peak = df[(df["entry_type"] == 'gain_at_peak')]
    acu = np.array(df['acu_version'])[0]

    th_request=np.array(df_request['theta_deg'])
    th_peak = np.array(df_peak['theta_deg'])
    ph_request= np.array(df_request['phi_deg'])
    ph_peak = np.array(df_peak['phi_deg'])
    phi_mispoint= ph_peak-ph_request
    th_mispoint= th_peak-th_request
    x = np.array(df_request['freq_GHz'])
    phi_meas_freq = np.array(df_request['pa_phi_deg'])





# for k in range(len(cal_freq_list)):
#
#
#     for l in range(len(Ph_deg)):
#         plt.figure(figsize=([7, 6]))
#         for i in range(len(fpathLog)):
#             Ph_degree=Ph_deg[l]
#             print(Ph_degree)
#
#             fpath = fpathLog[i]
#             plot__gainVstheta(fpath, cal_freq_list[k], meas_freq_list[k], Ph_degree)
#             plt.plot(x, y, markerList[i], markerfacecolor= colourMap[0][i], markeredgecolor='k', markersize=10, label='Gain ' + labelLog[i])
#             plt.plot(x, y-xpd_theta, markerList[i], markerfacecolor= colourMap[2][i], markeredgecolor='k', markersize=10, label='XP ' + labelLog[i])
#             plt.xlabel('Theta, [deg]', fontsize=10);
#             plt.ylabel('Gain & XP, [dB]\n(at req. angle)', fontsize=10)
#             plt.yticks(np.linspace(0, 100, num=21), fontsize=10)
#             plt.xticks(np.linspace(-100, 100, num=21), fontsize=10)
#             plt.xlim([-10, 80]);
#             plt.ylim([y_min_scan, y_max_scan]);  # plt.ylim([65, 75])
#             plt.grid('on')
#             plt.legend(loc='lower left', fontsize=10)
#             plt.title(
#                 Pol +' Gain & XP L3'+'\nSW: ' + acu + '\nFreq = ' + str(meas_freq_list[k]) + ' GHz' + '\nTh=' + 'X' + ', Phi=' + str(Ph_degree),
#                 fontsize=15)
#             plt.tight_layout()
#             plt.savefig(
#                 savePath + '\\' + 'Gain_XP_Pointing_angle_Phi_' + str(Ph_degree) + 'Freq_' + str(meas_freq_list[k]) + 'GHz.png',
#                 dpi=400)
#         plt.close('all')







# for p in range(len(Th_deg_list)):
#
#
#     for l in range(len(Ph_deg)):
#         plt.figure(figsize=([7, 6]))
#         for i in range(len(fpathLog)):
#             Ph_degree=Ph_deg[l]
#             fpath = fpathLog[i]
#             plot__gainVsfreq(fpath, Th_deg_list[p], Ph_degree)
#             plt.plot(x, y, markerList[i], markerfacecolor= colourMap[0][i], markeredgecolor='k', markersize=10, label='Gain ' + labelLog[i])
#             plt.plot(x, y - xpd_freq, markerList[i], markerfacecolor=colourMap[2][i], markeredgecolor='k', markersize=10, label='XP ' + labelLog[i])
#             plt.xlabel('Frequency, [GHz]', fontsize=10);
#             plt.ylabel('Gain & XP, [dB]\n(at req. angle)', fontsize=10)
#             plt.yticks(np.linspace(0,100,num=21), fontsize=10)
#             plt.xticks(fontsize=10)
#             #plt.xticks(np.linspace(-100,100,num=21))
#             plt.xlim([f_min,f_max]); plt.ylim([y_min_scan,y_max_scan]);# plt.ylim([65, 75])
#             plt.grid('on')
#             plt.legend(loc='lower left', fontsize=10)
#             plt.title(Pol + 'Gain & XP \nSW: ' + acu + '\nFreq = ' + ' X' + '\nTh=' + str(Th_deg_list[p]) + ', Phi=' + str(Ph_degree), fontsize=15)
#             plt.tight_layout()
#             plt.savefig(savePath + '\\' +  'Gain_XP_Frequency_comparison_Th_'+ str(Th_deg_list[p]) + '_Phi_' + str(Ph_degree)+'.png', dpi=400)
#         plt.close('all')



for p in range(len(Th_deg_list)):


    for l in range(len(Ph_deg)):
        plt.figure(figsize=([7, 6]))
        for i in range(len(fpathLog)):
            Ph_degree=Ph_deg[l]
            fpath = fpathLog[i]
            plot__mispointVsfreq(fpath, Th_deg_list[p], Ph_degree)
            print(x)
            print(th_mispoint)
            plt.plot(x, th_mispoint, markerList[i], markerfacecolor= colourMap[0][i], markeredgecolor='k', markersize=10, label='Gain ' + labelLog[i])
            #plt.plot(x, y - xpd_freq, markerList[i], markerfacecolor=colourMap[2][i], markeredgecolor='k', markersize=10, label='XP ' + labelLog[i])
            plt.xlabel('Frequency, [GHz]', fontsize=10);
            plt.ylabel('Gain & XP, [dB]\n(at req. angle)', fontsize=10)
            plt.yticks(np.linspace(-10,10,num=21), fontsize=10)
            plt.xticks(fontsize=10)
            #plt.xticks(np.linspace(-100,100,num=21))
            plt.xlim([f_min,f_max]); plt.ylim([-10,10]);# plt.ylim([65, 75])
            plt.grid('on')
            plt.legend(loc='lower left', fontsize=10)
            plt.title(Pol + 'Gain & XP \nSW: ' + acu + '\nFreq = ' + ' X' + '\nTh=' + str(Th_deg_list[p]) + ', Phi=' + str(Ph_degree), fontsize=15)
            plt.tight_layout()
            plt.savefig(savePath + '\\' +  'Theta_Mispoint_Frequency_comparison_Th_'+ str(Th_deg_list[p]) + '_Phi_' + str(Ph_degree)+'.png', dpi=400)
        plt.close('all')


# for p in range(len(Th_deg_list)):
#
#     for i in range(len(fpathLog)):
#         fpath = fpathLog[i]
#         plot__gainVsfreq(fpath, Th_deg_list[p])
#         plt.plot(x, xpd_freq, markerList[i], markeredgecolor='k', markersize=10, label = labelLog[i])
#         plt.xlabel('freq [GHz]'); plt.ylabel('Beam 1 XPD [dB]\n(at req. angle)')
#         plt.yticks(np.linspace(0,100,num=21))
#         #plt.xticks(np.linspace(-100,100,num=21))
#         plt.xlim([f_min,f_max]); plt.ylim([y_min_scan_xpd,y_max_scan_xpd]);# plt.ylim([65, 75])
#         plt.grid('on')
#         plt.legend(loc='lower left')
#         plt.title('SW: ' + acu + '\nFreq = ' + ' X' + '\nb1: Th=' + str(Th_deg_list[p]) + ', Phi=' + str(Ph_deg), fontsize=15)
#         plt.tight_layout()
#         plt.savefig(savePath + '\\' +  'XPD_Frequency_comparison_Th_'+ str(Th_deg_list[p]) + '_Phi_' + str(Ph_deg)+'.png', dpi=400)
#     plt.close('all')
#
#sb_mute = 'OFF'
    
