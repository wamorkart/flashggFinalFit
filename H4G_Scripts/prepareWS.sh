#!/bin/bash

year='2016 2017 2018'
# year='2016'
doSystematics='1'
var='bdt'
# mass='60'
mass='60 55 50 45 40 30 25 20 15'
NEvents='8'
type='PerYear'
numCat='1'

for m in ${mass};
do
  inDir='/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/'${m}'/'
  for n in ${numCat};
  do
     nCat=${inDir}categorize_nBins_190_nCat_${n}_v2.txt
     mkdir ${inDir}Reduced_${NEvents}Events_${n}Cats/
     outDir=${inDir}Reduced_${NEvents}Events_${n}Cats/
     mkdir ${outDir}WS_${n}Cats/
     outDirWS=${outDir}WS_${n}Cats/
     for y in ${year};
     do

         echo 'Skimming Signal ==> mass '${m} '==> year '${y}
         echo python reduceTrees.py --iD ${inDir} --i signal_m_${m}_${y}_even --m ${m} --s ${doSystematics} --opt signal --nCat ${nCat} --year ${y} --oD  ${outDir} --v ${var}
         python reduceTrees.py --iD ${inDir} --i signal_m_${m}_${y}_even --m ${m} --s ${doSystematics} --opt signal --nCat ${nCat} --year ${y} --oD  ${outDir} --v ${var}

         echo 'Skimming Data ==> mass '${m} '==> year '${y}
         echo python reduceTrees.py --iD ${inDir} --i data_${y} --m ${m} --s ${doSystematics} --opt data --nCat ${nCat} --year ${y} --oD  ${outDir} --v ${var}
         python reduceTrees.py --iD ${inDir} --i data_${y} --m ${m} --s ${doSystematics} --opt data --nCat ${nCat} --year ${y} --oD  ${outDir} --v ${var}

         # echo 'Make Signal WS'
         # echo python mkWS.py --iD ${outDir} --i signal_m_${m}_${y}_even_skim --opt signal --nCat ${n} --s ${doSystematics} --t ${type} --year ${y} --oD ${outDirWS}
         # python mkWS.py --iD ${outDir} --i signal_m_${m}_${y}_even_skim --opt signal --nCat ${n} --s ${doSystematics} --t ${type} --year ${y} --oD ${outDirWS}
         #
         # echo 'Make Data WS'
         # echo python mkWS.py --iD ${outDir} --i data_${y}_skim --opt data --nCat ${n} --t ${type} --year ${y} --oD ${outDirWS}
         # python mkWS.py --iD ${outDir} --i data_${y}_skim --opt data --nCat ${n} --t ${type} --year ${y} --oD ${outDirWS}
         #echo 'Make Signal WS'
         #echo python mkWS.py --iD ${outDir} --i signal_m_${m}_${y}_even_skim --opt signal  --s ${doSystematics} --t ${type} --year ${y} --oD ${outDirWS}
         #python mkWS.py --iD ${outDir} --i signal_m_${m}_${y}_even_skim --opt signal  --s ${doSystematics} --t ${type} --year ${y} --oD ${outDirWS}

         #echo 'Make Data WS'
         #echo python mkWS.py --iD ${outDir} --i data_${y}_skim --opt data  --t ${type} --year ${y} --oD ${outDirWS}
         #python mkWS.py --iD ${outDir} --i data_${y}_skim --opt data  --t ${type} --year ${y} --oD ${outDirWS}
       done
     done
done
