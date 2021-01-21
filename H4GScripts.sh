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
mass='55 50 45 40 30 25 20 15'
# mass='60'
# year='2016'
year='2016 2017 2018'
pdfindex='0 1 2 3'
expectSignal='0.3'
nToys='2000'
#rmin='2'
# year='2017'
##--Signal
if [ $step == "signal" ]; then
    cd Signal
    for m in ${mass};
    do
      for y in ${year};
      do
        echo 'Mass ='  ${m} ' Year =' ${y}
        echo python RunSignalScripts.py --inputConfig config_H4G.py --year ${y} --mass_a ${m}
        python RunSignalScripts.py --inputConfig config_H4G.py --year ${y} --mass_a ${m}

      done
    done

    cd ..
fi
#-- Background
if [ $step == "background" ]; then
    cd Background
    for m in ${mass};
    do
      echo python RunBackgroundScripts.py --inputConfig config_H4G.py  --mass_a ${m}
      python RunBackgroundScripts.py --inputConfig config_H4G.py  --mass_a ${m}

    done
    cd ..
fi

#-- Datacard
if [ $step == "datacard" ]; then
    cd Datacard
    for m in ${mass};
    do
      #python makeDatacard.py --inputWSDir /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats --mergeYears --mass_a ${m} --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018  --SignalWSDir outdir_H4G_HighStat_BiasStudies_M${m} --BkgWSDir outdir_fullrun2_M${m} --output Datacard_HighStat_noSyst_M${m}_forBiasStudy.txt
      # python makeDatacard.py --inputWSDir /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats --mergeYears --mass_a ${m} --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018  --SignalWSDir outdir_H4G_HighStat_M${m} --BkgWSDir outdir_fullrun2_M${m} --output Datacard_HighStat_noSyst_M${m}.txt
      python makeDatacard.py --inputWSDir /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats --doSystematics --mergeYears --mass_a ${m} --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018 --SignalWSDir outdir_H4G_NoVtxSplitting_M${m} --BkgWSDir outdir_fullrun2_M${m} --output Datacard_18Jan2021_M${m}.txt

    done
    cd ..
fi

#-- Combine
if [ $step == "combine" ]; then
    cd Datacard
    for m in ${mass};
    do
      datacardName='Datacard_18Jan2021_M'
      echo combine ${datacardName}${m}.txt  -m 125 -M AsymptoticLimits --run=blind -n ${datacardName}${m}
      combine ${datacardName}${m}.txt  -m 125 -M AsymptoticLimits --run=blind -n ${datacardName}${m}
      # echo combine Datacard_HighStat_M${m}.txt  -m 125 -M AsymptoticLimits --run=blind -n _HighStat_withsyst_M${m}
      # combine Datacard_HighStat_M${m}.txt  -m 125 -M AsymptoticLimits --run=blind -n _HighStat_withsyst_M${m}

      # echo combine Datacard_HighStat_noSyst_M${m}.txt  -m 125 -M AsymptoticLimits --run=blind -n _HighStat_nosyst_M${m}
      # combine Datacard_HighStat_noSyst_M${m}.txt  -m 125 -M AsymptoticLimits --run=blind -n _HighStat_nosyst_M${m}
    done
    cd ..
fi

if [ $step == "biasstudies" ]; then
    cd Datacard
    for m in ${mass};
    do
      mkdir BiasStudies_M${m}_${nToys}Toys_noSyst
      biasstudies_input=BiasStudies_M${m}_${nToys}Toys_noSyst
      inputDatacard=Datacard_NoVtxSplit_M${m}_wTheorySyst_noQCDSyst.txt
      echo text2workspace.py ${inputDatacard} -o ${biasstudies_input}/M${m}.root
      text2workspace.py ${inputDatacard} -o ${biasstudies_input}/M${m}.root
      for p in ${pdfindex};
      do
         for e in ${expectSignal};
         do
            echo combine ${biasstudies_input}/M${m}.root -M GenerateOnly  -t ${nToys} --setParameters pdfindex_H4GTag_Cat0_13TeV=${p},r=${e} --saveToys --name _M${m}_Cat0_13TeV_pdfindex${p}_signal${e} -m 125 --toysNoSystematics
            combine ${biasstudies_input}/M${m}.root -M GenerateOnly  -t ${nToys} --setParameters pdfindex_H4GTag_Cat0_13TeV=${p},r=${e} --saveToys --name _M${m}_Cat0_13TeV_pdfindex${p}_signal${e} -m 125 --toysNoSystematics
            mv higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root ${biasstudies_input}/

            #echo combine BiasStudies_noSyst_M${m}/M${m}_BiasStudies_noSyst.root -M MultiDimFit --toysFile=BiasStudies_noSyst_M${m}/higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root -P r --expectSignal ${e} -t 500 --saveSpecifiedIndex pdfindex_H4GTag_Cat0_13TeV -m 125 --cminDefaultMinimizerStrategy 0 --algo singles --saveFitResult --name _M${m}_pdfindex${p}_signal${e} --setParameterRanges r=-10,10
            #combine BiasStudies_noSyst_M${m}/M${m}_BiasStudies_noSyst.root -M MultiDimFit --toysFile=BiasStudies_noSyst_M${m}/higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root -P r --expectSignal ${e} -t 500 --saveSpecifiedIndex pdfindex_H4GTag_Cat0_13TeV -m 125 --cminDefaultMinimizerStrategy 0 --algo singles --saveFitResult --name _M${m}_pdfindex${p}_signal${e} --setParameterRanges r=-10,10
            #mv multidimfit_M${m}_pdfindex${p}_signal${e}.root BiasStudies_noSyst_M${m}/
            #mv higgsCombine_M${m}_pdfindex${p}_signal${e}.MultiDimFit.mH125.123456.root BiasStudies_noSyst_M${m}/
            #echo combine BiasStudies_noSyst_M${m}/M${m}_BiasStudies.root -M GenerateOnly --expectSignal ${e} -t ${nToys} --setParameters pdfindex_H4GTag_Cat0_13TeV=${p} --saveToys --name _M${m}_Cat0_13TeV_pdfindex${p}_signal${e} -m 125 --toysNoSystematics
            #combine BiasStudies_noSyst_M${m}/M${m}_BiasStudies.root -M GenerateOnly --expectSignal ${e} -t ${nToys} --setParameters pdfindex_H4GTag_Cat0_13TeV=${p} --saveToys --name _M${m}_Cat0_13TeV_pdfindex${p}_signal${e} -m 125 --toysNoSystematics
            #mv step3_m${m}_${e}.txt BiasStudies_noSyst_M${m}/
            #mv higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root BiasStudies_noSyst_M${m}/

            # echo combine BiasStudies_noSyst_M${m}/M${m}_BiasStudies.root -M MultiDimFit --toysFile=BiasStudies_noSyst_M${m}_${nToys}Toys/higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root -P r --expectSignal ${e} -t ${nToys} --saveSpecifiedIndex pdfindex_H4GTag_Cat0_13TeV -m 125 --cminDefaultMinimizerStrategy 0 --algo singles --saveFitResult --name _M${m}_pdfindex${p}_signal${e}_1000Toys --setParameterRanges r=-10,10
            #echo combine BiasStudies_noSyst_M${m}/M${m}_BiasStudies.root -M MultiDimFit --toysFile=BiasStudies_noSyst_M${m}/higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root -P r --expectSignal ${e} -t ${nToys} --saveSpecifiedIndex pdfindex_H4GTag_Cat0_13TeV -m 125 --cminDefaultMinimizerStrategy 0 --algo singles --saveFitResult --name _M${m}_pdfindex${p}_signal${e}_local --setParameterRanges r=-10,10
            #combine BiasStudies_noSyst_M${m}/M${m}_BiasStudies.root -M MultiDimFit --toysFile=BiasStudies_noSyst_M${m}/higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root -P r --expectSignal ${e} -t ${nToys} --saveSpecifiedIndex pdfindex_H4GTag_Cat0_13TeV -m 125 --cminDefaultMinimizerStrategy 0 --algo singles --saveFitResult --name _M${m}_pdfindex${p}_signal${e}_local --setParameterRanges r=-10,10 >& step4_m${m}_${e}_${p}.txt --toysNoSystematics

            #mv step4_m${m}_${e}_${p}.txt BiasStudies_noSyst_M${m}/
            #mv multidimfit_M${m}_pdfindex${p}_signal${e}_local.root BiasStudies_noSyst_M${m}/
            #mv higgsCombine_M${m}_pdfindex${p}_signal${e}_local.MultiDimFit.mH125.123456.root BiasStudies_noSyst_M${m}/
            # echo combine BiasStudies_noSyst_M${m}/M${m}_BiasStudies.root -M MultiDimFit --toysFile=BiasStudies_noSyst_M${m}_${nToys}Toys/higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root -P r --expectSignal ${e} -t ${nToys} --saveSpecifiedIndex pdfindex_H4GTag_Cat0_13TeV -m 125 --cminDefaultMinimizerStrategy 0 --algo singles --saveFitResult --name _M${m}_pdfindex${p}_signal${e}_${nToys}Toys --setParameterRanges r=-10,10
            # combine BiasStudies_noSyst_M${m}/M${m}_BiasStudies.root -M MultiDimFit --toysFile=BiasStudies_noSyst_M${m}_${nToys}Toys/higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root -P r --expectSignal ${e} -t ${nToys} --saveSpecifiedIndex pdfindex_H4GTag_Cat0_13TeV -m 125 --cminDefaultMinimizerStrategy 0 --algo singles --saveFitResult --name _M${m}_pdfindex${p}_signal${e}_${nToys}Toys --setParameterRanges r=-10,10
            # mv multidimfit_M${m}_pdfindex${p}_signal${e}_${nToys}Toys.root BiasStudies_noSyst_M${m}_${nToys}Toys/
            # mv higgsCombine_M${m}_pdfindex${p}_signal${e}_${nToys}Toys.MultiDimFit.mH125.123456.root BiasStudies_noSyst_M${m}_${nToys}Toys/


         done
      done
    done
    cd ..
fi
#-- Combine
# if [ $step == "combine" ]; then
#     cd Datacard
#     for m in ${mass};
#     do
#       echo combine Datacard_HighStat_M${m}_wTheorySyst.txt  -m 125 -M AsymptoticLimits --run=blind -n _HighStat_withsyst_wTheorySyst_M${m}
#       combine Datacard_HighStat_M${m}_wTheorySyst_noQCDSyst.txt  -m 125 -M AsymptoticLimits --run=blind -n _HighStat_withsyst_wTheorySyst_noQCDSyst_M${m}
#       # echo combine Datacard_HighStat_M${m}.txt  -m 125 -M AsymptoticLimits --run=blind -n _HighStat_withsyst_M${m}
#       # combine Datacard_HighStat_M${m}.txt  -m 125 -M AsymptoticLimits --run=blind -n _HighStat_withsyst_M${m}
#
#       # echo combine Datacard_HighStat_noSyst_M${m}.txt  -m 125 -M AsymptoticLimits --run=blind -n _HighStat_nosyst_M${m}
#       # combine Datacard_HighStat_noSyst_M${m}.txt  -m 125 -M AsymptoticLimits --run=blind -n _HighStat_nosyst_M${m}
#     done
#     cd ..
# fi
#-- Impact plots
if [ $step == "impacts" ]; then
    cd Datacard
    for m in ${mass};
    do
      datacardName='Datacard_18Jan2021_M'
      echo text2workspace.py ${datacardName}${m}.txt -m 125
      text2workspace.py ${datacardName}${m}.txt -m 125
      for e in ${expectSignal};
      do
        echo combineTool.py -M Impacts -d ${datacardName}${m}.root -m 125 --rMin -10 --rMax 10 --robustFit 1 --doInitialFit -t -1 --expectSignal ${e} --cminDefaultMinimizerStrategy 0
        combineTool.py -M Impacts -d ${datacardName}${m}.root -m 125 --rMin -10 --rMax 10 --robustFit 1 --doInitialFit -t -1 --expectSignal ${e} --cminDefaultMinimizerStrategy 0

        echo combineTool.py -M Impacts -d ${datacardName}${m}.root -m 125 --rMin -10 --rMax 10 --robustFit 1 --doFits -t -1 --expectSignal ${e} --cminDefaultMinimizerStrategy 0
        combineTool.py -M Impacts -d ${datacardName}${m}.root -m 125 --rMin -10 --rMax 10 --robustFit 1 --doFits -t -1 --expectSignal ${e} --cminDefaultMinimizerStrategy 0

        echo combineTool.py -M Impacts -d ${datacardName}${m}.root -m 125 -o ${datacardName}${m}.json
        combineTool.py -M Impacts -d ${datacardName}${m}.root -m 125 -o ${datacardName}${m}.json

        plotImpacts.py -i ${datacardName}${m}.json -o ${datacardName}${m}
        mv ${datacardName}${m}.pdf /eos/user/t/twamorka/www/Training_forPreApp_HighStat_oldfggfinalfit/
      done
    done

    cd ..
fi
