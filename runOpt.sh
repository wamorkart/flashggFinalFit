#!/bin/bash

NCat='2 3 4 5'
#Precision='0.01 0.013 0.015 0.017 0.02 0.03 0.05 0.07 0.1'
#NCat='3'
# mass='60 45 35 25 15'
year='"Run2"'
mass='60'
Precision='0.02'
Normalization='2'
inDir='"/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied/PerMass_FullRun2_DataMix_v8_SignalDataMix_NormalizedToDataSideband/"'
# outDir='"/eos/user/t/twamorka/www/H4G_Pre_PreApp/SignificanceChecks//"'
# outPlotDir="/eos/user/t/twamorka/www/H4G_Pre_PreApp/SignificanceChecks//"
# inDir='"/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied/PerMass_FullRun2_DataMix_v8_OldNormalization/"'
# inDir='"/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied/PerMass_FullRun2_DataMix_v8_SignalDataMix_NormalizedToDataSideband/"'
outDir='"/eos/user/t/twamorka/www/H4G_Pre_PreApp/SignificanceChecks/DataMix_v8_DataSBTraining_Norm2_11Nov2020_100Bins/"'
# inDir='"/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied/PerMass_FullRun2_DataMix_v8_OldNormalization/"'
# outDir='"/eos/user/t/twamorka/www/H4G_Pre_PreApp/SignificanceChecks/DataMix_v8_DataSBTraining_Norm2_/"'
outPlotDir="/eos/user/t/twamorka/www/H4G_Pre_PreApp/SignificanceChecks/DataMix_v8_DataSBTraining_Norm2_11Nov2020_100Bins/"
# outPlotDir="/eos/user/t/twamorka/www/H4G_Pre_PreApp/SignificanceChecks/DataMix_v8_LumiTraining_Norm2/"
# inDir='"/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied/Standard_M60_Run2_OldTraining/"'
# outDir='"/eos/user/t/twamorka/www/H4G_Pre_PreApp/SignificanceChecks/DataMix_v4_LumiTraining_Norm2_11Nov2020_50Bins/"'
# outPlotDir="/eos/user/t/twamorka/www/H4G_Pre_PreApp/SignificanceChecks/DataMix_v4_LumiTraining_Norm2_11Nov2020_50Bins/"
mkdir ${outPlotDir}
cp ${outPlotDir}../index.php ${outPlotDir}
for n in $NCat;
do
  echo `root -l optimize_cats_H4G.C'('${n}','${year}','${mass}','${Precision}','${inDir}','${outDir}','${Normalization}')' << EOF`
done

# for N in ${Norm};
# do
#   echo "Normalization " $N
#   mkdir /eos/user/t/twamorka/www/H4G_Pre_PreApp/SignificanceChecks/DataMix_v4_LumiNorm_Norm${N}/
#   outDir='"/eos/user/t/twamorka/www/H4G_Pre_PreApp/SignificanceChecks/DataMix_v4_LumiNorm_Norm'${N}'/"'
#   cp outDir/../index.php outDir
#   for m in ${mass};
#   do
#     for n in $NCat;
#     do
#       for p in $Precision;
#       do
#         echo 'NCat: ', ${n}, ' Precision: ', ${p}
#         echo `root -l optimize_cats_modifiedSig_OldNormalization.C'('${n}',1,1,-1,'${p}','${m}','${inDir}','${outDir}','${N}')' << EOF`
#       done
#     done
#   done
# done
