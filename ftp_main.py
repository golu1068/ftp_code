import ip
##import julian
import datetime
import sys
import time
import os
from datetime import datetime as dt
import converter as con
import rinex_func as rinex
import cggtts_func as cgg
###################################################################################
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename  

master = Tk()
dirname_rinex = ''
global choose_30_1
choose_30_1 = 30
rinex_file_list = []; cggtts_file_list = [];
m=2      #   random value  but important
master.title("FTP server")
#master.iconbitmap(r'E:\spyder_code\New_folder\multipath_test\favicon.ico')
#master.geometry('400x150')
#master.attributes('-fullscreen', True)
master.geometry('450x350+460+320')     #   Chnage the position of window
#w, h = master.winfo_screenwidth(), master.winfo_screenheight()
#master.overrideredirect(1)
#master.geometry("%dx%d+0+0" % (w, h))
master.minsize(100,100)
########################################################################
# check button
def button_1():
    C2.deselect()
    change_1()
    change_2()
    
            
def button_2():
    C1.deselect()
    change_2()
    change_1()

def button_11():
    global choose_30_1
    C22.deselect()
    choose_30_1 = 30
             
def button_22():
    global choose_30_1
    C11.deselect()
    choose_30_1 = 1
############################################################################
def change_1():
    if (ftp.get() == 1):
        ft='normal'
    else:
        ft='disabled'

    e1.config(state=ft)
    e2.config(state=ft)
    e3.config(state=ft)
    e4.config(state=ft)
    dirname.config(state=ft)
    

def change_2():
    if (off.get() == 1):
        of='normal'
    else:
        of='disabled'

    e5.config(state=of)
    e6.config(state=of)
    C3.config(state=of)
    C4.config(state=of)
    C5.config(state=of)
    C6.config(state=of)
    C7.config(state=of)
    C8.config(state=of)
    dir_rinex.config(state=of)
    dir_cggtts.config(state=of)
##################################################################################################
def goto_rinex_func_code(path_name, rinex_filename):
  global plot_type
  os.chdir(path_name)
  li = os.listdir(path_name)        #  List of all obs file in dir
  for k in range(len(li)):
     if (li[k][8:12] == ".20O" or li[k][8:12] == ".19O" or li[k][8:12] == ".18O"):
        rinex_file_list.append(li[k])
     else:
        pass
##  print(os.getcwd())   
  os.chdir("../")               # Change dir 
  if (single.get() == 1):
      for j in range(len(rinex_file_list)):
         if(int(rinex_file_list[j][4:8]) == int(rinex_filename[4:8])):
            retu = rinex.obs_file(path_name, rinex_file_list[j], m, plot_type, choose_30_1)
            if (retu == None):
               pass
            else:
               print("offline plot complete for %s\n" %rinex_file_list[j])
  else:
      for j in range(len(rinex_file_list)):
         if(int(rinex_file_list[j][4:8])>= int(rinex_filename[4:8])):
            retu = rinex.obs_file(path_name, rinex_file_list[j], m, plot_type, choose_30_1)
            if (retu == None):
               pass
            else:
               print("offline plot complete for %s\n" %rinex_file_list[j])
      
def goto_cggtts_func_code(path_name_cggtts, cggtts_filename):
  os.chdir(path_name_cggtts)
  li_cggtts = os.listdir(path_name_cggtts)
  for k in range(len(li_cggtts)):
     if (li_cggtts[k][12:15] == ''):
        cggtts_file_list.append(li_cggtts[k])
     else:
        pass
#  print(os.getcwd())  
##   os.chdir("../")
  if (single.get() == 1):      
      for j in range(len(cggtts_file_list)):
         if (int(cggtts_file_list[j][6:8]) == 58):
            if (int(cggtts_file_list[j][9:12]) == int(cggtts_filename[9:12])):
               cggt = cgg.cggtts(path_name_cggtts, cggtts_file_list[j])
               if (cggt == None):
                  pass
               else:
                  print("offline plot complete for %s\n" %cggtts_file_list[j])
  else:
      for j in range(len(cggtts_file_list)):
         if (int(cggtts_file_list[j][6:8]) == 58):
            if (int(cggtts_file_list[j][9:12]) >= int(cggtts_filename[9:12])):
               cggt = cgg.cggtts(path_name_cggtts, cggtts_file_list[j])
               if (cggt == None):
                  pass
               else:
                  print("offline plot complete for %s\n" %cggtts_file_list[j])
#################################################################################################

def main():
    destination = e4.get()          #  where u want to save the files

    ip_add = e1.get()           # ip address 
    
    path = destination + ip_add[8:12]
          
    rinex_no_of_days = int(e2.get())               #  from which day u want to plot obsevation data
    cggtts_no_of_days = int(e3.get())                 #  from which day u want to plot CGGTTS data 
    
    destination = e4.get()          #  where u want to save the files
    #######################################################################
    obs_day = 1
    obs_mjd = 58484

    d  = dt.now()
    mjd = int(con.date2mjd(d.year, d.month, d.day, 0, 0, 0))        ## hour=0, minu=0, sec=0
##    mjd = int(julian.to_jd(d, fmt="mjd"))
    nodays = mjd - obs_mjd

    current_obs_day = obs_day + nodays
    
    rinexday = int((current_obs_day - rinex_no_of_days)*10)

    cggttsday = float((mjd - cggtts_no_of_days)/1000)
    ###########################################################################
       
    #   download all Rinex files from that ip   
    m = 2   #    Random value   but important

    ip_data = ip.ftp(ip_add, destination, m, rinexday, cggttsday)
    if (ip_data == None):
        pass
    else:
        print("Work completed for IP '%s'" %ip_add)
#######################################################################################
def main_offline():                       # offline main function
    global choose_30_1
    a=e5.get()
    b=e6.get()
    for i in range (len(a)):
        if (a[i:(i+4)] == "ACCO" and (a[(i+8):(i+12)] == ".20O" or a[(i+8):(i+12)] == ".19O" or a[(i+8):(i+12)] == ".18O")):
            path_name = a[0:i]
            rinex_filename = a[i:(i+12)]
            goto_rinex_func_code(path_name, rinex_filename)
            break
        if (i == (len(a)-1)):
            print("This is not a Rinex observation file")
            break
         
    for j in range(len(b)):
        if (b[j:(j+6)] == "IRACCO" and b[(j+8):(j+9)] == "." and b[(j+12):(j+15)] == ''):
            path_name_cggtts = b[0:j]
            cggtts_filename = b[j:(j+12)]
            goto_cggtts_func_code(path_name_cggtts, cggtts_filename)
            break
        if (j == (len(b)-1)):
            print("This is not a CGGTTS file")
            break
    
        
###################################################################
def get_dirname():
#    master.withdraw()
    e4.delete(0,END)    # To delete the content in the search bar
    dirname = askdirectory(initialdir='', title='Please select a directory')
    e4.insert(10,dirname+r"/")
    return dirname
#    master.deiconify()   #  To display the window
def get_dirname_rinex():
    e5.delete(0,END)    # To delete the content in the search bar
    dirname_rinex = askopenfilename(initialdir='',title='Please select a rinex observation file')
    e5.insert(10,dirname_rinex)
    return dirname_rinex
def get_dirname_cggtts():
    e6.delete(0,END)    # To delete the content in the search bar
    dirname_cggtts = askopenfilename(initialdir='',title='Please select a CGGTTS file')
    e6.insert(10,dirname_cggtts)
    return dirname_cggtts
    
        
def show_entry_fields():
    cggtts_file_list.clear()
    rinex_file_list.clear()
    if (ftp.get() == 1):       
       print("IP Address: %s" % (e1.get()))
       print("Rinex no_days: %s" % (e2.get()))
       print("Cggtts no_days: %s" % (e3.get()))
       print("Output_file_path: %s\n" % (e4.get()))   
       main()                            #   Calling the main function
    else:
        print("\nOffline mode is running")

    if (off.get() == 1):
        print("Offline rinex path is: %s" %(e5.get()))
        print("Offline cggtts path is: %s" %(e6.get()))        
        main_offline()                           # Calling offline main function
    else:
        pass

   
def enter_key(event):
    show_entry_fields()
    
def quit_key(event):
    master.destroy()  

def browse_key(event):
    get_dirname()

def multiple_file():
    C4.deselect()
    
def single_file():
    C3.deselect()
plot_type=0   
def rang():
    global plot_type
    plot_type = 0
    C6.deselect()
    C7.deselect()
    C8.deselect()
def phase():
    global plot_type
    plot_type = 1
    C5.deselect()
    C7.deselect()
    C8.deselect()
def doppler():
    global plot_type
    plot_type = 2
    C5.deselect()
    C6.deselect()
    C8.deselect()
def cbyn():
    global plot_type
    plot_type = 3
    C5.deselect()
    C6.deselect()
    C7.deselect()
#################################################################################################                        
ftp = IntVar()
C1 = Checkbutton(master, text="FTP mode", variable=ftp, command=button_1)
C1.grid(row=0, column= 0, sticky=W)
C1.select()
off = IntVar()
C2 = Checkbutton(master, text="Offline mode", variable=off, command=button_2)
C2.grid(row=0, column=1, sticky=W)

sec_30 = IntVar()
C11 = Checkbutton(master, text="30 Second", variable=sec_30, command=button_11)
C11.grid(row=0, column=2, sticky=W)
C11.select()
sec_1 = IntVar()
C22 = Checkbutton(master, text="1 Second", variable=sec_1, command=button_22)
C22.grid(row=0, column=3, sticky=W)
#################################################################################################    
       
dirname =  Button(master, text="Browse", bg="light green", command=get_dirname, disabledforeground='grey')
dirname.grid(row=4, column=2, sticky=W, pady=0,padx=10)
master.bind('<b>', browse_key)

Label(master, text="IP Address").grid(row=1, pady=5)
Label(master, text="Rinex no_days").grid(row=2, pady=5)
Label(master, text="Cggtts no_days").grid(row=3, pady=5)
Label(master, text="Output_file_path").grid(row=4, pady=5)
Label(master, text="Offline mode").grid(row=6, pady=5)                     #  label for offline mode
Label(master, text="Select Plot").grid(row= 7, pady=5)
Label(master, text="Offline rinex path").grid(row= 8, pady=5)
Label(master, text="Offline cggtts path").grid(row= 9, pady=5)



e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)
e5 = Entry(master)    #  entry for offline mode
e5.config(state="disabled")
e6 = Entry(master)     #   entry for offline mode
e6.config(state="disabled")

e1.insert(10,"192.168.8.4")
e2.insert(10,"1")
e3.insert(10,"1")
e4.insert(10,"F:/Receiver_log/")


e1.grid(row=1, column=1)
e2.grid(row=2, column=1)
e3.grid(row=3, column=1)
e4.grid(row=4, column=1)
e5.grid(row=8, column=1)
e6.grid(row=9, column=1)

###################################################################################################################
multiple = IntVar()
C3 = Checkbutton(master, text='Multiple file', variable=multiple, command=multiple_file)
C3.grid(row = 6, column=1)
C3.config(state='disabled')
C3.select()
single = IntVar()
C4 = Checkbutton(master, text='Single file', variable=single, command=single_file)
C4.grid(row=6, column=2)
C4.config(state='disabled')

range_plot = IntVar()
C5 = Checkbutton(master, text='Range', variable=range_plot, command=rang, anchor=W, padx=1)
C5.grid(row = 7, column=1, sticky=W, padx=1)
C5.config(state='disabled')
C5.select()

phase_plot = IntVar()
C6 = Checkbutton(master, text='Phase', variable=phase_plot, command=phase, anchor=W)
C6.grid(row = 7, column=1,  sticky=E, padx=5)
C6.config(state='disabled')
#C6.select()

doppler_plot = IntVar()
C7 = Checkbutton(master, text='Doppler', variable=doppler_plot, command=doppler, anchor=W)
C7.grid(row = 7, column=2, sticky=W, padx=0)
C7.config(state='disabled')
#C7.select()

cbyn_plot = IntVar()
C8 = Checkbutton(master, text='C/N', variable=cbyn_plot, command=cbyn, anchor=W)
C8.grid(row = 7, column=3, sticky=W, padx=0)
C8.config(state='disabled')
#C8.select()
###########################################################################################################

dir_rinex =  Button(master, text="Browse", bg="light green", command=get_dirname_rinex, disabledforeground='grey')          ##   browse button for offlien mode
dir_rinex.grid(row=8, column=2, sticky=W, pady=0,padx=10)  
dir_rinex.config(state='disabled')    
dir_cggtts =  Button(master, text="Browse", bg="light green", command=get_dirname_cggtts, disabledforeground='grey')
dir_cggtts.grid(row=9, column=2, sticky=W, pady=0,padx=10)
dir_cggtts.config(state='disabled')

Button(master, text='Submit', bg= "light blue", command=show_entry_fields).grid(row=10, column=1, sticky=W, pady=4,padx=35)
master.bind('<Return>', enter_key)
Button(master, text='Quit', bg= "Red", command=master.destroy).grid(row=10, column=3, sticky=W, pady=4)
master.bind('<q>', quit_key)


master.mainloop()
