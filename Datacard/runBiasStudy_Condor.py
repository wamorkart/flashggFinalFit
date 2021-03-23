#!/usr/bin/python
import numpy as n
from ROOT import *
from root_numpy import tree2array
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
  step = "toys"
  if (step=="text2workspace"):
      script = '''#!/bin/sh -e

mass=$1;
datacard=$2;
nToys=$3;

cd /afs/cern.ch/work/t/twamorka/fggfinalfit_h4g_run2/CMSSW_10_2_13/src/flashggFinalFit/Datacard/
eval `scramv1 ru -sh`
BiasStudyDir=BiasStudy_23Mar2021_Parametrized_M${mass}_${nToys}Toys
mkdir ${BiasStudyDir}/
text2workspace.py ${datacard} -m 125 -o ${BiasStudyDir}/M${mass}.root

    '''

  else:
      script = '''#!/bin/sh -e

m=$1;
p=$2;
e=$3;
r_min=$4;
r_max=$5;
nToys=2000;

cd /afs/cern.ch/work/t/twamorka/fggfinalfit_h4g_run2/CMSSW_10_2_13/src/flashggFinalFit/Datacard/
eval `scramv1 ru -sh`
BiasStudyDir=BiasStudy_23Mar2021_Parametrized_M${m}_${nToys}Toys
cd ${BiasStudyDir}/
combine M${m}.root -M GenerateOnly  -t ${nToys} --setParameters pdfindex_H4GTag_Cat0_13TeV=${p},r=${e} --saveToys --name _M${m}_Cat0_13TeV_pdfindex${p}_signal${e} -m 125 --toysNoSystematics
combine M${m}.root -M MultiDimFit --toysFile=higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root -P r -t ${nToys} -m 125 --cminDefaultMinimizerStrategy 0 --algo singles --saveFitResult --name _M${m}_pdfindex${p}_signal${e}_${nToys}Toys_rmin${r_min}_rmax${r_max}_Envelope --setParameterRanges r=${r_min},${r_max} --setParameters r=${e}

    '''

  arguments=[]
  mass = []
  inDir = "/eos/user/t/twamorka/H4G_Limits/23March2021_ParametrizedTraining/"
  for m in range(15,61):
      mass.append(m)
  pdfindex=[0,1,2,3]
  toys=2000



  if (step=="text2workspace"):
      for m in mass:
          arguments.append("{} {} {}".format(m,"Datacard_18Mar2021_M"+str(m)+"_Parametrized_cleaned.txt",toys))

  else:
      r_min = 0
      r_max = 10
      for m in mass:
          file_in = TFile(inDir+"higgsCombineDatacard_18Mar2021_M"+str(m)+"_Parametrized_cleaned.AsymptoticLimits.mH125.root","read")
          tree_in = file_in.Get("limit")
          limit = tree2array(tree_in,branches="limit")
          # print(round(limit[2],2))
          expectSignal=[str(round(limit[2],2))]
          # print expectSignal
          for p in pdfindex:
              for e in expectSignal:
                  arguments.append("{} {} {} {} {}".format(m,p,e,r_min,r_max))
  with open("arguments.txt", "w") as args:
     args.write("\n".join(arguments))
  with open("run_script.sh", "w") as rs:
     rs.write(script)
