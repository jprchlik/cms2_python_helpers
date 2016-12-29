from sunpy.net import vso
from sunpy.sun import carrington_rotation_number
import astropy.units as u
from datetime import datetime,timedelta
import ftplib
import sys,os
import gzip


class download_cms_files:

# inital information about the directoies and time for sigmoid
    def __init__(self,time='2009/02/17 11:44:00',nproc=4,cmsdir='/Volumes/Pegasus/jprchlik/projects/sigmoid_catalog/CMS2'):
        if cmsdir[-1] != '/': cmsdir=cmsdir+'/'
        self.time = time
        self.nproc = nproc
        self.sform = '%Y/%m/%d %H:%M:%S'
        self.dttime = datetime.strptime(self.time,self.sform)
        self.basedir = datetime.strftime(self.dttime,'%Y/%m/%d/%H%M/')
        self.cmsdir = cmsdir


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
        res = client.get(qr,path=self.cmsdir+self.basedir+'{file}.fits')



#dowload magnetograms
    def get_magnetogram(self):
        if self.dttime >= datetime(2010,05,01,00,00,00):
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
       

        res = client.get(qr,path=self.cmsdir+self.basedir+'{file}.fits')

#get hmi magnetogram
    def get_hmi(self):
        client = vso.VSOClient()
        dt = timedelta(seconds=96)
        start = datetime.strftime(self.dttime-dt,self.sform)
        end = datetime.strftime(self.dttime+dt,self.sform)
    
        #set time span
        time = vso.attrs.Time(start,end)
        #set instrument
        ins = vso.attrs.Instrument('hmi')
        #query vso
        qr = client.query(time,ins)
        res = client.get(qr,path=self.cmsdir+self.basedir+'{file}.fits')


