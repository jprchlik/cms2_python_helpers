import sys, getopt
import create_model_files as cmf


def main(argv):

    inargs1 = 'ht:c:o:m'
    snargs1 = inargs1[1:].split(':')

    inargs2 = ['time','cmsdir','outdir','modeltemp']

    helpinfo = "create_model_files_wrapper.py is a command line utility which calls the class create_model_files\n"
    helpinfo = helpinfo+"The command takes only a few arguments and if you stick to a common theme you should only have to change the time between run\n"
    helpinfo = helpinfo+"python create_model_files_wrapper.py"
    for i in range(len(inargs2)): helpinfo=helpinfo+' -'+snargs1[i]+' <--'+inargs2[i]+'>'
    helpinfo=helpinfo+'\n'

   
#Descriptive information about each keyword
    argsdes=["A string time in the format of YYYY/MM/DD HH:MM:SS",
             "The directory containing the CMS2 (default = read 'cms2_dir' file)",
             "The directory format for the sigmoid (assumes a subdirectory of cmsdir (default = YYYY/MM/DD/HHMM/",
             "The initial model template already ran through CMS2. The model must end in 1 to work properly (default = model1)"]


    for i in range(len(inargs2)): helpinfo = helpinfo+' -'+snargs1[i]+' <--'+inargs2[i]+'> : '+argsdes[i]+'\n'

#load user values
    try:
        opts,args = getopt.getopt(argv,inargs1,inargs2)
    except getop.GetoptError:
        print helpinfo
        sys.exit(2)
#default for directory structure
    sigd = '%Y/%m/%d/%H%M/'
#default for the model template file (must end in a 1)
    temp = 'model1'
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
        elif opt in ("-m","--modeltemp"):
            temp = arg


    mod = cmf.create_cms2_files(time,cmsdir=cmsd,outdir=sigd,tempmodel=temp)
    mod.create_all_files()

if __name__ == "__main__":
    main(sys.argv[1:])
