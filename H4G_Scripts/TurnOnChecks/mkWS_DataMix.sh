#!/bin/bash

mass=$1
inDir='/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/Parametrized_NoCorrel_FullMassRange/'
for m in ${mass};
do
   echo Mass: ${m}
   inDir_TurnOn=${inDir}${m}/DataMix_Skim/
   
   for num in {1..100};
   do
      #echo $num
      e=$(($num*20000))

      echo ../python mkWS_DataMix.py --iD ${inDir_TurnOn} --i data_mix_run2_${e} --opt data --nCat 1 --t PerYear --year 2016 --oD ${inDir_TurnOn}
      python ../mkWS_DataMix.py --iD ${inDir_TurnOn} --i data_mix_run2_${e} --opt data --nCat 1 --t PerYear --year 2016 --oD ${inDir_TurnOn}
   done
done
