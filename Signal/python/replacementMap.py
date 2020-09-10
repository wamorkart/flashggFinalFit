# Python script to hold replacement model mapping for different analyses

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# WRONG VERTEX FITS:
#  > shape of mgg in WV ~identical across tags, therefore use single replacement

# Replacement proc for WV fit:
replacementProcWV = {
  "hig-16-040":"GG2H",
  "stage1":"GG2H_0J",
  "stage1_1":"GG2H_0J_PTH_GT10",
  "stage1_2":"GG2H_0J_PTH_GT10",
  # "HHWWgg":"ggF",
  "HHWWgg":"GluGluToHHTo",
  "H4G":"H4G"
}
# Replacement cat for WV fit:
replacementCatWV = {
  "hig-16-040":"UntaggedTag_2",
  "stage1":"RECO_0J_Tag1",
  "stage1_1":"RECO_0J_PTH_GT10_Tag1",
  "stage1_2":"RECO_0J_PTH_GT10_Tag1",
  "HHWWgg":"HHWWggTag_0",
  "H4G":"H4G_Cat0"
  # "HHWWgg":"HHWWggTag_1"
  # "HHWWgg_qqlnu" : "HHWWggTag_0",
  # "HHWWgg_qqqq" : "HHWWggTag_2"
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# RIGHT VERTEX FITS:
#  > default is to use diagonal process, keeping category constant
#  > if few events in diagonal process then may need to change the category aswell

# Replacement process for RV fit:
replacementProcRVMap = {

  # HIG-16-040 categorisation
  "hig-16-040":[
    "UntaggedTag_0:GG2H",
    "UntaggedTag_1:GG2H",
    "UntaggedTag_2:GG2H",
    "UntaggedTag_3:GG2H",
    "VBFTag_0:VBF",
    "VBFTag_1:VBF",
    "VBFTag_2:VBF",
    "TTHHadronicTag:TTH",
    "TTHLeptonicTag:TTH",
    "ZHLeptonicTag:QQ2HLL",
    "WHLeptonicTag:QQ2HLNU",
    "VHLeptonicLooseTag:QQ2HLNU",
    "VHHadronicTag:ZH2HQQ",
    "VHMetTag:QQ2HLNU"
  ],

  "HHWWgg":[
    "HHWWggTag_0:HHWWggTag_0"
  ],

  "H4G":[
    "H4G_Cat0:H4G",
    "H4G_Cat1:H4G",
    "H4G_Cat2:H4G",
    "H4G_Cat3:H4G",
    "H4G_Cat4:H4G"
  ],

  # STXS stage 1 categorisation (HIG-18-029)
  "stage1":[
    "RECO_0J_Tag0:GG2H_0J",
    "RECO_0J_Tag1:GG2H_0J",
    "RECO_0J_Tag2:GG2H_0J",
    "RECO_1J_PTH_0_60_Tag0:GG2H_1J_PTH_0_60",
    "RECO_1J_PTH_0_60_Tag1:GG2H_1J_PTH_0_60",
    "RECO_1J_PTH_60_120_Tag0:GG2H_1J_PTH_60_120",
    "RECO_1J_PTH_60_120_Tag1:GG2H_1J_PTH_60_120",
    "RECO_1J_PTH_120_200_Tag0:GG2H_1J_PTH_120_200",
    "RECO_1J_PTH_120_200_Tag1:GG2H_1J_PTH_120_200",
    "RECO_1J_PTH_GT200:GG2H_1J_PTH_GT200",
    "RECO_GE2J_PTH_0_60_Tag0:GG2H_GE2J_PTH_0_60",
    "RECO_GE2J_PTH_0_60_Tag1:GG2H_GE2J_PTH_0_60",
    "RECO_GE2J_PTH_60_120_Tag0:GG2H_GE2J_PTH_60_120",
    "RECO_GE2J_PTH_60_120_Tag1:GG2H_GE2J_PTH_60_120",
    "RECO_GE2J_PTH_120_200_Tag0:GG2H_GE2J_PTH_120_200",
    "RECO_GE2J_PTH_120_200_Tag1:GG2H_GE2J_PTH_120_200",
    "RECO_GE2J_PTH_GT200_Tag0:GG2H_GE2J_PTH_GT200",
    "RECO_GE2J_PTH_GT200_Tag1:GG2H_GE2J_PTH_GT200",
    "RECO_VBFTOPO_JET3VETO_Tag0:VBF_VBFTOPO_JET3VETO",
    "RECO_VBFTOPO_JET3VETO_Tag1:VBF_VBFTOPO_JET3VETO",
    "RECO_VBFTOPO_JET3VETO_Tag2:VBF_VBFTOPO_JET3VETO",
    "RECO_VBFTOPO_JET3_Tag0:VBF_VBFTOPO_JET3",
    "RECO_VBFTOPO_JET3_Tag1:VBF_VBFTOPO_JET3",
    "RECO_VBFTOPO_JET3_Tag2:VBF_VBFTOPO_JET3",
    "RECO_VBFTOPO_REST:VBF_REST",
    "RECO_VBFTOPO_BSM:VBF_PTJET1_GT200",
    "RECO_VHHAD:ZH2HQQ_VH2JET",
    "RECO_VHLEPLOOSE:QQ2HLNU_PTV_0_150",
    "RECO_VHMET:QQ2HLNU_PTV_0_150",
    "RECO_WHLEP:QQ2HLNU_PTV_0_150",
    "RECO_ZHLEP:QQ2HLL_PTV_0_150",
    "RECO_ZHLEP:QQ2HLNU_PTV_0_150",
    "RECO_TTH_LEP:TTH",
    "RECO_TTH_HAD:TTH"
  ],

  # STXS stage 1.1 categorisation
  "stage1_1":[
    "RECO_0J_PTH_GT10_Tag0:GG2H_0J_PTH_GT10",
    "RECO_0J_PTH_GT10_Tag1:GG2H_0J_PTH_GT10",
    "RECO_0J_PTH_0_10_Tag0:GG2H_0J_PTH_0_10",
    "RECO_0J_PTH_0_10_Tag1:GG2H_0J_PTH_0_10",
    "RECO_PTH_GT200_Tag0:GG2H_PTH_GT200",
    "RECO_PTH_GT200_Tag1:GG2H_PTH_GT200",
    "RECO_1J_PTH_120_200_Tag0:GG2H_1J_PTH_120_200",
    "RECO_1J_PTH_120_200_Tag1:GG2H_1J_PTH_120_200",
    "RECO_1J_PTH_60_120_Tag0:GG2H_1J_PTH_60_120",
    "RECO_1J_PTH_60_120_Tag1:GG2H_1J_PTH_60_120",
    "RECO_1J_PTH_0_60_Tag0:GG2H_1J_PTH_0_60",
    "RECO_1J_PTH_0_60_Tag1:GG2H_1J_PTH_0_60",
    "RECO_GE2J_PTH_120_200_Tag0:GG2H_GE2J_MJJ_0_350_PTH_120_200",
    "RECO_GE2J_PTH_120_200_Tag1:GG2H_GE2J_MJJ_0_350_PTH_120_200",
    "RECO_GE2J_PTH_60_120_Tag0:GG2H_GE2J_MJJ_0_350_PTH_60_120",
    "RECO_GE2J_PTH_60_120_Tag1:GG2H_GE2J_MJJ_0_350_PTH_60_120",
    "RECO_GE2J_PTH_0_60_Tag0:GG2H_GE2J_MJJ_0_350_PTH_0_60",
    "RECO_GE2J_PTH_0_60_Tag1:GG2H_GE2J_MJJ_0_350_PTH_0_60",
    "RECO_VBFTOPO_BSM:VBF_GE2J_MJJ_GT350_PTH_GT200",
    "RECO_VBFTOPO_JET3VETO_Tag0:VBF_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25",
    "RECO_VBFTOPO_JET3VETO_Tag1:VBF_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25",
    "RECO_VBFTOPO_JET3_Tag0:VBF_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25",
    "RECO_VBFTOPO_JET3_Tag1:VBF_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25"
    #"RECO_VBFTOPO_VHHAD:WH2HQQ_MJJ_60_120"
  ],

  # STXS stage 1.2 categorisation
  "stage1_2":[
    "RECO_0J_PTH_0_10_Tag0:GG2H_0J_PTH_0_10",
    "RECO_0J_PTH_0_10_Tag1:GG2H_0J_PTH_0_10",
    "RECO_0J_PTH_GT10_Tag0:GG2H_0J_PTH_GT10",
    "RECO_0J_PTH_GT10_Tag1:GG2H_0J_PTH_GT10",
    "RECO_1J_PTH_0_60_Tag0:GG2H_1J_PTH_0_60",
    "RECO_1J_PTH_0_60_Tag1:GG2H_1J_PTH_0_60",
    "RECO_1J_PTH_60_120_Tag0:GG2H_1J_PTH_60_120",
    "RECO_1J_PTH_60_120_Tag1:GG2H_1J_PTH_60_120",
    "RECO_1J_PTH_120_200_Tag0:GG2H_1J_PTH_120_200",
    "RECO_1J_PTH_120_200_Tag1:GG2H_1J_PTH_120_200",
    "RECO_GE2J_PTH_0_60_Tag0:GG2H_GE2J_MJJ_0_350_PTH_0_60",
    "RECO_GE2J_PTH_0_60_Tag1:GG2H_GE2J_MJJ_0_350_PTH_0_60",
    "RECO_GE2J_PTH_60_120_Tag0:GG2H_GE2J_MJJ_0_350_PTH_60_120",
    "RECO_GE2J_PTH_60_120_Tag1:GG2H_GE2J_MJJ_0_350_PTH_60_120",
    "RECO_GE2J_PTH_120_200_Tag0:GG2H_GE2J_MJJ_0_350_PTH_120_200",
    "RECO_GE2J_PTH_120_200_Tag1:GG2H_GE2J_MJJ_0_350_PTH_120_200",
    "RECO_PTH_200_300:GG2H_PTH_200_300",
    "RECO_PTH_300_450:GG2H_PTH_300_450",
    "RECO_PTH_450_650:GG2H_PTH_450_650",
    "RECO_PTH_GT650:GG2H_PTH_GT650",
    "RECO_THQ_LEP:THQ",
    "RECO_TTH_HAD_HIGH_Tag0:TTH_PTH_120_200",
    "RECO_TTH_HAD_HIGH_Tag1:TTH_PTH_120_200",
    "RECO_TTH_HAD_HIGH_Tag2:TTH_PTH_120_200",
    "RECO_TTH_HAD_HIGH_Tag3:TTH_PTH_120_200",
    "RECO_TTH_HAD_LOW_Tag0:TTH_PTH_60_120",
    "RECO_TTH_HAD_LOW_Tag1:TTH_PTH_60_120",
    "RECO_TTH_HAD_LOW_Tag2:TTH_PTH_60_120",
    "RECO_TTH_HAD_LOW_Tag3:TTH_PTH_60_120",
    "RECO_TTH_LEP_HIGH_Tag0:TTH_PTH_120_200",
    "RECO_TTH_LEP_HIGH_Tag1:TTH_PTH_120_200",
    "RECO_TTH_LEP_HIGH_Tag2:TTH_PTH_120_200",
    "RECO_TTH_LEP_HIGH_Tag3:TTH_PTH_120_200",
    "RECO_TTH_LEP_LOW_Tag0:TTH_PTH_60_120",
    "RECO_TTH_LEP_LOW_Tag1:TTH_PTH_60_120",
    "RECO_TTH_LEP_LOW_Tag2:TTH_PTH_60_120",
    "RECO_TTH_LEP_LOW_Tag3:TTH_PTH_60_120",
    "RECO_VBFLIKEGGH_Tag0:GG2H_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25",
    "RECO_VBFLIKEGGH_Tag1:GG2H_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25",
    "RECO_VBFTOPO_BSM_Tag0:VBF_GE2J_MJJ_GT350_PTH_GT200",
    "RECO_VBFTOPO_BSM_Tag1:VBF_GE2J_MJJ_GT350_PTH_GT200",
    "RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag0:VBF_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25",
    "RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag1:VBF_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_0_25",
    "RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag0:VBF_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25",
    "RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag1:VBF_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_0_25",
    "RECO_VBFTOPO_JET3_HIGHMJJ_Tag0:VBF_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_GT25",
    "RECO_VBFTOPO_JET3_HIGHMJJ_Tag1:VBF_GE2J_MJJ_GT700_PTH_0_200_PTHJJ_GT25",
    "RECO_VBFTOPO_JET3_LOWMJJ_Tag0:VBF_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25",
    "RECO_VBFTOPO_JET3_LOWMJJ_Tag1:VBF_GE2J_MJJ_350_700_PTH_0_200_PTHJJ_GT25",
    "RECO_VBFTOPO_VHHAD_Tag0:WH2HQQ_GE2J_MJJ_60_120",
    "RECO_VBFTOPO_VHHAD_Tag1:WH2HQQ_GE2J_MJJ_60_120",
    "RECO_WH_LEP_HIGH_Tag0:QQ2HLNU_PTV_75_150",
    "RECO_WH_LEP_HIGH_Tag1:QQ2HLNU_PTV_75_150",
    "RECO_WH_LEP_HIGH_Tag2:QQ2HLNU_PTV_75_150",
    "RECO_WH_LEP_LOW_Tag0:QQ2HLNU_PTV_0_75",
    "RECO_WH_LEP_LOW_Tag1:QQ2HLNU_PTV_0_75",
    "RECO_WH_LEP_LOW_Tag2:QQ2HLNU_PTV_0_75",
    "RECO_ZH_LEP:QQ2HLL_PTV_0_75"
  ]
}

# Replacement category for RV fit:
replacementCatRVMap = {

  # HIG-16-040 categorisation
  "hig-16-040":[
    "UntaggedTag_0:UntaggedTag_0",
    "UntaggedTag_1:UntaggedTag_1",
    "UntaggedTag_2:UntaggedTag_2",
    "UntaggedTag_3:UntaggedTag_3",
    "VBFTag_0:VBFTag_0",
    "VBFTag_1:VBFTag_1",
    "VBFTag_2:VBFTag_2",
    "TTHHadronicTag:TTHHadronicTag",
    "TTHLeptonicTag:TTHLeptonicTag",
    "ZHLeptonicTag:ZHLeptonicTag",
    "WHLeptonicTag:WHLeptonicTag",
    "VHLeptonicLooseTag:VHLeptonicLooseTag",
    "VHHadronicTag:VHHadronicTag",
    "VHMetTag:VHMetTag"
  ],

  "HHWWgg":[
    "HHWWggTag_0:HHWWggTag_0"
  ],
  "H4G":[
    "H4G_Cat0:H4G_Cat0",
    "H4G_Cat1:H4G_Cat0",
    "H4G_Cat2:H4G_Cat0",
    "H4G_Cat3:H4G_Cat0",
    "H4G_Cat4:H4G_Cat0",

  ],

  # STXS stage 1 categorisation (HIG-18-029)
  "stage1":[
    "RECO_0J_Tag0:RECO_0J_Tag0",
    "RECO_0J_Tag1:RECO_0J_Tag1",
    "RECO_0J_Tag2:RECO_0J_Tag2",
    "RECO_1J_PTH_0_60_Tag0:RECO_1J_PTH_0_60_Tag0",
    "RECO_1J_PTH_0_60_Tag1:RECO_1J_PTH_0_60_Tag1",
    "RECO_1J_PTH_60_120_Tag0:RECO_1J_PTH_60_120_Tag0",
    "RECO_1J_PTH_60_120_Tag1:RECO_1J_PTH_60_120_Tag1",
    "RECO_1J_PTH_120_200_Tag0:RECO_1J_PTH_120_200_Tag0",
    "RECO_1J_PTH_120_200_Tag1:RECO_1J_PTH_120_200_Tag1",
    "RECO_1J_PTH_GT200:RECO_1J_PTH_GT200",
    "RECO_GE2J_PTH_0_60_Tag0:RECO_GE2J_PTH_0_60_Tag0",
    "RECO_GE2J_PTH_0_60_Tag1:RECO_GE2J_PTH_0_60_Tag1",
    "RECO_GE2J_PTH_60_120_Tag0:RECO_GE2J_PTH_60_120_Tag0",
    "RECO_GE2J_PTH_60_120_Tag1:RECO_GE2J_PTH_60_120_Tag1",
    "RECO_GE2J_PTH_120_200_Tag0:RECO_GE2J_PTH_120_200_Tag0",
    "RECO_GE2J_PTH_120_200_Tag1:RECO_GE2J_PTH_120_200_Tag1",
    "RECO_GE2J_PTH_GT200_Tag0:RECO_GE2J_PTH_GT200_Tag0",
    "RECO_GE2J_PTH_GT200_Tag1:RECO_GE2J_PTH_GT200_Tag1",
    "RECO_VBFTOPO_JET3VETO_Tag0:RECO_VBFTOPO_JET3VETO_Tag0",
    "RECO_VBFTOPO_JET3VETO_Tag1:RECO_VBFTOPO_JET3VETO_Tag1",
    "RECO_VBFTOPO_JET3VETO_Tag2:RECO_VBFTOPO_JET3VETO_Tag2",
    "RECO_VBFTOPO_JET3_Tag0:RECO_VBFTOPO_JET3_Tag0",
    "RECO_VBFTOPO_JET3_Tag1:RECO_VBFTOPO_JET3_Tag1",
    "RECO_VBFTOPO_JET3_Tag2:RECO_VBFTOPO_JET3_Tag2",
    "RECO_VBFTOPO_REST:RECO_VBFTOPO_REST",
    "RECO_VBFTOPO_BSM:RECO_VBFTOPO_BSM",
    "RECO_VHHAD:RECO_VHHAD",
    "RECO_VHLEPLOOSE:RECO_VHLEPLOOSE",
    "RECO_VHMET:RECO_VHMET",
    "RECO_WHLEP:RECO_WHLEP",
    "RECO_ZHLEP:RECO_WHLEP", #NON DIAGONAL: too few in diagonal proc x cat
    "RECO_TTH_LEP:RECO_TTH_LEP",
    "RECO_TTH_HAD:RECO_TTH_HAD"
  ],

  # STXS stage 1.1 categorisation
  "stage1_1":[
    "RECO_0J_PTH_GT10_Tag0:RECO_0J_PTH_GT10_Tag0",
    "RECO_0J_PTH_GT10_Tag1:RECO_0J_PTH_GT10_Tag1",
    "RECO_0J_PTH_0_10_Tag0:RECO_0J_PTH_0_10_Tag0",
    "RECO_0J_PTH_0_10_Tag1:RECO_0J_PTH_0_10_Tag1",
    "RECO_PTH_GT200_Tag0:RECO_PTH_GT200_Tag0",
    "RECO_PTH_GT200_Tag1:RECO_PTH_GT200_Tag1",
    "RECO_1J_PTH_120_200_Tag0:RECO_1J_PTH_120_200_Tag0",
    "RECO_1J_PTH_120_200_Tag1:RECO_1J_PTH_120_200_Tag1",
    "RECO_1J_PTH_60_120_Tag0:RECO_1J_PTH_60_120_Tag0",
    "RECO_1J_PTH_60_120_Tag1:RECO_1J_PTH_60_120_Tag1",
    "RECO_1J_PTH_0_60_Tag0:RECO_1J_PTH_0_60_Tag0",
    "RECO_1J_PTH_0_60_Tag1:RECO_1J_PTH_0_60_Tag1",
    "RECO_GE2J_PTH_120_200_Tag0:RECO_GE2J_PTH_120_200_Tag0",
    "RECO_GE2J_PTH_120_200_Tag1:RECO_GE2J_PTH_120_200_Tag1",
    "RECO_GE2J_PTH_60_120_Tag0:RECO_GE2J_PTH_60_120_Tag0",
    "RECO_GE2J_PTH_60_120_Tag1:RECO_GE2J_PTH_60_120_Tag1",
    "RECO_GE2J_PTH_0_60_Tag0:RECO_GE2J_PTH_0_60_Tag0",
    "RECO_GE2J_PTH_0_60_Tag1:RECO_GE2J_PTH_0_60_Tag1",
    "RECO_VBFTOPO_BSM:RECO_VBFTOPO_BSM",
    "RECO_VBFTOPO_JET3VETO_Tag0:RECO_VBFTOPO_JET3VETO_Tag0",
    "RECO_VBFTOPO_JET3VETO_Tag1:RECO_VBFTOPO_JET3VETO_Tag1",
    "RECO_VBFTOPO_JET3_Tag0:RECO_VBFTOPO_JET3_Tag0",
    "RECO_VBFTOPO_JET3_Tag1:RECO_VBFTOPO_JET3_Tag1"#,
    #"RECO_VBFTOPO_VHHAD:RECO_VBFTOPO_VHHAD"
  ],

  # STXS stage 1.2 categorisation
  "stage1_2":[
    "RECO_0J_PTH_0_10_Tag0:RECO_0J_PTH_0_10_Tag0",
    "RECO_0J_PTH_0_10_Tag1:RECO_0J_PTH_0_10_Tag1",
    "RECO_0J_PTH_GT10_Tag0:RECO_0J_PTH_GT10_Tag0",
    "RECO_0J_PTH_GT10_Tag1:RECO_0J_PTH_GT10_Tag1",
    "RECO_1J_PTH_0_60_Tag0:RECO_1J_PTH_0_60_Tag0",
    "RECO_1J_PTH_0_60_Tag1:RECO_1J_PTH_0_60_Tag1",
    "RECO_1J_PTH_120_200_Tag0:RECO_1J_PTH_120_200_Tag0",
    "RECO_1J_PTH_120_200_Tag1:RECO_1J_PTH_120_200_Tag1",
    "RECO_1J_PTH_60_120_Tag0:RECO_1J_PTH_60_120_Tag0",
    "RECO_1J_PTH_60_120_Tag1:RECO_1J_PTH_60_120_Tag1",
    "RECO_GE2J_PTH_0_60_Tag0:RECO_GE2J_PTH_0_60_Tag0",
    "RECO_GE2J_PTH_0_60_Tag1:RECO_GE2J_PTH_0_60_Tag1",
    "RECO_GE2J_PTH_120_200_Tag0:RECO_GE2J_PTH_120_200_Tag0",
    "RECO_GE2J_PTH_120_200_Tag1:RECO_GE2J_PTH_120_200_Tag1",
    "RECO_GE2J_PTH_60_120_Tag0:RECO_GE2J_PTH_60_120_Tag0",
    "RECO_GE2J_PTH_60_120_Tag1:RECO_GE2J_PTH_60_120_Tag1",
    "RECO_PTH_200_300:RECO_PTH_200_300",
    "RECO_PTH_300_450:RECO_PTH_300_450",
    "RECO_PTH_450_650:RECO_PTH_450_650",
    "RECO_PTH_GT650:RECO_PTH_GT650",
    "RECO_THQ_LEP:RECO_THQ_LEP",
    "RECO_TTH_HAD_HIGH_Tag0:RECO_TTH_HAD_HIGH_Tag0",
    "RECO_TTH_HAD_HIGH_Tag1:RECO_TTH_HAD_HIGH_Tag1",
    "RECO_TTH_HAD_HIGH_Tag2:RECO_TTH_HAD_HIGH_Tag2",
    "RECO_TTH_HAD_HIGH_Tag3:RECO_TTH_HAD_HIGH_Tag3",
    "RECO_TTH_HAD_LOW_Tag0:RECO_TTH_HAD_LOW_Tag0",
    "RECO_TTH_HAD_LOW_Tag1:RECO_TTH_HAD_LOW_Tag1",
    "RECO_TTH_HAD_LOW_Tag2:RECO_TTH_HAD_LOW_Tag2",
    "RECO_TTH_HAD_LOW_Tag3:RECO_TTH_HAD_LOW_Tag3",
    "RECO_TTH_LEP_HIGH_Tag0:RECO_TTH_LEP_HIGH_Tag0",
    "RECO_TTH_LEP_HIGH_Tag1:RECO_TTH_LEP_HIGH_Tag1",
    "RECO_TTH_LEP_HIGH_Tag2:RECO_TTH_LEP_HIGH_Tag2",
    "RECO_TTH_LEP_HIGH_Tag3:RECO_TTH_LEP_HIGH_Tag3",
    "RECO_TTH_LEP_LOW_Tag0:RECO_TTH_LEP_LOW_Tag0",
    "RECO_TTH_LEP_LOW_Tag1:RECO_TTH_LEP_LOW_Tag1",
    "RECO_TTH_LEP_LOW_Tag2:RECO_TTH_LEP_LOW_Tag2",
    "RECO_TTH_LEP_LOW_Tag3:RECO_TTH_LEP_LOW_Tag3",
    "RECO_VBFLIKEGGH_Tag0:RECO_VBFLIKEGGH_Tag0",
    "RECO_VBFLIKEGGH_Tag1:RECO_VBFLIKEGGH_Tag1",
    "RECO_VBFTOPO_BSM_Tag0:RECO_VBFTOPO_BSM_Tag0",
    "RECO_VBFTOPO_BSM_Tag1:RECO_VBFTOPO_BSM_Tag1",
    "RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag0:RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag0",
    "RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag1:RECO_VBFTOPO_JET3VETO_HIGHMJJ_Tag1",
    "RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag0:RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag0",
    "RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag1:RECO_VBFTOPO_JET3VETO_LOWMJJ_Tag1",
    "RECO_VBFTOPO_JET3_HIGHMJJ_Tag0:RECO_VBFTOPO_JET3_HIGHMJJ_Tag0",
    "RECO_VBFTOPO_JET3_HIGHMJJ_Tag1:RECO_VBFTOPO_JET3_HIGHMJJ_Tag1",
    "RECO_VBFTOPO_JET3_LOWMJJ_Tag0:RECO_VBFTOPO_JET3_LOWMJJ_Tag0",
    "RECO_VBFTOPO_JET3_LOWMJJ_Tag1:RECO_VBFTOPO_JET3_LOWMJJ_Tag1",
    "RECO_VBFTOPO_VHHAD_Tag0:RECO_VBFTOPO_VHHAD_Tag0",
    "RECO_VBFTOPO_VHHAD_Tag1:RECO_VBFTOPO_VHHAD_Tag1",
    "RECO_WH_LEP_HIGH_Tag0:RECO_WH_LEP_HIGH_Tag0",
    "RECO_WH_LEP_HIGH_Tag1:RECO_WH_LEP_HIGH_Tag1",
    "RECO_WH_LEP_HIGH_Tag2:RECO_WH_LEP_HIGH_Tag2",
    "RECO_WH_LEP_LOW_Tag0:RECO_WH_LEP_LOW_Tag0",
    "RECO_WH_LEP_LOW_Tag1:RECO_WH_LEP_LOW_Tag1",
    "RECO_WH_LEP_LOW_Tag2:RECO_WH_LEP_LOW_Tag2",
    "RECO_ZH_LEP:RECO_ZH_LEP"
  ]
}
