import sys, getopt
import create_model_files as cmf


def main(argv):

    inargs1 = 'ht:c:o:m:a:p:s:'
    snargs1 = inargs1[1:].split(':')

    inargs2 = ['time','cmsdir','outdir','modeltemp','axial','poloidal','start']

    helpinfo = "create_model_files_wrapper.py is a command line utility which calls the class create_model_files\n"
    helpinfo = helpinfo+"The command takes only a few arguments and if you stick to a common theme you should only have to change the time between run\n"
    helpinfo = helpinfo+"python create_model_files_wrapper.py"
    for i in range(len(inargs2)): helpinfo=helpinfo+' -'+snargs1[i]+' <--'+inargs2[i]+'>'
    helpinfo=helpinfo+'\n'

   
#Descriptive information about each keyword
    argsdes=["A string time in the format of YYYY/MM/DD HH:MM:SS",
             "The directory containing the CMS2 (default = read 'cms2_dir' file)",
             "The directory format for the sigmoid (assumes a subdirectory of cmsdir (default = YYYY/MM/DD/HHMM/)",
             "The initial model template already ran through CMS2. The model must end in 1 to work properly (default = model1)",
             "Axial Fluxes to use (Default = 1.00000e19,3.00000e19,5.00000e19,7.00000e19,9.00000e19,1.00000e20,3.00000e20,5.00000e20,7.00000e20,9.00000e20,1.00000e21,1.50000e21)",
             "Polodial Fluxes to use (Default = 1.00000E9,5.00000E9,1.00000E10,5.00000E10,1.00000E11)",
             "Index to start grid (Default = 1)"]


    for i in range(len(inargs2)): helpinfo = helpinfo+' -'+snargs1[i]+' <--'+inargs2[i]+'> : '+argsdes[i]+'\n'

    #Add user example
    helpinfo = helpinfo+"""\n Example: \n python create_model_files_wrapper.py -t "2017/12/31 23:59:00" -p "1.00000E9,5.00000E9" -a '7.00000e19,9.00000e19,1.00000e20,3.00000e20' -s 1"""

#load user values
    try:
        opts,args = getopt.getopt(argv,inargs1,inargs2)
    except getop.GetoptError:
        print(helpinfo)
        sys.exit(2)
#default for directory structure
    sigd = '%Y/%m/%d/%H%M/'
#default for the model template file (must end in a 1)
    temp = 'model1'
#default for cms2 directory
    cmsd = ''

    #list of axial and poloidal fluxes
    axi = []
    pol = []


    #index to start creating files
    start = 1


    for opt, arg in opts:
        if opt == '-h':
            print(helpinfo)
            sys.exit(0)

        elif opt in ("-t","--time"):
            time = arg
        elif opt in ("-c","--cmsdir"):
            cmsd = arg
        elif opt in ("-o","--outdir"):
            sigd = arg
        elif opt in ("-m","--modeltemp"):
            temp = arg
        elif opt in ("-a","--axial"):
            axi = arg.split(',')
        elif opt in ("-p","--poloidal"):
            pol = arg.split(',')
        elif opt in ("-s","--start"):
            start = int(arg)


    mod = cmf.create_cms2_files(time,cmsdir=cmsd,outdir=sigd,tempmodel=temp,axi=axi,pol=pol,start=start)
    mod.create_all_files()

if __name__ == "__main__":
    main(sys.argv[1:])
