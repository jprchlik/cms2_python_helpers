A script set to assist in cutting down some of the monotony associated with running CMS2 and relaxing the force free model.
The script and file list is as follows:

#create_model_files.py and create_model_files_wrapper.py
These scripts are only useful after you ran CMS2 in idl previous,
thus creating as model1 and associated files.
The create_model_files_wrapper.py command line utility calls create_model_files.py to do the heavy lifting.
You man call the wrapper by typing "python create_model_files_wrapper.py -t <--time> -c <--cmsdir> -o <--outdir> -m <--modeltemp>".
Where -t <--time> corresponds to the sigmoid observation time in "YYYY/MM/DD HH:MM:SS",
-c <--cmsdir> corresponds to the top CMS2 directory (not need if you update cmd2_dir file),
-o <--outdir> corresponds to the output directories format (default = YYYY/MM/DD/HHMM/, therefore not required),
and -m <--modeltemp> corresponds to the first model you created in CMS2, which must end in a 1 (e.g. model1, which is assumed unless -m is set).



#fff2_input_models.py and (wrapper coming soon)

#grab_sigmoid_fits_files.py and grab_sigmoid_download_wrapper.py
These two scripts in combination produce the observational file necessary to run CMS2.
grab_sigmoid_downloa_ wrapper is the command line wrapper which call grab_sigmoid_fits_fitles.
You may call grab_sigmoid_download_wrapper by typing "python grab_sigmoid_download_wrapper.py -t <--time> -c <--cmsdir> -o <--outdir>".
Where -t <--time> corresponds to the sigmoid observation time in "YYYY/MM/DD HH:MM:SS",
-c <--cmsdir> corresponds to the top CMS2 directory (not need if you update cmd2_dir file),
and -o <--outdir> corresponds to the output directories format (default = YYYY/MM/DD/HHMM/, therefore not required).
You may also avoid typing "python grab_sigmoid_fits_files.py" by creating an alias for it in your ~/.cshrc file.
For example I use the alias gsff, so I put the following line in my ~/.cshrc file:

alias gsff "/PATHTO/CMS2HELPERS/grab_sigmoid_fits_files.py"

Examples:

python grab_sigmoid_download_wrapper.py -t 2009/02/17/1144 

or using the alias

gsff -t 2009/02/17/1144



Now grab_sigmoind_fits_files works because it calls the class defined in grab_sigmoid_download_wrapper.
The defined class in grab_sigmoid_download_wrapper is download_cms_files and takes information passed by the wrapper.
If the directory structure does not exist grab_sigmoid_fits_files will create subdirectories in the CMS2 directory,
so running this script before anything else is ideal as it saves you the time of creating the subdirectories yourself.
From the date it determines the closest Carrington rotation number and downloads the Carrington map for -1,0, and +1 rotations from solis.nso.edu.
The code then unzips the file and produces an uncompressed file with the Carrington rotation number in the file name.
Then the code downloads the nearest 4 minutes (+/-2 minutes) of STEREO SECCHI observations from the VSO.
Finally, it downloads a high resolution magnetogram from either mdi (before  or hmi from the VSO.


#cms2_dir
The location of your CMS2 directory, which create_model_files.py and grab_sigmoid_fits_files.py respectively use to copy and download files.
The directory must be placed on the first line of the file with no other text.

