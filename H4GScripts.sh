#!/bin/bash
#
#########################################################################################
# The purpose of this script is to run all fggfinalfit steps for the H4G analysis    #
#                                                                                       #
# Example usage:                                                                        #
# . H4GScripts.sh background
# . H4GScripts.sh signal
#########################################################################################

step=$1
mass='60 55 50 45 40 30 25 20 15'
# mass='60'
year='2016 2017 2018'
# year='2017'
##--Signal
if [ $step == "signal" ]; then
    cd Signal
    for m in ${mass};
    do
      for y in ${year};
      do
        echo 'Mass ='  ${m} ' Year =' ${y}
        echo  python RunSignalScripts.py --inputConfig config_H4G.py --year ${y} --mass_a ${m} --mode fTest --modeOpts "--mass_a ${m} --year ${y} --doPlots --outPlot /eos/user/t/twamorka/www/Training_forPreApp_HighStat/${m} --skipWV"
        python RunSignalScripts.py --inputConfig config_H4G.py --year ${y} --mass_a ${m} --mode fTest --modeOpts "--mass_a ${m} --year ${y} --doPlots --outPlot /eos/user/t/twamorka/www/Training_forPreApp_HighStat/${m} --skipWV"

        echo python RunSignalScripts.py --inputConfig config_H4G.py --mass_a ${m} --year ${y} --mode calcPhotonSyst --modeOpts "--mass_a ${m}  --year ${y}"
        python RunSignalScripts.py --inputConfig config_H4G.py --mass_a ${m} --year ${y} --mode calcPhotonSyst --modeOpts "--mass_a ${m}  --year ${y}"

        echo python RunSignalScripts.py --inputConfig config_H4G.py --mode signalFit --mass_a ${m} --year ${y} --groupSignalFitJobsByCat --modeOpts "--analysis H4G --skipVertexScenarioSplit --useDCB --year ${y} --mass_a ${m} --massPoints 125 --doPlots --outPlot /eos/user/t/twamorka/www/Training_forPreApp_HighStat/${m}"
        python RunSignalScripts.py --inputConfig config_H4G.py --mode signalFit --mass_a ${m} --year ${y} --groupSignalFitJobsByCat --modeOpts "--analysis H4G --skipVertexScenarioSplit --useDCB --year ${y} --mass_a ${m} --massPoints 125 --doPlots --outPlot /eos/user/t/twamorka/www/Training_forPreApp_HighStat/${m}"

        echo python scripts/packageSignal.py --cat Cat0 --outputExt packaged_${y}_${m} --massPoints 125 --exts dcb_${y}_${m} --year ${y}
        python scripts/packageSignal.py --cat Cat0 --outputExt packaged_${y}_${m} --massPoints 125 --exts dcb_${y}_${m} --year ${y}

        echo python RunPlotter.py  --procs all --years ${y} --cats Cat0 --ext packaged_${y}_${m} --outPlot /eos/user/t/twamorka/www/Training_forPreApp_HighStat/${m}/ --doFWHM
        python RunPlotter.py  --procs all --years ${y} --cats Cat0 --ext packaged_${y}_${m} --outPlot /eos/user/t/twamorka/www/Training_forPreApp_HighStat/${m}/ --doFWHM

      done
    done

    cd ..
fi
#-- Background
if [ $step == "background" ]; then
    cd Background
    for m in ${mass};
    do
      echo ./bin/fTest -i /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats/allData.root --saveMultiPdf outdir_fullrun2_${m}/CMS-HGG_multipdf_H4GTag_Cat0.root  -D outdir_fullrun2_${m}/bkgfTest-Data -O /eos/user/t/twamorka/www/Training_forPreApp_HighStat/${m}/ -f H4GTag_Cat0  --isData 1 --year all --catOffset 0
      ./bin/fTest -i /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats/allData.root --saveMultiPdf outdir_fullrun2_${m}/CMS-HGG_multipdf_H4GTag_Cat0.root  -D outdir_fullrun2_${m}/bkgfTest-Data -O /eos/user/t/twamorka/www/Training_forPreApp_HighStat/${m}/ -f H4GTag_Cat0  --isData 1 --year all --catOffset 0
      #echo python RunBackgroundScripts.py --inputConfig config_H4G.py --mode fTestParallel --mass_a ${m} --outdirplot /eos/user/t/twamorka/www/Training_forPreApp_HighStat/${m}/
      #python RunBackgroundScripts.py --inputConfig config_H4G.py --mode fTestParallel --mass_a ${m} --outdirplot /eos/user/t/twamorka/www/Training_forPreApp_HighStat/${m}/
    done
    cd ..
fi

#-- Background
if [ $step == "datacard" ]; then
    cd Datacard
    for m in ${mass};
    do
      echo python RunYields.py --cats Cat0 --inputWSDir 2016=/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats,2017=/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats,2018=/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats --procs H4GTag --doSystematics --batch local --mass_a ${m} --sigModelExt packaged_${m} --bkgModelExt multipdf_H4GTag --mergeYears --sigModelWSDir ../Signal/outdir_packaged --bkgModelWSDir ../Background/outdir_fullrun2 --ext M${m}
      python RunYields.py --cats Cat0 --inputWSDir 2016=/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats,2017=/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats,2018=/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats --procs H4GTag --doSystematics --batch local --mass_a ${m} --sigModelExt packaged_${m} --bkgModelExt multipdf_H4GTag --mergeYears --sigModelWSDir ../Signal/outdir_packaged --bkgModelWSDir ../Background/outdir_fullrun2 --ext M${m}

      echo python makeDatacard.py --years 2016,2017,2018 --prune --doSystematics --ext M${m} --doTrueYield --analysis H4G --output Datacard_M${m}
      python makeDatacard.py --years 2016,2017,2018 --prune --doSystematics --ext M${m} --doTrueYield --analysis H4G --output Datacard_M${m}
    done
    cd ..
fi

#-- Combine
if [ $step == "combine" ]; then
    cd Datacard
    for m in ${mass};
    do
      echo combine Datacard_M${m}.txt  -m 125 -M AsymptoticLimits --run=blind -n _HighStat_withsyst_M${m}
      combine Datacard_M${m}.txt  -m 125 -M AsymptoticLimits --run=blind -n _HighStat_withsyst_M${m}
    done
    cd ..
fi
