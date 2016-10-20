# mycfqc

The fist step is a basic but important quality control. In my experience, the most common errors in a file are missing data, wrong dates, or unacceptable values for the variable. It is almost a certainty that errors would exist in files without QC.

The header in my_qc_step1.py describes what are being checked. Needs python, grep, and ncdump to run, otherwise no other further installation is necessary. I have used the scripts specifically on our CORDEX files, which should be also CF compliant. Note that this is for internal use. Data submitted to ESGF from international coordinated experiments such as CMIP and CORDEX needs to pass slightly more stringent tests with the DKRZ QC Checker.

There is also a second script my_qc_step2.py, which is used to check expected range of values in the variable in a file. This needs also cdo. At the moment I haven't included range values specific to each type of variables. Ideally, these values for each variable can be written in the csv files. And then my_qc_step2.py carries out the checks based on what are given in the csv file. At the moment, the range being checked is hard coded in my_qc_step2.py. 

There are some comments given in the scripts, but no manual or documentation available at present. If you need some explanation, please ask me. Any improvement, modification or correction will be appreciated, please use pull requests on Github or communicated to/discuss with me directly. 
