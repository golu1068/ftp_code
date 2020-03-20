import os
import sys
import time
import plotly
import converter
import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
#from IPython.display import HTML


def cggtts(cggtts_path, file_name):
    print(file_name)

    path = cggtts_path + "\\" + file_name
    
##    fout = open(os.path.join(cggtts_path, file_name[0:14]+"_time_missed.txt"), "w")
    try:
        cggtts_file = open(path,"r")
        fout = open(os.path.join(cggtts_path, file_name[0:14]+"_time_missed.txt"), "w")
    except:
        print("Cannot open file %s" %file_name)
##        sys.exit(0)
    ####################################################################################
    second_list=[];refsys_list=[];srsys_list=[];msio_list=[]; smsi_list=[];iontype_list=[];
    elv_list=[];azth_list=[];second_first=0;time_from=[];time_to=[];
    ##############################################################################
    for j in range(1,12):
        
        second_list.clear();refsys_list.clear();srsys_list.clear();msio_list.clear();smsi_list.clear();iontype_list.clear();
        elv_list.clear();azth_list.clear();time_from.clear();time_to.clear();
        
        while 1:
            line = cggtts_file.readline()
            if (line == ""):
                print("Data is not in the file: ")
                break        
            if "hhmmss" in line:
                break   
        while 1:
            line = cggtts_file.readline()
            
            if (line == ""):
##                print("End of cggtts file reached: ")
                break
            
            try:
                prn = int(line[1:3])
                if (prn == j):
                    mjd = int(line[7:12])
                    hh = int(line[13:15])
                    minute = int(line[15:17])
                    sec = int(line[17:19])
                    second = hh*3600 + minute*60 + sec
                    second_list.append(second)

                    elv = int(line[25:28])
                    elv_list.append(elv)
                    azth = int(line[29:33])
                    azth_list.append(azth)
                    
                    refsys = int(line[53:64])
                    refsys_list.append(refsys)
                    srsys = int(line[65:71])
                    srsys_list.append(srsys)

                    msio_str = (line[101:105])
                    if (msio_str == "    "):
                        pass
                    else:   
                        msio_list.append(int(msio_str))
                    smsi_str = (line[106:110])
                    if (smsi_str == "    "):
                        pass
                    else:   
                        smsi_list.append(int(smsi_str))

                    iontype = (line[128:132])    
                    if (iontype == "DUAL"):
                        iono = 20
                    elif(iontype == "GCD "):
                        iono = 18
                    elif(iontype == "ICM "):
                        iono = 16
                    elif(iontype == "IGM "):
                        iono = 14
                    elif(iontype == "GD  "):
                        iono = 12
                    elif(iontype == "GC  "):
                        iono = 10  
                    elif(iontype == "CD  "):
                        iono = 8
                    elif(iontype == "D   "):
                        iono = 6
                    elif(iontype == "G   "):
                        iono = 4
                    elif(iontype == "C   "):
                        iono = 2
                    else:
                        print("Iontype %s is not in the list" %iontype)

                    iontype_list.append(iono)        
                else:
                    continue
            except:
##                print("Problem in reading line after hh:min:sec= %d:%d:%d" %(hh, minute, sec))
                continue
        ##########################################################################
        
        x_elv = list(range(0,len(elv_list)))
        y_elv = elv_list
        x_azth = list(range(0,len(azth_list)))
        y_azth = azth_list
        x_refsys = list(range(0,len(refsys_list)))
        y_refsys = refsys_list
        x_srsys = list(range(0,len(srsys_list)))
        y_srsys = srsys_list
        x_msio = list(range(0,len(msio_list)))
        y_msio = msio_list
        x_smsi = list(range(0,len(smsi_list)))
        y_smsi = smsi_list
        x_iontype = list(range(0,len(iontype_list)))
        y_iontype = iontype_list
        ##########################################################################
##        os.chdir(r"F:\plot")
        cgg_plot_path = os.getcwd()
        try:
            if (j==1):
                if (len(second_list) != 0):
                    
                    second_first = second_list[0]
                    for j in range(1,len(second_list)):
                        if ((second_list[j] - second_first) != 960 and (second_list[j] - second_first) != 1680):
                            time_pre = time.asctime(time.gmtime(second_first))[11:19]
                            time_next = time.asctime(time.gmtime(second_list[j]))[11:19]
                            
                            time_from.append(time_pre)
                            time_to.append(time_next)
                            fout.write("For PRN= 1\n")
                            fout.write("Time missed from %s to %s\n\n" %(time_pre, time_next))
                            second_first = second_list[j]
                        else:
                            second_first = second_list[j]
                    xy_data_elv = go.Scatter( x=x_elv, y=y_elv, mode='lines+markers', name='ELV_1' )
                    xy_data_azth = go.Scatter( x=x_azth, y=y_azth, mode='lines+markers', name='AZTH_1' )
                    xy_data_refsys = go.Scatter( x=x_refsys, y=y_refsys, mode='lines+markers', name='REFSYS_1' )
                    xy_data_srsys = go.Scatter( x=x_srsys, y=y_srsys, mode='lines+markers', name='SRSYS_1' )
                    xy_data_msio = go.Scatter( x=x_msio, y=y_msio, mode='lines+markers', name='MSIO_1' )
                    xy_data_smsi = go.Scatter( x=x_smsi, y=y_smsi, mode='lines+markers', name='SMSI_1' )
                    xy_data_iontype1 = go.Scatter( x=x_iontype, y=y_iontype, mode='lines+markers', name='IONTYPE_1' )
                    xy_data_prn1 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
                else:
                    xy_data_elv = go.Scatter( x=[], y=[], mode='lines+markers', name='ELV_1' )
                    xy_data_azth = go.Scatter( x=[], y=[], mode='lines+markers', name='AZTH_1' )
                    xy_data_refsys = go.Scatter( x=[], y=[], mode='lines+markers', name='REFSYS_1' )
                    xy_data_srsys = go.Scatter( x=[], y=[], mode='lines+markers', name='SRSYS_1' )
                    xy_data_msio = go.Scatter( x=[], y=[], mode='lines+markers', name='MSIO_1' )
                    xy_data_smsi = go.Scatter( x=[], y=[], mode='lines+markers', name='SMSI_1' )
                    xy_data_iontype1 = go.Scatter( x=[], y=[], mode='lines+markers', name='IONTYPE_1' )
                    xy_data_prn1 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
            elif (j==2):
                if (len(second_list) != 0):
                    
                    second_first = second_list[0]
                    for j in range(1,len(second_list)):
                        if ((second_list[j] - second_first) != 960 and (second_list[j] - second_first) != 1680):
                            time_pre = time.asctime(time.gmtime(second_first))[11:19]
                            time_next = time.asctime(time.gmtime(second_list[j]))[11:19]
                            
                            time_from.append(time_pre)
                            time_to.append(time_next)
                            fout.write("For PRN= 2\n")
                            fout.write("Time missed from %s to %s\n\n" %(time_pre, time_next))
                            second_first = second_list[j]
                        else:
                            second_first = second_list[j]
                    xy_data_elv = go.Scatter( x=x_elv, y=y_elv, mode='lines+markers', name='ELV_2' )
                    xy_data_azth = go.Scatter( x=x_azth, y=y_azth, mode='lines+markers', name='AZTH_2' )
                    xy_data_refsys = go.Scatter( x=x_refsys, y=y_refsys, mode='lines+markers', name='REFSYS_2' )
                    xy_data_srsys = go.Scatter( x=x_srsys, y=y_srsys, mode='lines+markers', name='SRSYS_2' )
                    xy_data_msio = go.Scatter( x=x_msio, y=y_msio, mode='lines+markers', name='MSIO_2' )
                    xy_data_smsi = go.Scatter( x=x_smsi, y=y_smsi, mode='lines+markers', name='SMSI_2' )
                    xy_data_iontype2 = go.Scatter( x=x_iontype, y=y_iontype, mode='lines+markers', name='IONTYPE_2' )
                    xy_data_prn2 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
                else:
                    xy_data_elv = go.Scatter( x=[], y=[], mode='lines+markers', name='ELV_2' )
                    xy_data_azth = go.Scatter( x=[], y=[], mode='lines+markers', name='AZTH_2' )
                    xy_data_refsys = go.Scatter( x=[], y=[], mode='lines+markers', name='REFSYS_2' )
                    xy_data_srsys = go.Scatter( x=[], y=[], mode='lines+markers', name='SRSYS_2' )
                    xy_data_msio = go.Scatter( x=[], y=[], mode='lines+markers', name='MSIO_2' )
                    xy_data_smsi = go.Scatter( x=[], y=[], mode='lines+markers', name='SMSI_2' )
                    xy_data_iontype2 = go.Scatter( x=[], y=[], mode='lines+markers', name='IONTYPE_2' )
                    xy_data_prn2 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
            ###############################################################################################################################
            elif (j==3):
                if (len(second_list) != 0):
                    
                    second_first = second_list[0]
                    for j in range(1,len(second_list)):
                        if ((second_list[j] - second_first) != 960 and (second_list[j] - second_first) != 1680):
                            time_pre = time.asctime(time.gmtime(second_first))[11:19]
                            time_next = time.asctime(time.gmtime(second_list[j]))[11:19]
                            
                            time_from.append(time_pre)
                            time_to.append(time_next)
                            fout.write("For PRN= 3\n")
                            fout.write("Time missed from %s to %s\n\n" %(time_pre, time_next))
                            second_first = second_list[j]
                        else:
                            second_first = second_list[j]
                    xy_data_elv = go.Scatter( x=x_elv, y=y_elv, mode='lines+markers', name='ELV_3' )
                    xy_data_azth = go.Scatter( x=x_azth, y=y_azth, mode='lines+markers', name='AZTH_3' )
                    xy_data_refsys = go.Scatter( x=x_refsys, y=y_refsys, mode='lines+markers', name='REFSYS_3' )
                    xy_data_srsys = go.Scatter( x=x_srsys, y=y_srsys, mode='lines+markers', name='SRSYS_3' )
                    xy_data_msio = go.Scatter( x=x_msio, y=y_msio, mode='lines+markers', name='MSIO_3' )
                    xy_data_smsi = go.Scatter( x=x_smsi, y=y_smsi, mode='lines+markers', name='SMSI_3' )
                    xy_data_iontype3 = go.Scatter( x=x_iontype, y=y_iontype, mode='lines+markers', name='IONTYPE_3' )
                    xy_data_prn3 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
                else:
                    xy_data_elv = go.Scatter( x=[], y=[], mode='lines+markers', name='ELV_3' )
                    xy_data_azth = go.Scatter( x=[], y=[], mode='lines+markers', name='AZTH_3' )
                    xy_data_refsys = go.Scatter( x=[], y=[], mode='lines+markers', name='REFSYS_3' )
                    xy_data_srsys = go.Scatter( x=[], y=[], mode='lines+markers', name='SRSYS_3' )
                    xy_data_msio = go.Scatter( x=[], y=[], mode='lines+markers', name='MSIO_3' )
                    xy_data_smsi = go.Scatter( x=[], y=[], mode='lines+markers', name='SMSI_3' )
                    xy_data_iontype3 = go.Scatter( x=[], y=[], mode='lines+markers', name='IONTYPE_3' )
                    xy_data_prn3 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
            elif (j==4):
                if (len(second_list) != 0):
                    
                    second_first = second_list[0]
                    for j in range(1,len(second_list)):
                        if ((second_list[j] - second_first) != 960 and (second_list[j] - second_first) != 1680):
                            time_pre = time.asctime(time.gmtime(second_first))[11:19]
                            time_next = time.asctime(time.gmtime(second_list[j]))[11:19]
                            
                            time_from.append(time_pre)
                            time_to.append(time_next)
                            fout.write("For PRN= 4\n")
                            fout.write("Time missed from %s to %s\n\n" %(time_pre, time_next))
                            second_first = second_list[j]
                        else:
                            second_first = second_list[j]
                    xy_data_elv = go.Scatter( x=x_elv, y=y_elv, mode='lines+markers', name='ELV_4' )
                    xy_data_azth = go.Scatter( x=x_azth, y=y_azth, mode='lines+markers', name='AZTH_4' )
                    xy_data_refsys = go.Scatter( x=x_refsys, y=y_refsys, mode='lines+markers', name='REFSYS_4' )
                    xy_data_srsys = go.Scatter( x=x_srsys, y=y_srsys, mode='lines+markers', name='SRSYS_4' )
                    xy_data_msio = go.Scatter( x=x_msio, y=y_msio, mode='lines+markers', name='MSIO_4' )
                    xy_data_smsi = go.Scatter( x=x_smsi, y=y_smsi, mode='lines+markers', name='SMSI_4' )
                    xy_data_iontype4 = go.Scatter( x=x_iontype, y=y_iontype, mode='lines+markers', name='IONTYPE_4' )
                    xy_data_prn4 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
                else:
                    xy_data_elv = go.Scatter( x=[], y=[], mode='lines+markers', name='ELV_4' )
                    xy_data_azth = go.Scatter( x=[], y=[], mode='lines+markers', name='AZTH_4' )
                    xy_data_refsys = go.Scatter( x=[], y=[], mode='lines+markers', name='REFSYS_4' )
                    xy_data_srsys = go.Scatter( x=[], y=[], mode='lines+markers', name='SRSYS_4' )
                    xy_data_msio = go.Scatter( x=[], y=[], mode='lines+markers', name='MSIO_4' )
                    xy_data_smsi = go.Scatter( x=[], y=[], mode='lines+markers', name='SMSI_4' )
                    xy_data_iontype4 = go.Scatter( x=[], y=[], mode='lines+markers', name='IONTYPE_4' )
                    xy_data_prn4 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
            elif (j==5):
                if (len(second_list) != 0):
                    
                    second_first = second_list[0]
                    for j in range(1,len(second_list)):
                        if ((second_list[j] - second_first) != 960 and (second_list[j] - second_first) != 1680):
                            time_pre = time.asctime(time.gmtime(second_first))[11:19]
                            time_next = time.asctime(time.gmtime(second_list[j]))[11:19]
                            
                            time_from.append(time_pre)
                            time_to.append(time_next)
                            fout.write("For PRN= 5\n")
                            fout.write("Time missed from %s to %s\n\n" %(time_pre, time_next))
                            second_first = second_list[j]
                        else:
                            second_first = second_list[j]
                    xy_data_elv = go.Scatter( x=x_elv, y=y_elv, mode='lines+markers', name='ELV_5' )
                    xy_data_azth = go.Scatter( x=x_azth, y=y_azth, mode='lines+markers', name='AZTH_5' )
                    xy_data_refsys = go.Scatter( x=x_refsys, y=y_refsys, mode='lines+markers', name='REFSYS_5' )
                    xy_data_srsys = go.Scatter( x=x_srsys, y=y_srsys, mode='lines+markers', name='SRSYS_5' )
                    xy_data_msio = go.Scatter( x=x_msio, y=y_msio, mode='lines+markers', name='MSIO_5' )
                    xy_data_smsi = go.Scatter( x=x_smsi, y=y_smsi, mode='lines+markers', name='SMSI_5' )
                    xy_data_iontype5 = go.Scatter( x=x_iontype, y=y_iontype, mode='lines+markers', name='IONTYPE_5' )
                    xy_data_prn5 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
                else:
                    xy_data_elv = go.Scatter( x=[], y=[], mode='lines+markers', name='ELV_5' )
                    xy_data_azth = go.Scatter( x=[], y=[], mode='lines+markers', name='AZTH_5' )
                    xy_data_refsys = go.Scatter( x=[], y=[], mode='lines+markers', name='REFSYS_5' )
                    xy_data_srsys = go.Scatter( x=[], y=[], mode='lines+markers', name='SRSYS_5' )
                    xy_data_msio = go.Scatter( x=[], y=[], mode='lines+markers', name='MSIO_5' )
                    xy_data_smsi = go.Scatter( x=[], y=[], mode='lines+markers', name='SMSI_5' )
                    xy_data_iontype5 = go.Scatter( x=[], y=[], mode='lines+markers', name='IONTYPE_5' )
                    xy_data_prn5 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
            elif (j==6):
                if (len(second_list) != 0):
                    
                    second_first = second_list[0]
                    for j in range(1,len(second_list)):
                        if ((second_list[j] - second_first) != 960 and (second_list[j] - second_first) != 1680):
                            time_pre = time.asctime(time.gmtime(second_first))[11:19]
                            time_next = time.asctime(time.gmtime(second_list[j]))[11:19]
                            
                            time_from.append(time_pre)
                            time_to.append(time_next)
                            fout.write("For PRN= 6\n")
                            fout.write("Time missed from %s to %s\n\n" %(time_pre, time_next))
                            second_first = second_list[j]
                        else:
                            second_first = second_list[j]
                    xy_data_elv = go.Scatter( x=x_elv, y=y_elv, mode='lines+markers', name='ELV_6' )
                    xy_data_azth = go.Scatter( x=x_azth, y=y_azth, mode='lines+markers', name='AZTH_6' )
                    xy_data_refsys = go.Scatter( x=x_refsys, y=y_refsys, mode='lines+markers', name='REFSYS_6' )
                    xy_data_srsys = go.Scatter( x=x_srsys, y=y_srsys, mode='lines+markers', name='SRSYS_6' )
                    xy_data_msio = go.Scatter( x=x_msio, y=y_msio, mode='lines+markers', name='MSIO_6' )
                    xy_data_smsi = go.Scatter( x=x_smsi, y=y_smsi, mode='lines+markers', name='SMSI_6' )
                    xy_data_iontype6 = go.Scatter( x=x_iontype, y=y_iontype, mode='lines+markers', name='IONTYPE_6' )
                    xy_data_prn6 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
                else:
                    xy_data_elv = go.Scatter( x=[], y=[], mode='lines+markers', name='ELV_6' )
                    xy_data_azth = go.Scatter( x=[], y=[], mode='lines+markers', name='AZTH_6' )
                    xy_data_refsys = go.Scatter( x=[], y=[], mode='lines+markers', name='REFSYS_6' )
                    xy_data_srsys = go.Scatter( x=[], y=[], mode='lines+markers', name='SRSYS_6' )
                    xy_data_msio = go.Scatter( x=[], y=[], mode='lines+markers', name='MSIO_6' )
                    xy_data_smsi = go.Scatter( x=[], y=[], mode='lines+markers', name='SMSI_6' )
                    xy_data_iontype6 = go.Scatter( x=[], y=[], mode='lines+markers', name='IONTYPE_6' )
                    xy_data_prn6 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
            elif (j==7):
                if (len(second_list) != 0):
                    
                    second_first = second_list[0]
                    for j in range(1,len(second_list)):
                        if ((second_list[j] - second_first) != 960 and (second_list[j] - second_first) != 1680):
                            time_pre = time.asctime(time.gmtime(second_first))[11:19]
                            time_next = time.asctime(time.gmtime(second_list[j]))[11:19]
                            
                            time_from.append(time_pre)
                            time_to.append(time_next)
                            fout.write("For PRN= 7\n")
                            fout.write("Time missed from %s to %s\n\n" %(time_pre, time_next))
                            second_first = second_list[j]
                        else:
                            second_first = second_list[j]
                    xy_data_elv = go.Scatter( x=x_elv, y=y_elv, mode='lines+markers', name='ELV_7' )
                    xy_data_azth = go.Scatter( x=x_azth, y=y_azth, mode='lines+markers', name='AZTH_7' )
                    xy_data_refsys = go.Scatter( x=x_refsys, y=y_refsys, mode='lines+markers', name='REFSYS_7' )
                    xy_data_srsys = go.Scatter( x=x_srsys, y=y_srsys, mode='lines+markers', name='SRSYS_7' )
                    xy_data_msio = go.Scatter( x=x_msio, y=y_msio, mode='lines+markers', name='MSIO_7' )
                    xy_data_smsi = go.Scatter( x=x_smsi, y=y_smsi, mode='lines+markers', name='SMSI_7' )
                    xy_data_iontype7 = go.Scatter( x=x_iontype, y=y_iontype, mode='lines+markers', name='IONTYPE_7' )
                    xy_data_prn7 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
                else:
                    xy_data_elv = go.Scatter( x=[], y=[], mode='lines+markers', name='ELV_7' )
                    xy_data_azth = go.Scatter( x=[], y=[], mode='lines+markers', name='AZTH_7' )
                    xy_data_refsys = go.Scatter( x=[], y=[], mode='lines+markers', name='REFSYS_7' )
                    xy_data_srsys = go.Scatter( x=[], y=[], mode='lines+markers', name='SRSYS_7' )
                    xy_data_msio = go.Scatter( x=[], y=[], mode='lines+markers', name='MSIO_7' )
                    xy_data_smsi = go.Scatter( x=[], y=[], mode='lines+markers', name='SMSI_7' )
                    xy_data_iontype7 = go.Scatter( x=[], y=[], mode='lines+markers', name='IONTYPE_7' )
                    xy_data_prn7 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
            elif (j==8):
                if (len(second_list) != 0):
                    
                    second_first = second_list[0]
                    for j in range(1,len(second_list)):
                        if ((second_list[j] - second_first) != 960 and (second_list[j] - second_first) != 1680):
                            time_pre = time.asctime(time.gmtime(second_first))[11:19]
                            time_next = time.asctime(time.gmtime(second_list[j]))[11:19]
                            
                            time_from.append(time_pre)
                            time_to.append(time_next)
                            fout.write("For PRN= 8\n")
                            fout.write("Time missed from %s to %s\n\n" %(time_pre, time_next))
                            second_first = second_list[j]
                        else:
                            second_first = second_list[j]
                    xy_data_elv = go.Scatter( x=x_elv, y=y_elv, mode='lines+markers', name='ELV_8' )
                    xy_data_azth = go.Scatter( x=x_azth, y=y_azth, mode='lines+markers', name='AZTH_8' )
                    xy_data_refsys = go.Scatter( x=x_refsys, y=y_refsys, mode='lines+markers', name='REFSYS_8' )
                    xy_data_srsys = go.Scatter( x=x_srsys, y=y_srsys, mode='lines+markers', name='SRSYS_8' )
                    xy_data_msio = go.Scatter( x=x_msio, y=y_msio, mode='lines+markers', name='MSIO_8' )
                    xy_data_smsi = go.Scatter( x=x_smsi, y=y_smsi, mode='lines+markers', name='SMSI_8' )
                    xy_data_iontype8 = go.Scatter( x=x_iontype, y=y_iontype, mode='lines+markers', name='IONTYPE_8' )
                    xy_data_prn8 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
                else:
                    xy_data_elv = go.Scatter( x=[], y=[], mode='lines+markers', name='ELV_8' )
                    xy_data_azth = go.Scatter( x=[], y=[], mode='lines+markers', name='AZTH_8' )
                    xy_data_refsys = go.Scatter( x=[], y=[], mode='lines+markers', name='REFSYS_8' )
                    xy_data_srsys = go.Scatter( x=[], y=[], mode='lines+markers', name='SRSYS_8' )
                    xy_data_msio = go.Scatter( x=[], y=[], mode='lines+markers', name='MSIO_8' )
                    xy_data_smsi = go.Scatter( x=[], y=[], mode='lines+markers', name='SMSI_8' )
                    xy_data_iontype8 = go.Scatter( x=[], y=[], mode='lines+markers', name='IONTYPE_8' )
                    xy_data_prn8 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
            elif (j==9):
                if (len(second_list) != 0):
                    
                    second_first = second_list[0]
                    for j in range(1,len(second_list)):
                        if ((second_list[j] - second_first) != 960 and (second_list[j] - second_first) != 1680):
                            time_pre = time.asctime(time.gmtime(second_first))[11:19]
                            time_next = time.asctime(time.gmtime(second_list[j]))[11:19]
                            
                            time_from.append(time_pre)
                            time_to.append(time_next)
                            fout.write("For PRN= 9\n")
                            fout.write("Time missed from %s to %s\n\n" %(time_pre, time_next))
                            second_first = second_list[j]
                        else:
                            second_first = second_list[j]
                    xy_data_elv = go.Scatter( x=x_elv, y=y_elv, mode='lines+markers', name='ELV_9' )
                    xy_data_azth = go.Scatter( x=x_azth, y=y_azth, mode='lines+markers', name='AZTH_9' )
                    xy_data_refsys = go.Scatter( x=x_refsys, y=y_refsys, mode='lines+markers', name='REFSYS_9' )
                    xy_data_srsys = go.Scatter( x=x_srsys, y=y_srsys, mode='lines+markers', name='SRSYS_9' )
                    xy_data_msio = go.Scatter( x=x_msio, y=y_msio, mode='lines+markers', name='MSIO_9' )
                    xy_data_smsi = go.Scatter( x=x_smsi, y=y_smsi, mode='lines+markers', name='SMSI_9' )
                    xy_data_iontype9 = go.Scatter( x=x_iontype, y=y_iontype, mode='lines+markers', name='IONTYPE_9' )
                    xy_data_prn9 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
                else:
                    xy_data_elv = go.Scatter( x=[], y=[], mode='lines+markers', name='ELV_9' )
                    xy_data_azth = go.Scatter( x=[], y=[], mode='lines+markers', name='AZTH_9' )
                    xy_data_refsys = go.Scatter( x=[], y=[], mode='lines+markers', name='REFSYS_9' )
                    xy_data_srsys = go.Scatter( x=[], y=[], mode='lines+markers', name='SRSYS_9' )
                    xy_data_msio = go.Scatter( x=[], y=[], mode='lines+markers', name='MSIO_9' )
                    xy_data_smsi = go.Scatter( x=[], y=[], mode='lines+markers', name='SMSI_9' )
                    xy_data_iontype9 = go.Scatter( x=[], y=[], mode='lines+markers', name='IONTYPE_9' )
                    xy_data_prn9 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
            elif (j==10):
                if (len(second_list) != 0):
                    
                    second_first = second_list[0]
                    for j in range(1,len(second_list)):
                        if ((second_list[j] - second_first) != 960 and (second_list[j] - second_first) != 1680):
                            time_pre = time.asctime(time.gmtime(second_first))[11:19]
                            time_next = time.asctime(time.gmtime(second_list[j]))[11:19]
                            
                            time_from.append(time_pre)
                            time_to.append(time_next)
                            fout.write("For PRN= 10\n")
                            fout.write("Time missed from %s to %s\n\n" %(time_pre, time_next))
                            second_first = second_list[j]
                        else:
                            second_first = second_list[j]
                    xy_data_elv = go.Scatter( x=x_elv, y=y_elv, mode='lines+markers', name='ELV_10' )
                    xy_data_azth = go.Scatter( x=x_azth, y=y_azth, mode='lines+markers', name='AZTH_10' )
                    xy_data_refsys = go.Scatter( x=x_refsys, y=y_refsys, mode='lines+markers', name='REFSYS_10' )
                    xy_data_srsys = go.Scatter( x=x_srsys, y=y_srsys, mode='lines+markers', name='SRSYS_10' )
                    xy_data_msio = go.Scatter( x=x_msio, y=y_msio, mode='lines+markers', name='MSIO_10' )
                    xy_data_smsi = go.Scatter( x=x_smsi, y=y_smsi, mode='lines+markers', name='SMSI_10' )
                    xy_data_iontype10 = go.Scatter( x=x_iontype, y=y_iontype, mode='lines+markers', name='IONTYPE_10' )
                    xy_data_prn10 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
                else:
                    xy_data_elv = go.Scatter( x=[], y=[], mode='lines+markers', name='ELV_10' )
                    xy_data_azth = go.Scatter( x=[], y=[], mode='lines+markers', name='AZTH_10' )
                    xy_data_refsys = go.Scatter( x=[], y=[], mode='lines+markers', name='REFSYS_10' )
                    xy_data_srsys = go.Scatter( x=[], y=[], mode='lines+markers', name='SRSYS_10' )
                    xy_data_msio = go.Scatter( x=[], y=[], mode='lines+markers', name='MSIO_10' )
                    xy_data_smsi = go.Scatter( x=[], y=[], mode='lines+markers', name='SMSI_10' )
                    xy_data_iontype10 = go.Scatter( x=[], y=[], mode='lines+markers', name='IONTYPE_10' )
                    xy_data_prn10 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
            elif (j==11):
                if (len(second_list) != 0):
                    
                    second_first = second_list[0]
                    for j in range(1,len(second_list)):
                        if ((second_list[j] - second_first) != 960 and (second_list[j] - second_first) != 1680):
                            time_pre = time.asctime(time.gmtime(second_first))[11:19]
                            time_next = time.asctime(time.gmtime(second_list[j]))[11:19]
                            
                            time_from.append(time_pre)
                            time_to.append(time_next)
                            fout.write("For PRN= 11\n")
                            fout.write("Time missed from %s to %s\n\n" %(time_pre, time_next))
                            second_first = second_list[j]
                        else:
                            second_first = second_list[j]
                    xy_data_elv = go.Scatter( x=x_elv, y=y_elv, mode='lines+markers', name='ELV_11' )
                    xy_data_azth = go.Scatter( x=x_azth, y=y_azth, mode='lines+markers', name='AZTH_11' )
                    xy_data_refsys = go.Scatter( x=x_refsys, y=y_refsys, mode='lines+markers', name='REFSYS_11' )
                    xy_data_srsys = go.Scatter( x=x_srsys, y=y_srsys, mode='lines+markers', name='SRSYS_11' )
                    xy_data_msio = go.Scatter( x=x_msio, y=y_msio, mode='lines+markers', name='MSIO_11' )
                    xy_data_smsi = go.Scatter( x=x_smsi, y=y_smsi, mode='lines+markers', name='SMSI_11' )
                    xy_data_iontype11 = go.Scatter( x=x_iontype, y=y_iontype, mode='lines+markers', name='IONTYPE_11' )
                    xy_data_prn11 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
                else:
                    xy_data_elv = go.Scatter( x=[], y=[], mode='lines+markers', name='ELV_11' )
                    xy_data_azth = go.Scatter( x=[], y=[], mode='lines+markers', name='AZTH_11' )
                    xy_data_refsys = go.Scatter( x=[], y=[], mode='lines+markers', name='REFSYS_11' )
                    xy_data_srsys = go.Scatter( x=[], y=[], mode='lines+markers', name='SRSYS_11' )
                    xy_data_msio = go.Scatter( x=[], y=[], mode='lines+markers', name='MSIO_11' )
                    xy_data_smsi = go.Scatter( x=[], y=[], mode='lines+markers', name='SMSI_11' )
                    xy_data_iontype11 = go.Scatter( x=[], y=[], mode='lines+markers', name='IONTYPE_11' )
                    xy_data_prn11 = [xy_data_elv, xy_data_azth, xy_data_refsys, xy_data_srsys, xy_data_msio, xy_data_smsi]
                
            
            else:
                cggtts_file.seek(0,0)
                continue
        except:
            print("problem in scatter for j= %d" %j)
        ###################################################################################################################################
        
        cggtts_file.seek(0,0)

    try:
        xy_data_2 = xy_data_iontype1, xy_data_iontype2, xy_data_iontype3, xy_data_iontype4, xy_data_iontype5, xy_data_iontype6, xy_data_iontype7, xy_data_iontype8, xy_data_iontype9, xy_data_iontype10, xy_data_iontype11  
        xy_data_1 = xy_data_prn1 + xy_data_prn2 + xy_data_prn3 + xy_data_prn4 + xy_data_prn5 + xy_data_prn6 + xy_data_prn7 + xy_data_prn8 + xy_data_prn9 + xy_data_prn10 + xy_data_prn11
    except:
        print("problem in xy_data")
        
    layout_1 = go.Layout(
    title='CGGTTS parameters plot<br>values in (0.1ns) unit and slope in (0.1ps/s) unit',
    xaxis=dict(
        title='x Axis',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='cggtts parameter',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
            )
        )
    )
    
    layout_2 = go.Layout(
    title='CGGTTS ionospheric plot',
    xaxis=dict(
        title='x Axis',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='cggtts parameter',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
            )
        )
    )
    ############################################################################
    updatemenus_1=list([    
        dict(
            buttons=list([
		dict(
                    args=[{'visible': [True, True, True, True, True, True]}],
                    label='ALL',
                    method='update'
                ),
                dict(
                    args=[{'visible': [True, False, False, False, False, False]}],
                    label='Elevation',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, True, False, False, False, False]}],
                    label='AZIMUTH',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, True, False, False, False]}],
                    label='REFSYS',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, True, False, False]}],
                    label='REFSYS_slope',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, True, False]}],
                    label='iono_delay',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, True]}],
                    label='iono_slope',
                    method='update'
                )
                                       
            ]),
            direction = 'down',
            pad = {'r': 10, 't': 10},
            showactive = True,
            x = 0.1,
            xanchor = 'left',
            y = 1.3,
            yanchor = 'top' 
        ),
    ])

    updatemenus_2=list([
        dict(
            buttons=list([  
				dict(
                    args=[{'visible': [True, True, True, True, True, True, True, True, True, True, True]}],
                    label='ALL',
                    method='update'
                ),
                dict(
                    args=[{'visible': [True, False, False, False, False, False, False, False, False, False, False]}],
                    label='PRN1',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, True, False, False, False, False, False, False, False, False, False]}],
                    label='PRN2',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, True, False, False, False, False, False, False, False, False]}],
                    label='PRN3',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, True, False, False, False, False, False, False, False]}],
                    label='PRN4',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, True, False, False, False, False, False, False]}],
                    label='PRN5',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, True, False, False, False, False, False]}],
                    label='PRN6',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False, True, False, False, False, False]}],
                    label='PRN7',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False, False, True, False, False, False]}],
                    label='PRN8',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False , False, False, True, False, False]}],
                    label='PRN9',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False, False, False, False, True, False]}],
                    label='PRN10',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False, False, False, False, False, True]}],
                    label='PRN11',
                    method='update'
                )
                                       
            ]),
            direction = 'down',
            pad = {'r': 10, 't': 10},
            showactive = True,
            x = 0.1,
            xanchor = 'left',
            y = 1.3,
            yanchor = 'top' 
        ),
    ])

    annotations_1 = list([
        dict(text='Choose<br>parameter', x=0.0, y=1.28, yref='paper', align='left', showarrow=False ),
            
    ])

    annotations_2 = list([
        dict(text='Choose<br>PRN', x=0.0, y=1.28, yref='paper', align='left', showarrow=False ),
		dict(text='DUAL= 20<br>GCD = 18<br>ICM = 16<br>IGM = 14<br>GD  = 12<br>GC  = 10<br>CD  = 08<br>D   = 06<br>G   = 04<br>C   = 02', x=95, y=0.65, yref='paper', align='right',
         font = dict(
          color = "red",
          size = 18
        ),showarrow=False ),
    ])

    layout_1['updatemenus'] = updatemenus_1
    layout_1['annotations'] = annotations_1
    layout_2['updatemenus'] = updatemenus_2
    layout_2['annotations'] = annotations_2
    ###############################################################################
    try:
        fig_2 = go.Figure(data=xy_data_2, layout=layout_2)
        fig_1 = go.Figure(data=xy_data_1, layout=layout_1)
    except:
        print("problem in fig")
        
    
    cggtts_html_file_name_para =  file_name + "_parameter" + '.html'
    path_1_html = "file:///" + cgg_plot_path + "/" + cggtts_html_file_name_para    # file_name                
##    plotly.offline.plot(fig_1, filename=cggtts_html_file_name)

##    fig_2 = go.Figure(xy_data_2, layout=layout_2)
    cggtts_html_file_name_iono =  file_name + "_iontype" + '.html'
    path_2_html = "file:///" + cgg_plot_path + "/" + cggtts_html_file_name_iono    # file_name                

    try:
        plotly.offline.plot(fig_1, filename=cggtts_html_file_name_para, auto_open=False)
        plotly.offline.plot(fig_2, filename=cggtts_html_file_name_iono, auto_open=False)
    except:
        print("problem in plotly")
        raise

    time_missed_path = "file:///" + path + "_time_missed.txt"

    os.chdir("../")
    back_to_cggtts_dir = os.getcwd()
    if (j==2): 
        f = open('report.html','w')
    else:
        f = open("report.html","a")

    cggtts_string = '''
    <html>
        <head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
            <style>body{ margin:0 100; background:whitesmoke}</style>
                        
        </head>
        
        <body>
            <h1>CGGTTS Refsys plot</h1>
             <h2>''' + file_name + '''</h2>
            <!-- *** Section 1 *** --->
           
            <iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="yes" \
    src="''' + path_1_html + '''" ></iframe>
            <h2>IonType plot</h2>
            <iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="yes" \
    src="''' + path_2_html + '''" ></iframe>

      <h2>CGGTTS time missed</h2>
      
      
      
      <p>You can see if any <a href="''' + time_missed_path +'''" target="iframe_''' + file_name + '''">missed time</a> is there.</p> 
      
      
      <iframe width="1000" height="20" frameborder="0" seamless="seamless" scrolling="yes"></iframe>

          
          
          
        
            </body>
    </html>'''
    
    try:
        os.chdir(back_to_cggtts_dir + "\CGGTTS")
    except:
        pass
    
    f.write(cggtts_string)
    f.close()
            
    ##########################################################################################
    fout.close()
    cggtts_file.close()
	
    return file_name

            


