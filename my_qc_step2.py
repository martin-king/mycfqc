#Created by martin.king@uni.no, 21 Nov 2013.
#This script does range of data values checks
#I will write in the realistic ranges in a csv file.
#Now, the example given below checks tas to be 100<tas<400.
#Needs ncdump, grep, and cdo.

import glob, os

#os.system('module load netcdf')
#os.system('module load cdo')

timemean=['day']

for tm in timemean:
#PERPHAPS THE ONLY LINE YOU NEED TO CHANGE
  filelist=sorted(glob.glob('output/EUR-44/BCCR/*/evaluation/r1i1p1/BCCR-WRF331C/v1/'+tm+'/tas*/v20160817/*'))
#
  for file in filelist:
     names=file.split('/')
     filename_in=names[11]
     filename_in=filename_in.split('_')
     var=filename_in[0]
     print 'Checking file: '+file
     os.system('cdo -s -O fldmax '+file+' rub.nc > /dev/null 2>&1')
     line_in=os.popen('ncdump -v '+var+' rub.nc | grep -A 2000 "'+var+' ="').read()
     att_ins=line_in.split(' =\n ')
     att_ins=att_ins[1].split(',\n  ')
     leng=len(att_ins)
     for att_in in att_ins[0:leng-1]:
       if float(att_in) > 400.0:
         print 'WARNING possible out of range maximum data values in file: '+file
#
     os.system('cdo -s -O fldmin '+file+' rub.nc > /dev/null 2>&1')
     line_in=os.popen('ncdump -v '+var+' rub.nc | grep -A 2000 "'+var+' ="').read()
     att_ins=line_in.split(' =\n ')
     att_ins=att_ins[1].split(',\n  ')
     leng=len(att_ins)
     for att_in in att_ins[0:leng-1]:
       if float(att_in) < 100.0:
         print 'WARNING possible out of range minimum data values in file: '+file
#
     print '---DONE---'
