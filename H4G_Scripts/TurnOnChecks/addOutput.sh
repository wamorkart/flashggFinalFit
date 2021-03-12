#!/bin/bash

mass='55 50 45 40 35 30 25 20 15'
#mass='60'
inDir='/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/Parametrized_NoCorrel_FullMassRange/'

for m in ${mass};
do
   echo Mass: ${m}
   for num in {1..100};
   do
      #echo $num
      e=$(($num*20000))
      echo hadd -f ${inDir}${m}/DataMix_Skim/data_mix_run2_${e}.root  ${inDir}${m}/DataMix_Skim/data_mix_2016_${e}_Cut*.root ${inDir}${m}/DataMix_Skim/data_mix_2017_${e}_Cut*.root ${inDir}${m}/DataMix_Skim/data_mix_2018_${e}_Cut*.root
      hadd -f ${inDir}${m}/DataMix_Skim/data_mix_run2_${e}.root  ${inDir}${m}/DataMix_Skim/data_mix_2016_${e}_Cut*.root ${inDir}${m}/DataMix_Skim/data_mix_2017_${e}_Cut*.root ${inDir}${m}/DataMix_Skim/data_mix_2018_${e}_Cut*.root
      rm ${inDir}${m}/DataMix_Skim/data_mix_2016_${e}_Cut*.root
      rm ${inDir}${m}/DataMix_Skim/data_mix_2017_${e}_Cut*.root
      rm ${inDir}${m}/DataMix_Skim/data_mix_2018_${e}_Cut*.root
   done
done
