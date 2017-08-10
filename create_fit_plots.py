import matplotlib as mpl
mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.size'] = 10.0
mpl.rcParams['font.weight'] = 'bold'
from astropy.io import ascii
from astropy.table import join
import glob
import os,shutil
from datetime import datetime,timedelta
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
try:
    from fancy_plot import fancy_plot
    fp = True
except:
    print 'Fancy plot not in your python path please add'
    fp = False


class cms2_plot:

    def __init__(self,time,cmsdir='',outdir='%Y/%m/%d/%H%M/',fit_file='fit_information.dat',lop_file='fit_loops.dat'):
        """Creates plots of helicity vs free energy and Poloidal vs Axial flux"""
        if cmsdir == '': cmsdir = open('cms2_dir','r').readlines()[0][:-1]#read in first line of cms2_dir and format to send to script
        if cmsdir[-1] != '/': cmsdir=cmsdir+'/'
        self.time = time
        self.form = "%Y/%m/%d %H:%M:%S"
        self.time = datetime.strptime(self.time,self.form)
        if outdir[-1] != '/': outdir = outdir+'/'
        self.bdir = datetime.strftime(self.time,outdir)
        self.cdir = cmsdir
        self.ifit = fit_file
        self.loop = lop_file


    def read_model(self):
        """Reads the formatted model file to extract axial and poloidal fluxes"""

        axi = []
        pol = []
        #read the file name for each model
        for i in self.tdat['mod_nam']:
            mod_num = i.split('_')[0] #get modelN
            mod_pat = mod_num+'_path' #path file
            
            fil = open(self.cdir+self.bdir+mod_pat,'r').readlines()
            pol.append(fil[1].split()[-1]) #get polodial flux
            axi.append(fil[-3].split()[-1]) #get axial flux
         
        #add axial and poloidal flux to main table    
        self.tdat['axi'] = np.array(axi)
        self.tdat['pol'] = np.array(pol)
            

    def read_infit(self):
        """Read the best fit model file""" 
        from astropy.io import ascii
        self.fdat = ascii.read(self.cdir+self.bdir+self.ifit)
        self.ldat = ascii.read(self.cdir+self.bdir+self.loop)
        self.tdat = join(self.fdat,self.ldat,keys=['mod_nam'])
        self.comp_tsig()
        self.read_model()
        #remove some bad coronal loops

#use model id for abbicus
        self.tdat['mod_id'] = [int(i.split('_')[0].replace('model','')) for i in self.tdat['mod_nam']]

    def comp_tsig(self):
        """Add total sigma to table"""
        cols = self.tdat.columns.keys() #list of columns in table
        bfit = [i for i in cols if "bfit" in i] #All the bfit columns
        self.sind = int(bfit[0].split('_')[1])#start index for loops
        self.eind = int(bfit[-1].split('_')[1])#end index for loops
        self.tind = self.eind-self.sind+1 #total number of coronal loops
        

        #fitting stat values 
        fsta = [i for i in bfit if ((("_5" in i) & ("_5_" not in i)) | ("_5_5" in i))]

        #normalize minimums
        for i in fsta: self.tdat[i] = self.tdat[i]/self.tdat[i][self.tdat[i] > 0.].min()

        #init new column
        self.tdat['bfit_t_5'] = 0.0
        self.tdat['bfit_s_5'] = 0.0
        for i in fsta: self.tdat['bfit_t_5'] = self.tdat[i]+self.tdat['bfit_t_5']#total uncertainty
        for i in fsta: self.tdat['bfit_s_5'] = self.tdat[i]+self.tdat['bfit_s_5']**2.#sq. total uncertainty
        self.tdat['bfit_a_5'] = self.tdat['bfit_t_5']/self.tind #average 
        self.tdat['bfit_s_5'] = (self.tdat['bfit_s_5'])**.5/self.tind #sum squared average 

        #uncertainty in average
        self.tdat['bfit_u_5'] = 0.0
        for i in fsta: self.tdat['bfit_u_5'] = (self.tdat[i]-self.tdat['bfit_a_5'])**2.+self.tdat['bfit_u_5']
        self.tdat['bfit_u_5'] = np.sqrt(self.tdat['bfit_u_5'])/float(self.tind)
        


    def create_plots(self):
        """Create plots using the best fit data"""
        self.read_infit()

        self.figt,self.axt = plt.subplots(ncols=3,nrows=1,gridspec_kw={'width_ratios':[50,50,10]},figsize=(8,4))
        #self.figt.subplots_adjust(wspace=0.6)
        self.figi,self.axi = plt.subplots(nrows=2,ncols=2,sharey=True)
        #model number plots
        self.figm,self.axm = plt.subplots()

#        self.grid = gridspec.GridSpec(1,3,width_ratios=[10,10,1],height_ratios=[1]) 
        self.axt = [i for i in self.axt.ravel()]
        self.axi = [i for i in self.axi.ravel()]

#xvalues for 4 figure plot
        xfigs = ['axi','pol','free_energy','helicity']
        names = {'axi': ['Axial','Mx'],'pol': ['Poloidal','Mx/cm'], 'free_energy' : ['Free Energy','ergs'], 'helicity': ['Helicity','Mx$^2$']}
       
       
#set color for eruptions and non eruptive states
        self.tdat['color'] = 'black'
        self.tdat['color'][self.tdat['eruption'] == 'Yes'] = 'red'

        use = self.tdat['bfit_a_5'] > 0 #reject filled values
        print self.tdat['bfit_a_5'][use].max(),self.tdat['bfit_a_5'][use].min()
#plot 4 panel plot
        ccolor = plt.cm.jet #colors for cycling
        ocolor = ccolor(np.linspace(0,1,self.tind))
        for i in np.arange(self.tind)+self.sind:
        #plot as a function of model number
            self.axm.scatter(self.tdat['mod_id'][use].astype('float'),self.tdat['bfit_{0:1d}_5'.format(i)][use].astype('float'),c=ocolor[i],label='{0:1d}'.format(i)) 
            for k,j in enumerate(self.axi): j.scatter(self.tdat[xfigs[k]][use].astype('float'),self.tdat['bfit_{0:1d}_5'.format(i)][use].astype('float'),c=ocolor[i],label='{0:1d}'.format(i)) 


        for k,j in enumerate(self.axi): 
            j.set_xlabel('{0} [{1}]'.format(*names[xfigs[k]]))
            j.set_ylabel('Normed Quad. Mean Dis.')
        self.axi[0].legend(loc='upper left',frameon=False,fontsize=4)
        #self.pol[0].set_ylim([-3.5,-2.])
        self.axi[0].set_yscale('log')
        self.axi[0].set_xscale('log')
        self.axi[1].set_xscale('log')
        #self.axi[0].set_ylim([0.0001,0.01])
         
#model fit parameter fit labels
        self.axm.scatter(self.tdat['mod_id'][use],self.tdat['bfit_a_5'][use].astype('float'),marker='x',c='black',label='Ave.')
        self.axm.errorbar(self.tdat['mod_id'][use],self.tdat['bfit_a_5'][use].astype('float'),yerr=self.tdat['bfit_u_5'][use],fmt='x',c='black',label=None,markersize=1)
        self.axm.set_ylabel('Normed Quad. Mean Dis.')
        self.axm.set_xlabel('Model ID')
        self.axm.set_yscale('log')


#3D plot
        vmin =  0.0015
        vmax =  0.0025
        vmin =  1.00
        vmax =  2.0
        cmap =  plt.cm.Greys
        cmap =  plt.cm.Blues
        cax =self.axt[0].scatter(self.tdat['axi'][use].astype('float'),self.tdat['pol'][use].astype('float'),c=self.tdat['bfit_a_5'][use],cmap=cmap,vmin=vmin,vmax=vmax,edgecolor=self.tdat['color'][use])
        self.axt[1].scatter(self.tdat['free_energy'][use],self.tdat['helicity'][use],c=self.tdat['bfit_a_5'][use],cmap=cmap,vmin=vmin,vmax=vmax,edgecolor=self.tdat['color'][use])
       
        #set labels
        self.axt[0].set_xlabel('Axial Flux [Mx]')
        self.axt[0].set_ylabel('Poloidal Flux [Mx/cm]')
        self.axt[0].set_yscale('log')
        self.axt[0].set_xscale('log')
 
        self.axt[1].set_xlabel('Free Energy [erg]')
        self.axt[1].set_ylabel('Helicity [Mx$^2$]')
 
     


        cbar = self.figt.colorbar(cax,cax=self.axt[2])
        cbar.set_label('Normed Quad. Mean Dis.')
 #       self.axt[1,1].scatter(self.tdat['free_energy'][use],self.tdat['helicity'][use],c=self.tdat['bfit_s_5'][use],cmap=plt.cm.magma,vmin= 0.00015,vmax=0.000600)
#Use fancy plot if module exists
        if fp:
            fancy_plot(self.axm)
            for i in self.axt: fancy_plot(i)
            for i in self.axi: fancy_plot(i)

        self.figt.tight_layout()



        self.figt.savefig(self.cdir+self.bdir+'total_fit_{0:%Y%m%d%H%M%S}.png'.format(self.time),bbox_pad=.1,bbox_inches='tight')
        self.figt.savefig(self.cdir+self.bdir+'total_fit_{0:%Y%m%d%H%M%S}.eps'.format(self.time),bbox_pad=.1,bbox_inches='tight')
        self.figi.savefig(self.cdir+self.bdir+'indvd_fit_{0:%Y%m%d%H%M%S}.png'.format(self.time),bbox_pad=.1,bbox_inches='tight')
        self.figm.savefig(self.cdir+self.bdir+'model_fit_{0:%Y%m%d%H%M%S}.eps'.format(self.time),bbox_pad=.1,bbox_inches='tight')
        self.figm.savefig(self.cdir+self.bdir+'model_fit_{0:%Y%m%d%H%M%S}.png'.format(self.time),bbox_pad=.1,bbox_inches='tight')
        self.figi.savefig(self.cdir+self.bdir+'indvd_fit_{0:%Y%m%d%H%M%S}.eps'.format(self.time),bbox_pad=.1,bbox_inches='tight')
