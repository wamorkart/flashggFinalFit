#!/bin/bash

year='2016 2017 2018'
# year='2016'
doSystematics='1'
var='bdt'
# mass='60'
mass='60 55 50 45 40 30 25 20 15'
NEvents='8'
type='PerYear'
# numCat='2 3 4 5'
numCat='1'
# nCat='/eos/user/t/twamorka/www/H4G_Pre_PreApp_24Nov2020/DataMix_KinWeight_M60_ANTrainingVars/BDTReweighting_50Bins_SRPlusSB_NoRequirementOnData/output_SB_bdt_cat5_minevents8_10_11_2020_Run2_0.010000_bdt.txt'
# nCat='/eos/user/t/twamorka/www/H4G_Pre_PreApp_24Nov2020/DataMix_Old_KinWeight_M60_ManyKinVars/BDTReweighting_50Bins_SRPlusSB_NoRequirementOnData/output_SB_bdt_cat5_minevents8_10_11_2020_Run2_0.010000_bdt.txt'
# mkdir ${inDir}Reduced_${NEvents}Events/
# outDir=${inDir}Reduced_${NEvents}Events/
# mkdir ${outDir}WS/
# outDirWS=${outDir}WS/
for m in ${mass};
do
  inDir='/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/'${m}'/'
  # inDir='/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_9Dec2020/dataset_PhoMVA_manyKinVars_fullRun2_datamix_old_kinWeight_dataSBScaling_m'${m}'/'
  #inDir='/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_datamix_old_kinWeight_dataSBScaling_MGPodd/'${m}'/'
  for n in ${numCat};
  do
    # nCat=${inDir}categorize_nBins_190_nCat_${n}_a1_a2MassCut.txt
    nCat=${inDir}categorize_nBins_190_nCat_${n}_v2.txt
    # nCat='/afs/cern.ch/work/t/twamorka/Scripts/forH4G/Categories_M'${m}'_'${n}'Cats.txt'
    # nCat='/afs/cern.ch/work/t/twamorka/Scripts/forH4G/Categories_'${n}'Cats.txt'
    # nCat='/eos/user/t/twamorka/www/H4G_Pre_PreApp_24Nov2020/Significance_10Dec2020/m'${m}'/output_SB_bdt_cat'${n}'_minevents8_10_12_2020_Run2_0.010000_bdt.txt'

    mkdir ${inDir}Reduced_${NEvents}Events_${n}Cats/
    outDir=${inDir}Reduced_${NEvents}Events_${n}Cats/
    mkdir ${outDir}WS_${n}Cats/
    outDirWS=${outDir}WS_${n}Cats/

       for y in ${year};
       do

         #echo 'Skimming Signal'
         #echo python reduceTrees.py --iD ${inDir} --i signal_m_${m}_${y}_even --m ${m} --s ${doSystematics} --opt signal --nCat ${nCat} --year ${y} --oD  ${outDir} --v ${var}
         #python reduceTrees.py --iD ${inDir} --i signal_m_${m}_${y}_even --m ${m} --s ${doSystematics} --opt signal --nCat ${nCat} --year ${y} --oD  ${outDir} --v ${var}

         #echo 'Skimming Data'
         #echo python reduceTrees.py --iD ${inDir} --i data_${y} --m ${m} --s ${doSystematics} --opt data --nCat ${nCat} --year ${y} --oD  ${outDir} --v ${var}
         #python reduceTrees.py --iD ${inDir} --i data_${y} --m ${m} --s ${doSystematics} --opt data --nCat ${nCat} --year ${y} --oD  ${outDir} --v ${var}

         #echo 'Make Signal WS'
         #echo python mkWS.py --iD ${outDir} --i signal_m_${m}_${y}_even_skim --opt signal --nCat ${n} --s ${doSystematics} --t ${type} --year ${y} --oD ${outDirWS}
         #python mkWS.py --iD ${outDir} --i signal_m_${m}_${y}_even_skim --opt signal --nCat ${n} --s ${doSystematics} --t ${type} --year ${y} --oD ${outDirWS}

         echo 'Make Data WS'
         echo python mkWS.py --iD ${outDir} --i data_${y}_skim --opt data --nCat ${n} --t ${type} --year ${y} --oD ${outDirWS}
         python mkWS.py --iD ${outDir} --i data_${y}_skim --opt data --nCat ${n} --t ${type} --year ${y} --oD ${outDirWS}
       done
     done
done
