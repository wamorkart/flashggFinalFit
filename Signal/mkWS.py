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

  tp_mass = ROOT.RooRealVar("tp_mass","tp_mass",125,110,180)
  tp_mass.setConstant(False)
  tp_mass.setBins(160)
  getattr(ws, 'import')(tp_mass, ROOT.RooFit.Silence())



def add_dataset_to_workspace(data=None,ws=None,name=None):

  arg_set = ROOT.RooArgSet(ws.var("weight"))
  variables = ["dZ_bdtVtx","tp_mass","centralObjectWeight","PreselSFUp01sigma","PreselSFDown01sigma","electronVetoSFUp01sigma","electronVetoSFDown01sigma","TriggerWeightUp01sigma","TriggerWeightDown01sigma"]

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
  variables = ["tp_mass"]
  for var in variables :
      arg_set.add(ws.var(var))

  #define roodataset to add to workspace
  roodatahist = ROOT.RooDataHist(name, name, arg_set)

  #Fill the dataset with values
  for index,row in data.iterrows():
    for var in variables:
        ws.var(var).setVal( row[ var ] )

        w_val = row['weight']

        roodatahist.add( arg_set, w_val )

  #Add to the workspace
  getattr(ws, 'import')(roodatahist)
  # print [name]
  return [name]

def get_options():

    parser = OptionParser()
    parser.add_option("--iD",type='string',dest="inp_dir",default='')
    parser.add_option("--i",type='string',dest='inp_files',default='h4g')
    parser.add_option("--m",type='string',dest='m',default='h4g')
    parser.add_option("--opt",type='string',dest="option",default='')
    parser.add_option("--t",type='string',dest="type",default='')
    parser.add_option("--year",type='string',dest="year",default='')
    # parser.add_option("--suf",type='string',dest="out_file_suf",default='')
    parser.add_option("--oD",type='string',dest="out_dir",default='')
    return parser.parse_args()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(opt,args) = get_options()

input_files = opt.inp_files.split(',')

systLabels = [""]
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

Cats = ['Cat0','Cat1','Cat2','Cat3','Cat4']
for num,f in enumerate(input_files):
 print 'input file: ',f
 tfile = ROOT.TFile(opt.inp_dir+f+'.root')
 datasets = []
 datahists = []
 ws = ROOT.RooWorkspace("cms_hgg_13TeV", "cms_hgg_13TeV")
 add_mc_vars_to_workspace( ws)
 treename = ""
 treelist = []
 for cat in Cats:
     if (opt.option == 'signal'):
        for sys_i,syst in enumerate(systLabels):
            systLabel = ""
            # print (syst)
            if syst != "":
               systLabel += '_' + syst
            if (opt.year == '2016'):
                treename = "SUSYGluGluToHToAA_AToGG_M_"+opt.m+"_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0"+systLabel+'_'+cat
            elif (opt.year == '2017'):
               treename = "SUSYGluGluToHToAA_AToGG_M_"+opt.m+"_TuneCP5_13TeV_pythia8_13TeV_H4GTag_0"+systLabel+'_'+cat
            elif (opt.year == '2018'):
               treename = "HAHMHToAA_AToGG_MA_"+opt.m+"GeV_TuneCP5_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0"+systLabel+'_'+cat
            treelist.append(treename)
     else:
         treename = "Data_13TeV_H4GTag_0"+'_'+cat
         treelist.append(treename)

 for tree_i, tree in enumerate(treelist):
     # print  tree
     newname = ''
     if ('H4GTag_0_Cat' in tree):
        data = pd.DataFrame(tree2array(tfile.Get(tree)))
     #    print treelist[0]
        print tree, "  # of events: ", tfile.Get(tree).GetEntries()
        # newname = ''
        if (opt.option == 'signal' and opt.year == '2016'):
            newname = tree.replace('SUSYGluGluToHToAA_AToGG_M_'+opt.m+'_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0','H4G')
        elif (opt.option == 'signal' and opt.year == '2017'):
            newname = tree.replace('SUSYGluGluToHToAA_AToGG_M_'+opt.m+'_TuneCP5_13TeV_pythia8_13TeV_H4GTag_0','H4G')
        elif (opt.option == 'signal' and opt.year == '2018'):
            newname = tree.replace('HAHMHToAA_AToGG_MA_'+opt.m+'GeV_TuneCP5_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0','H4G')
        print newname
        datasets += add_dataset_to_workspace(data,ws,newname)
     else:
         print "here ", tree
         data = pd.DataFrame(tree2array(tfile.Get(tree)))
         if (opt.option == 'signal' and opt.year == '2016'):
            newname = tree.replace('SUSYGluGluToHToAA_AToGG_M_'+opt.m+'_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0','H4G')
         elif (opt.option == 'signal' and opt.year == '2017'):
            newname = tree.replace('SUSYGluGluToHToAA_AToGG_M_'+opt.m+'_TuneCP5_13TeV_pythia8_13TeV_H4GTag_0','H4G')
         elif (opt.option == 'signal' and opt.year == '2018'):
            newname = tree.replace('HAHMHToAA_AToGG_MA_'+opt.m+'GeV_TuneCP5_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0','H4G')
         print newname
         datahists += add_datahist_to_workspace(data,ws,newname)


 dZ = ws.var('dZ_bdtVtx').clone('dZ')
 getattr(ws, 'import')(dZ, ROOT.RooFit.Silence())
 CMS_hgg_mass = ws.var('tp_mass').clone('CMS_hgg_mass')
 getattr(ws, 'import')(CMS_hgg_mass, ROOT.RooFit.Silence())
 for dataset in datasets:
     print dataset
     ws.data(dataset).changeObservableName('dZ_bdtVtx','dZ')
     ws.data(dataset).changeObservableName('tp_mass','CMS_hgg_mass')

 for datahist in datahists:
    print datahist
    ws.data(datahist).changeObservableName('tp_mass','CMS_hgg_mass')


 f_out = ROOT.TFile.Open(opt.out_dir+opt.inp_files+"_WS.root","RECREATE")
 dir_ws = f_out.mkdir("tagsDumper")
 dir_ws.cd()
 ws.Write()
 f_out.Close()
