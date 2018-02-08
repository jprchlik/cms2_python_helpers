from sunpy.net import vso, Fido
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
    def __init__(self,time='2009/02/17 11:44:00',nproc=4,cmsdir='',outdir='%Y/%m/%d/%H%M/',x=None,y=None):
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
        self.x = x
        self.y = y

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

                       #check for acceptable filters
                       fil_check = (((hdr['EC_FW2_'] == 'Ti_poly') | (hdr['EC_FW1_'] == 'Al_poly') | (hdr['EC_FW2_'] == 'Al_mesh') | (hdr['EC_FW1_'] == 'Be_thin') | (hdr['EC_FW2_'] != 'Gband')))
                       #check header information on fits files to get just synoptics
                       if ((hdr['NAXIS1'] == 1024) & (hdr['NAXIS2'] == 1024) & (fil_check)):
                           self.xrt_files.append(j)
                       #check to make sure self.x and self.y are defined
                       if ((self.x != None) & (self.y != None)):
                            #Also check to see if there are any small FOV XRT files within 100'' of y and x
                           dist = (((hdr['CRVAL1']-self.x)**2.+(hdr['CRVAL2']-self.y)**2.))**.5
                           if ((dist  <= 100) & (fil_check)):
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
        #loop through repoint file lines
        for i in repoint:
            if end:
                end = False
                try:
                    self.xrt_end.append(datetime.strptime(i[20:39],timefmt))
                except:
                    self.xrt_end.append(self.xrt_beg[-1]+timedelta(minutes=20)) #if syntopic is last pointing just add 20 minutes
            #look for lines containing the word synoptic 
            if 'synoptic' in i.lower():
                end = True
                self.xrt_beg.append(datetime.strptime(i[20:39],timefmt))
                #Add continue to prevent errors when synoptic pointing is close to observed AR
                continue

            #if you want to look for local AR files
            if ((self.x != None) & (self.y != None)):
                #check for nearby pointings with small FoV J. Prchlik 2018/01/24
                try:
                    p_x = float(i[72:78]) 
                    p_y = float(i[79:87])  
                #if values are not floats continue
                except:
                    continue
                
                #distance from pointing to planned AR
                dist = (((p_x-self.x)**2.+(p_y-self.y)**2.))**.5
                #if distance less than 100'' from AR add to list to look for XRT files
                if dist < 100: 
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
            print('Failed unexpectedly, closing ftp access',sys.exc_info()[0])
            self.ftp.close()
            raise

#get carrington roation  files  
    def grab_car(self):
    
        #primary rotation number
        prot = int(self.rotnum)
        #rotation number +/- 1
        brot = prot-1
        arot = prot+1

        #only get 3 carrington rotations
        rot_list = [brot,prot,arot]
        #only get exact carrington rotation number
        #rot_list = [prot]

        #NSO synoptic maps only go until 2166
        if self.rotnum > 2166:
           #Use HMI synoptics
           import urllib2
           fname = 'hmi.Synoptic_Mr_small.{0:1.0f}.fits'.format(self.rotnum)
           hmi_url = 'http://jsoc.stanford.edu/data/hmi/synoptic/'+fname
           res = urllib2.urlopen(hmi_url)
           #read binary fits file
           f_carrot = res.read()

           #write fits file locally
           with open(self.cmsdir+self.basedir+fname,'wb') as f:
               f.write(f_carrot)
            #print("Carrington rotation {0:1.0f} is beyond NSO archive".format(self.rotnum))

        else:
            for rot in rot_list:
                fname = self.forfil.format(rot)

                #see if file exists with or without .gz
                testfile = ((os.path.isfile(self.cmsdir+self.basedir+fname)) | (os.path.isfile(self.cmsdir+self.basedir+fname[:-3])))

                #if file does not exist download new file
                if testfile == False:
                    try:
                        fhandle = open(self.cmsdir+self.basedir+fname,'wb')
                        self.ftp.retrbinary('RETR {0}'.format(fname),fhandle.write)
                        fhandle.close()
                        self.unzip_fil(self.cmsdir+self.basedir+fname)
                    except:
                        print("Unable to download carrington rotation map at {0}".format(fname))

#unzip carrington file
    def unzip_fil(self,fname):
        oname = fname[:-3]

        with gzip.open(fname,'rb') as infile:
            with open(oname,'wb') as outfile:
                for line in infile:
                    outfile.write(line)

    #Get AIA 1024x1024  synoptics from Stanford, since CMS2 cannot handle 4096x4096 files
    def get_aia_syn(self):
        import urllib

        #synoptic archive location
        syn_arch = 'http://jsoc.stanford.edu/data/aia/synoptic/'

        #check if current minute is even, since synoptics are every 2 minutes
        if self.dttime.minute % 2 == 0:
            inp_time = self.dttime
        #otherwise add 1 minute to current time
        else:
            inp_time = self.dttime+timedelta(minutes=1)

        #reduced time to 12 seconds for AIA observation download J. Prchlik 2018/01/24
        dt = timedelta(minutes=2)
        start = inp_time-dt
        end   = inp_time

        #wavelengths to download
        d_wav = [131,171,193,211,304]

        #create directory path minus the wavelength
        f_dir = '{0:%Y/%m/%d/H%H00/AIA%Y%m%d_%H%M_}'
        s_dir = f_dir.format(start)
        e_dir = f_dir.format(end)

        #wavelength format
        w_fmt = '{0:04d}.fits'
     
        #download files from archive for each wavelength
        for i in d_wav:
           #format wavelength
           w_fil = w_fmt.format(i)
           urllib.urlretrieve(syn_arch+s_dir+w_fil,self.cmsdir+self.basedir+s_dir.split('/')[-1]+w_fil) 
           urllib.urlretrieve(syn_arch+e_dir+w_fil,self.cmsdir+self.basedir+e_dir.split('/')[-1]+w_fil) 
      


    #Get aia files from VSO
    def get_aia(self):
        #Get Stereo observations
        client = vso.VSOClient()
        #reduced time to 12 seconds for AIA observation download J. Prchlik 2018/01/18
        dt = timedelta(seconds=12)
        start = datetime.strftime(self.dttime-dt,self.sform)
        end = datetime.strftime(self.dttime+dt,self.sform)
    
        #set time span
        time = vso.attrs.Time(start,end)
        #grabs both stereo a and b
        ins = vso.attrs.Instrument('aia')
        #grab particular (UV) wavelengths
        wave = vso.attrs.Wavelength(171*u.AA,171*u.AA)
        qr1 = client.query(time,ins,wave)
        res1 = client.get(qr1,path=self.cmsdir+self.basedir+'{file}').wait()
        #grab particular (UV) wavelengths
        wave = vso.attrs.Wavelength(193*u.AA,193*u.AA)
        qr2 = client.query(time,ins,wave)
        res2 = client.get(qr2,path=self.cmsdir+self.basedir+'{file}').wait()
        #grab particular (UV) wavelengths
        wave = vso.attrs.Wavelength(304*u.AA,304*u.AA)
        qr3 = client.query(time,ins,wave)
        res3 = client.get(qr3,path=self.cmsdir+self.basedir+'{file}').wait()
        #grab particular (UV) wavelengths
        wave = vso.attrs.Wavelength(211*u.AA,211*u.AA)
        qr4 = client.query(time,ins,wave)
        res4 = client.get(qr4,path=self.cmsdir+self.basedir+'{file}').wait()


    #grab stereo files from stereo archive 
    def grab_stereo(self):
        #look in both stereo ahead and behind
        beacons = ['ahead','behind']

        #set time range around to look for stereo files
        dt = timedelta(minutes=30)
        start = self.dttime-dt
        end = self.dttime+dt

        #base directory for start and end directory 
        f_bdir = '{0:%Y%m%d}/*fts'
        s_bdir = f_bdir.format(start)
        e_bdir = f_bdir.format(end)

        #loop over subdirectories if start and end time cross days
        if s_bdir == e_bdir: 
            l_dir = [s_bdir]
        else:
            l_dir = [s_bdir,e_bdir]

        #loop over stereo ahead and behind
        for bea in beacons:
            #change to stereo ahead and behind directory continue if directories do not exist
            try:
                self.s_ftp.cwd('/pub/beacon/{0}/secchi/img/euvi/'.format(bea))
            except:
                print('No STEREO {0} OBS'.format(bea)) 
                continue

            #get list of files in subdirectory
            fit_list = []
            try:
                for days in l_dir: fit_list.append(self.s_ftp.nlst(days))
            except:
                print('No STEREO {0} OBS at {1}'.format(bea,days)) 
                continue

            #flatten the list
            flat_list = [item for sublist in fit_list for item in sublist]

            #list of files to download
            d_list = []


            #time reange for looping
            t_r = 1
            #try expanding the time search range
            loop = True 
            #make sure you get at least 4 files
            while ((len(d_list) <= 4) & (loop)):
                #check datetime in list is between start and end
                for fil in flat_list:
                    #get datetime from list
                    obs_time = datetime.strptime(fil.split('/')[-1][:15],'%Y%m%d_%H%M%S')
                    #if in time range add to download list
                    if ((obs_time >= self.dttime-(dt*t_r)) & (obs_time <= self.dttime+(dt*t_r))): d_list.append(fil)
                #increment index
                t_r += 1
                #don't loop more than 5 times
                if t_r > 6: loop = False

            #finally download stereo files
            for fil in d_list:
                fname = fil.split('/')[-1] 
                testfile = os.path.isfile(self.cmsdir+self.basedir+fname)

                #if file does not exist download new file
                if testfile == False:
                    try:
                        fhandle = open(self.cmsdir+self.basedir+fname,'wb')
                        self.s_ftp.retrbinary('RETR {0}'.format(fil),fhandle.write)
                        fhandle.close()
                    except:
                        print("Unable to download STEREO observation at {0}".format(fil))
                        continue

#unzip carrington file
    def unzip_fil(self,fname):
        oname = fname[:-3]



    #get stereo files directly from archive
    def get_stereo(self):

        #connect to ftp directory
        self.s_ftp = ftplib.FTP('stereoftp.nascom.nasa.gov','anonymous')


        try:
            self.grab_stereo()
        except:
            print('Unable to download STEREO files')

        #close ftp connection
        self.s_ftp.close()


    

    def get_stereo_vso(self):
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
        wave = vso.attrs.Wavelength(100*u.AA,3000*u.AA)
        #qr = client.query(time,ins,wave)
        qr = client.search(time,ins,wave)
        #res = client.get(qr,path=self.cmsdir+self.basedir+'{file}')
        res = client.fetch(qr,path=self.cmsdir+self.basedir+'{file}')

        #Move file to a file name with wavelength time included
        for k in qr:
            swave = k['wave']['wavemin']
            sfile = k['fileid'].split('/')[-1].lower() #

            shutil.move(self.cmsdir+self.basedir+sfile,self.cmsdir+self.basedir+sfile.replace('.fts','_'+swave+'.fits'))


#Download EUV images
    def get_euv(self):
        if self.dttime >= self.sdo_start:
            #self.get_aia()
            self.get_aia_syn()
            #include get stereo on recent observaitons J. Prchlik (2018/01/18)
            self.get_stereo_vso()
        else:
            self.get_stereo_vso()



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
        #prov = vso.attrs.Provider('SDAC')
        #query vso
        #qr = client.query(time,ins,prov)
        qr = client.search(time,ins)#,prov)
        self.qr = qr
       

        #res = client.get(qr,path=self.cmsdir+self.basedir+'{file}').wait()
        res = client.fetch(qr,path=self.cmsdir+self.basedir+'{file}').wait()

#Move file to a file name with start time included
        for k in qr:
            stime = k['time']['start']
            stime = stime[:8]+'_'+stime[8:]
            sfile = k['fileid'].split('/')[-1].lower().replace('.','_').replace('_fits','.fits')

            shutil.move(self.cmsdir+self.basedir+sfile,self.cmsdir+self.basedir+stime+'_'+sfile)

    #Get AIA 1024x1024  synoptics from Stanford, since CMS2 cannot handle 4096x4096 files
    def get_hmi(self):
        import urllib

        #hmi archive location
        hmi_arch = 'http://jsoc.stanford.edu/data/hmi/fits/'

        #check if current minute is even, since synoptics are every 2 minutes
        if self.dttime.minute == 0:
            inp_time = self.dttime
        #otherwise add 1 minute to current time
        else:
            inp_time = self.dttime+timedelta(minutes=60)

        #reduced time to 12 seconds for AIA observation download J. Prchlik 2018/01/24
        dt = timedelta(minutes=60)
        start = inp_time-dt
        end   = inp_time

        #create full file path hmi
        f_dir = '{0:%Y/%m/%d/hmi.M_720s.%Y%m%d_%H0000_TAI.fits}'
        s_fil = f_dir.format(start)
        e_fil = f_dir.format(end)

        #see if files already exsist
        s_tst = os.path.isfile(self.cmsdir+self.basedir+s_fil.split('/')[-1]) == False
        e_tst = os.path.isfile(self.cmsdir+self.basedir+e_fil.split('/')[-1]) == False
     
        #download files from archive
        if s_tst: urllib.urlretrieve(hmi_arch+s_fil,self.cmsdir+self.basedir+s_fil.split('/')[-1]) 
        if e_tst: urllib.urlretrieve(hmi_arch+e_fil,self.cmsdir+self.basedir+e_fil.split('/')[-1]) 

#get hmi magnetogram
    def get_hmi_vso(self):
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
        try:
            self.get_euv()
        except:
            print('Could not retrieve EUV images')
        try:
            self.get_carrington()
        except:
            print('Could not retrieve Carrington Rotation Mag.')
        try:
           self.get_magnetogram()
        except:
            print('Could not retrieve High Resoution Mag.')

#create subdirectory tree
    def build_subtree(self):


        try:
            os.makedirs(self.cmsdir+self.basedir)
        except:
            print('Directory {0} already exists. Proceeding'.format(self.cmsdir+self.basedir))
        


