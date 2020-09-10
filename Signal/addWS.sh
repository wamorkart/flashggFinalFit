#!/bin/bash

inDir='/eos/user/t/twamorka/h4g_fullRun2/withSystematics/fullRun2/1Sep2020/Run2/m'
mass='60 45 35 25 15'
outDir='/eos/user/t/twamorka/h4g_fullRun2/withSystematics/fullRun2/1Sep2020/Run2/m'
add='120 125 130'
# add='Syst'

for m in $mass;
do
  echo ${m}
  for a in ${add};
  do
    echo ${a}
    hadd_workspaces ${inDir}${m}/Skim/signal_m_${m}_Run2_skim_WS_${a}.root ${inDir}${m}/Skim/signal_m_${m}_2016_skim_WS_${a}.root ${inDir}${m}/Skim/signal_m_${m}_2017_skim_WS_${a}.root ${inDir}${m}/Skim/signal_m_${m}_2018_skim_WS_${a}.root
    # hadd_workspaces ${inDir}${m}/Skim/signal_m_${m}_Run2_skim_WS_${a}.root ${inDir}${m}/Skim/signal_m_${m}_2016_skim_WS_${a}.root ${inDir}${m}/Skim/signal_m_${m}_2017_skim_WS_${a}.root ${inDir}${m}/Skim/signal_m_${m}_2018_skim_WS_${a}.root
  done
done
