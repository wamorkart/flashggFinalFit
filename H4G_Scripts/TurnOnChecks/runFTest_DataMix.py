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

  if not os.path.isdir('error'): os.mkdir('error')
  if not os.path.isdir('output'): os.mkdir('output')
  if not os.path.isdir('log'): os.mkdir('log')
  # Prepare condor jobs
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
INFILE=$1;
OUTMULTIPDF=$2;
OUTDIR=$3;

cd /afs/cern.ch/work/t/twamorka/fggfinalfit_h4g_run2/CMSSW_10_2_13/src/flashggFinalFit/Background/
eval `scramv1 ru -sh`
./bin/fTest -i ${INFILE} --saveMultiPdf ${OUTMULTIPDF}  -D ${OUTDIR} -f H4GTag_Cat0  --isData 1 --year all  --unblind
'''
  arguments=[]

  mass = [60,55,50,45,40,35,30,25,20,15]
  inDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/Parametrized_NoCorrel_FullMassRange/'
  outDir = '/afs/cern.ch/work/t/twamorka/fggfinalfit_h4g_run2/CMSSW_10_2_13/src/flashggFinalFit/Background/'
  for num in range(1,101):
      e=num*20000
      for m in mass:
          os.mkdir(outDir+"Parametrized_DataMix_M"+str(m)+"_"+str(e)+"_TurnOn_12Mar2021/")
          arguments.append("{} {} {}".format(inDir+str(m)+"/DataMix_Skim/data_mix_run2_"+str(e)+"_WS.root", outDir+"Parametrized_DataMix_M"+str(m)+"_"+str(e)+"_TurnOn_12Mar2021/CMS-HGG_multipdf_H4G_Parametrized_DataMix_"+str(e)+"_TurnOn_M"+str(m)+".root", outDir+"Parametrized_DataMix_M"+str(m)+"_"+str(e)+"_TurnOn_12Mar2021/bkgfTest-Data"))      

  with open("arguments.txt", "w") as args:
     args.write("\n".join(arguments))
  with open("run_script.sh", "w") as rs:
     rs.write(script)
