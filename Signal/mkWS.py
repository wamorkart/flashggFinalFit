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
  getattr(ws, 'import')(IntLumi)

  weight = ROOT.RooRealVar("weight","weight",1)
  weight.setConstant(False)
  getattr(ws, 'import')(weight)

  dZ_bdtVtx = ROOT.RooRealVar("dZ_bdtVtx","dZ_bdtVtx",0.0,-20,20)
  dZ_bdtVtx.setConstant(False)
  dZ_bdtVtx.setBins(40)
  getattr(ws, 'import')(dZ_bdtVtx)

  pho1_MVA = ROOT.RooRealVar("pho1_MVA","pho1_MVA",1)
  pho1_MVA.setConstant(False)
  getattr(ws, 'import')(pho1_MVA)

  pho2_MVA = ROOT.RooRealVar("pho2_MVA","pho2_MVA",1)
  pho2_MVA.setConstant(False)
  getattr(ws, 'import')(pho2_MVA)

  pho3_MVA = ROOT.RooRealVar("pho3_MVA","pho3_MVA",1)
  pho3_MVA.setConstant(False)
  getattr(ws, 'import')(pho3_MVA)

  pho4_MVA = ROOT.RooRealVar("pho4_MVA","pho4_MVA",1)
  pho4_MVA.setConstant(False)
  getattr(ws, 'import')(pho4_MVA)

  pho1_pt = ROOT.RooRealVar("pho1_pt","pho1_pt",1)
  pho1_pt.setConstant(False)
  getattr(ws, 'import')(pho1_pt)

  pho2_pt = ROOT.RooRealVar("pho2_pt","pho2_pt",1)
  pho2_pt.setConstant(False)
  getattr(ws, 'import')(pho2_pt)

  pho3_pt = ROOT.RooRealVar("pho3_pt","pho3_pt",1)
  pho3_pt.setConstant(False)
  getattr(ws, 'import')(pho3_pt)

  pho4_pt = ROOT.RooRealVar("pho4_pt","pho4_pt",1)
  pho4_pt.setConstant(False)
  getattr(ws, 'import')(pho4_pt)

  pho1_eta = ROOT.RooRealVar("pho1_eta","pho1_eta",1)
  pho1_eta.setConstant(False)
  getattr(ws, 'import')(pho1_eta)

  pho2_eta = ROOT.RooRealVar("pho2_eta","pho2_eta",1)
  pho2_eta.setConstant(False)
  getattr(ws, 'import')(pho2_eta)

  pho3_eta = ROOT.RooRealVar("pho3_eta","pho3_eta",1)
  pho3_eta.setConstant(False)
  getattr(ws, 'import')(pho3_eta)

  pho4_eta = ROOT.RooRealVar("pho4_eta","pho4_eta",1)
  pho4_eta.setConstant(False)
  getattr(ws, 'import')(pho4_eta)

  pho1_electronveto = ROOT.RooRealVar("pho1_electronveto","pho1_electronveto",1)
  pho1_electronveto.setConstant(False)
  getattr(ws, 'import')(pho1_electronveto)

  pho2_electronveto = ROOT.RooRealVar("pho2_electronveto","pho2_electronveto",1)
  pho2_electronveto.setConstant(False)
  getattr(ws, 'import')(pho2_electronveto)

  pho3_electronveto = ROOT.RooRealVar("pho3_electronveto","pho3_electronveto",1)
  pho3_electronveto.setConstant(False)
  getattr(ws, 'import')(pho3_electronveto)

  pho4_electronveto = ROOT.RooRealVar("pho4_electronveto","pho4_electronveto",1)
  pho4_electronveto.setConstant(False)
  getattr(ws, 'import')(pho4_electronveto)

  #cat_MVA_value_oldmethod = ROOT.RooRealVar("cat_MVA_value_oldmethod","cat_MVA_value_oldmethod",1)
  #cat_MVA_value_oldmethod.setConstant(False)
  # getattr(ws, 'import')(cat_MVA_value_oldmethod)

  cat_MVA_value = ROOT.RooRealVar("bdt","bdt",1)
  cat_MVA_value.setConstant(False)
  getattr(ws, 'import')(cat_MVA_value)

  cat_MVA_transformed_value = ROOT.RooRealVar("bdtTransformed","bdtTransformed",1)
  cat_MVA_transformed_value.setConstant(False)
  getattr(ws, 'import')(cat_MVA_transformed_value)

  tp_mass = ROOT.RooRealVar("tp_mass","tp_mass",125,110,180)
  tp_mass.setConstant(False)
  getattr(ws, 'import')(tp_mass)


def add_dataset_to_workspace(data=None,ws=None,name=None):

  arg_set = ROOT.RooArgSet(ws.var("weight"))
  # variables = ["dZ_bdtVtx","cat_MVA_value_oldmethod","tp_mass"]
  # variables = ["dZ_bdtVtx","cat_MVA_value","tp_mass"]
  variables = ["dZ_bdtVtx","tp_mass","pho1_MVA","pho2_MVA","pho3_MVA","pho4_MVA","pho1_pt","pho2_pt","pho3_pt","pho4_pt","pho1_eta","pho2_eta","pho3_eta","pho4_eta","pho1_electronveto","pho2_electronveto","pho3_electronveto","pho4_electronveto","bdt","bdtTransformed"]

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
  # print "HERE 1"
  print [name]
  return [name]

def get_options():

    parser = OptionParser()
    parser.add_option("--iD",type='string',dest="inp_dir",default='')
    parser.add_option("--i",type='string',dest='inp_files',default='h4g')
    parser.add_option("--m",type='string',dest='m',default='h4g')
    parser.add_option("--v",type='string',dest='var',default='h4g')
    parser.add_option("--WP",type='string',dest="WP",default='')
    parser.add_option("--opt",type='string',dest="option",default='')
    parser.add_option("--nCat",type='string',dest="nCat",default='')
    parser.add_option("--year",type='string',dest="year",default='')
    parser.add_option("--addc",type='string',dest='addcut',default='')
    parser.add_option("--suf",type='string',dest="out_file_suf",default='')
    parser.add_option("--oD",type='string',dest="out_dir",default='')
    return parser.parse_args()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(opt,args) = get_options()

# mass = '125'
# masses = [-5,5.]
input_files = opt.inp_files.split(',')
input_names = []
target_names = []
target_files = []

for num,f in enumerate(input_files):
   name=f
   print f
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
# print len(cut_list)

cut_MVA = ''
if (opt.WP == 'CutBased'):
   cut_MVA = '1>0'
if (opt.WP == 'veryLoose'):
   cut_MVA = 'pho1_MVA > -0.9 && pho2_MVA > -0.9 && pho3_MVA > -0.9 && pho4_MVA > -0.9'
elif (opt.WP == 'Loose'):
   cut_MVA = 'pho1_MVA > -0.9 && pho2_MVA > -0.9 && pho3_MVA > -0.75 && pho4_MVA > -0.75'
elif (opt.WP == 'Medium'):
   cut_MVA = 'pho1_MVA > -0.2 && pho2_MVA > -0.4 && pho3_MVA > -0.75 && pho4_MVA > -0.75'
elif (opt.WP == 'Tight_MC'):
    cut_MVA = 'pho1_MVA > -0.9 && pho2_MVA > -0.9 && pho3_MVA > -0.65 && pho4_MVA > 0.15'
#else:
    #cut_MVA = 'pho1_MVA > -0.65 && pho2_MVA > -0.6 && pho3_MVA > -0.4 && pho4_MVA > 0.2'


cut_add = opt.addcut
common_cut = 'pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 &&  abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass < 180 && ' + str(cut_MVA) + '&&' + str(cut_add)
#
print "common_cut: ", common_cut
for num,f in enumerate(input_files):
 print 'doing file ',f
 tfile = ROOT.TFile(opt.inp_dir+f+'.root')
 datasets = []
 ws = ROOT.RooWorkspace("cms_hgg_13TeV", "cms_hgg_13TeV")
 add_mc_vars_to_workspace( ws)
 treename = ""
 if (opt.option == 'signal' and opt.year == '2016'):
     treename = "SUSYGluGluToHToAA_AToGG_M_"+opt.m+"_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0"
 elif (opt.option == 'signal' and opt.year == '2017'):
    treename = "SUSYGluGluToHToAA_AToGG_M_"+opt.m+"_TuneCP5_13TeV_pythia8_13TeV_H4GTag_0"
 elif (opt.option == 'signal' and opt.year == '2018'):
    treename = "HAHMHToAA_AToGG_MA_"+opt.m+"GeV_TuneCP5_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0"
 else:
     treename = "Data_13TeV_H4GTag_0"
 print "Tree: ", treename

 data = pd.DataFrame(tree2array(tfile.Get(treename)))

 newname = 'cms_hgg_13TeV'
 datasets += add_dataset_to_workspace(data,ws,newname)

 values = [-5,0,5]
 higgs_mass = 125
 for dataset in datasets:
     dataset_list = []
     for icat, cat in enumerate(cut_list):
         Cat_name = '_Cat' + str(icat)+'_'+str(opt.year)
         print "Cat_name: ", Cat_name
         temp_dataset = ws.data(dataset).Clone(dataset+Cat_name)
         # print "CUT: ", cut_list[icat]
         dataset_cut = common_cut + '&&' + cut_list[icat]
         print "Cut: ", dataset_cut
         temp_dataset_reduced = temp_dataset.reduce(dataset_cut)
         temp_dataset_reduced.Print()
         temp_dataset_reduced.changeObservableName('dZ_bdtVtx','dZ')
         temp_dataset_reduced.changeObservableName('tp_mass','CMS_hgg_mass')
         print temp_dataset_reduced.numEntries()
         dataset_list.append(temp_dataset_reduced)

     print "dataset_list: ", dataset_list
     for d in range(0,len(dataset_list)):
         getattr(ws, 'import')(dataset_list[d])

 f_out = ROOT.TFile.Open("%s/%s.root"%(opt.out_dir,target_files[num]),"RECREATE")
 # f_out = ROOT.TFile.Open("test_ws.root","RECREATE")
 dir_ws = f_out.mkdir("tagsDumper")
 dir_ws.cd()
 ws.Write()
 f_out.Close()
