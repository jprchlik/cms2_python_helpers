Python Helpers for CMS2
=======================
A script set to assist in cutting down some of the monotony associated with running CMS2 and relaxing the force free model.
These scripts support CMS2 so they cannot be ran one immediately after another, but are only broken by required user interaction in CMS2.
An example run through follows:

Download supporting observational files.
>python grab_sigmoid_download_wrapper.py -t "2009/02/17 11:44:01" 

RUN CMS2 for model1 and trace a flux rope path.

Create a set of flux ropes with different polodial and axial fluxes (also creates input files to run later,
it copies most of the information from model1)
>python create_model_files_wrapper.py -t "2009/02/17 11:44:01"

Run CMS2 on the remaining 47 models by loading the previously created model and flux rope path files 

Relax all models created defined in CMS2 using input files created in the previous python script
>python fff2_input_models_wrapper.py -t "2009/02/17 11:44:01"

NOW wait a long time for all CMS2 models to relax (may take a month).

The script and file list explanations are as follows:


create_model_files.py and create_model_files_wrapper.py
----------------
These scripts are only useful after you ran CMS2 in idl previous,
thus creating as model1 and associated files.
The create_model_files_wrapper.py command line utility calls create_model_files.py to do the heavy lifting.
You man call the wrapper by typing "python create_model_files_wrapper.py -t <--time> -c <--cmsdir> -o <--outdir> -m <--modeltemp>".
Where -t <--time> corresponds to the sigmoid observation time in "YYYY/MM/DD HH:MM:SS",
-c <--cmsdir> corresponds to the top CMS2 directory (not need if you update cms2_dir file),
-o <--outdir> corresponds to the output directories format (default = YYYY/MM/DD/HHMM/, therefore not required),
and -m <--modeltemp> corresponds to the first model you created in CMS2, which must end in a 1 (e.g. model1, which is assumed unless -m is set).
You may avoid typing "python create_model_files_wrapper.py" by creating an alias for the utility in your ~/.cshrc file.
For example you could use the alias cmfw, so I put the following line in my ~/.cshrc file.

alias cmfw "/PATHTO/CMS2HELPERS/create_model_files_wrapper.py"

Examples:

>python create_model_files_wrapper.py -t "2009/02/17 11:44:01"

or using the alias

>cmfw -t "2009/02/17 11:44:01"

create_model_files_wrapper works by calling the class create_cms2_files in create_model_files.py.
The first task which uses the create_cms2_files is modelXX_setup file for all 47 models 
(1 addition model comes from the first run through making a total of 48 models).
The setup files are the same for all models and primarily define the nearest high resolution and Carrington rotation magnetograms.
Therefore, the code copies the initial setup file but changes the name to the corresponding model.
Next, the code creates a set of "path" files for each model.
The path file corresponds to previously traced flux rope,
but the code changes the values for the axial and poloidal flux.
CMS2 will ask for this when recomputing a new flux model.
Finally, the code produces an "input" file.
The input file is used by fff2.90 code to generate a series of relaxed force free models for each poloidal and axial flux.



fff2_input_models.py and fff2_input_models_wrapper.py
----------------
fff2_input_models relaxes the different axial and poloidal models created in CMS2.
Therefore, it is only useful after you ran models through CMS2.
The code preforms the task in parallel using multiprocessing Pool and creating new c-shell or just loops through the models if the users prefers that.
All user specification are callable through the wrapper for this program fff2_input_models_wrapper.py.
Running the wrapper requires you run "python fff2_input_models_wrapper.py -t <--time> -c <--cmsdir> -o <--outdir> -i <--ifile> -n <--nproc> -s <--minmod> -l <--maxmod>"
. Where -t <--time> corresponds to the sigmoid observation time in "YYYY/MM/DD HH:MM:SS",
-c <--cmsdir> corresponds to the top CMS2 directory (not need if you update the cms2_dir file), 
-o <--outdir> corresponds to the directory where the input files were output (default = YYYY/MM/DD/HHMM/, therefore not required),
-i <--ifile> corresponds to the start of the input files format which to pass to fff2 (default = inputYYYYMMDDHHMMSS_mod, therefore not required),
-n <--nproc> corresponds to the number of processors to run the fff2 FORTRAN program (default = 6),
-s <--minmod> corresponds to the first model you would like to relax with fff2 (default = 1),
and
-l <--maxmod> corresponds to the last model you would like fff2 to relax (default = 48). 
You may avoid typing "python fff2_input_models_wrapper.py" by creating an alias for the utility in your ~/.cshrc file.
For example you could use the alias cmfw, so I put the following line in my ~/.cshrc file.


alias fimw "/PATHTO/CMS2HELPERS/fff2_input_models_wrapper.py"

Examples:

>python fff2_input_models_wrapper.py -t "2009/02/17 11:44:01"

or using the alias

>fimw -t "2009/02/17 11:44:01"


grab_sigmoid_fits_files.py and grab_sigmoid_download_wrapper.py
----------------
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

>python grab_sigmoid_download_wrapper.py -t "2009/02/17 11:44:01" 

or using the alias

>gsff -t "2009/02/17 11:44:01"



Now grab_sigmoind_fits_files works because it calls the class defined in grab_sigmoid_download_wrapper.
The defined class in grab_sigmoid_download_wrapper is download_cms_files and takes information passed by the wrapper.
If the directory structure does not exist grab_sigmoid_fits_files will create subdirectories in the CMS2 directory,
so running this script before anything else is ideal as it saves you the time of creating the subdirectories yourself.
From the date it determines the closest Carrington rotation number and downloads the Carrington map for -1,0, and +1 rotations from solis.nso.edu.
The code then unzips the file and produces an uncompressed file with the Carrington rotation number in the file name.
Then the code downloads the nearest 4 minutes (+/-2 minutes) of STEREO SECCHI observations from the VSO.
Finally, it downloads a high resolution magnetogram from either mdi (before  or hmi from the VSO.


cms2_dir
----------------
The location of your CMS2 directory, which create_model_files.py and grab_sigmoid_fits_files.py respectively use to copy and download files.
The directory must be placed on the first line of the file with no other text.

