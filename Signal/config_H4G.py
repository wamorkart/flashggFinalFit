# Config file: options for signal fitting

# _year = '2016'
# _mass_a = '60'

signalScriptCfg = {

  # Setup
  'inputWSDir':'/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/H4G_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_noCorrel/',
  #'inputWSDir':'/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/Parametrized_NoCorrel_FullMassRange/',
  #'inputWSDir':'/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_newSignalWeights_parametrized_v2/',
  #'inputWSDir':'/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/FullRun2_Parametrized/M55_Cat/',
  #'inputWSDir':'/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/FullRun2_PerMassPoint_WithoutMa/',
  #'inputWSDir':'/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/FullRun2_Parametrized/',
  #'inputWSDir':'/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/FullRun2_AllMasses_WithoutMa/',
  #'inputWSDir':'/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/',
  #'inputWSDir':'/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/SignalInterpol_M55/',
  #'inputWSDir':'/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataDriven_crA_MGPodd/',
  'usrprocs':'H4G', # if auto: inferred automatically from filenames
  'cats':'Cat0', # if auto: inferred automatically from (0) workspace
  'ext':'H4G_10Mar2021_NoCorrel',
  'analysis':'H4G', # To specify which replacement dataset mapping (defined in ./python/replacementMap.py)
  'analysis_type':'H4G',
  # 'year':'%s'%_year, # Use 'combined' if merging all years: not recommended
  # 'mass_a':'%s'%_mass_a,
  'beamspot':'3.4',
  'numberOfBins':'320',
  'massPoints':'120,125,130',
  #'FinalState':'fullRun2',
  #Photon shape systematics
  'scales':'HighR9EB,HighR9EE,LowR9EB,LowR9EE,Gain1EB,Gain6EB', # separate nuisance per year
  'scalesCorr':'MaterialCentralBarrel,MaterialOuterBarrel,MaterialForward,FNUFEE,FNUFEB,ShowerShapeHighR9EE,ShowerShapeHighR9EB,ShowerShapeLowR9EE,ShowerShapeLowR9EB', # correlated across years
  'scalesGlobal':'NonLinearity,Geant4', # affect all processes equally, correlated across years
  'smears':'HighR9EBPhi,HighR9EBRho,HighR9EEPhi,HighR9EERho,LowR9EBPhi,LowR9EBRho,LowR9EEPhi,LowR9EERho', # separate nuisance per year
  'systematics':'1',
  # Job submission options
  'batch':'local', # ['condor','SGE','IC','local']
  'queue':'',
  #'batch':'condor', # ['condor','SGE','IC','local']
  #'queue':'espresso',
  'useDCB':1,
  # Mode allows script to carry out single function
  'mode':'std', # Options: [std,getFractions,sigFitOnly,sigFitOnly,sigFitOnly,packageOnly,sigPlotsOnly]
  'verbosity':'0'
}
