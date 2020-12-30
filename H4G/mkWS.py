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

  prefireWeightDown01sigma = ROOT.RooRealVar("prefireWeightDown01sigma","prefireWeightDown01sigma",1.0)
  prefireWeightDown01sigma.setConstant(False)
  getattr(ws, 'import')(prefireWeightDown01sigma, ROOT.RooFit.Silence())

  prefireWeightUp01sigma = ROOT.RooRealVar("prefireWeightUp01sigma","prefireWeightUp01sigma",1.0)
  prefireWeightUp01sigma.setConstant(False)
  getattr(ws, 'import')(prefireWeightUp01sigma, ROOT.RooFit.Silence())

  dZ_bdtVtx = ROOT.RooRealVar("dZ_bdtVtx","dZ_bdtVtx",0.0,-20,20)
  dZ_bdtVtx.setConstant(False)
  dZ_bdtVtx.setBins(40)
  getattr(ws, 'import')(dZ_bdtVtx, ROOT.RooFit.Silence())

  tp_mass = ROOT.RooRealVar("tp_mass","tp_mass",125,100,180)
  tp_mass.setConstant(False)
  tp_mass.setBins(160)
  getattr(ws, 'import')(tp_mass, ROOT.RooFit.Silence())


def add_data_vars_to_workspace(ws=None):
  IntLumi = ROOT.RooRealVar("IntLumi","IntLumi",1000)
  IntLumi.setConstant(True)
  getattr(ws, 'import')(IntLumi, ROOT.RooFit.Silence())

  weight = ROOT.RooRealVar("weight","weight",1)
  weight.setConstant(False)
  getattr(ws, 'import')(weight, ROOT.RooFit.Silence())

  dZ_bdtVtx = ROOT.RooRealVar("dZ_bdtVtx","dZ_bdtVtx",0.0,-20,20)
  dZ_bdtVtx.setConstant(False)
  dZ_bdtVtx.setBins(40)
  getattr(ws, 'import')(dZ_bdtVtx, ROOT.RooFit.Silence())

  tp_mass = ROOT.RooRealVar("tp_mass","tp_mass",125,100,180)
  tp_mass.setConstant(False)
  tp_mass.setBins(160)
  getattr(ws, 'import')(tp_mass, ROOT.RooFit.Silence())



def add_dataset_to_workspace(data=None,ws=None,name=None,year=None):

  arg_set = ROOT.RooArgSet(ws.var("weight"))
  variables = []
  if (year=="2018"):
        variables = ["dZ_bdtVtx","tp_mass","centralObjectWeight","PreselSFUp01sigma","PreselSFDown01sigma","electronVetoSFUp01sigma","electronVetoSFDown01sigma","TriggerWeightUp01sigma","TriggerWeightDown01sigma"]
  else:
        variables = ["dZ_bdtVtx","tp_mass","centralObjectWeight","PreselSFUp01sigma","PreselSFDown01sigma","electronVetoSFUp01sigma","electronVetoSFDown01sigma","TriggerWeightUp01sigma","TriggerWeightDown01sigma","prefireWeightDown01sigma","prefireWeightUp01sigma"]

  for var in variables :
      arg_set.add(ws.var(var))

  #define roodataset to add to workspace
  roodataset = ROOT.RooDataSet (name, name, arg_set, "weight" )


  #Fill the dataset with values
  for index,row in data.iterrows():
    for var in variables:
        ws.var(var).setVal( row[ var ] )

    w_val = 2*row['weight']

    roodataset.add( arg_set, w_val )
  #Add to the workspace

  getattr(ws, 'import')(roodataset)
  # print [name]
  return [name]

def add_dataset_to_workspace_data(data=None,ws=None,name=None):

  arg_set = ROOT.RooArgSet()
  variables = ["dZ_bdtVtx","tp_mass"]

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

        w_val = 2*row['weight']

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
    parser.add_option("--s",type='string',dest='systematics',default='0')
    parser.add_option("--nCat",type='string',dest='nCat',default='0')
    parser.add_option("--oD",type='string',dest="out_dir",default='')
    return parser.parse_args()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(opt,args) = get_options()

input_files = opt.inp_files.split(',')

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

Cats = []
for i in range(0, int(opt.nCat)):
    Cats.append('Cat'+str(i))

for num,f in enumerate(input_files):
 # print 'input file: ',f
 tfile = ROOT.TFile(opt.inp_dir+f+'.root')
 datasets = []
 datahists = []
 ws = ROOT.RooWorkspace("cms_hgg_13TeV", "cms_hgg_13TeV")
 if (opt.option == 'signal'):
     add_mc_vars_to_workspace( ws)
 else: add_data_vars_to_workspace(ws)
 treename = ""
 treelist = []
 for cat in Cats:
     if (opt.option == 'signal'):
        for sys_i,syst in enumerate(systLabels):
            systLabel = ""
            if syst != "":
               systLabel += '_' + syst
            treename = "H4GTag_"+cat+systLabel+"_13TeV"

            treelist.append(treename)
     else:
         treename = "H4GTag_"+cat+"_13TeV"
         treelist.append(treename)
 # print treelist
 for tree_i, tree in enumerate(treelist):
     # print  tree
     newname = ''
     if (opt.option == 'data'):
     # if ('Data' in tree):
         data = pd.DataFrame(tree2array(tfile.Get(tree)))
         newname = 'Data_13TeV_H4GTag_'+Cats[tree_i]
         datasets += add_dataset_to_workspace_data(data,ws,newname)

     else:
        # print tree
        if ('sigma' in tree):
           # print "here"
           data = pd.DataFrame(tree2array(tfile.Get(tree)))
           # newname = tree.replace('H4GTag_0_','H4G_')
           if (opt.option == 'signal' and opt.year == '2016'):
               newname = tree.replace('HAHMHToAA_AToGG_MA_'+opt.m+'GeV_TuneCUETP8M1_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_','H4GTag_')
           elif (opt.option == 'signal' and opt.year == '2017'):
               newname = tree.replace('HAHMHToAA_AToGG_MA_'+opt.m+'GeV_TuneCP5_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_','H4GTag_')
           elif (opt.option == 'signal' and opt.year == '2018'):
               newname = tree.replace('HAHMHToAA_AToGG_MA_'+opt.m+'GeV_TuneCP5_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_','H4GTag_')
           # print "newname", newname
           if (opt.type=='Run2'):
              datahists += add_datahist_to_workspace(data,ws,newname)
           else: datahists += add_datahist_to_workspace(data,ws,newname+'_'+str(opt.year))
        else:

            data = pd.DataFrame(tree2array(tfile.Get(tree)))
            if(opt.type=='Run2'):
                datasets += add_dataset_to_workspace(data,ws,tree, str(opt.year))
            else:datasets += add_dataset_to_workspace(data,ws,tree+'_'+str(opt.year),str(opt.year))
 dZ = ws.var('dZ_bdtVtx').clone('dZ')
 getattr(ws, 'import')(dZ, ROOT.RooFit.Silence())
 CMS_hgg_mass = ws.var('tp_mass').clone('CMS_hgg_mass')
 getattr(ws, 'import')(CMS_hgg_mass, ROOT.RooFit.Silence())
 for dataset in datasets:
     #print "roodataset numentries: ", ws.data(dataset).numEntries()
     ws.data(dataset).changeObservableName('dZ_bdtVtx','dZ')
     ws.data(dataset).changeObservableName('tp_mass','CMS_hgg_mass')

 for datahist in datahists:
    # print datahist
    ws.data(datahist).changeObservableName('tp_mass','CMS_hgg_mass')


 f_out = ROOT.TFile.Open(opt.out_dir+opt.inp_files+"_WS.root","RECREATE")
 dir_ws = f_out.mkdir("tagsDumper")
 dir_ws.cd()
 ws.Write()
 f_out.Close()
