#!/usr/bin/python
import numpy as n
from ROOT import *
from root_numpy import tree2array
import sys, getopt
from array import array
import itertools
import argparse
import operator
import os



if __name__ == '__main__':

  parser =  argparse.ArgumentParser(description='Envelope bias study')
  parser.add_argument('-s', '--step', dest='step', default='', required=True ,type=str, help='step of bias study to be performed')
  parser.add_argument('-n', '--name', dest='name', default='', required=True ,type=str, help='extension used for name of output transfer_input_files')
  parser.add_argument('-t', '--toys', dest='toys', default='', required=False ,type=int, help='number of toys generated')
  options = parser.parse_args()

  step = options.step
  name = options.name
  toys = options.toys

  if not os.path.isdir('error'): os.mkdir('error')
  if not os.path.isdir('output'): os.mkdir('output')
  if not os.path.isdir('log'): os.mkdir('log')

  if not os.path.isdir('InputDatacards'): os.mkdir('InputDatacards')
  if not os.path.isdir('ToysDir'): os.mkdir('ToysDir')
  if not os.path.isdir('FitsDir'): os.mkdir('FitsDir')


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

  # INPUTFILE=$1;
  # MASS=$2;
  # SYSTEMATICS=$3;
  # YEAR=$4;
  # WEIGHT=$5;
  # OUTPUT=$6;
  # python /afs/cern.ch/work/t/twamorka/flashgg_16aug2020/CMSSW_10_6_8/src/flashgg/Scripts/ApplyTraining/ApplyCatBDT.py ${INPUTFILE} ${MASS} ${SYSTEMATICS} ${YEAR} ${WEIGHT} ${OUTPUT}
  with open("condor_job.txt", "w") as cnd_out:
     cnd_out.write(condor)

  currentDir = os.getcwd()
  script = '''#!/bin/sh -e

  INDIR=$1;
  STEP=$2;
  DATACARD=$3;
  NAME=$4;

  cd ${INDIR}
  eval `scramv1 ru -sh`

  if  [ $STEP == "text2workspace" ]; then
      text2workspace.py ${INDIR}/../Datacard/${DATACARD}.txt -m 125 -o InputDatacards/${NAME}.root
  fi

  if  [ $STEP == "toys" ]; then
      nToys=$5;
      p=$6;
      e=$7;
      m=$8;
      combine InputDatacards/${NAME}.root -M GenerateOnly  -t ${nToys} --setParameters pdfindex_H4GTag_Cat0_13TeV=${p},r=${e} --saveToys --name _M${m}_Cat0_13TeV_pdfindex${p}_signal${e}_${NAME} -m 125 --toysNoSystematics
      mv higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}_${NAME}.GenerateOnly.mH125.123456.root ToysDir/
  fi

  if  [ $STEP == "fits" ]; then
      nToys=$5;
      p=$6;
      e=$7;
      m=$8;
      rMin=$9;
      rMax=$10;
      combine InputDatacards/${NAME}.root -M MultiDimFit --toysFile=ToysDir/higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root -P r -t ${nToys} -m 125 --cminDefaultMinimizerStrategy 0 --algo singles  --saveFitResult --name _M${m}_Cat0_13TeV_pdfindex${p}_signal${e}_${NAME} --setParameters r=${e}  --setParameterRanges r=0,10

      # combine InputDatacards/${NAME}.root -M MultiDimFit --toysFile=ToysDir/higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root -P r -t ${nToys} -m 125 --cminDefaultMinimizerStrategy 0 --algo singles  --saveFitResult --name _M${m}_Cat0_13TeV_pdfindex${p}_signal${e} --setParameters r=${e}  --setParameterRanges r=${rMin},${rMax}
      mv higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}_${NAME}.MultiDimFit.mH125.123456.root FitsDir/
      mv multidimfit_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}_${NAME}.root FitsDir/
  fi

echo -e "DONE";
'''
  arguments=[]
  pdfindex=[0,1,2,3]
  #pdfindex=[0]
  rMin=0
  rMax=10;

  limit_file_inDir = "/eos/user/t/torimoto/H4G_Limits/H4G_Analysis_Files/Limit_RootFiles/HybridNew/"
  mass = [56,57,58,59,54,53,52,51,49,48,47,46]
  # for m in range(16,61):
  # for m in range(15,16):
  for m in mass:

      Datacard = "Datacard_9April2021_ChangeSystParams_M"+str(m)+"_noSyst"
      limit_file_in = TFile(limit_file_inDir+"/higgsCombine_M"+str(m)+"_0.5.HybridNew.mH125.root","read")
      limit_tree_in = limit_file_in.Get("limit")
      expectedlimit = float(round(tree2array(limit_tree_in,branches="limit")[0],3))
      # print expectedlimit
      inDir = os.getcwd()
      if (step=="text2workspace"):
          arguments.append("{} {} {} {}".format(inDir,step, Datacard, "M"+str(m)+"_"+name))


      elif (step=="toys"):
          for p in pdfindex:
              arguments.append("{} {} {} {} {} {} {} {}".format(inDir,step, Datacard, "M"+str(m)+"_"+name,toys,p,expectedlimit,m))

      elif (step=="fits"):
          for p in pdfindex:
              arguments.append("{} {} {} {} {} {} {} {} {} {}".format(inDir,step, Datacard, "M"+str(m)+"_"+name,toys,p,expectedlimit,m, rMin, rMax))

  with open("arguments.txt", "w") as args:
     args.write("\n".join(arguments))
  with open("run_script.sh", "w") as rs:
     rs.write(script)
