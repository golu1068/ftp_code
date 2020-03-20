import ftplib
import sys
#from ftplib import FTP
import os
#import shutil
import cggtts_func as cgg
import rinex_func as rinex
########################################
#import test_cggtts as cgg
#import test_rinex as rinex
################################################################################################
listt = [];
##############################################################################################    
def ftp(ip_address, destination, m, file_day, cggtts_days): 
    

    cggtts_day = cggtts_days
    listt.clear();rand_value=0;
###########################################################################################    
    try:
        ftp = ftplib.FTP(ip_address, timeout=3, user="root", passwd="root_123")
    except:
        print("\nERROR: IP is not connected to server\n")
        return
		
##        sys.exit(0)
######################################################################################### 
#    ftp = ftplib.FTP(ip_address, timeout=3, user="root", passwd="root_123")
#    ftp = FTP(ip_address)
#    ftp.login('root',"root_123")
        
    try:
        ftp.cwd("/2018")                 #  go to the destination dir
    except:
        print("ERROR: 2018 Dir is not available")
        return
    
    try:
        ftp.cwd("/2018/Rinex")                 #  go to the destination dir
    except:
        print("ERROR: Rinex file is not available")
        return
        
    observation_file_pattern = ".18O"    
    path_obs = destination + ip_address[8:14] + "/OBS"
    path_nav = destination + ip_address[8:14] + "/NAV" 
    path_CGGTTS = destination + ip_address[8:14] + "/CGGTTS"
####################################################################################################
    try:
        os.mkdir(destination)
    except:
        pass
##################################################################################################	
    try:
        os.mkdir(destination + ip_address[8:14])
        print("Dir do not exist, creating new Dir")
    
#    shutil.rmtree(destination + ip_address[8:12], ignore_errors=True)
#    shutil.rmtree(path_obs, ignore_errors=True)       ##   Remove the current dir
#    shutil.rmtree(path_nav, ignore_errors=True)
#    shutil.rmtree(path_CGGTTS, ignore_errors=True)
#    
#    os.mkdir(destination + ip_address[8:12])   
        os.mkdir(path_obs)              #  make a new dir
        os.mkdir(path_nav)
        os.mkdir(path_CGGTTS)  
    except:
        print("Dir exist")
#############################################################################################################                                    
    files_rinex = ftp.nlst()                       #  list all the file in cwd in list
    
    
    for filename in range(len(files_rinex)):
#        if (int(files[filename][4:8]) >= file_day):
        if (files_rinex[filename][8:12] == ".18O"):
            os.chdir(path_obs)                   #  change the dir
        else:
            os.chdir(path_nav)            
        file = open(files_rinex[filename],"wb")
        ftp.retrbinary("RETR " + files_rinex[filename], file.write)  
        file.close()
    
    print("Rinex files download complete for: " + ip_address[8:14])
    os.chdir("../")                     #  one step back on system dir 
    os.getcwd()                    #    get the current working dir of system
    ftp.cwd("../")                    #  go back one step on server dir
    ftp.cwd("../")
#    print(ftp.pwd())                    #  tell the current working dir on serer
    file.close()
    
##############################################################################################
#    #  Read CGGTTS file from ftp
    try:
        ftp.cwd("2018/CGGTTS")
    except:
        print("ERROR: CGGTTS dir is not available")
        return
    
    os.chdir(path_CGGTTS)
    
    files_cggtts = ftp.nlst()                       #  list all the file in cwd in list
    for filename in range(len(files_cggtts)):           
        file = open(files_cggtts[filename],"wb")
        ftp.retrbinary("RETR " + files_cggtts[filename], file.write)
#        if (int(files_cggtts[filename][9:12]) >= 327):
#            cgg.cggtts(path_CGGTTS, files_cggtts[filename])
#            print("CGGTTS plot completed for : " + ip_address[8:12])
        file.close()
    print("CGGTTS files download complete for: " + ip_address[8:14])
##    os.chdir("../")                     #  one step back on system dir 
##    os.chdir("../")
##    os.chdir("../")
##    os.getcwd()                    #    get the current working dir of system
##    ftp.cwd("../")                    #  go back one step on server dir
##    ftp.pwd()     
#    
    ftp.close()      
    file.close()    
        
#############################################################################################
#     rinex obs file offset plot
    
    obs_list=[]
    
    for dirpath, dirnames, files in os.walk(path_obs):
        for i in range(len(files)):
            if (observation_file_pattern == files[i][8:14]):
                obs = files[i]
                obs_list.append(obs)
    os.chdir("../")
    
    try:
        os.remove("report.html")
    except:
        pass
    
    for file in range(len(obs_list)):
        if (int(obs_list[file][4:8]) >= file_day):
            rinex.obs_file(path_obs,obs_list[file], m)
            print("Plot complete for %s" %obs_list[file])
    print("Observation file plot completed  for: " + ip_address[8:14])        

    
##############################################################################################    
    os.chdir(path_CGGTTS)
    li = os.listdir(path_CGGTTS)
    if (len(li) == 0):
        print("CGGTTS data is not available for '%s'" %ip_address)
        return ip_address
    for i in range(len(li)):
        if (li[i][12:15] == ''):
            if (os.path.isdir(os.path.join(path_CGGTTS, li[i])) == False):
                listt.append(li[i]) 
    if (len(listt) == 0): 
        print("CGGTTS data is not available for '%s'" %ip_address)
    else:
        for j in range(len(listt)):
            if (float(listt[j][6:12]) >= cggtts_day):
                rand_value += 1
                cgg.cggtts(path_CGGTTS, listt[j])
                print("CGGTTS plot completed for " + listt[j])                
        if (rand_value == 0):
            print("Current CGGTTS data is not available for '%s'" %ip_address)
            

    return ip_address           
            
            
    
    



    
