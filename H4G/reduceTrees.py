# from ROOT import *
import ROOT
from optparse import OptionParser

def get_options():

    parser = OptionParser()
    parser.add_option("--iD",type='string',dest="inp_dir",default='')
    parser.add_option("--i",type='string',dest='inp_files',default='h4g')
    parser.add_option("--m",type='string',dest='m',default='h4g')
    parser.add_option("--s",type='string',dest='systematics',default='0')
    parser.add_option("--opt",type='string',dest="option",default='')
    parser.add_option("--nCat",type='string',dest="nCat",default='')
    parser.add_option("--year",type='string',dest="year",default='')
    parser.add_option("--oD",type='string',dest="out_dir",default='')
    parser.add_option("--v",type='string',dest='var',default='bdt')
    return parser.parse_args()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(opt,args) = get_options()

input_files = opt.inp_files.split(',')
input_names = []

cut_list = []

nCat_file = open(opt.nCat,'r')
nCat_list = []
nCat_list_tmp = []
for ln in nCat_file:
    if (len(ln.split())>0):
        if not ln.startswith("Tot_Significance:"):
           nCat_list_tmp.append(ln.split()[0])
           nCat_list_tmp.append(ln.split()[1])


for i in nCat_list_tmp:
    if i not in nCat_list:
        nCat_list.append(i)
nCat = len(nCat_list)
print nCat_list
if (nCat == 2):
    print "1 category"
    cut_list.append(opt.var+'>='+str(nCat_list[nCat-2]))
if (nCat == 3):
    print "2 categories"

    cut_list.append(opt.var+'>='+str(nCat_list[nCat-2]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-2]+'&&'+opt.var+'>='+str(nCat_list[nCat-3])))

if (nCat==4):
    print "3 categories"
    cut_list.append(opt.var+'>='+str(nCat_list[nCat-2]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-2])+'&&'+opt.var+'>='+str(nCat_list[nCat-3]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-3]+'&&'+opt.var+'>='+str(nCat_list[nCat-4])))

if (nCat==5):
    print "4 categories"
    cut_list.append(opt.var+'>='+str(nCat_list[nCat-2]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-2])+'&&'+opt.var+'>='+str(nCat_list[nCat-3]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-3])+'&&'+opt.var+'>='+str(nCat_list[nCat-4]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-4]+'&&'+opt.var+'>='+str(nCat_list[nCat-5])))

if (nCat==6):
    print "5 categories"
    cut_list.append(opt.var+'>='+str(nCat_list[nCat-2]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-2])+'&&'+opt.var+'>='+str(nCat_list[nCat-3]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-3])+'&&'+opt.var+'>='+str(nCat_list[nCat-4]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-4])+'&&'+opt.var+'>='+str(nCat_list[nCat-5]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-5]+'&&'+opt.var+'>='+str(nCat_list[nCat-6])))

print cut_list
systLabels = [""]
if (opt.systematics=="1"):
   for direction in ["Up","Down"]:
           systLabels.append("MvaShift%s01sigma"%direction)
           systLabels.append("SigmaEOverEShift%s01sigma"%direction)
           systLabels.append("MaterialCentralBarrel%s01sigma"%direction)
           systLabels.append("MaterialOuterBarrel%s01sigma"%direction)
           systLabels.append("MaterialForward%s01sigma"%direction)
           systLabels.append("FNUFEB%s01sigma"%direction)
           systLabels.append("FNUFEE%s01sigma"%direction)
           systLabels.append("MCScaleGain6EB%s01sigma"%direction)
           systLabels.append("MCScaleGain1EB%s01sigma"%direction)
           systLabels.append("MCScaleGain1EB%s01sigma"%direction)
           systLabels.append("MCScaleHighR9EB%s01sigma" % direction)
           systLabels.append("MCScaleHighR9EE%s01sigma" % direction)
           systLabels.append("MCScaleLowR9EB%s01sigma" % direction)
           systLabels.append("MCScaleLowR9EE%s01sigma" % direction)
           systLabels.append("MCSmearHighR9EBPhi%s01sigma" % direction)
           systLabels.append("MCSmearHighR9EBRho%s01sigma" % direction)
           systLabels.append("MCSmearHighR9EEPhi%s01sigma" % direction)
           systLabels.append("MCSmearHighR9EERho%s01sigma" % direction)
           systLabels.append("MCSmearLowR9EBPhi%s01sigma" % direction)
           systLabels.append("MCSmearLowR9EBRho%s01sigma" % direction)
           systLabels.append("MCSmearLowR9EEPhi%s01sigma" % direction)
           systLabels.append("MCSmearLowR9EERho%s01sigma" % direction)
           systLabels.append("ShowerShapeHighR9EB%s01sigma" % direction)
           systLabels.append("ShowerShapeHighR9EE%s01sigma" % direction)
           systLabels.append("ShowerShapeLowR9EB%s01sigma" % direction)
           systLabels.append("ShowerShapeLowR9EE%s01sigma" % direction)
           systLabels.append("SigmaEOverEShift%s01sigma" % direction)

for num,f in enumerate(input_files):
 print 'input file: ',f
 tfile = ROOT.TFile(opt.inp_dir+f+'.root')
 treename = ""
 treelist = []
 if (opt.option == 'signal'):
    for sys_i,syst in enumerate(systLabels):
        systLabel = ""
        if syst != "":
           systLabel += '_' + syst
        if (opt.year == '2016'):
            treename = "HAHMHToAA_AToGG_MA_"+opt.m+"GeV_TuneCUETP8M1_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0"+systLabel
        elif (opt.year == '2017' or opt.year == '2018'):
           treename = "HAHMHToAA_AToGG_MA_"+opt.m+"GeV_TuneCP5_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0"+systLabel

        treelist.append(treename)

 elif ('QCD_30to40' in f):
     if (opt.year == "2016"):
         treename = "QCD_Pt_30to40_DoubleEMEnriched_MGG_80toInf_TuneCUETP8M1_13TeV_Pythia8_13TeV_H4GTag_0"
     elif (opt.year ==  "2017" or opt.year =="2018"):
         treename = "QCD_Pt_30to40_DoubleEMEnriched_MGG_80toInf_TuneCP5_13TeV_Pythia8_13TeV_H4GTag_0"
 elif ('QCD_30toInf' in f):
     if (opt.year == "2016"):
         treename = "QCD_Pt_30toInf_DoubleEMEnriched_MGG_40to80_TuneCUETP8M1_13TeV_Pythia8_13TeV_H4GTag_0"
     elif (opt.year ==  "2017" or opt.year =="2018"):
         treename = "QCD_Pt_30toInf_DoubleEMEnriched_MGG_40to80_TuneCP5_13TeV_Pythia8_13TeV_H4GTag_0"

 elif ('QCD_40toInf' in f):
     if (opt.year == "2016"):
         treename = "QCD_Pt_40toInf_DoubleEMEnriched_MGG_80toInf_TuneCUETP8M1_13TeV_Pythia8_13TeV_H4GTag_0"
     elif (opt.year ==  "2017" or opt.year =="2018"):
         treename = "QCD_Pt_40toInf_DoubleEMEnriched_MGG_80toInf_TuneCP5_13TeV_Pythia8_13TeV_H4GTag_0"
 elif ('GJet_20to40' in f):
     if (opt.year == "2016"):
         treename = "GJet_Pt_20to40_DoubleEMEnriched_MGG_80toInf_TuneCUETP8M1_13TeV_Pythia8_13TeV_H4GTag_0"
     elif (opt.year ==  "2017" or opt.year =="2018"):
         treename = "GJet_Pt_20to40_DoubleEMEnriched_MGG_80toInf_TuneCP5_13TeV_Pythia8_13TeV_H4GTag_0"
 elif ('GJet_20toInf' in f):
     if (opt.year == "2016"):
         treename = "GJet_Pt_20toInf_DoubleEMEnriched_MGG_40to80_TuneCUETP8M1_13TeV_Pythia8_13TeV_H4GTag_0"
     elif (opt.year ==  "2017" or opt.year =="2018"):
         treename = "GJet_Pt_20toInf_DoubleEMEnriched_MGG_40to80_TuneCP5_13TeV_Pythia8_13TeV_H4GTag_0"
 elif ('GJet_40toInf' in f):
     if (opt.year == "2016"):
         treename = "GJet_Pt_40toInf_DoubleEMEnriched_MGG_80toInf_TuneCUETP8M1_13TeV_Pythia8_13TeV_H4GTag_0"
     elif (opt.year ==  "2017" or opt.year =="2018"):
         treename = "GJet_Pt_40toInf_DoubleEMEnriched_MGG_80toInf_TuneCP5_13TeV_Pythia8_13TeV_H4GTag_0"
 elif ('DiPho_40to80' in f):
     treename = "DiPhotonJetsBox_M40_80_Sherpa_13TeV_H4GTag_0"
 elif ('DiPho_80toInf' in f):
     treename = "DiPhotonJetsBox_MGG_80toInf_13TeV_Sherpa_13TeV_H4GTag_0"
 else:
     treename = "Data_13TeV_H4GTag_0"
     treelist.append(treename)

 # print treelist
 f_out = ROOT.TFile.Open(opt.out_dir+opt.inp_files+'_skim.root','RECREATE')
 # common_cut = '(weight)*(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1&& pho4_electronveto==1  && tp_mass > 110 && tp_mass < 180)'
 common_cut = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1&& pho4_electronveto==1  && tp_mass > 100 && tp_mass < 180)'
 # common_cut = '(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1&& pho4_electronveto==1  && tp_mass > 100 && tp_mass < 180 && abs(a1_mass_dM-'+str(opt.m)+')<'+str(float(0.15*float(opt.m)))+'&& abs(a2_mass_dM-'+str(opt.m)+')<'+str(float(0.15*float(opt.m)))+')'
 # print (common_cut)
 for tree_i, tree in enumerate(treelist):
     ntuple = tfile.Get(treelist[tree_i])
     for icat, cat in enumerate(cut_list):
         small = ntuple.CopyTree(common_cut+'&&'+cut_list[icat])
         if (tree_i == 0):
             treename_tmp = 'H4GTag_Cat'+str(icat)+'_13TeV'
         else: treename_tmp = 'H4GTag_Cat'+str(icat)+'_'+systLabels[tree_i]+'_13TeV'

         small.SetName(treename_tmp)
         small.SetTitle(treename_tmp)
f_out.Write()
