from multiprocessing import Pool
import subprocess,glob,os
from datetime import datetime,timedelta

def run_fff2(i):

#check if file exists before running a.out
    if os.path.exists(i):
#call cms2 a.out program. This takes a long time so be patient 
        callfff2 = subprocess.Popen(['csh -i -c ./a.out < '+i],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,close_fds=True,shell=True)
        stdout = callfff2.communicate()
#alternative way to run program
#    os.system("../a.out < "+i+" > /dev/null ")
    

class fff2_input_models:

    def __init__(self,time,mdir='%Y/%m/%d/%H%M_scr/',fstart='input%y%m%d%H%M%S_mod',nproc=6,modmin=1,modmax=48,cmsdir=''):

        self.time = time
        self.sform = '%Y/%m/%d %H:%M:%S'
        self.ddtime = datetime.strptime(self.time,self.sform)

        if mdir[-1] != '/': mdir = mdir+'/'

#set up files you are looking for based on input time
        self.mdir = datetime.strftime(self.ddtime,mdir)
        self.fstart = datetime.strftime(self.ddtime,fstart)
#number of processors to use
        self.nproc = nproc

#don't just search blindly instead go over a specific range
#        self.inputf = glob.glob(mdir+fstart+'*')
        self.inputf = ['{2}{0}{1:1d}.dat'.format(self.fstart,i,self.mdir) for i in range(modmin,modmax+1)]

#change working directory to cms2 directory 
        if cmsdir == '': cmsdir = open('cms2_dir','r').readlines()[0][:-1]#read in first line of cms2_dir and format to send to script
        if cmsdir[-1] != '/': cmsdir=cmsdir+'/'
        os.chdir(cmdir)
    

    def run_loop(self):
        for i in self.inputf:
            run_fff2(i)


    def run_par(self):
        pool = Pool(processes=self.nproc)
        out = pool.map(run_fff2,self.inputf)
        pool.close()
        pool.join()


