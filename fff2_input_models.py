from multiprocessing import Pool
import subprocess,glob

def run_fff2(i):
    callfff2 = subprocess.Popen(['csh -i -c ./a.out < '+i],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,close_fds=True,shell=True)
    stdout = callfff2.communicate()

class fff2_input_models:

    def __init__(self,mdir='2009/02/17/1144_scr/',fstart='input',nproc=8):

        if mdir[-1] != '/': mdir = mdir+'/'
        self.mdir = mdir
        self.fstart = fstart
        self.nproc = nproc

        self.inputf = glob.glob(mdir+fstart+'*')

    

    def run_loop(self):
        for i in self.inputf:
            run_fff2(i)


    def run_par(self):
        pool = Pool(processes=self.nproc)
        out = pool.map(run_fff2,self.inputf)
        pool.close()


