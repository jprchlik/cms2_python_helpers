import sys, getopt
import create_fit_plots as cfp


def main(argv):

    inargs1 = 'ht:c:o:f:l:'
    snargs1 = inargs1[1:].split(':')

    inargs2 = ['time','cmsdir','outdir','fitfile','loopfile']

    helpinfo = "create_model_files_wrapper.py is a command line utility which calls the class create_model_files\n"
    helpinfo = helpinfo+"The command takes only a few arguments and if you stick to a common theme you should only have to change the time between run\n"
    helpinfo = helpinfo+"python create_model_files_wrapper.py"
    for i in range(len(inargs2)): helpinfo=helpinfo+' -'+snargs1[i]+' <--'+inargs2[i]+'>'
    helpinfo=helpinfo+'\n'

   
#Descriptive information about each keyword
    argsdes=["A string time in the format of YYYY/MM/DD HH:MM:SS",
             "The directory containing the CMS2 (default = read 'cms2_dir' file)",
             "The directory format for the sigmoid (assumes a subdirectory of cmsdir (default = YYYY/MM/DD/HHMM/",
             "The fit file (default = fit_information.dat)",
             "The loop file (default = fit_loops.dat)"]


    for i in range(len(inargs2)): helpinfo = helpinfo+' -'+snargs1[i]+' <--'+inargs2[i]+'> : '+argsdes[i]+'\n'

#load user values
    try:
        opts,args = getopt.getopt(argv,inargs1,inargs2)
    except getop.GetoptError:
        print helpinfo
        sys.exit(2)
#default for directory structure
    sigd = '%Y/%m/%d/%H%M/'
#default for the fit file
    fitf = 'fit_information.dat'
#default for the loop file
    lpsf = 'fit_loops.dat'
#default for cms2 directory
    cmsd = ''




    for opt, arg in opts:
        if opt == '-h':
            print helpinfo

        elif opt in ("-t","--time"):
            time = arg
        elif opt in ("-c","--cmsdir"):
            cmsd = arg
        elif opt in ("-o","--outdir"):
            sigd = arg
        elif opt in ("-f","--fitfile"):
            fitf = arg
        elif opt in ("-l","--loopfile"):
            lpsf = arg


    plot = cfp.cms2_plot(time,cmsdir=cmsd,outdir=sigd,fit_file=fitf,lop_file=lpsf)
    plot.create_plots()

if __name__ == "__main__":
    main(sys.argv[1:])
