import pandas as pd
import numpy as np
import ROOT
import json
from ROOT import *

from root_numpy import tree2array

from optparse import OptionParser

def add_mc_vars_to_workspace(ws=None):
  IntLumi = ROOT.RooRealVar("IntLumi","IntLumi",1000)
  IntLumi.setConstant(True)
  getattr(ws, 'import')(IntLumi, ROOT.RooFit.Silence())

  weight = ROOT.RooRealVar("weight","weight",1)
  weight.setConstant(False)
  getattr(ws, 'import')(weight, ROOT.RooFit.Silence())

  centralObjectWeight = ROOT.RooRealVar("centralObjectWeight","centralObjectWeight",1.0)
  centralObjectWeight.setConstant(False)
  getattr(ws, 'import')(centralObjectWeight, ROOT.RooFit.Silence())

  PreselSFUp01sigma = ROOT.RooRealVar("PreselSFUp01sigma","PreselSFUp01sigma",1.0)
  PreselSFUp01sigma.setConstant(False)
  getattr(ws, 'import')(PreselSFUp01sigma, ROOT.RooFit.Silence())

  PreselSFDown01sigma = ROOT.RooRealVar("PreselSFDown01sigma","PreselSFDown01sigma",1.0)
  PreselSFDown01sigma.setConstant(False)
  getattr(ws, 'import')(PreselSFDown01sigma, ROOT.RooFit.Silence())

  electronVetoSFUp01sigma = ROOT.RooRealVar("electronVetoSFUp01sigma","electronVetoSFUp01sigma",1.0)
  electronVetoSFUp01sigma.setConstant(False)
  getattr(ws, 'import')(electronVetoSFUp01sigma, ROOT.RooFit.Silence())

  electronVetoSFDown01sigma = ROOT.RooRealVar("electronVetoSFDown01sigma","electronVetoSFDown01sigma",1.0)
  electronVetoSFDown01sigma.setConstant(False)
  getattr(ws, 'import')(electronVetoSFDown01sigma, ROOT.RooFit.Silence())

  TriggerWeightUp01sigma = ROOT.RooRealVar("TriggerWeightUp01sigma","TriggerWeightUp01sigma",1.0)
  TriggerWeightUp01sigma.setConstant(False)
  getattr(ws, 'import')(TriggerWeightUp01sigma, ROOT.RooFit.Silence())

  TriggerWeightDown01sigma = ROOT.RooRealVar("TriggerWeightDown01sigma","TriggerWeightDown01sigma",1.0)
  TriggerWeightDown01sigma.setConstant(False)
  getattr(ws, 'import')(TriggerWeightDown01sigma, ROOT.RooFit.Silence())

  dZ_bdtVtx = ROOT.RooRealVar("dZ_bdtVtx","dZ_bdtVtx",0.0,-20,20)
  dZ_bdtVtx.setConstant(False)
  dZ_bdtVtx.setBins(40)
  getattr(ws, 'import')(dZ_bdtVtx, ROOT.RooFit.Silence())

  cat_MVA_value = ROOT.RooRealVar("bdt","bdt",1)
  cat_MVA_value.setConstant(False)
  getattr(ws, 'import')(cat_MVA_value, ROOT.RooFit.Silence())

  tp_mass = ROOT.RooRealVar("tp_mass","tp_mass",125,110,180)
  tp_mass.setConstant(False)
  getattr(ws, 'import')(tp_mass, ROOT.RooFit.Silence())

  pho1_pt = ROOT.RooRealVar("pho1_pt","pho1_pt",1)
  pho1_pt.setConstant(False)
  getattr(ws, 'import')(pho1_pt, ROOT.RooFit.Silence())

  pho2_pt = ROOT.RooRealVar("pho2_pt","pho2_pt",1)
  pho2_pt.setConstant(False)
  getattr(ws, 'import')(pho2_pt, ROOT.RooFit.Silence())

  pho3_pt = ROOT.RooRealVar("pho3_pt","pho3_pt",1)
  pho3_pt.setConstant(False)
  getattr(ws, 'import')(pho3_pt, ROOT.RooFit.Silence())

  pho4_pt = ROOT.RooRealVar("pho4_pt","pho4_pt",1)
  pho4_pt.setConstant(False)
  getattr(ws, 'import')(pho4_pt, ROOT.RooFit.Silence())

  pho1_eta = ROOT.RooRealVar("pho1_eta","pho1_eta",1)
  pho1_eta.setConstant(False)
  getattr(ws, 'import')(pho1_eta, ROOT.RooFit.Silence())

  pho2_eta = ROOT.RooRealVar("pho2_eta","pho2_eta",1)
  pho2_eta.setConstant(False)
  getattr(ws, 'import')(pho2_eta, ROOT.RooFit.Silence())

  pho3_eta = ROOT.RooRealVar("pho3_eta","pho3_eta",1)
  pho3_eta.setConstant(False)
  getattr(ws, 'import')(pho3_eta, ROOT.RooFit.Silence())

  pho4_eta = ROOT.RooRealVar("pho4_eta","pho4_eta",1)
  pho4_eta.setConstant(False)
  getattr(ws, 'import')(pho4_eta, ROOT.RooFit.Silence())

  pho1_electronveto = ROOT.RooRealVar("pho1_electronveto","pho1_electronveto",1)
  pho1_electronveto.setConstant(False)
  getattr(ws, 'import')(pho1_electronveto, ROOT.RooFit.Silence())

  pho2_electronveto = ROOT.RooRealVar("pho2_electronveto","pho2_electronveto",1)
  pho2_electronveto.setConstant(False)
  getattr(ws, 'import')(pho2_electronveto, ROOT.RooFit.Silence())

  pho3_electronveto = ROOT.RooRealVar("pho3_electronveto","pho3_electronveto",1)
  pho3_electronveto.setConstant(False)
  getattr(ws, 'import')(pho3_electronveto, ROOT.RooFit.Silence())

  pho4_electronveto = ROOT.RooRealVar("pho4_electronveto","pho4_electronveto",1)
  pho4_electronveto.setConstant(False)
  getattr(ws, 'import')(pho4_electronveto, ROOT.RooFit.Silence())


def add_dataset_to_workspace(data=None,ws=None,name=None):

  arg_set = ROOT.RooArgSet(ws.var("weight"))
  variables = ["dZ_bdtVtx","tp_mass","bdt","centralObjectWeight","PreselSFUp01sigma","PreselSFDown01sigma","electronVetoSFUp01sigma","electronVetoSFDown01sigma","TriggerWeightUp01sigma","TriggerWeightDown01sigma","pho1_pt","pho2_pt","pho3_pt","pho4_pt","pho1_eta","pho2_eta","pho3_eta","pho4_eta","pho1_electronveto","pho2_electronveto","pho3_electronveto","pho4_electronveto"]

  for var in variables :
      arg_set.add(ws.var(var))

  #define roodataset to add to workspace
  roodataset = ROOT.RooDataSet (name, name, arg_set, "weight" )

  #Fill the dataset with values
  for index,row in data.iterrows():
    for var in variables:
        ws.var(var).setVal( row[ var ] )

    w_val = row['weight']

    roodataset.add( arg_set, w_val )

  #Add to the workspace
  getattr(ws, 'import')(roodataset)
  # print [name]
  return [name]

def add_datahist_to_workspace(data=None,ws=None,name=None):

  # arg_set = ROOT.RooArgSet(ws.var("weight"))
  arg_set = ROOT.RooArgSet()
  variables = ["tp_mass","bdt","pho1_pt","pho2_pt","pho3_pt","pho4_pt","pho1_eta","pho2_eta","pho3_eta","pho4_eta","pho1_electronveto","pho2_electronveto","pho3_electronveto","pho4_electronveto"]
  # variables = ["tp_mass"]
  for var in variables :
      arg_set.add(ws.var(var))

  #define roodataset to add to workspace
  # roodataset = ROOT.RooDataHist (name, name, arg_set, "weight" )
  roodataset = ROOT.RooDataHist(name, name, arg_set)

  #Fill the dataset with values
  for index,row in data.iterrows():
    for var in variables:
        ws.var(var).setVal( row[ var ] )

    w_val = row['weight']

    roodataset.add( arg_set, w_val )

  #Add to the workspace
  getattr(ws, 'import')(roodataset)
  # print [name]
  return [name]

def get_options():

    parser = OptionParser()
    parser.add_option("--iD",type='string',dest="inp_dir",default='')
    parser.add_option("--i",type='string',dest='inp_files',default='h4g')
    parser.add_option("--m",type='string',dest='m',default='h4g')
    parser.add_option("--v",type='string',dest='var',default='h4g')
    parser.add_option("--opt",type='string',dest="option",default='')
    parser.add_option("--t",type='string',dest="type",default='')
    parser.add_option("--nCat",type='string',dest="nCat",default='')
    parser.add_option("--year",type='string',dest="year",default='')
    parser.add_option("--suf",type='string',dest="out_file_suf",default='')
    parser.add_option("--oD",type='string',dest="out_dir",default='')
    return parser.parse_args()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(opt,args) = get_options()

input_files = opt.inp_files.split(',')
input_names = []
target_names = []
target_files = []

for num,f in enumerate(input_files):
   name=f
   # print "input file: ",f
   target_names.append(f+'_WS')
   target_files.append('output_'+f+'_WS_'+str(opt.out_file_suf))

cut_list = []

nCat_file = open(opt.nCat,"r")
nCat_list = []
for word in nCat_file.read().split():
    nCat_list.append(word)

print (nCat_list)
nCat = len(nCat_list)

if (nCat == 3):
    print "2 categories"

    cut_list.append(opt.var+'>='+str(nCat_list[nCat-2]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-2]))

if (nCat==4):
    print "3 categories"
    cut_list.append(opt.var+'>='+str(nCat_list[nCat-2]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-2])+'&&'+opt.var+'>='+str(nCat_list[nCat-3]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-3]))

if (nCat==5):
    print "4 categories"
    cut_list.append(opt.var+'>='+str(nCat_list[nCat-2]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-2])+'&&'+opt.var+'>='+str(nCat_list[nCat-3]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-3])+'&&'+opt.var+'>='+str(nCat_list[nCat-4]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-4]))

if (nCat==6):
    print "5 categories"
    cut_list.append(opt.var+'>='+str(nCat_list[nCat-2]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-2])+'&&'+opt.var+'>='+str(nCat_list[nCat-3]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-3])+'&&'+opt.var+'>='+str(nCat_list[nCat-4]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-4])+'&&'+opt.var+'>='+str(nCat_list[nCat-5]))
    cut_list.append(opt.var+'<'+str(nCat_list[nCat-5]))

# common_cut = 'pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1&& pho4_electronveto==1  && tp_mass > 110 && tp_mass < 180'
common_cut = '1'
systLabels = [""]
for direction in ["Up","Down"]:
           systLabels.append("MvaShift%s01sigma"%direction)
           #systLabels.append("SigmaEOverEShift%s01sigma"%direction)
           #systLabels.append("MaterialCentralBarrel%s01sigma"%direction)
           #systLabels.append("MaterialOuterBarrel%s01sigma"%direction)
           #systLabels.append("MaterialForward%s01sigma"%direction)
           #systLabels.append("FNUFEB%s01sigma"%direction)
           #systLabels.append("FNUFEE%s01sigma"%direction)
           #systLabels.append("MCScaleGain6EB%s01sigma"%direction)
           #systLabels.append("MCScaleGain1EB%s01sigma"%direction)
           #systLabels.append("MCScaleGain1EB%s01sigma"%direction)
           #systLabels.append("MCScaleHighR9EB%s01sigma" % direction)
           #systLabels.append("MCScaleHighR9EE%s01sigma" % direction)
           #systLabels.append("MCScaleLowR9EB%s01sigma" % direction)
           #systLabels.append("MCScaleLowR9EE%s01sigma" % direction)
           #systLabels.append("MCSmearHighR9EBPhi%s01sigma" % direction)
           #systLabels.append("MCSmearHighR9EBRho%s01sigma" % direction)
           #systLabels.append("MCSmearHighR9EEPhi%s01sigma" % direction)
           #systLabels.append("MCSmearHighR9EERho%s01sigma" % direction)
           #systLabels.append("MCSmearLowR9EBPhi%s01sigma" % direction)
           #systLabels.append("MCSmearLowR9EBRho%s01sigma" % direction)
           #systLabels.append("MCSmearLowR9EEPhi%s01sigma" % direction)
           #systLabels.append("MCSmearLowR9EERho%s01sigma" % direction)
           #systLabels.append("ShowerShapeHighR9EB%s01sigma" % direction)
           #systLabels.append("ShowerShapeHighR9EE%s01sigma" % direction)
           #systLabels.append("ShowerShapeLowR9EB%s01sigma" % direction)
           #systLabels.append("ShowerShapeLowR9EE%s01sigma" % direction)
           #systLabels.append("SigmaEOverEShift%s01sigma" % direction)

for num,f in enumerate(input_files):
 print 'input file: ',f
 tfile = ROOT.TFile(opt.inp_dir+f+'.root')
 datasets = []
 datahists = []
 ws = ROOT.RooWorkspace("cms_hgg_13TeV", "cms_hgg_13TeV")
 add_mc_vars_to_workspace( ws)
 treename = ""
 treelist = []
 if (opt.option == 'signal'):
    for sys_i,syst in enumerate(systLabels):
        systLabel = ""
        print (syst)
        if syst != "":
           systLabel += '_' + syst
        if (opt.year == '2016'):
            treename = "tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_"+opt.m+"_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0"+systLabel
            print "tree: ", treename
            treelist.append(treename)
           # treename = "tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_"+opt.m+"_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0"
        # elif (opt.year == '2017'):
           # treename = "tagsDumper/trees/SUSYGluGluToHToAA_AToGG_M_"+opt.m+"_TuneCP5_13TeV_pythia8_13TeV_H4GTag_0"
        # elif (opt.year == '2018'):
           # treename = "tagsDumper/trees/HAHMHToAA_AToGG_MA_"+opt.m+"GeV_TuneCP5_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0"
 else: treename = "tagsDumper/trees/Data_13TeV_H4GTag_0"
 print treelist

 # data = pd.DataFrame(tree2array(tfile.Get(treename)))
 for tree_i, tree in enumerate(treelist):
     if (tree_i==0):
        data = pd.DataFrame(tree2array(tfile.Get(treelist[0])))
        newname = 'H4G'
        datasets += add_dataset_to_workspace(data,ws,newname)
     else:
        data = pd.DataFrame(tree2array(tfile.Get(treelist[tree_i])))
        newname = 'H4G_'+systLabels[tree_i]
        datahists += add_datahist_to_workspace(data,ws,newname)


 for dataset in datasets:
     dataset_list = []
     for icat, cat in enumerate(cut_list):
         Cat_name = ''
         if (opt.type=='Run2'):
            Cat_name = '_Cat' + str(icat)
         else: Cat_name = '_Cat' + str(icat)+'_'+str(opt.year)
         print "Cat_name: ", Cat_name
         temp_dataset = ws.data(dataset).Clone(dataset+Cat_name)
         dataset_cut = common_cut + '&&' + cut_list[icat]
         print "Cut: ", dataset_cut
         temp_dataset_reduced = temp_dataset.reduce(dataset_cut)
         temp_dataset_reduced.Print()
         temp_dataset_reduced.changeObservableName('dZ_bdtVtx','dZ')
         temp_dataset_reduced.changeObservableName('tp_mass','CMS_hgg_mass')
         print temp_dataset_reduced.numEntries()
         dataset_list.append(temp_dataset_reduced)

     # print "dataset_list: ", dataset_list
     for d in range(0,len(dataset_list)):
         getattr(ws, 'import')(dataset_list[d])

 for datahist in datahists:
     datahist_list = []
     for icat, cat in enumerate(cut_list):
        Cat_name = ''
        if (opt.type=='Run2'):
           Cat_name = '_Cat' + str(icat)
        else: Cat_name = '_Cat' + str(icat)+'_'+str(opt.year)
        print "Cat_name: ", Cat_name
        temp_datahist = ws.data(datahist).Clone(datahist+Cat_name)
        print temp_datahist.numEntries()
        # datahist_cut = common_cut + '&&' + cut_list[icat]
        # datahist_cut = 'pho1_MVA > 0'
        # print "Cut: ", datahist_cut
        temp_datahist_reduced = temp_datahist#.reduce(datahist_cut)
        temp_datahist_reduced.Print()
        temp_datahist_reduced.changeObservableName('tp_mass','CMS_hgg_mass')

        print temp_datahist_reduced.numEntries()
        datahist_list.append(temp_datahist_reduced)

    # print "dataset_list: ", dataset_list
     for d in range(0,len(datahist_list)):
         getattr(ws, 'import')(datahist_list[d])

 f_out = ROOT.TFile.Open("%s/%s.root"%(opt.out_dir,target_files[num]),"RECREATE")
 dir_ws = f_out.mkdir("tagsDumper")
 dir_ws.cd()
 ws.Write()
 f_out.Close()
