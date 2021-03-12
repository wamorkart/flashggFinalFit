#!/bin/bash

mass='60 55 50 45 40 35 30 25 20 15'
inDir='/afs/cern.ch/work/t/twamorka/fggfinalfit_h4g_run2/CMSSW_10_2_13/src/flashggFinalFit/Background'


for num in {1..100};
do
  e=$(($num*20000))
  for m in ${mass};
  do
      echo python histoFromDataset.py -i ${inDir} -e ${e} -m ${m}
      python histoFromDataset.py -i ${inDir} -e ${e} -m ${m}
  done
done  
   
