import sys, getopt
import grab_sigmoid_fits_files as gsff



def main(argv):

    inargs1 = 'ht:c:o:x:y:'
    snargs1 = inargs1[1:].split(':')

    inargs2 = ['time','cmsdir','outdir','xval','yval']

    helpinfo = "grab_sigmoid_download_wrapper.py is a command line utility which calls the class download_cms_files\n"
    helpinfo = helpinfo+"The command takes only a few arguments and if you stick to a common theme you should only have to change the time between run\n"
    helpinfo = helpinfo+"python grab_sigmoid_download_wrapper.py"
    for i in range(len(inargs2)): helpinfo=helpinfo+' -'+snargs1[i]+' <--'+inargs2[i]+'>'
    helpinfo=helpinfo+'\n'

#Descriptive information about each keyword
    argsdes=["A string time in the format of YYYY/MM/DD HH:MM:SS",
             "The directory containing the CMS2 (default= read 'cms2_dir' file",
             "The directory format for the sigmoid (assumes a subdirectory of cmsdir (default = YYYY/MM/DD/HHMM/)",
             "The x-value of the active region at the give time in arcsec",
             "The y-value of the active region at the give time in arcsec"]
          

    for i in range(len(inargs2)): helpinfo = helpinfo+' -'+snargs1[i]+' <--'+inargs2[i]+'> : '+argsdes[i]+'\n'


    #Usage Example
    helpinfo = helpinfo+'\n Example: python grab_sigmoid_download_wrapper.py -t "2008/01/12 00:00:00"'

#load user values
    try:
        opts,args = getopt.getopt(argv,inargs1,inargs2)
    except getop.GetoptError:
        print(helpinfo)
        sys.exit(2)
#default for directory structure
    sigd = '%Y/%m/%d/%H%M/'
#default for cms2 directory
    cmsd = ''

    #default for xval
    xval = None
    #default for yval
    yval = None


    for opt, arg in opts:
        if opt == '-h':
            print(helpinfo)
            sys.exit(2)

        elif opt in ("-t","--time"):
            time = arg
        elif opt in ("-c","--cmsdir"):
            cmsd = arg
        elif opt in ("-o","--outdir"):
            sigd = arg
        elif opt in ("-x","--xval"):
            xval = float(arg)
        elif opt in ("-y","--yval"):
            yval = float(arg)


    mod =gsff.download_cms_files(time=time,cmsdir=cmsd,outdir=sigd,x=xval,y=yval)
    mod.build_subtree()
    mod.download_all()
        

if __name__ == "__main__":
    main(sys.argv[1:])
