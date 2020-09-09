#!/bin/bash
inDir='/eos/user/t/twamorka/h4g_fullRun2/withSystematics/fullRun2/1Sep2020/Run2/m'
mass='60 45 35 25 15'
# mass='15'
opt='signal'
year='2018'
# year='2016 2017 2018'
outDir='/eos/user/t/twamorka/h4g_fullRun2/withSystematics/fullRun2/1Sep2020/Run2/m'

for m in $mass;
do
  echo $m
  for y in $year;
  do
    echo $y
    python shiftHiggsDatasets.py --i signal_m_${m}_${y}_skim_WS --inDir ${inDir}${m}/Skim/ --m ${m}  --outDir ${inDir}${m}/Skim/
  done
done
