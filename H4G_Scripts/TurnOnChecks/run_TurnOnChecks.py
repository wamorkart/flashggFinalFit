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
INPUTWSDIR=$1;
MASS=$2;
SIGNALWSDIR=$3;
BKGWSDIR=$4;
BKGEXT=$5;
OUTPUTNAME=$6;
TOYNAME=$7;
STEP=$8;

scriptDir=/afs/cern.ch/work/t/twamorka/fggfinalfit_h4g_run2/CMSSW_10_2_13/src/flashggFinalFit/Datacard
cd ${scriptDir}
eval `scramv1 ru -sh`
if [ $STEP == "Datacard_TH1" ]; then
   python ${scriptDir}/makeDatacard_DataMix.py --inputWSDir ${INPUTWSDIR} --mergeYears --mass_a ${MASS} --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018  --SignalWSDir ${SIGNALWSDIR} --BkgWSDir ${BKGWSDIR} --BkgExt ${BKGEXT} --output ${scriptDir}/${OUTPUTNAME}_TH1.txt
   text2workspace.py ${scriptDir}/${OUTPUTNAME}_TH1.txt
   combine ${scriptDir}/${OUTPUTNAME}_TH1.root -M GenerateOnly -t 1000 --setParameters r=1 --saveToys --name ${TOYNAME} -m 125 --toysNoSystematics
fi
if [ $STEP == "Datacard_Multipdf" ]; then   
   python ${scriptDir}/makeDatacard.py --inputWSDir ${INPUTWSDIR} --mergeYears --mass_a ${MASS} --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018  --SignalWSDir ${SIGNALWSDIR} --BkgWSDir ${BKGWSDIR} --BkgExt ${BKGEXT} --output ${scriptDir}/${OUTPUTNAME}.txt
   text2workspace.py ${scriptDir}/${OUTPUTNAME}.txt
fi
if [ $STEP == "Datacard_Fit" ]; then 
   combine ${scriptDir}/${OUTPUTNAME}.root -M MultiDimFit --toysFile=${scriptDir}/higgsCombine${TOYNAME}.GenerateOnly.mH125.123456.root -P r --expectSignal 1 -t 1000 -m 125 --cminDefaultMinimizerStrategy 0 --algo singles  --saveFitResult --setParameterRanges r=0,10 --name ${TOYNAME}
fi

if [ $STEP == "All" ]; then 
   python ${scriptDir}/makeDatacard_DataMix.py --inputWSDir ${INPUTWSDIR} --mergeYears --mass_a ${MASS} --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018  --SignalWSDir ${SIGNALWSDIR} --BkgWSDir ${BKGWSDIR} --BkgExt ${BKGEXT} --output ${scriptDir}/${OUTPUTNAME}_TH1.txt
   text2workspace.py ${scriptDir}/${OUTPUTNAME}_TH1.txt
   combine ${scriptDir}/${OUTPUTNAME}_TH1.root -M GenerateOnly -t 1000 --setParameters r=1 --saveToys --name ${TOYNAME} -m 125 --toysNoSystematics
   python ${scriptDir}/makeDatacard.py --inputWSDir ${INPUTWSDIR} --mergeYears --mass_a ${MASS} --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018  --SignalWSDir ${SIGNALWSDIR} --BkgWSDir ${BKGWSDIR} --BkgExt ${BKGEXT} --output ${scriptDir}/${OUTPUTNAME}.txt
   text2workspace.py ${scriptDir}/${OUTPUTNAME}.txt
   #combine ${scriptDir}/${OUTPUTNAME}.root -M MultiDimFit --toysFile=${scriptDir}/higgsCombine${TOYNAME}.GenerateOnly.mH125.123456.root -P r --expectSignal 1 -t 1000 -m 125 --cminDefaultMinimizerStrategy 0 --algo singles  --saveFitResult --setParameterRanges r=0,10 --name ${TOYNAME}
fi
echo -e "DONE";
'''
  arguments=[]

  inDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/H4G_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_noCorrel/'
  SignalWSDir = 'outdir_H4G_10Mar2021_NoCorrel_M'
  BkgWSDir = 'NoCorrelTraining_DataMix_M'
  BkgExt = 'H4G_NoCorrelTraining_DataMix'
  Output = 'NoCorrel_DataMix_18Mar2021'
  mass = [15]
  step = "Datacard_Fit"
  for m in mass:
      for num in range(1,101):
          e=num*20000
          arguments.append("{} {} {} {} {} {} {} {}". format(inDir+str(m)+"/Reduced_8Events_1Cats/WS_1Cats", m, SignalWSDir+str(m), BkgWSDir+str(m)+"_"+str(e)+"_TurnOn_18Mar2021", BkgExt+"_"+str(e)+"_TurnOn", Output+"_M"+str(m)+"_"+str(e),Output+"_M"+str(m)+"_"+str(e),step ))

  with open("arguments.txt", "w") as args:
     args.write("\n".join(arguments))
  with open("run_script.sh", "w") as rs:
     rs.write(script)
