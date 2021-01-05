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

combine BiasStudies_noSyst_M${m}/M${m}_BiasStudies.root -M MultiDimFit --toysFile=BiasStudies_noSyst_M${m}_1000Toys/higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root -P r --expectSignal ${e} -t 1000 --saveSpecifiedIndex pdfindex_H4GTag_Cat0_13TeV -m 125 --cminDefaultMinimizerStrategy 0 --algo singles --saveFitResult --name _M${m}_pdfindex${p}_signal${e}_1000Toys --setParameterRanges r=-10,10
mv multidimfit_M${m}_pdfindex${p}_signal${e}_1000Toys.root BiasStudies_noSyst_M${m}_1000Toys/
mv higgsCombine_M${m}_pdfindex${p}_signal${e}_1000Toys.MultiDimFit.mH125.123456.root BiasStudies_noSyst_M${m}_1000Toys/
'''
  arguments=[]


  #mass = [60, 55, 50, 45, 40, 30, 25, 20, 15]
  #pdfindex=[0,1,2, 3]
  #expectSignal=[0,1]
  mass = [60]
  pdfindex = [0]
  expectSignal = [0]
  nToys=500
  for m in mass:
      for p in pdfindex:
          for e in expectSignal:
              arguments.append("{} {} {}".format(m,p,e))
  with open("arguments.txt", "w") as args:
     args.write("\n".join(arguments))
  with open("run_script.sh", "w") as rs:
     rs.write(script)
