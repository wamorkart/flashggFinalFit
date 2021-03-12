#!/usr/bin/python
import numpy as n
from ROOT import *
import sys, getopt
from array import array
import itertools
from optparse import OptionParser
import operator
import os



if __name__ == '__main__':



  inputDir = os.getcwd()
  if not os.path.isdir('error'): os.mkdir('error')
  if not os.path.isdir('output'): os.mkdir('output')
  if not os.path.isdir('log'): os.mkdir('log')


  condor = '''executable              = run_script.sh
output                  = output/strips.$(ClusterId).$(ProcId).out
error                   = error/strips.$(ClusterId).$(ProcId).err
log                     = log/strips.$(ClusterId).log
transfer_input_files    = run_script.sh
on_exit_remove          = (ExitBySignal == False) && (ExitCode == 0)
periodic_release        = (NumJobStarts < 3) && ((CurrentTime - EnteredCurrentStatus) > (60*60))
+JobFlavour             = "workday"
+AccountingGroup        = "group_u_CMS.CAF.ALCA"
queue arguments from arguments.txt
'''

  with open("condor_job.txt", "w") as cnd_out:
     cnd_out.write(condor)

  outputDir = os.getcwd()

  script = '''#!/bin/sh -e
LOCAL=$1;
INDIR=$2;
OUTDIR=$3;
MASS=$4;
YEAR=$5;
EVENT_NUM=$6;
BDTSEL=$7;

python ${LOCAL}/skimDataMix.py ${INDIR} ${OUTDIR} ${MASS} ${YEAR} ${EVENT_NUM} ${BDTSEL}
echo -e "DONE";
'''
  arguments=[]

  inDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/Parametrized_NoCorrel_FullMassRange/'
  outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/Parametrized_NoCorrel_FullMassRange/'
  year = [2016, 2017, 2018]
  mass = {"60":0.9875, "55":0.97625, "50":0.95875, "45":0.9525, "40":0.945, "35":0.93125,"30":0.8975, "25":0.87625, "20":0.89125,"15":0.88375}

  for m in mass:
      # print m, mass[m]
      for y in year:
          for num in range(1,101):
             e=num*20000
             arguments.append("{} {} {} {} {} {} {}". format(inputDir, inDir, outDir, m, y, e, mass[m]  ))

  with open("arguments.txt", "w") as args:
     args.write("\n".join(arguments))
  with open("run_script.sh", "w") as rs:
     rs.write(script)
