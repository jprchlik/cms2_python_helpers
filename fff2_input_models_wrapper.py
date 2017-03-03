import sys, getopt
import fff2_input_models as fim


def main(argv):

    inargs1 = 'ht:c:o:i:n:s:l'
    snargs1 = inargs1[1:].split(':')

    inargs2 = ['time','cmsdir','outdir','ifile',"nproc","minmod","maxmod"]

    helpinfo = "create_model_files_wrapper.py is a command line utility which calls the class create_model_files\n"
    helpinfo = helpinfo+"The command takes only a few arguments and if you stick to a common theme you should only have to change the time between run\n"
    helpinfo = helpinfo+"python create_model_files_wrapper.py"
    for i in range(len(inargs2)): helpinfo=helpinfo+' -'+snargs1[i]+' <--'+inargs2[i]+'>'
    helpinfo=helpinfo+'\n'

   
#Descriptive information about each keyword
    argsdes=["A string time in the format of YYYY/MM/DD HH:MM:SS",
             "The directory containing the CMS2 (default = read 'cms2_dir' file)",
             "The directory format for the sigmoid (assumes a subdirectory of cmsdir (default = YYYY/MM/DD/HHMM/",
             "The input file format (default = inputYYYYMMDDHHMMSS_mod)",
             "The number of processors to run on (default = 6)",
             "The first model input number to look for (default = 1)",
             "The last model input number to look for (default = 48)"
            ]


    for i in range(len(inargs2)): helpinfo = helpinfo+' -'+snargs1[i]+' <--'+inargs2[i]+'> : '+argsdes[i]+'\n'

#load user values
    try:
        opts,args = getopt.getopt(argv,inargs1,inargs2)
    except getop.GetoptError:
        print helpinfo
        sys.exit(2)

#default for cms2 directory
    cmsd = ''
#default for directory structure
    sigd = '%Y/%m/%d/%H%M/'
#default for the input model template file (must end in a 1)
    fstart = 'input%y%m%d%H%M%S_mod' 
#default number of processors
    nproc = 6
#model input number to start with
    modmin = 1
#model input number to end wtih
    modmax = 48




    for opt, arg in opts:
        if opt == '-h':
            print helpinfo

        elif opt in ("-t","--time"):
            time = arg
        elif opt in ("-c","--cmsdir"):
            cmsd = arg
        elif opt in ("-o","--outdir"):
            sigd = arg
        elif opt in ("-i","--ifile"):
            fstart = arg
        elif opt in ("-n","--nproc"):
            nproc = int(arg)
        elif opt in ("-s","--minmod"):
            minmod = int(arg)
        elif opt in ("-l","--maxmod"):
            maxmod = int(arg)

    print time
    print cmsd
    print sigd
    print fstart
    print nproc
    print modmin
    print modmax

 
    inp = fim.fff2_input_models(time,cmsdir=cmsd,mdir=sigd,fstart=fstart,nproc=nproc,modmin=modmin,modmax=modmax)
    if nproc == 1:
        inp.run_loop()
    elif nproc > 1:
        inp.run_par()
    elif nproc < 1:
        print "Number of processors used must be greater than 0"
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
