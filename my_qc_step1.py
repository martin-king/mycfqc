#Created by martin.king@uni.no, 9 Nov 2013.
#Foreign file or missing meta data (meta data field too) would cause the script to crash
#because I have not coded in checking (non)existence of variables.
#Currently the set-ups below are to check CORDEX files.
#This script also needs the cordex_variables_metadata.csv file.
#The script also needs ncdump, grep
#------
#This script does the following checks:
#check filenames
#check file format
#check global attributes
#check time meta data
#check rlat and rlon meta data
#check lat and lon meta data
#check time_bnds meta data
#check rotated_pole meta data
#check dimensions (rlon, rlat, time, timestamps)
#check variable meta data
#which are commented similarly in sections below.

import glob, os, datetime

#mpk for norstore os.system('module load netcdf')

timemean=['day','mon','sem']

#This is the big loop
for tm in timemean:
#PERHAPS THE ONLY LINE YOU NEED TO CHANGE
 filelist=sorted(glob.glob('EUR-44/BCCR/*/evaluation/r1i1p1/BCCR-WRF331C/v1/'+tm+'/*/v20160817/*'))

#check filenames
#REF filelist=sorted(glob.glob('EUR-44/BCCR/ECMWF-ERAINT/evaluation/r1i1p1/BCCR-WRF331C/v1/day/tas/v20160817/*'))
#REF hus850_EAS-44_ECMWF-ERAINT_evaluation_r1i1p1_BCCR-WRF331_v1_day_19890101-19901231.nc
 print 'Checking filenames'
 for file in filelist:
  names=file.split('/')
  filename_in=names[10]
  filename_in=filename_in.split('_')
  if filename_in[0] != names[8]:
   print 'WARNING for filename of file: '+file
  if filename_in[1] != names[0]:
   print 'WARNING for filename of file: '+file
  i=2
  for fn in filename_in[2:8]:
   if fn != names[i]:
     print 'WARNING for filename of file: '+file
   i=i+1
 print '---DONE---'

#check file format
 print 'Checking file format'
 for file in filelist:
  os.system('ncdump -k '+file+' > file_format.txt')
  line_in=os.popen('head -1 file_format.txt').read()
  if line_in != 'netCDF-4 classic model\n':
   print 'WARNING for file format for: '+file
 print '---DONE---'
 
 #check global attributes 
 atts=['CORDEX_domain', 'institute_id', 'driving_model_id', 'experiment_id', 'driving_experiment_name',
      'driving_model_ensemble_member', 'model_id', 'rcm_version_id', 'frequency', 'driving_experiment',
      'project_id'
     ]
 print 'Checking global attributes'
 for file in filelist:
  names=file.split('/')
  names_in=[names[0], names[1], names[2], names[3], names[3], names[4], names[5], names[6], names[7],
           names[2]+', '+names[3]+', '+names[4], 'CORDEX'
          ]
#  print 'Checking global attributes in file: '+file
  os.system('ncdump -h '+file+' | grep -A 20 global > glob_atts.txt')
  i=0
  for att in atts:
   line_in=os.popen('grep ":'+att+' " glob_atts.txt').read()
   att_in=line_in.split('"')
   if att_in[1] != names_in[i]:
     print 'WARNING for global attribute: "'+att+'" error in file '+file
   i=i+1
 print '---DONE---'
 
 #check time meta data
 timevars=['standard_name', 'long_name', 'units', 'calendar', 'bounds', 'axis']
 timevals=['time', 'time', 'days since 1949-12-01 00:00:00', 'standard', 'time_bnds', 'T']
 print 'Checking time meta data'
 for file in filelist:
#  print 'Checking time meta data in file: '+file
  os.system('ncdump -h '+file+' | grep -A 6 "double time(time)" > time_att.txt')
  i=0
  for timevar in timevars:
    line_in=os.popen('grep time:'+timevar+' time_att.txt').read()
    att_in=line_in.split('"')
    if att_in[1] != timevals[i]:
     print 'WARNING for time attribute: "'+timevar+'" error in file '+file
    i=i+1
 print '---DONE---'
 
 #check rlat and rlon meta data
 rlatvars=['standard_name', 'long_name', 'units', 'axis']
 rlatvals=['grid_latitude', 'latitude in rotated pole grid', 'degrees', 'Y']
 rlonvals=['grid_longitude', 'longitude in rotated pole grid', 'degrees', 'X']
 print 'Checking rlat and rlon meta data'
 for file in filelist:
#  print 'Checking rlat and rlon meta data in file: '+file
  os.system('ncdump -h '+file+' | grep -A 4 "double rlat(rlat)" > rlat_att.txt')
  os.system('ncdump -h '+file+' | grep -A 4 "double rlon(rlon)" > rlon_att.txt')
  i=0
  for rlatvar in rlatvars:
   line_in=os.popen('grep rlat:'+rlatvar+' rlat_att.txt').read()
   att_in=line_in.split('"')
   if att_in[1] != rlatvals[i]:
      print 'WARNING for rlat attribute: "'+rlatvar+'" error in file '+file
   line_in=os.popen('grep rlon:'+rlatvar+' rlon_att.txt').read()
   att_in=line_in.split('"')
   if att_in[1] != rlonvals[i]:
      print 'WARNING for rlon attribute: "'+rlatvar+'" error in file '+file
   i=i+1
 print '---DONE---'
 
 #check lat and lon meta data
 latvars=['standard_name', 'long_name', 'units', 'coordinates', 'bounds']
 latvals=['latitude', 'latitude', 'degrees_north', 'lon lat', 'lat_bnds']
 lonvals=['longitude', 'longitude', 'degrees_east', 'lon lat', 'lon_bnds']
 print 'Checking lat and lon meta data'
 for file in filelist:
#  print 'Checking lat and lon meta data in file: '+file
  os.system('ncdump -h '+file+' | grep -A 5 "double lat(rlat, rlon)" > lat_att.txt')
  os.system('ncdump -h '+file+' | grep -A 5 "double lon(rlat, rlon)" > lon_att.txt')
  i=0
  for latvar in latvars:
   line_in=os.popen('grep lat:'+latvar+' lat_att.txt').read()
   att_in=line_in.split('"')
   if att_in[1] != latvals[i]:
      print 'WARNING for lat attribute: "'+latvar+'" error in file '+file
   line_in=os.popen('grep lon:'+latvar+' lon_att.txt').read()
   att_in=line_in.split('"')
   if att_in[1] != lonvals[i]:
      print 'WARNING for lon attribute: "'+latvar+'" error in file '+file
   i=i+1
 print '---DONE---'
 
 #check time_bnds meta data
 timebndsvars=['standard_name', 'long_name', 'coordinates', 'units']
 timebndsvals=['time bounds', 'time bounds', 'time bnds', 'days since 1949-12-01 00:00:00']
 print 'Checking time_bnds meta data'
 for file in filelist:
#  print 'Checking time_bnds meta data in file: '+file
  os.system('ncdump -h '+file+' | grep -A 4 "double time_bnds(time, bnds)" > timebnds_att.txt')
  i=0
  for timebndsvar in timebndsvars:
   line_in=os.popen('grep time_bnds:'+timebndsvar+' timebnds_att.txt').read()
   att_in=line_in.split('"')
   if att_in[1] != timebndsvals[i]:
      print 'WARNING for time_bnds attribute: "'+timebndsvar+'" error in file '+file
   i=i+1
 print '---DONE---'
 
 #check rotated_pole meta data
 rotatedpolevars=['grid_mapping_name', 'grid_north_pole_latitude', 'grid_north_pole_longitude']
 if names[0]=='EAS-44':
  rotatedpolevals=['"rotated_latitude_longitude" ;\n', '77.61f ;\n', '-64.78f ;\n']
 elif names[0]=='EUR-44':
  rotatedpolevals=['"rotated_latitude_longitude" ;\n', '39.25f ;\n', '-162.f ;\n']
 elif names[0]=='AFR-44':
  rotatedpolevals=['"rotated_latitude_longitude" ;\n', '90.f ;\n', '-180.f ;\n']
 print 'Checking rotated_pole meta data'
 for file in filelist:
#  print 'Checking rotated_pole meta data in file: '+file
  os.system('ncdump -h '+file+' | grep -A 3 "char rotated_pole" > rotatedpole_att.txt')
  i=0
  for rotatedpolevar in rotatedpolevars:
   line_in=os.popen('grep rotated_pole:'+rotatedpolevar+' rotatedpole_att.txt').read()
   att_in=line_in.split('= ')
   if att_in[1] != rotatedpolevals[i]:
      print 'WARNING for rotated_pole attribute: "'+rotatedpolevar+'" error in file '+file
   i=i+1
 print '---DONE---'
 
 #check dimensions: BEGIN
 dimensionsvars=['rlon', 'rlat']
 if names[0]=='EAS-44':
  dimensionsvals=['203 ;\n', '167 ;\n']
 elif names[0]=='EUR-44':
  dimensionsvals=['106 ;\n', '103 ;\n']
 elif names[0]=='AFR-44':
  dimensionsvals=['194 ;\n', '201 ;\n']
 print 'Checking dimensions'
 for file in filelist:
  names=file.split('/')
#  print 'Checking dimensions in file: '+file
  os.system('ncdump -h '+file+' | grep -A 6 "dimensions:" > dimensions_att.txt')
  i=0
#check rlon, rlat dimensions
  for dimensionsvar in dimensionsvars:
   line_in=os.popen('grep '+dimensionsvar+' dimensions_att.txt').read()
   att_in=line_in.split('= ')
   if att_in[1] != dimensionsvals[i]:
      print 'WARNING for dimension: "'+dimensionsvar+'" error in file '+file
   i=i+1
#check time 
  if tm=='day':
    filename=names[10].split('_day_')
    timerange=filename[1]
    yearstart=int(timerange[0:4])
    monthstart=int(timerange[4:6])
    daystart=int(timerange[6:8])
    yearend=int(timerange[9:13])
    monthend=int(timerange[13:15])
    dayend=int(timerange[15:17])
    daynumbers=(datetime.date(yearend,monthend,dayend)-datetime.date(yearstart,monthstart,daystart)).days+1
#check timesteps number
    line_in=os.popen('grep "time =" dimensions_att.txt').read()
    att_in=line_in.split(' ')
    att_in=att_in[5]
    att_in=int(att_in[1:5])
    daynumbers_in=att_in
    if att_in != daynumbers:
      print 'WARNING for inconsistency in timesteps number in file: '+file
#check timestamps
    line_in=os.popen('ncdump -v time '+file+' | grep " time =" -A 1000').read()
    att_in=line_in.split(' = ')
    att_in=att_in[1].split(', ')
    dd1=(datetime.date(yearstart,monthstart,daystart)-datetime.date(1949,12,1)).days
    timed=dd1+0.5
    day=0
    escape=0
    while day < daynumbers_in-1:  #check all but last one
     if (float(att_in[day]) != timed) and (escape==0):  #only warn once  
      date=datetime.date(1949,12,1)+datetime.timedelta(days=timed)
      print 'WARNING for possible timestamp error in file: '+file+' on '+str(date)+' '+str(timed)
      escape=1
     timed=timed+1
     day=day+1
#     
  if tm=='mon':
    filename=names[10].split('_mon_')
    timerange=filename[1]
    yearstart=int(timerange[0:4])
    monthstart=int(timerange[4:6])
    daystart=1
    yearend=int(timerange[7:11])
    monthend=int(timerange[11:13])
    dayend=1
    d1=datetime.date(yearstart,monthstart,daystart)
    d2=datetime.date(yearend,monthend,dayend)
    monthnumbers=(d2.year-d1.year)*12+d2.month-d1.month+1
#check timesteps number
    line_in=os.popen('grep "time =" dimensions_att.txt').read()
    att_in=line_in.split(' ')
    att_in=att_in[5]
    att_in=int(att_in[1:5])
    if att_in != monthnumbers:
      print 'WARNING for inconsistency in timesteps number in file: '+file
#check timestamps
    line_in=os.popen('ncdump -v time '+file+' | grep " time =" -A 1000').read()
    att_in=line_in.split(' = ')
    att_in=att_in[1].split(', ')
    year=yearstart
    month=monthstart
    imonth=0
    while year <= yearend:
     if year != yearstart:
      month = 1
     while (month <= 12) and (imonth<=monthnumbers-2) :  #check all but last one
       dd1=(datetime.date(year,month,1)-datetime.date(1949,12,1)).days
       monthp=month+1
       if month == 12:
        daysinthismonth=31
       else:
        daysinthismonth=(datetime.date(year,monthp,1)-datetime.date(year,month,1)).days
       dd2=(datetime.date(year,month,daysinthismonth)-datetime.date(1949,12,1)).days + 1
       timed=(dd1+dd2)/2.0
       if float(att_in[imonth]) != timed:
         date=datetime.date(1949,12,1)+datetime.timedelta(days=timed)
         print 'WARNING for possible timestamp error in file'+file+' on '+str(date)+' '+str(timed)
       imonth=imonth+1
       month=month+1
     year=year+1
#
  if tm == 'sem':
    filename=names[10].split('_sem_')
    timerange=filename[1]
    yearstart=int(timerange[0:4])
    monthstart=int(timerange[4:6])
    daystart=1
    yearend=int(timerange[7:11])
    monthend=int(timerange[11:13])
    dayend=1
    d1=datetime.date(yearstart,monthstart,daystart)
    d2=datetime.date(yearend,monthend,dayend)
    monthnumbers=(d2.year-d1.year)*12+d2.month-d1.month+1
    seasonnumbers=monthnumbers/3.
#check timesteps number
    line_in=os.popen('grep "time =" dimensions_att.txt').read()
    att_in=line_in.split(' ')
    att_in=att_in[5]
    att_in=int(att_in[1:5])
    if att_in != seasonnumbers:
      print 'WARNING for inconsistency in timesteps number in file: '+file
 print '---DONE---'
#check dimensions: END

#check variable meta data   
 print 'Checking variable meta data'
 line_in=os.popen('grep var cordex_variables_metadata.csv').read()
 att_vars=line_in.split(', ')
 leng=len(att_vars)
 for file in filelist:
  names=file.split('/')
  varname=names[8]
  os.system('ncdump -h '+file+' | grep -A 10 "float '+varname+'" > var_att.txt')
#REF ua850, eastward_wind, Eastward Wind, m s-1, lon lat, time:mean, 1.e+20f, 1.e+20f 
#REF var, standard_name, long_name, units, coordinates, cell_methods, missing_values, _FillValue  
  line_in=os.popen('grep '+varname+', cordex_variables_metadata.csv').read()
  att_vals=line_in.split(', ')  #att_vals read from the csv file matches att_vars read from the csv file element by element
  i=1
  for att_var in att_vars[1:leng-1]:
    line_in=os.popen('grep '+varname+':'+att_var+' var_att.txt').read()
    att_val_in=line_in.split(' = ')
    if (att_val_in[1] != '"'+att_vals[i]+'" ;\n'):
     print 'WARNING for variable '+att_var+' in file: '+file
    i=i+1
  line_in=os.popen('grep missing_value var_att.txt').read()
  att_val_in=line_in.split(' = ')
  if (att_val_in[1] != '1.e+20f ;\n'):
   print 'WARNING for variable missing_value in file: '+file
  line_in=os.popen('grep FillValue var_att.txt').read()
  att_val_in=line_in.split(' = ')
  if (att_val_in[1] != '1.e+20f ;\n'):
   print 'WARNING for variable _FillValue in file: '+file
 print '---DONE---'

