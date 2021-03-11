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
mass='60 55 50 45 40 35 30 25 20 15'

year='2016 2017 2018'
# pdfindex='3'
pdfindex='0 1 2 3'
expectSignal='1'
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

#-- DataMix
if [ $step == "DataMix" ]; then
    #cd Background
    cd Datacard
    for num in {1..100};
    #for num in 1;
    do
      e=$(($num*20000))
      #echo python RunBackgroundScripts.py --inputConfig config_H4G.py  --mass_a 60 --dataMix ${e}
      #python RunBackgroundScripts.py --inputConfig config_H4G.py  --mass_a 60 --dataMix ${e}
      echo python makeDatacard.py --inputWSDir /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/Parametrized_NoCorrel_FullMassRange/60/Reduced_8Events_1Cats/WS_1Cats --mergeYears --mass_a 60 --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018 --SignalWSDir outdir_H4G_8Mar2021_Cut0p98_Parametrized_NoCorrel_DataMix_Bias_M60 --BkgWSDir outdir_H4G_8Mar2021_Cut0p98_Parametrized_NoCorrel_DataMix_Bias_M60_${e} --output Datacard_8Mar2021_Cut0p98_Parametrized_NoCorrel_${e}.txt --BkgExt H4G_8Mar2021_Cut0p98_Parametrized_NoCorrel_DataMix_Bias_ --DataMix ${e}
      python makeDatacard.py --inputWSDir /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/Parametrized_NoCorrel_FullMassRange/60/Reduced_8Events_1Cats/WS_1Cats --mergeYears --mass_a 60 --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018 --SignalWSDir outdir_H4G_8Mar2021_Cut0p98_Parametrized_NoCorrel_DataMix_Bias_M60 --BkgWSDir outdir_H4G_8Mar2021_Cut0p98_Parametrized_NoCorrel_DataMix_Bias_M60_${e} --output Datacard_8Mar2021_Cut0p98_Parametrized_NoCorrel_${e}.txt --BkgExt H4G_8Mar2021_Cut0p98_Parametrized_NoCorrel_DataMix_Bias_ --DataMix ${e}
      #python makeDatacard.py --inputWSDir /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/H4G_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_noCorrel/60/Reduced_8Events_1Cats/WS_1Cats --mergeYears --mass_a 60 --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018 --SignalWSDir outdir_H4G_2Mar2021_PerMassPoint_WithMa_NoCorrel_M60 --BkgWSDir outdir_H4G_3Mar2021_NoCorrelTraining_DataMix_M60_${e} --output Datacard_4Mar2021_DataMix_${e}_TH1.txt --BkgExt H4G_3Mar2021_NoCorrelTraining_DataMix_ --DataMix ${e}
      #echo text2workspace.py Datacard_8Mar2021_Cut0p98_Parametrized_NoCorrel_${e}_TH1.txt -m 125
      #text2workspace.py Datacard_8Mar2021_Cut0p98_Parametrized_NoCorrel_${e}_TH1.txt -m 125
      text2workspace.py Datacard_8Mar2021_Cut0p98_Parametrized_NoCorrel_${e}.txt -m 125
      #echo combine Datacard_8Mar2021_Cut0p98_Parametrized_NoCorrel_${e}_TH1.root -M GenerateOnly -t 500 --setParameters r=1 --saveToys --name _8Mar2021_Cut0p98_Parametrized_NoCorrel_${e} -m 125 --toysNoSystematics
      #combine Datacard_8Mar2021_Cut0p98_Parametrized_NoCorrel_${e}_TH1.root -M GenerateOnly -t 500 --setParameters r=1 --saveToys --name _8Mar2021_Cut0p98_Parametrized_NoCorrel_${e} -m 125 --toysNoSystematics
      #combine Datacard_4Mar2021_DataMix_${e}_TH1.root -M GenerateOnly -t 1000 --setParameters r=1 --saveToys --name _4Mar2021_${e} -m 125 --toysNoSystematics
      #echo combine Datacard_4Mar2021_DataMix_${e}.root -M MultiDimFit --toysFile=higgsCombine_4Mar2021_${e}.GenerateOnly.mH125.123456.root -P r --expectSignal 1 -t 1000 -m 125 --cminDefaultMinimizerStrategy 0 --algo singles  --saveFitResult --setParameterRanges r=0,10 --name _4Mar2021_${e}
      #combine Datacard_4Mar2021_DataMix_${e}.root -M MultiDimFit --toysFile=higgsCombine_4Mar2021_${e}.GenerateOnly.mH125.123456.root -P r --expectSignal 1 -t 1000 -m 125 --cminDefaultMinimizerStrategy 0 --algo singles  --saveFitResult --setParameterRanges r=0,10 --name _4Mar2021_${e}
    done
    cd ..
fi

#-- Datacard
if [ $step == "datacard" ]; then
    cd Datacard
    for m in ${mass};
    do
    #inputTraining='dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd'
    #inputTraining='FullRun2_AllMasses_WithoutMa'
    #SignalWSDir='outdir_H4G_20Feb2021_AllMasses_WithoutMa'
    #BkgWSDir='outdir_H4G_20Feb2021_AllMasses_WithoutMa'
    #BkgWSDir='outdir_H4G_23Jan2021'
    #outputName=Datacard_20Feb2021_M${m}_AllMasses_WithoutMa
    #BkgExt='H4G_20Feb2021_AllMasses_WithoutMa'
    inputTraining='Parametrized_NoCorrel_FullMassRange'
    SignalWSDir='outdir_H4G_10Mar2021_Parametrized'
    BkgWSDir=outdir_H4G_10Mar2021_Parametrized_M${m}
    BkgExt='H4G_10Mar2021_Parametrized'
    #outputName=Datacard_2Mar2021_M${m}_PerMassPoint_WithMa_NoCorrel_DataMix_withoutweight_110
    outputName=Datacard_10Mar2021_M${m}_Parametrized
    python makeDatacard.py --inputWSDir /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/${inputTraining}/${m}/Reduced_8Events_1Cats/WS_1Cats l  --mergeYears --mass_a ${m} --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018 --SignalWSDir ${SignalWSDir}_M${m}  --BkgWSDir ${BkgWSDir} --output ${outputName}.txt --BkgExt ${BkgExt} --doSystematics
    #python makeDatacard.py --inputWSDir /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/${inputTraining}/${m}/Reduced_8Events_1Cats/WS_1Cats --doSystematics  --mergeYears --mass_a ${m} --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018 --SignalWSDir ${SignalWSDir}_M${m}  --BkgWSDir ${BkgWSDir}_M${m} --output ${outputName}.txt --BkgExt ${BkgExt}
      #python makeDatacard.py --inputWSDir /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats  --mergeYears --mass_a ${m} --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018 --SignalWSDir outdir_H4G_23Jan2021_M${m} --BkgWSDir outdir_H4G_23Jan2021_M${m} --output Datacard_23Jan2021_M${m}_noSyst.txt

      #python makeDatacard.py --inputWSDir /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats --mergeYears --mass_a ${m} --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018 --SignalWSDir outdir_H4G_23Jan2021_M${m} --BkgWSDir outdir_H4G_23Jan2021_M${m} --output Datacard_3Feb2021_M${m}_noSyst.txt

      #python makeDatacard.py --inputWSDir /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats --mergeYears --mass_a ${m} --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018  --SignalWSDir outdir_H4G_HighStat_BiasStudies_M${m} --BkgWSDir outdir_fullrun2_M${m} --output Datacard_HighStat_noSyst_M${m}_forBiasStudy.txt
      # python makeDatacard.py --inputWSDir /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats --mergeYears --mass_a ${m} --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018  --SignalWSDir outdir_H4G_HighStat_M${m} --BkgWSDir outdir_fullrun2_M${m} --output Datacard_HighStat_noSyst_M${m}.txt
      # python makeDatacard.py --inputWSDir /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats --doSystematics --mergeYears --mass_a ${m} --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018 --SignalWSDir outdir_H4G_NoVtxSplitting_M${m} --BkgWSDir outdir_fullrun2_M${m} --output Datacard_18Jan2021_M${m}.txt

    done
    cd ..
fi

#-- Combine
if [ $step == "combine" ]; then
    cd Datacard
    for m in ${mass};
    do
      datacardName=Datacard_10Mar2021_M${m}_Parametrized.txt
      #datacardName=Datacard_20Feb2021_M${m}_AllMasses_WithoutMa.txt
      #datacardName='Datacard_3Feb2021_M'
      #echo combine ${datacardName}${m}.txt  -m 125 -M AsymptoticLimits --run=blind -n ${datacardName}${m}_AllTheorySyst
      #combine ${datacardName}${m}.txt  -m 125 -M AsymptoticLimits --run=blind -n ${datacardName}${m}_AllTheorySyst
      echo combine ${datacardName}  -m 125 -M AsymptoticLimits --cminDefaultMinimizerStrategy 0 --run="blind" -t -1 -n ${datacardName}
      combine ${datacardName}  -m 125 -M AsymptoticLimits --cminDefaultMinimizerStrategy 0 --run="blind" -t -1 -n ${datacardName}
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
      mkdir BiasStudies_M${m}_${nToys}Toys_2Mar2021_PerMassPoint_WithMa_NoCorrel_DataMix_withoutweight_110
      biasstudies_input=BiasStudies_M${m}_${nToys}Toys_2Mar2021_PerMassPoint_WithMa_NoCorrel_DataMix_withoutweight_110
      # inputDatacard=Datacard_NoVtxSplit_M${m}_wTheorySyst_noQCDSyst.txt
      inputDatacard=Datacard_2Mar2021_M${m}_PerMassPoint_WithMa_NoCorrel_DataMix_withoutweight_110.txt
      echo text2workspace.py ${inputDatacard} -o ${biasstudies_input}/M${m}.root
      text2workspace.py ${inputDatacard} -o ${biasstudies_input}/M${m}.root
      if [[ $m == "60" ]]; then
      expectSignal='1'
      elif [[ $m == "55" ]]; then
      expectSignal=0.41
      elif [[ $m == "50" ]]; then
      expectSignal=0.53
      elif [[ $m == "45" ]]; then
      expectSignal=0.70
      elif [[ $m == "40" ]]; then
      expectSignal=0.73
      elif [[ $m == "30" ]]; then
      expectSignal=0.87
      elif [[ $m == "25" ]]; then
      expectSignal=0.88
      elif [[ $m == "20" ]]; then
      expectSignal=0.74
      elif [[ $m == "15" ]]; then
      expectSignal=0.99
      fi
      for p in ${pdfindex};
      do
         for e in ${expectSignal};
         do
            echo combine ${biasstudies_input}/M${m}.root -M GenerateOnly  -t ${nToys} --setParameters pdfindex_H4GTag_Cat0_13TeV=${p},r=${e} --saveToys --name _M${m}_Cat0_13TeV_pdfindex${p}_signal${e} -m 125 --toysNoSystematics
            #combine ${biasstudies_input}/M${m}.root -M GenerateOnly  -t ${nToys} --setParameters pdfindex_H4GTag_Cat0_13TeV=${p},r=${e} --saveToys --name _M${m}_Cat0_13TeV_pdfindex${p}_signal${e} -m 125 --toysNoSystematics
            #mv higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root ${biasstudies_input}/
         done
      done
    done
    cd ..
fi

#-- Impact plots
if [ $step == "impacts" ]; then
    cd Datacard
    for m in ${mass};
    do
      #datacardName=Datacard_3Feb2021_M${m}_wTheory
      datacardName=Datacard_20Feb2021_M${m}_PerMassPoint_WithMa
      echo text2workspace.py ${datacardName}.txt -m 125
      text2workspace.py ${datacardName}.txt -m 125
      for e in ${expectSignal};
      do
        echo combineTool.py -M Impacts -d ${datacardName}.root -m 125 --rMin -1 --rMax 10 --robustFit 1 --doInitialFit -t -1 --expectSignal ${e} --cminDefaultMinimizerStrategy 0
        combineTool.py -M Impacts -d ${datacardName}.root -m 125 --rMin -1 --rMax 10 --robustFit 1 --doInitialFit -t -1 --expectSignal ${e} --cminDefaultMinimizerStrategy 0

        echo combineTool.py -M Impacts -d ${datacardName}.root -m 125 --rMin -1 --rMax 10 --robustFit 1 --doFits -t -1 --expectSignal ${e} --cminDefaultMinimizerStrategy 0
        combineTool.py -M Impacts -d ${datacardName}.root -m 125 --rMin -1 --rMax 10 --robustFit 1 --doFits -t -1 --expectSignal ${e} --cminDefaultMinimizerStrategy 0

        echo combineTool.py -M Impacts -d ${datacardName}.root -m 125 -o ${datacardName}.json
        combineTool.py -M Impacts -d ${datacardName}.root -m 125 -o ${datacardName}.json

        plotImpacts.py -i ${datacardName}.json -o ${datacardName}_${expectSignal}_PerMassPoint_WithMa
        mv ${datacardName}_${expectSignal}_PerMassPoint_WithMa.pdf /eos/user/t/twamorka/www/H4G_for_PreApp/ImpactPlots/
      done
    done

    cd ..
fi
