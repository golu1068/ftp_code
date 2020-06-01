import converter as conv
import os
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import pandas as pd




def obs_file(pathr, filename, m, plot_type, choose_30_1):
    print(filename)
#    csv_filename = 'test_3.csv'
#    file_write = open(csv_filename, 'a+', newline='')
    
    #############################################################################c
    mjd=[];l=0;k=0;nosatt=[];secondd=[];SS1=[];SS2=[];offsett=[];CN= [];PRN_1=[];missed_from=[];missed_to=[];
    PRN_2=[];PRN_3=[];PRN_4=[];PRN_5=[];PRN_6=[];PRN_7=[];PRN_8=[];PRN_9=[];PRN_10=[];PRN_11=[];
    y_CN_1_PRN_1=[];y_CN_1_PRN_2=[];y_CN_1_PRN_3=[];y_CN_1_PRN_4=[];y_CN_1_PRN_5=[];y_CN_1_PRN_6=[];y_CN_1_PRN_7=[];y_CN_1_PRN_8=[];
    y_CN_1_PRN_9=[];y_CN_1_PRN_10=[];y_CN_1_PRN_11=[];
    y_CN_2_PRN_1=[];y_CN_2_PRN_2=[];y_CN_2_PRN_3=[];y_CN_2_PRN_4=[];y_CN_2_PRN_5=[];y_CN_2_PRN_6=[];y_CN_2_PRN_7=[];y_CN_2_PRN_8=[];
    y_CN_2_PRN_9=[];y_CN_2_PRN_10=[];y_CN_2_PRN_11=[];
    ##############################################################################
##    pathr = r"E:\LOG\9.14\OBS"          ## Path of the observation file  
##    filename = "ACCO1945"
    ####################################################################
    obs = open(os.path.join(pathr,filename),"r+")
    fout = open(os.path.join(pathr,filename[0:8] + "_offset.txt"),"w+")
    fout_1 = open(os.path.join(pathr,filename[0:8] + "_time_missed.txt"),"w+")
    if (m == 2):
        fout_2 = open(os.path.join(pathr,filename[0:8] + "_CN.txt"),"w+")
        m += 1
    else:
        fout_2 = open(os.path.join(pathr,filename[0:8] + "_CN.txt"),"a")

#########################################################################################
    
    try:
        
        SS1.clear();SS2.clear();nosatt.clear();offsett.clear();l=0;missed_from.clear();missed_to.clear();second_start=0;
        while 1:
            line = obs.readline()
            if (line==""):
                print("End of the file reached:")
                break
            if "SYS / # / OBS TYPES" in line:            #  to find a particular word in a string
                noobs = int(line[4:6])
                for i in range(noobs):
                    a= (4*i) + 7
                    b= a + 3
                    if line[a:b] == "C5C":
                        c5c= i+1
                    elif line[a:b] == "L5C":
                        l5c= i+1
                    elif line[a:b] == "D5C":
                        d5c = i+1
                    elif line[a:b] == "S5C":
                        s5c = i+1
                    elif line[a:b] == "C9C":
                        c9c = i+1
                    elif line[a:b] == "L9C":
                        l9c= i+1
                    elif line[a:b] == "D9C":
                        d9c= i+1
                    elif line[a:b] == "S9C":
                        s9c= i+1
            if "END OF HEADER" in line:
                break
            
        while 1:
            line = obs.readline()
            if (line == ""):
                break
            year = int(line[2:6])
            month = int(line[7:9])
            day = int(line[10:12])
            hour = int(line[13:15])
            minute = int(line[16:18])
            sec= float(line[19:29])
            nosat = int(line[33:35])
            nosatt.append(nosat)
            offset = float(line[41:58])
            offsett.append(offset)

            if(l==0):
                second_start = conv.time2sec(hour,minute,sec)
                nosat_start=nosat
                l+=1
##                   plt.plot(second_s,nosat, '-', color='b')
            else:
                second = conv.time2sec(hour,minute,sec)
                change = nosat - nosat_start
                if ((second - second_start)!= choose_30_1 and (second - second_start)!= 0):
#                if ((second - second_start)!= 1 and (second - second_start)!= 0):
                    hh_start, mm_start, ss_start = conv.sec2time(second_start)
                    hh, mm ,ss = conv.sec2time(second)
                    
                    hh_start_1 = str(hh_start)
                    mm_start_1 = str(mm_start)
                    ss_start_1 = str(ss_start)
                    
                    hh_1 = str(hh)
                    mm_1 = str(mm)
                    ss_1 = str(ss)

                    sec_from = hh_start_1 + ":" +  mm_start_1 + ":" +  ss_start_1
                    sec_to = hh_1 + ":" +  mm_1 + ":" +  ss_1
#                    print(filename) 
#                    print("missed")  
###############################################################################################################
                    missed_from.append(sec_from)
                    missed_to.append(sec_to)                
##################################################################################################################
                    fout_1.write("\nTime missed from (%d:%d:%d) to  (%d:%d:%d)\n\n" %(hh_start, mm_start, ss_start, hour,minute,sec))
                second_start=second   
                nosat_start=nosat
    ##########################################################################################
            c=16*(c5c-1) + 4
            d= c + 13
            e=16*(l5c-1) + 4
            f= e + 13
            g=16*(d5c-1) + 4
            h= g + 13
            a=16*(s5c-1) + 4
            b= a + 13    
            for i in range(nosat):
                line = obs.readline()
                prn = int(line[1:3])
                if (prn == 1):
                    R1 = float(line[c:d])
                    R2 = float(line[c+64:d+64])
                    L1 = float(line[e:f])
                    L2 = float(line[e+64:f+64])
                    D1 = float(line[g:h])
                    D2 = float(line[g+64:h+64])
                    S1 = float(line[a:b])
                    S2 = float(line[a+64:b+64])
                    PRN_1.append(R1)
                    PRN_1.append(L1)
                    PRN_1.append(D1)
                    PRN_1.append(S1)
                    PRN_1.append(R2)
                    PRN_1.append(L2)
                    PRN_1.append(D2)
                    PRN_1.append(S2)
                elif (prn == 2):
                    R1 = float(line[c:d])
                    R2 = float(line[c+64:d+64])
                    L1 = float(line[e:f])
                    L2 = float(line[e+64:f+64])
                    D1 = float(line[g:h])
                    D2 = float(line[g+64:h+64])
                    S1 = float(line[a:b])
                    S2 = float(line[a+64:b+64])
                    PRN_2.append(R1)
                    PRN_2.append(L1)
                    PRN_2.append(D1)
                    PRN_2.append(S1)
                    PRN_2.append(R2)
                    PRN_2.append(L2)
                    PRN_2.append(D2)
                    PRN_2.append(S2)
                elif (prn == 3):
                    R1 = float(line[c:d])
                    R2 = float(line[c+64:d+64])
                    L1 = float(line[e:f])
                    L2 = float(line[e+64:f+64])
                    D1 = float(line[g:h])
                    D2 = float(line[g+64:h+64])
                    S1 = float(line[a:b])
                    S2 = float(line[a+64:b+64])
                    PRN_3.append(R1)
                    PRN_3.append(L1)
                    PRN_3.append(D1)
                    PRN_3.append(S1)
                    PRN_3.append(R2)
                    PRN_3.append(L2)
                    PRN_3.append(D2)
                    PRN_3.append(S2)
                elif (prn == 4):
                    R1 = float(line[c:d])
                    R2 = float(line[c+64:d+64])
                    L1 = float(line[e:f])
                    L2 = float(line[e+64:f+64])
                    D1 = float(line[g:h])
                    D2 = float(line[g+64:h+64])
                    S1 = float(line[a:b])
                    S2 = float(line[a+64:b+64])
                    PRN_4.append(R1)
                    PRN_4.append(L1)
                    PRN_4.append(D1)
                    PRN_4.append(S1)
                    PRN_4.append(R2)
                    PRN_4.append(L2)
                    PRN_4.append(D2)
                    PRN_4.append(S2)
                elif (prn == 5):
                    R1 = float(line[c:d])
                    R2 = float(line[c+64:d+64])
                    L1 = float(line[e:f])
                    L2 = float(line[e+64:f+64])
                    D1 = float(line[g:h])
                    D2 = float(line[g+64:h+64])
                    S1 = float(line[a:b])
                    S2 = float(line[a+64:b+64])
                    PRN_5.append(R1)
                    PRN_5.append(L1)
                    PRN_5.append(D1)
                    PRN_5.append(S1)
                    PRN_5.append(R2)
                    PRN_5.append(L2)
                    PRN_5.append(D2)
                    PRN_5.append(S2)
                elif (prn == 6):
                    R1 = float(line[c:d])
                    R2 = float(line[c+64:d+64])
                    L1 = float(line[e:f])
                    L2 = float(line[e+64:f+64])
                    D1 = float(line[g:h])
                    D2 = float(line[g+64:h+64])
                    S1 = float(line[a:b])
                    S2 = float(line[a+64:b+64])
                    PRN_6.append(R1)
                    PRN_6.append(L1)
                    PRN_6.append(D1)
                    PRN_6.append(S1)
                    PRN_6.append(R2)
                    PRN_6.append(L2)
                    PRN_6.append(D2)
                    PRN_6.append(S2)
                elif (prn == 7):
                    R1 = float(line[c:d])
                    R2 = float(line[c+64:d+64])
                    L1 = float(line[e:f])
                    L2 = float(line[e+64:f+64])
                    D1 = float(line[g:h])
                    D2 = float(line[g+64:h+64])
                    S1 = float(line[a:b])
                    S2 = float(line[a+64:b+64])
                    PRN_7.append(R1)
                    PRN_7.append(L1)
                    PRN_7.append(D1)
                    PRN_7.append(S1)
                    PRN_7.append(R2)
                    PRN_7.append(L2)
                    PRN_7.append(D2)
                    PRN_7.append(S2)
                elif (prn == 8):
                    R1 = float(line[c:d])
                    R2 = float(line[c+64:d+64])
                    L1 = float(line[e:f])
                    L2 = float(line[e+64:f+64])
                    D1 = float(line[g:h])
                    D2 = float(line[g+64:h+64])
                    S1 = float(line[a:b])
                    S2 = float(line[a+64:b+64])
                    PRN_8.append(R1)
                    PRN_8.append(L1)
                    PRN_8.append(D1)
                    PRN_8.append(S1)
                    PRN_8.append(R2)
                    PRN_8.append(L2)
                    PRN_8.append(D2)
                    PRN_8.append(S2)
                elif (prn == 9):
                    R1 = float(line[c:d])
                    R2 = float(line[c+64:d+64])
                    L1 = float(line[e:f])
                    L2 = float(line[e+64:f+64])
                    D1 = float(line[g:h])
                    D2 = float(line[g+64:h+64])
                    S1 = float(line[a:b])
                    S2 = float(line[a+64:b+64])
                    PRN_9.append(R1)
                    PRN_9.append(L1)
                    PRN_9.append(D1)
                    PRN_9.append(S1)
                    PRN_9.append(R2)
                    PRN_9.append(L2)
                    PRN_9.append(D2)
                    PRN_9.append(S2)
                elif (prn == 10):
                    R1 = float(line[c:d])
                    R2 = float(line[c+64:d+64])
                    L1 = float(line[e:f])
                    L2 = float(line[e+64:f+64])
                    D1 = float(line[g:h])
                    D2 = float(line[g+64:h+64])
                    S1 = float(line[a:b])
                    S2 = float(line[a+64:b+64])
                    PRN_10.append(R1)
                    PRN_10.append(L1)
                    PRN_10.append(D1)
                    PRN_10.append(S1)
                    PRN_10.append(R2)
                    PRN_10.append(L2)
                    PRN_10.append(D2)
                    PRN_10.append(S2)
                elif (prn == 11):
                    R1 = float(line[c:d])
                    R2 = float(line[c+64:d+64])
                    L1 = float(line[e:f])
                    L2 = float(line[e+64:f+64])
                    D1 = float(line[g:h])
                    D2 = float(line[g+64:h+64])
                    S1 = float(line[a:b])
                    S2 = float(line[a+64:b+64])
                    PRN_11.append(R1)
                    PRN_11.append(L1)
                    PRN_11.append(D1)
                    PRN_11.append(S1)
                    PRN_11.append(R2)
                    PRN_11.append(L2)
                    PRN_11.append(D2)
                    PRN_11.append(S2)
                else:
#                    print("PRN is greater than 11 for file %s at %d:%d:%f" %(filename, hour, minute, sec))
                    pass
#                    print(filename)
                    
                if (prn != 1):
                    if (R1==0 and R2==0):
                        fout_2.write("\nPRN = %d.    Both R1 and R2 are zero(0).\n" %prn)
                        fout_2.write("%2d : %2d : %2d\n" %(hour, minute, sec))
                        fout_2.write(line)
                        fout_2.write("********************************************************************************************************************************")
                    elif (R1 == 0):
                          fout_2.write("\nPRN = %d     Only R1 is zero.\n" %prn)
                          fout_2.write("%2d : %2d : %2d   R1= %12.3f   C/N is %f\n" %(hour, minute, sec, R1, S1))
                          fout_2.write(line+"\n")
                          fout_2.write("********************************************************************************************************************************")
##
##                          CN_1.append(S1)
                    elif (R2 == 0):
                          fout_2.write("\nPRN = %d    Only R2 is zero.\n" %prn)
                          fout_2.write("%2d : %2d : %2d   R2= %12.3f   C/N is %f\n" %(hour, minute, sec, R2, S2))
                          fout_2.write(line+"\n")
                          fout_2.write("********************************************************************************************************************************")
##
##                          CN_2.append(S2)

    except:
        print("Cannot read the line in %s after: %d:%d:%d" %(filename, hour, minute, sec))
    #########################################################################################

##    fig=plt.figure(1)               ### C/N for frequency L5 ratio
##    for j in np.arange(3, int(len(PRN_1)), 8):
##        xy_prn_1 = plt.plot(j,PRN_1[j],color='red', linestyle='--', linewidth = 3,
##         marker='o',markerfacecolor='blue', markersize=5)
##        
##    for i in np.arange(7, int(len(PRN_1)), 8):
##        plt.plot(i,PRN_1[i],color='green', linestyle='--', linewidth = 3,
##         marker='*',markerfacecolor='blue', markersize=5)    
##    plt.grid(True) 
##    plt.title("Receiver_offset_" + filename)
##    plt.xlabel("Number of Samples", fontdict=None, labelpad=None)
##    plt.ylabel("Offset", fontdict=None, labelpad=None)   
##    fig.savefig(os.path.join(pathr,"%s_CN.png" %filename[0:8]))
        
    parame = plot_type    ## 0:range, 1:phase, 2:doppler, 3:C/N
    
    for j in np.arange(parame, int(len(PRN_1)), 8):
        y_CN_1_PRN_1.append(PRN_1[j])
        y_CN_2_PRN_1.append(PRN_1[j+4])
    for j in np.arange(parame, int(len(PRN_2)), 8):
        y_CN_1_PRN_2.append(PRN_2[j])
        y_CN_2_PRN_2.append(PRN_2[j+4])
    for j in np.arange(parame, int(len(PRN_3)), 8):
        y_CN_1_PRN_3.append(PRN_3[j])
        y_CN_2_PRN_3.append(PRN_3[j+4])
    for j in np.arange(parame, int(len(PRN_4)), 8):
        y_CN_1_PRN_4.append(PRN_4[j])
        y_CN_2_PRN_4.append(PRN_4[j+4])
    for j in np.arange(parame, int(len(PRN_5)), 8):
        y_CN_1_PRN_5.append(PRN_5[j])
        y_CN_2_PRN_5.append(PRN_5[j+4])
    for j in np.arange(parame, int(len(PRN_6)), 8):
        y_CN_1_PRN_6.append(PRN_6[j])
        y_CN_2_PRN_6.append(PRN_6[j+4])
    for j in np.arange(parame, int(len(PRN_7)), 8):
        y_CN_1_PRN_7.append(PRN_7[j])
        y_CN_2_PRN_7.append(PRN_7[j+4])
    for j in np.arange(parame, int(len(PRN_8)), 8):
        y_CN_1_PRN_8.append(PRN_8[j])
        y_CN_2_PRN_8.append(PRN_8[j+4])
    for j in np.arange(parame, int(len(PRN_9)), 8):
        y_CN_1_PRN_9.append(PRN_9[j])
        y_CN_2_PRN_9.append(PRN_9[j+4])
    for j in np.arange(parame, int(len(PRN_10)), 8):
        y_CN_1_PRN_10.append(PRN_10[j])
        y_CN_2_PRN_10.append(PRN_10[j+4])
    for j in np.arange(parame, int(len(PRN_11)), 8):
        y_CN_1_PRN_11.append(PRN_11[j])
        y_CN_2_PRN_11.append(PRN_11[j+4])
#    #########################################################################################
#    diff=[];
#    for k in range(1,len(y_CN_1_PRN_2)):
#        diff.append(y_CN_1_PRN_2[k] - y_CN_1_PRN_2[k-1])
#    y_CN_1_PRN_2 = diff
#    diff_2=[];
#    for k in range(1,len(y_CN_1_PRN_2)):
#        diff_2.append(y_CN_1_PRN_2[k] - y_CN_1_PRN_2[k-1])
#    y_CN_2_PRN_2 = diff_2
#    ########################################################################################
    x_CN_1_PRN_1 = list(range(0,int(len(PRN_1)/8)))
    x_CN_1_PRN_2 = list(range(0,int(len(PRN_2)/8)))
    x_CN_1_PRN_3 = list(range(0,int(len(PRN_3)/8)))
    x_CN_1_PRN_4 = list(range(0,int(len(PRN_4)/8)))
    x_CN_1_PRN_5 = list(range(0,int(len(PRN_5)/8)))
    x_CN_1_PRN_6 = list(range(0,int(len(PRN_6)/8)))
    x_CN_1_PRN_7 = list(range(0,int(len(PRN_7)/8)))
    x_CN_1_PRN_8 = list(range(0,int(len(PRN_8)/8)))
    x_CN_1_PRN_9 = list(range(0,int(len(PRN_9)/8)))
    x_CN_1_PRN_10 = list(range(0,int(len(PRN_10)/8)))
    x_CN_1_PRN_11 = list(range(0,int(len(PRN_11)/8)))


    
    x_CN_2_PRN_1 = list(range(0,int(len(PRN_1)/8)))
    x_CN_2_PRN_2 = list(range(0,int(len(PRN_2)/8)))
    x_CN_2_PRN_3 = list(range(0,int(len(PRN_3)/8)))
    x_CN_2_PRN_4 = list(range(0,int(len(PRN_4)/8)))
    x_CN_2_PRN_5 = list(range(0,int(len(PRN_5)/8)))
    x_CN_2_PRN_6 = list(range(0,int(len(PRN_6)/8)))
    x_CN_2_PRN_7 = list(range(0,int(len(PRN_7)/8)))
    x_CN_2_PRN_8 = list(range(0,int(len(PRN_8)/8)))
    x_CN_2_PRN_9 = list(range(0,int(len(PRN_9)/8)))
    x_CN_2_PRN_10 = list(range(0,int(len(PRN_10)/8)))
    x_CN_2_PRN_11 = list(range(0,int(len(PRN_11)/8)))
        
    #########################################################################################    
    x_offset = list(range(0, len(offsett)))
    y_offset = offsett
    
#    df = pd.DataFrame(offsett)   
#    df.to_csv(file_write, index=False)
#    file_write.close()
##################################################################
##    print("path= "+os.getcwd())
##    os.chdir("../")
    os.chdir(pathr)    #change dir to Rinex obs file
    
##    path_to_obs = os.getcwd()
####    print("pa= " + path_to_obs)
##    os.chdir(path_to_obs + "\OBS")
    
    path_for_plot = os.getcwd()
    
##    print("paa= " + path_for_plot)
    
################################################################    
    os.chdir("../")
    f = open('report.html','a')
    ####################################################################################################
    prn_1_l5=[];prn_1_s =[];prn_2_l5=[];prn_2_s =[];prn_3_l5=[];prn_3_s =[];prn_4_l5=[];prn_4_s =[];prn_5_l5=[];
    prn_5_s =[];prn_6_l5=[];prn_6_s =[];prn_7_l5=[];prn_7_s =[];prn_8_l5=[];prn_8_s =[];prn_9_l5=[];prn_9_s =[];
    prn_10_l5=[];prn_10_s =[];prn_11_l5=[];prn_11_s =[];
    
    l5_dict =  {1: prn_1_l5,2: prn_2_l5,3: prn_3_l5,4: prn_4_l5,5: prn_5_l5,6: prn_6_l5,
                7: prn_7_l5,8: prn_8_l5,9: prn_9_l5,10: prn_10_l5,11: prn_11_l5} 
    s_dict =  {1: prn_1_s,2: prn_2_s,3: prn_3_s,4: prn_4_s,5: prn_5_s,6: prn_6_s,
                7: prn_7_s,8: prn_8_s,9: prn_9_s,10: prn_10_s,11: prn_11_s} 

    if (plot_type == 0):
        plot_name = 'range'
    elif (plot_type == 1):
        plot_name = 'phase'
    elif (plot_type == 2):
        plot_name = 'doppler'
    else:
        plot_name = 'C/N'
    for k in range(1,12):
        l5_dict[k].append(plot_name + '_L5' + '_prn_' + str(k))
        s_dict[k].append(plot_name + '_S' + '_prn_' + str(k))
        
    xy_CN_1_PRN_1 = go.Scatter( x=x_CN_1_PRN_1, y=y_CN_1_PRN_1, mode='lines+markers', name=prn_1_l5[0] )
    xy_CN_2_PRN_1 = go.Scatter( x=x_CN_2_PRN_1, y=y_CN_2_PRN_1, mode='lines+markers', name=prn_1_s[0] )
    xy_CN_1_PRN_2 = go.Scatter( x=x_CN_1_PRN_2, y=y_CN_1_PRN_2, mode='lines+markers', name=prn_2_l5[0] )
    xy_CN_2_PRN_2 = go.Scatter( x=x_CN_2_PRN_2, y=y_CN_2_PRN_2, mode='lines+markers', name=prn_2_s[0] )
    xy_CN_1_PRN_3 = go.Scatter( x=x_CN_1_PRN_3, y=y_CN_1_PRN_3, mode='lines+markers', name=prn_3_l5[0] )
    xy_CN_2_PRN_3 = go.Scatter( x=x_CN_2_PRN_3, y=y_CN_2_PRN_3, mode='lines+markers', name=prn_3_s[0] )
    xy_CN_1_PRN_4 = go.Scatter( x=x_CN_1_PRN_4, y=y_CN_1_PRN_4, mode='lines+markers', name=prn_4_l5[0] )
    xy_CN_2_PRN_4 = go.Scatter( x=x_CN_2_PRN_4, y=y_CN_2_PRN_4, mode='lines+markers', name=prn_4_s[0] )
    xy_CN_1_PRN_5 = go.Scatter( x=x_CN_1_PRN_5, y=y_CN_1_PRN_5, mode='lines+markers', name=prn_5_l5[0] )
    xy_CN_2_PRN_5 = go.Scatter( x=x_CN_2_PRN_5, y=y_CN_2_PRN_5, mode='lines+markers', name=prn_5_s[0] )
    xy_CN_1_PRN_6 = go.Scatter( x=x_CN_1_PRN_6, y=y_CN_1_PRN_6, mode='lines+markers', name=prn_6_l5[0] )
    xy_CN_2_PRN_6 = go.Scatter( x=x_CN_2_PRN_6, y=y_CN_2_PRN_6, mode='lines+markers', name=prn_6_s[0] )
    xy_CN_1_PRN_7 = go.Scatter( x=x_CN_1_PRN_7, y=y_CN_1_PRN_7, mode='lines+markers', name=prn_7_l5[0] )
    xy_CN_2_PRN_7 = go.Scatter( x=x_CN_2_PRN_7, y=y_CN_2_PRN_7, mode='lines+markers', name=prn_7_s[0] )
    xy_CN_1_PRN_8 = go.Scatter( x=x_CN_1_PRN_8, y=y_CN_1_PRN_8, mode='lines+markers', name=prn_8_l5[0] )
    xy_CN_2_PRN_8 = go.Scatter( x=x_CN_2_PRN_8, y=y_CN_2_PRN_8, mode='lines+markers', name=prn_8_s[0] )
    xy_CN_1_PRN_9 = go.Scatter( x=x_CN_1_PRN_9, y=y_CN_1_PRN_9, mode='lines+markers', name=prn_9_l5[0] )
    xy_CN_2_PRN_9 = go.Scatter( x=x_CN_2_PRN_9, y=y_CN_2_PRN_9, mode='lines+markers', name=prn_9_s[0] )
    xy_CN_1_PRN_10 = go.Scatter( x=x_CN_1_PRN_10, y=y_CN_1_PRN_10, mode='lines+markers', name=prn_10_l5[0] )
    xy_CN_2_PRN_10 = go.Scatter( x=x_CN_2_PRN_10, y=y_CN_2_PRN_10, mode='lines+markers', name=prn_10_s[0] )
    xy_CN_1_PRN_11 = go.Scatter( x=x_CN_1_PRN_11, y=y_CN_1_PRN_11, mode='lines+markers', name=prn_11_l5[0] )
    xy_CN_2_PRN_11 = go.Scatter( x=x_CN_2_PRN_11, y=y_CN_2_PRN_11, mode='lines+markers', name=prn_11_s[0])
    ######################################################################################################
    
    xy_data = go.Scatter( x=x_offset, y=y_offset, mode='lines+markers', name='offset' )
    #########################################################################################
#    xy_CN_1_PRN_1 = go.Scatter( x=x_CN_1_PRN_1, y=y_CN_1_PRN_1, mode='lines+markers', name='CN_1_prn_1' )
#    xy_CN_2_PRN_1 = go.Scatter( x=x_CN_2_PRN_1, y=y_CN_2_PRN_1, mode='lines+markers', name='CN_2_prn_1' )
#    xy_CN_1_PRN_2 = go.Scatter( x=x_CN_1_PRN_2, y=y_CN_1_PRN_2, mode='lines+markers', name='CN_1_prn_2' )
#    xy_CN_2_PRN_2 = go.Scatter( x=x_CN_2_PRN_2, y=y_CN_2_PRN_2, mode='lines+markers', name='CN_2_prn_2' )
#    xy_CN_1_PRN_3 = go.Scatter( x=x_CN_1_PRN_3, y=y_CN_1_PRN_3, mode='lines+markers', name='CN_1_prn_3' )
#    xy_CN_2_PRN_3 = go.Scatter( x=x_CN_2_PRN_3, y=y_CN_2_PRN_3, mode='lines+markers', name='CN_2_prn_3' )
#    xy_CN_1_PRN_4 = go.Scatter( x=x_CN_1_PRN_4, y=y_CN_1_PRN_4, mode='lines+markers', name='CN_1_prn_4' )
#    xy_CN_2_PRN_4 = go.Scatter( x=x_CN_2_PRN_4, y=y_CN_2_PRN_4, mode='lines+markers', name='CN_2_prn_4' )
#    xy_CN_1_PRN_5 = go.Scatter( x=x_CN_1_PRN_5, y=y_CN_1_PRN_5, mode='lines+markers', name='CN_1_prn_5' )
#    xy_CN_2_PRN_5 = go.Scatter( x=x_CN_2_PRN_5, y=y_CN_2_PRN_5, mode='lines+markers', name='CN_2_prn_5' )
#    xy_CN_1_PRN_6 = go.Scatter( x=x_CN_1_PRN_6, y=y_CN_1_PRN_6, mode='lines+markers', name='CN_1_prn_6' )
#    xy_CN_2_PRN_6 = go.Scatter( x=x_CN_2_PRN_6, y=y_CN_2_PRN_6, mode='lines+markers', name='CN_2_prn_6' )
#    xy_CN_1_PRN_7 = go.Scatter( x=x_CN_1_PRN_7, y=y_CN_1_PRN_7, mode='lines+markers', name='CN_1_prn_7' )
#    xy_CN_2_PRN_7 = go.Scatter( x=x_CN_2_PRN_7, y=y_CN_2_PRN_7, mode='lines+markers', name='CN_2_prn_7' )
#    xy_CN_1_PRN_8 = go.Scatter( x=x_CN_1_PRN_8, y=y_CN_1_PRN_8, mode='lines+markers', name='CN_1_prn_8' )
#    xy_CN_2_PRN_8 = go.Scatter( x=x_CN_2_PRN_8, y=y_CN_2_PRN_8, mode='lines+markers', name='CN_2_prn_8' )
#    xy_CN_1_PRN_9 = go.Scatter( x=x_CN_1_PRN_9, y=y_CN_1_PRN_9, mode='lines+markers', name='CN_1_prn_9' )
#    xy_CN_2_PRN_9 = go.Scatter( x=x_CN_2_PRN_9, y=y_CN_2_PRN_9, mode='lines+markers', name='CN_2_prn_9' )
#    xy_CN_1_PRN_10 = go.Scatter( x=x_CN_1_PRN_10, y=y_CN_1_PRN_10, mode='lines+markers', name='CN_1_prn_10' )
#    xy_CN_2_PRN_10 = go.Scatter( x=x_CN_2_PRN_10, y=y_CN_2_PRN_10, mode='lines+markers', name='CN_2_prn_10' )
#    xy_CN_1_PRN_11 = go.Scatter( x=x_CN_1_PRN_11, y=y_CN_1_PRN_11, mode='lines+markers', name='CN_1_prn_11' )
#    xy_CN_2_PRN_11 = go.Scatter( x=x_CN_2_PRN_11, y=y_CN_2_PRN_11, mode='lines+markers', name='CN_2_prn_11' )
    ###########################################################################################
    data_1 = [xy_data, xy_CN_1_PRN_1, xy_CN_2_PRN_1, xy_CN_1_PRN_2, xy_CN_2_PRN_2, xy_CN_1_PRN_3, xy_CN_2_PRN_3, xy_CN_1_PRN_4, xy_CN_2_PRN_4, xy_CN_1_PRN_5,
              xy_CN_2_PRN_5,xy_CN_1_PRN_6, xy_CN_2_PRN_6, xy_CN_1_PRN_7, xy_CN_2_PRN_7, xy_CN_1_PRN_8, xy_CN_2_PRN_8, xy_CN_1_PRN_9, xy_CN_2_PRN_9, 
              xy_CN_1_PRN_10, xy_CN_2_PRN_10, xy_CN_1_PRN_11, xy_CN_2_PRN_11] 
#    data_1 = [xy_data]
  ###########################################################################################  
    layout = go.Layout(
    title='Clock Bias plot & C/N ratio for all prn<br>offset in (ns) unit and C/N in (db-hz)',
    xaxis=dict(
        title='x Axis',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='green'
        )
    ),
    yaxis=dict(
        title='Clock bias & C/N',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='green'
            )
        )
    )
######################################################################################################
    updatemenus=list([
        dict(
            buttons=list([
                dict(
                    args=[{'visible': [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, 
                                       True, True, True,True, True, True]}],
                    label='All',
                    method='update',
                ),
                dict(
                    args=[{'visible': [True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, 
                                       False, False, False,False, False, False]}],
                    label='offset',
                    method='update',
                ),
                dict(
                    args=[{'visible': [False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, 
                                       False, False, False,False, False, False]}],
                    label='PRN_1',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, 
                                       False, False, False, False, False, False]}],
                    label='PRN_2',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, 
                                       False, False, False, False, False, False]}],
                    label='PRN_3',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, 
                                       False, False, False, False, False, False]}],
                    label='PRN_4',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, False, 
                                       False, False, False, False, False, False]}],
                    label='PRN_5',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, 
                                       False, False, False, False, False, False]}],
                    label='PRN_6',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, False, False, 
                                       False, False, False, False, False, False]}],
                    label='PRN_7',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, 
                                       False, False, False, False, False, False]}],
                    label='PRN_8',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, 
                                       True, True, False, False, False, False]}],
                    label='PRN_9',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, 
                                       False, False, True, True, False, False]}],
                    label='PRN_10',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, 
                                       False, False, False, False, True, True]}],
                    label='PRN_11',
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

    annotations = list([
        dict(text='Choose<br>PRN:', x=0, y=1.28, yref='paper', align='left', showarrow=False)
    ])
    
    layout['updatemenus'] = updatemenus
    layout['annotations'] = annotations
    
#########################################################################################################    
    
    fig_1 = dict(data=data_1, layout=layout)

    
    rinex_html_file_name = path_for_plot + "\\" +  filename[0:8] + '.html'
    path_1_html = "file:///"  + rinex_html_file_name      #  file_name

    

    plotly.offline.plot(fig_1, filename= rinex_html_file_name, auto_open=False)
    
    missed_time_path = "file:///" + pathr + "\\" + filename[0:8] + "_time_missed.txt"
    
    CN_path  = "file:///" + pathr + "\\" + filename[0:8] + "_CN.txt"
    
    html_string = '''
    <html>
        <head>
            <style>body{ margin:0 100; background:whitesmoke}</style>
                        
        </head>
        
        
        
        <body>
            <h1>Clock bias offset</h1>
            <h2>''' + filename + '''</h2>
            <!-- *** Section 1 *** --->
           
            <iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="yes" \
    src="''' + path_1_html + '''"></iframe>
           
             <h2>Rinex time missed</h2>
      
      <iframe width="1000" height=550" frameborder="0" seamless="seamless" scrolling="yes" name="iframe_''' + filename + '''"></iframe>

      <p>You can see if any <a href="''' + missed_time_path +'''" target="iframe_''' + filename + '''">missed time</a> is there.</p>
      <p>To see the C/N ratio, <a href="''' + CN_path +'''" target="iframe_''' + filename + '''">click here</a> is there.</p>

      <iframe width="100" height="20" frameborder="0" seamless="seamless" scrolling="yes" name="iframe_''' + filename + '''"></iframe>
        
            </body>
    </html>'''
    
    
    
    f.write(html_string)
    f.close()
    

    obs.close()
    fout.close()
    fout_1.close()
    fout_2.close()


    return filename
                    
            
