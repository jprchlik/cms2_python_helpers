import os,shutil

##########################template = 'model1_setup'
##########################for i in range(5,49):
##########################    shutil.copy(template,template.replace('1',str(i)))
##########################
##########################
##########################
##########################pathtxt = "       1       0     102\n"
##########################pathtxt = pathtxt+"      21       5       5        {0}\n"
##########################pathtxt = pathtxt+"      152.500      150.500      145.500      140.500      134.500      129.500\n"
##########################pathtxt = pathtxt+"      127.500      127.500      129.500      132.500      134.500      134.500\n"
##########################pathtxt = pathtxt+"      133.500      129.500      128.500      123.500      117.500      114.500\n"
##########################pathtxt = pathtxt+"      107.500      99.5000      93.5000\n"
##########################pathtxt = pathtxt+"     -54.5000     -46.5000     -43.5000     -40.5000     -40.5000     -43.5000\n"
##########################pathtxt = pathtxt+"     -45.5000     -49.5000     -53.5000     -55.5000     -59.5000     -61.5000\n"
##########################pathtxt = pathtxt+"     -63.5000     -66.5000     -67.5000     -69.5000     -72.5000     -73.5000\n"
##########################pathtxt = pathtxt+"     -73.5000     -72.5000     -73.5000\n"
##########################pathtxt = pathtxt+"      4.00000 -1.54518e+20  {1}\n"
##########################pathtxt = pathtxt+"      4.00000  1.23960e+19 -{1}\n"
##########################pathtxt = pathtxt+"           0"
##########################
##########################
##########################
##########################pol = ['1.000E9','5.000E9','1.000E10','5.000E10','1.000E11']
##########################axi = ['5.00000e19','7.00000e19','9.00000e19','1.00000e20','3.00000e20','5.00000e20','7.00000e20','9.00000e20','1.00000e21','1.50000e21']
##########################
##########################template = template.replace('setup','path')
##########################
##########################i = 1
##########################for p in pol:
##########################    for a in axi:
##########################        run = True
###########################remove early 7E20 models for some reason unknown to me
##########################        if ((float(p) < 9e9) & (a == '7.00000e20')): run = False 
##########################
##########################        if run:
##########################            files = open(template.replace('1',str(i)),'w')
##########################            files.write(pathtxt.format(p,a))
##########################            files.close()
##########################
##########################            i+=1
##########################
#text format for input file

modin = "2009/02/17/1144_scr/\n"
modin = modin+"11                  \n"
modin = modin+"model{0}              \n"
modin = modin+"0                   \n"
modin = modin+"100                 \n"
modin = modin+"0                   \n"
modin = modin+"0                   \n"
modin = modin+"0                   \n"
modin = modin+"model{0}              \n"
modin = modin+"100                 \n"
modin = modin+"900                 \n"
modin = modin+"0                   \n"
modin = modin+"0                   \n"
modin = modin+"0.003               \n"
modin = modin+"model{0}              \n"
modin = modin+"1000                \n"
modin = modin+"9000                \n"
modin = modin+"0                   \n"
modin = modin+"0                   \n"
modin = modin+"0.001               \n"
modin = modin+"model{0}              \n"
modin = modin+"10000               \n"
modin = modin+"10000               \n"
modin = modin+"0                   \n"
modin = modin+"0                   \n"
modin = modin+"0.0003              \n"
modin = modin+"model{0}              \n"
modin = modin+"20000               \n"
modin = modin+"10000               \n"
modin = modin+"0                   \n"
modin = modin+"0                   \n"
modin = modin+"0.0001              \n"
modin = modin+"model{0}              \n"
modin = modin+"30000               \n"
modin = modin+"10000               \n"
modin = modin+"0                   \n"
modin = modin+"0                   \n"
modin = modin+"0.0001              \n"
modin = modin+"model{0}              \n"
modin = modin+"40000               \n"
modin = modin+"10000               \n"
modin = modin+"0                   \n"
modin = modin+"0                   \n"
modin = modin+"0.0001              \n"
modin = modin+"model{0}              \n"
modin = modin+"50000               \n"
modin = modin+"10000               \n"
modin = modin+"0                   \n"
modin = modin+"0                   \n"
modin = modin+"0.0001              \n"
modin = modin+"model{0}              \n"
modin = modin+"60000               \n"
modin = modin+"10000               \n"
modin = modin+"0                   \n"
modin = modin+"0                   \n"
modin = modin+"0.0001              \n"
modin = modin+"model{0}              \n"
modin = modin+"70000               \n"
modin = modin+"10000               \n"
modin = modin+"0                   \n"
modin = modin+"0                   \n"
modin = modin+"0.0001              \n"
modin = modin+"model{0}              \n"
modin = modin+"80000               \n"
modin = modin+"10000               \n"
modin = modin+"0                   \n"
modin = modin+"0                   \n"
modin = modin+"0.0001              \n"

#create input files
for i in range(1,49):
    files = open("input090217114401_mod{0}.dat".format(str(i)),'w')
    files.write(modin.format(str(i)))


    files.close()
    
