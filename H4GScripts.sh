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
#mass='50'
year='2016 2017 2018'
pdfindex='0 1 2 3 4 5'
expectSignal='0 1'
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
      python makeDatacard.py --inputWSDir /eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/${m}/Reduced_8Events_1Cats/WS_1Cats --mergeYears --mass_a ${m} --procs H4GTag --removeNoTag --cats Cat0 --years 2016,2017,2018 --doSystematics --SignalWSDir outdir_H4G_HighStat_M${m} --BkgWSDir outdir_fullrun2_M${m} --output Datacard_HighStat_M${m}.txt
    done
    cd ..
fi

#-- Combine
if [ $step == "combine" ]; then
    cd Datacard
    for m in ${mass};
    do
      echo combine Datacard_HighStat_M${m}.txt  -m 125 -M AsymptoticLimits --run=blind -n _HighStat_withsyst_M${m}
      combine Datacard_HighStat_M${m}.txt  -m 125 -M AsymptoticLimits --run=blind -n _HighStat_withsyst_M${m}
    done
    cd ..
fi

if [ $step == "biasstudies" ]; then
    cd Datacard
    for m in ${mass};
    do
      mkdir BiasStudies_M${m}
      echo text2workspace.py Datacard_M${m}.txt -o BiasStudies_M${m}/M${m}_BiasStudies.root
      text2workspace.py Datacard_M${m}.txt -o BiasStudies_M${m}/M${m}_BiasStudies.root
      for p in ${pdfindex};
      do
         for e in ${expectSignal};
         do
            echo combine BiasStudies_M${m}/M${m}_BiasStudies.root -M GenerateOnly --expectSignal ${e} -t 500 --setParameters pdfindex_H4GTag_Cat0_13TeV=${p} --saveToys --name _M${m}_Cat0_13TeV_pdfindex${p}_signal${e} -m 125
            combine BiasStudies_M${m}/M${m}_BiasStudies.root -M GenerateOnly --expectSignal ${e} -t 500 --setParameters pdfindex_H4GTag_Cat0_13TeV=${p} --saveToys --name _M${m}_Cat0_13TeV_pdfindex${p}_signal${e} -m 125

            mv higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root BiasStudies_M${m}/

            echo combine BiasStudies_M${m}/M${m}_BiasStudies.root -M MultiDimFit --toysFile=BiasStudies_M${m}/higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root -P r --expectSignal ${e} -t 500 --saveSpecifiedIndex pdfindex_H4GTag_Cat0_13TeV -m 125 --cminDefaultMinimizerStrategy 0 --algo singles --saveFitResult --name _M${m}_pdfindex${p}_signal${e} --setParameterRanges r=-10,10
            combine BiasStudies_M${m}/M${m}_BiasStudies.root -M MultiDimFit --toysFile=BiasStudies_M${m}/higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root -P r --expectSignal ${e} -t 500 --saveSpecifiedIndex pdfindex_H4GTag_Cat0_13TeV -m 125 --cminDefaultMinimizerStrategy 0 --algo singles --saveFitResult --name _M${m}_pdfindex${p}_signal${e} --setParameterRanges r=-10,10

            mv multidimfit_M${m}_pdfindex${p}_signal${e}.root BiasStudies_M${m}/
            mv higgsCombine_M${m}_pdfindex${p}_signal${e}.MultiDimFit.mH125.123456.root BiasStudies_M${m}/


         done
         # combine BiasStudies_M${m}/M${m}_BiasStudies.root -M MultiDimFit --toysFile=higgsCombine_M60_Cat0_13TeV_pdfindex0.GenerateOnly.mH125.123456.root -P r --expectSignal 1 -t 500 --saveSpecifiedIndex pdfindex_H4GTag_Cat0_13TeV -m 125 --cminDefaultMinimizerStrategy 0 --algo singles --saveFitResult --name M60 --setParameterRanges r=-10,10
      done
    done
    cd ..
fi
