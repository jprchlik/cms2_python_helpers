from sunpy.net import vso
from numpy import unique
import glob
from sunpy.sun import carrington_rotation_number
import astropy.units as u
from astropy.io import fits
from datetime import datetime,timedelta
import ftplib
import sys,os
import gzip
import shutil


class download_cms_files:

# inital information about the directoies and time for sigmoid
    def __init__(self,time='2009/02/17 11:44:00',nproc=4,cmsdir='',outdir='%Y/%m/%d/%H%M/'):
        """Sets up inital variables to pass to rest of download_cms_file functions.
           Really only need to set the input time string "YYYY/MM/DD HH:MM:SS" and full path to the CMS2 directory.
           Then assuming you set up the sigmoid directory to be YYYY/MM/DD/HHMM (can change with outdir variable if needed) you are set."""
        if cmsdir == '': cmsdir = open('cms2_dir','r').readlines()[0][:-1]#read in first line of cms2_dir and format to send to script
        if cmsdir[-1] != '/': cmsdir=cmsdir+'/'
        self.time = time
        self.nproc = nproc
        self.sform = '%Y/%m/%d %H:%M:%S'
        self.dttime = datetime.strptime(self.time,self.sform)
        self.basedir = datetime.strftime(self.dttime,outdir)
        self.cmsdir = cmsdir

#start date from using sdo data
        self.sdo_start =  datetime(2010,05,01,00,00,00)


#copy hinode synoptic files
    def get_hinode(self):
#Hinode archive
        self.hinode_date = '%Y/%m/%d/'
        self.hinode_arch = '/archive/hinode/xrt/level1/'+datetime.strftime(self.dttime,self.hinode_date)
#look for timeline to get synoptic timelines
        self.find_synoptic_times()


#find times for synoptics
    def find_synoptic_times(self):
        self.hinode_tfmt = self.hinode_date+'%Y%m%d_exported/'#location of hinode timelines
        m = 0 # counter for number of days looking back
        for p in range(2):#dirty way to prevent timeline start day from only returning one set of synoptics
            lookt = True # found the proper timeline
            while lookt:
                self.hinode_time = self.dttime-timedelta(days=m)
                self.hinode_tldr = '/archive/hinode/xrt/timelines/'+datetime.strftime(self.hinode_time,self.hinode_tfmt)
                foundt = os.path.exists(self.hinode_tldr)
                m += 1 #increment by 1 day
                if m >= 14: return #exit downloading hinode data if no timeline found for 14 days
                if foundt:  lookt = False #if find hinode directory exit loop

            self.copy_synoptics()

#copy xrt synoptics to local directory
    def copy_synoptics(self):
        self.read_xrt_timeline()
        self.xrt_file_list()
        for i in self.xrt_files: shutil.copy(i,self.cmsdir+self.basedir)

#get list of files in timerange
    def xrt_file_list(self):
        
#get formatted list of hours
        self.xrt_hours = []
        for i in self.xrt_beg: self.xrt_hours.append('H{0:%H}00'.format(i)) 
        for i in self.xrt_end: self.xrt_hours.append('H{0:%H}00'.format(i)) 

#get unique hours
        self.xrt_hours = unique(self.xrt_hours)
        
#get all files in hours and their associated times
        self.xrt_files = []

#loop over unique hours
        for i in self.xrt_hours:
            tempfiles = glob.glob('{0}/{1}/*fits'.format(self.hinode_arch,i))
            for j in tempfiles:
                temptime = datetime.strptime(j.split('/')[-1].split('.')[0],'L1_XRT%Y%m%d_%H%M%S')
#check if time is in range
                for k in range(len(self.xrt_beg)):
                   if ((temptime >= self.xrt_beg[k]) & (temptime <= self.xrt_end[k])):
#check if header information is compatible with a syntopic
                       dat = fits.open(j)
                       hdr = dat[0].header
#check header information on fits files to get just synoptics
                       if ((hdr['NAXIS1'] == 1024) & (hdr['NAXIS2'] == 1024) & ((hdr['EC_FW2_'] == 'Ti_poly') | (hdr['EC_FW1_'] == 'Al_poly') | (hdr['EC_FW2_'] == 'Al_mesh') | (hdr['EC_FW1_'] == 'Be_thin') | (hdr['EC_FW2_'] != 'Gband'))):
                           self.xrt_files.append(j)

     
        
   
#read timeline and return synoptic times
    def read_xrt_timeline(self):        
        fmtrept = self.hinode_tldr+'re-point_{0:%Y%m%d}*.txt'.format(self.hinode_time)
        repfile = glob.glob(fmtrept)
        repoint = open(repfile[-1],'r') # read the repoint file
#list of beginning and end time for synoptics
        self.xrt_beg = []
        self.xrt_end = []
        ender = False #gets the end time for synoptic
        timefmt = '%Y/%m/%d %H:%M:%S' #format of time in pointing file

#do not start with an end
        end = False
#get the begging and end times of xrt syntopics
        for i in repoint:
            if end:
                end = False
                try:
                    self.xrt_end.append(datetime.strptime(i[20:39],timefmt))
                except:
                    self.xrt_end.append(self.xrt_beg[-1]+timedelta(minutes=20)) #if syntopic is last pointing just add 20 minutes
               
            if 'synoptic' in i.lower():
                end = True
                self.xrt_beg.append(datetime.strptime(i[20:39],timefmt))
 


#find carrington rotation number and as politely for the files
    def get_carrington(self):
        self.rotnum = carrington_rotation_number(self.time) 
#connect to ftp directory
        self.ftp = ftplib.FTP('solis.nso.edu','anonymous')
#change to carrigoton rotation number directory
        self.ftp.cwd('synoptic/level3/vsm/merged/carr-rot/')
#format of the fits file
        self.forfil = "svsm_m21lr_B3_cr{0:4d}.fts.gz"

        try:
            self.grab_car()
            self.ftp.close()
        except:
            print 'Failed unexpectedly, closing ftp access',sys.exc_info()[0]
            self.ftp.close()
            raise

#get carrington roation  files  
    def grab_car(self):
    
        #primary rotation number
        prot = int(self.rotnum)
        #rotation number +/- 1
        brot = prot-1
        arot = prot+1

        rot_list = [brot,prot,arot]

        for rot in rot_list:
            fname = self.forfil.format(rot)

            #see if file exists with or without .gz
            testfile = ((os.path.isfile(self.cmsdir+self.basedir+fname)) | (os.path.isfile(self.cmsdir+self.basedir+fname[:-3])))


            if testfile == False:
                fhandle = open(self.cmsdir+self.basedir+fname,'wb')
                self.ftp.retrbinary('RETR {0}'.format(fname),fhandle.write)
                fhandle.close()
                self.unzip_fil(self.cmsdir+self.basedir+fname)

#unzip carrington file
    def unzip_fil(self,fname):
        oname = fname[:-3]

        with gzip.open(fname,'rb') as infile:
            with open(oname,'wb') as outfile:
                for line in infile:
                    outfile.write(line)

    def get_aia(self):
        #Get Stereo observations
        client = vso.VSOClient()
        dt = timedelta(minutes=1)
        start = datetime.strftime(self.dttime-dt,self.sform)
        end = datetime.strftime(self.dttime+dt,self.sform)
    
        #set time span
        time = vso.attrs.Time(start,end)
        #grabs both stereo a and b
        ins = vso.attrs.Instrument('aia')
        #grab particular (UV) wavelengths
        wave = vso.attrs.Wave(171*u.AA,171*u.AA)
        qr1 = client.query(time,ins,wave)
        res1 = client.get(qr1,path=self.cmsdir+self.basedir+'{file}').wait()
        #grab particular (UV) wavelengths
        wave = vso.attrs.Wave(193*u.AA,193*u.AA)
        qr2 = client.query(time,ins,wave)
        res2 = client.get(qr2,path=self.cmsdir+self.basedir+'{file}').wait()
        #grab particular (UV) wavelengths
        wave = vso.attrs.Wave(304*u.AA,304*u.AA)
        qr3 = client.query(time,ins,wave)
        res3 = client.get(qr3,path=self.cmsdir+self.basedir+'{file}').wait()
        #grab particular (UV) wavelengths
        wave = vso.attrs.Wave(211*u.AA,211*u.AA)
        qr4 = client.query(time,ins,wave)
        res4 = client.get(qr4,path=self.cmsdir+self.basedir+'{file}').wait()




    def get_stereo(self):
        #Get Stereo observations
        client = vso.VSOClient()
        dt = timedelta(minutes=2)
        start = datetime.strftime(self.dttime-dt,self.sform)
        end = datetime.strftime(self.dttime+dt,self.sform)
    
        #set time span
        time = vso.attrs.Time(start,end)
        #grabs both stereo a and b
        ins = vso.attrs.Instrument('secchi')
        #grab particular (UV) wavelengths
        wave = vso.attrs.Wave(100*u.AA,3000*u.AA)
        qr = client.query(time,ins,wave)
        res = client.get(qr,path=self.cmsdir+self.basedir+'{file}')


#Download EUV images
    def get_euv(self):
        if self.dttime >= self.sdo_start:
            self.get_aia()
            #include get stereo on recent observaitons J. Prchlik (2018/01/18)
            self.get_stereo()
        else:
            self.get_stereo()



#dowload magnetograms
    def get_magnetogram(self):
        if self.dttime >= self.sdo_start:
            self.get_hmi()
        else:
            self.get_mdi()

#get mdi magnetogram
    def get_mdi(self):
        client = vso.VSOClient()
        dt = timedelta(minutes=96)
        start = datetime.strftime(self.dttime-dt,self.sform)
        end = datetime.strftime(self.dttime+dt,self.sform)
    
        #set time span
        time = vso.attrs.Time(start,end)
        #set instrument
        ins = vso.attrs.Instrument('mdi')
        #set provider which reduces to just 96m magnetograms
        prov = vso.attrs.Provider('SDAC')
        #query vso
        qr = client.query(time,ins,prov)
        self.qr = qr
       

        res = client.get(qr,path=self.cmsdir+self.basedir+'{file}').wait()

#Move file to a file name with start time included
        for k in qr:
            stime = k['time']['start']
            stime = stime[:8]+'_'+stime[8:]
            sfile = k['fileid'].split('/')[-1].lower().replace('.','_').replace('_fits','.fits')

            shutil.move(self.cmsdir+self.basedir+sfile,self.cmsdir+self.basedir+stime+'_'+sfile)

#get hmi magnetogram
    def get_hmi(self):
        client = vso.VSOClient()
        dt = timedelta(minutes=1)
        start = datetime.strftime(self.dttime-dt,self.sform)
        end = datetime.strftime(self.dttime+dt,self.sform)
        phys = vso.attrs.Physobs('LOS_magnetic_field')
        
    
        #set time span
        time = vso.attrs.Time(start,end)
        #set instrument
        ins = vso.attrs.Instrument('hmi')
        #query vso
        qr = client.query(time,ins,phys)
        res = client.get(qr,path=self.cmsdir+self.basedir+'{file}',methods=("URL-FILE_Rice","URL-FILE")).wait()

#download all
    def download_all(self):
        self.get_hinode()
        self.get_euv()
        self.get_carrington()
        self.get_magnetogram()

#create subdirectory tree
    def build_subtree(self):


        try:
            os.makedirs(self.cmsdir+self.basedir)
        except:
            print 'Directory {0} already exists. Proceeding'.format(self.cmsdir+self.basedir)
        


