import os,shutil
from datetime import datetime,timedelta



class create_cms2_files:

    def __init__(self,time,cmsdir='',nproc=4,outdir='%Y/%m/%d/%H%M/',tempmodel='model1'):
        """Sets up initial variables to pass to rest of create_model_cms_files functions.
           Really only need to set the input time string "YYYY/MM/DD HH:MM:SS" and possibly the path to the CMS2 directory (assuming you downloaded git repo in cms2 directory then cmsdir vairable already).
           Then assuming you set up the sigmoid directory to be YYYY/MM/DD/HHMM (can change with outdir variable if needed) you are set."""

        if cmsdir == '': cmsdir = open('cms2_dir','r').readlines()[0][:-1]#read in first line of cms2_dir and format to send to script
        if cmsdir[-1] != '/': cmsdir=cmsdir+'/'
        self.time = time
        self.nproc = nproc
        self.sform = '%Y/%m/%d %H:%M:%S'
        self.dttime = datetime.strptime(self.time,self.sform)
        self.basedir = datetime.strftime(self.dttime,outdir)
        self.cmsdir = cmsdir
        self.tempmodel = tempmodel # template model




#Potential model parameters 
    def setup_file(self):
        template = self.cmsdir+self.basedir+self.tempmodel+'_setup'
        for i in range(2,self.nparam):
            shutil.copy(template,self.cmsdir+self.basedir+self.tempmodel.replace('1',str(i))+'_setup')


#copy path files after 1st one is complete
    def path_file(self):
#get number of lines in file
        pathf = open(self.cmsdir+self.basedir+self.tempmodel+"_path",'r')
        flines = len(pathf.readlines())

#initalize text variable 
        pathtxt = ""

#path for fluxrope file
        pathf = open(self.cmsdir+self.basedir+self.tempmodel+"_path",'r')

#loop through file and create large text block
        for j,i in enumerate(pathf):
            #if j == 1: i = i[:-12]+'{0}'+'\n'
            if ((j == flines-2) | (j == flines-3)):i = i[:-12]+'{1:6.5e}\n' 
            if (j == 1): i = i[:-12]+'{0:6.5e}\n'
            pathtxt = pathtxt+i
        
#model parameters
        pol = ['1.00000E9','5.00000E9','1.00000E10','5.00000E10','1.00000E11']
#Updated per conversation with antonia 2017/04/03
#       axi = ['5.00000e19','7.00000e19','9.00000e19','1.00000e20','3.00000e20','5.00000e20','7.00000e20','9.00000e20','1.00000e21','1.50000e21']
        axi = ['1.00000e19','3.00000e19','5.00000e19','7.00000e19','9.00000e19','1.00000e20','3.00000e20','5.00000e20','7.00000e20','9.00000e20','1.00000e21','1.50000e21']
        
        i = 1
        for p in pol:
            for a in axi:
                run = True
        #remove early 7E20 models for some reason unknown to me
                if ((float(p) < 9e9) & (a == '7.00000e20')): run = False 
        
                if run:
                    files = open(self.cmsdir+self.basedir+self.tempmodel.replace('1',str(i))+"_path",'w')
                    files.write(pathtxt.format(float(p),float(a)))
                    files.close()
        
                    i+=1
        self.nparam = i #get number of models to create 

#text format for input file
    def model_input(self):
        modin = self.basedir+"\n"
        modin = modin+"11                  \n"
        modin = modin+"model{0}              \n"
        modin = modin+"0                   \n"
        modin = modin+"100                 \n"
        modin = modin+"0                   \n"
        modin = modin+"0                   \n"
        modin = modin+"0                   \n"
        modin = modin+"model{0}              \n"
        modin = modin+"100                 \n"
        modin = modin+"900                 \n"
        modin = modin+"0                   \n"
        modin = modin+"0                   \n"
        modin = modin+"0.003               \n"
        modin = modin+"model{0}              \n"
        modin = modin+"1000                \n"
        modin = modin+"9000                \n"
        modin = modin+"0                   \n"
        modin = modin+"0                   \n"
        modin = modin+"0.001               \n"
        modin = modin+"model{0}              \n"
        modin = modin+"10000               \n"
        modin = modin+"10000               \n"
        modin = modin+"0                   \n"
        modin = modin+"0                   \n"
        modin = modin+"0.0003              \n"
        modin = modin+"model{0}              \n"
        modin = modin+"20000               \n"
        modin = modin+"10000               \n"
        modin = modin+"0                   \n"
        modin = modin+"0                   \n"
        modin = modin+"0.0001              \n"
        modin = modin+"model{0}              \n"
        modin = modin+"30000               \n"
        modin = modin+"10000               \n"
        modin = modin+"0                   \n"
        modin = modin+"0                   \n"
        modin = modin+"0.0001              \n"
        modin = modin+"model{0}              \n"
        modin = modin+"40000               \n"
        modin = modin+"10000               \n"
        modin = modin+"0                   \n"
        modin = modin+"0                   \n"
        modin = modin+"0.0001              \n"
        modin = modin+"model{0}              \n"
        modin = modin+"50000               \n"
        modin = modin+"10000               \n"
        modin = modin+"0                   \n"
        modin = modin+"0                   \n"
        modin = modin+"0.0001              \n"
        modin = modin+"model{0}              \n"
        modin = modin+"60000               \n"
        modin = modin+"10000               \n"
        modin = modin+"0                   \n"
        modin = modin+"0                   \n"
        modin = modin+"0.0001              \n"
        modin = modin+"model{0}              \n"
        modin = modin+"70000               \n"
        modin = modin+"10000               \n"
        modin = modin+"0                   \n"
        modin = modin+"0                   \n"
        modin = modin+"0.0001              \n"
        modin = modin+"model{0}              \n"
        modin = modin+"80000               \n"
        modin = modin+"10000               \n"
        modin = modin+"0                   \n"
        modin = modin+"0                   \n"
        modin = modin+"0.0001              \n"
        
# what to write out the file as
        filetime = datetime.strftime(self.dttime,'input%y%m%d%H%M%S_mod')
        #create input files
        for i in range(1,self.nparam):
            files = open(self.cmsdir+self.basedir+filetime+"{0}.dat".format(str(i)),'w')
            files.write(modin.format(str(i)))
        
        
            files.close()

#run creation on all files
    def create_all_files(self):
        self.path_file()
        self.setup_file()
        self.model_input()
            
