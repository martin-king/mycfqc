# mycfqc

The fist step is a basic but important quality control. The header in my_qc_step1.py describes what are being checked. Needs python, grep, and ncdump to run, otherwise no other further installation is necessary. I have used the scripts specifically on our CORDEX files, which are also CF compliant. 

There is also a second script my_qc_step2.py, which is used to checked expected range values in the variable in a file. This needs also cdo. At the moment I haven't included range values specific to each type of variables. Ideally, these values for each variable can be written in in csv files. And then my_qc_step2.py carries out the checks based on what are given in the csv file. At the moment, the range being checked is hard coded in my_qc_step2.py.
