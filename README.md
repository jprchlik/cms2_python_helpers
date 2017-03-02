A script set to assist in cutting down some of the monotony associated with running CMS2 and relaxing the force free model.
The script and file list is as follows:

#create_model_files.py and create_model_files_wrapper.py


#fff2_input_models.py and (wrapper coming soon)

#grab_sigmoid_fits_files.py and grab_sigmoid_download_wrapper.py
These two scripts in combination produce the observational file necessary to run CMS2.
grab_sigmoid_downloa_ wrapper is the command line wrapper which call grab_sigmoid_fits_fitles.
You may call grab_sigmoid_download_wrapper by typing "python grab_sigmoid_fits_files.py -t <--time> -c <--cmsdir> -o <--outdir>".
Where -t <--time> corresponds to the sigmoid observation time in "YYYY/MM/DD HH:MM:SS",
-c <--cmsdir> corresponds to the top CMS2 directory (not need if you update cmd2_dir file),
and -o <--outdir> corresponds to the output directories format (default = YYYY/MM/DD/HHMM/, therefore not required).

#cms2_dir
The location of your CMS2 directory, which create_model_files.py and grab_sigmoid_fits_files.py respectively use to copy and download files.
The directory must be placed on the first line of the file with no other text.

