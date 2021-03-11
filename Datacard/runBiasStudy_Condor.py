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

m=$1;
p=$2;
e=$3;
r_min=$4;
r_max=$5;

nToys=2000;
BiasStudyDir=BiasStudy_10Mar2021_Parametrized_FullMassRange_M${m}_${nToys}Toys
Datacard=Datacard_10Mar2021_M${m}_Parametrized.txt
cd /afs/cern.ch/work/t/twamorka/fggfinalfit_h4g_run2/CMSSW_10_2_13/src/flashggFinalFit/Datacard/
eval `scramv1 ru -sh`
text2workspace.py  ${Datacard} -o ${BiasStudyDir}/M${m}.root
cd ${BiasStudyDir}/
combine M${m}.root -M GenerateOnly  -t ${nToys} --setParameters pdfindex_H4GTag_Cat0_13TeV=${p},r=${e} --saveToys --name _M${m}_Cat0_13TeV_pdfindex${p}_signal${e} -m 125 --toysNoSystematics
combine M${m}.root -M MultiDimFit --toysFile=higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root -P r -t ${nToys} -m 125 --cminDefaultMinimizerStrategy 0 --algo singles --saveFitResult --name _M${m}_pdfindex${p}_signal${e}_${nToys}Toys_rmin${r_min}_rmax${r_max}_Envelope --setParameterRanges r=${r_min},${r_max} --setParameters r=${e}

'''
  arguments=[]

  mass = [60,55,50,45,40,35,30,25,20,15]
  pdfindex=[0,1,2,3]

  r_min = -2
  r_max = 10
  for m in mass:
      if (m==60): expectSignal=["0.2"]
      elif (m==55): expectSignal=["0.4"]
      elif (m==50): expectSignal=["0.7"]
      elif (m==45): expectSignal=["0.8"]
      elif (m==40): expectSignal=["0.6"]
      elif (m==30): expectSignal=["0.9"]
      elif (m==25): expectSignal=["1.0"]
      elif (m==20): expectSignal=["0.8"]
      elif (m==15): expectSignal=["1.0"]
      for p in pdfindex:
          for e in expectSignal:
              arguments.append("{} {} {} {} {}".format(m,p,e,r_min,r_max))
  with open("arguments.txt", "w") as args:
     args.write("\n".join(arguments))
  with open("run_script.sh", "w") as rs:
     rs.write(script)
