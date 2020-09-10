#!/bin/bash

inDir='/eos/user/t/twamorka/h4g_fullRun2/withSystematics/fullRun2/1Sep2020/Run2/m'
mass='60 45 35 25 15'
# mass='60'
opt='signal'
# year='2016'
year='2016 2017 2018'
outDir='/eos/user/t/twamorka/h4g_fullRun2/withSystematics/fullRun2/1Sep2020/Run2/m'
nCat='output_SB_bdt_cat5_mineventborders8_borders_04_08_2020_fineBinning_combined_04_08_2020_bdt.txt'
var='bdt'

for m in $mass;
do
  echo $m
  for y in $year;
  do
    echo $y
    python reduceTrees.py --iD ${inDir}${m}/ --i signal_m_${m}_${y} --m ${m} --opt ${opt} --year ${y}  --oD ${inDir}${m}/Skim/ --nCat ${inDir}${m}/${nCat} --v ${var}
    done
done
