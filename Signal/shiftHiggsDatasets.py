import ROOT
from ROOT import *
import argparse
import sys
import os
parser = argparse.ArgumentParser(description='shift datasets')
parser.add_argument('--i',metavar='i', type=str, help='input file',required=True)
parser.add_argument('--inDir',metavar='inDir', type=str, help='input directory',required=True)
parser.add_argument('--m',metavar='m', type=str, help='mass',required=True)
parser.add_argument('--outDir',metavar='outDir', type=str, help='output file',required=True)

opt = parser.parse_args()

values = [-5,0,5]
higgs_mass = 125


print "Looking at mass = ", opt.m
ws_name = 'tagsDumper/cms_hgg_13TeV'
temp_ws = TFile(opt.inDir + opt.i+'.root').Get(ws_name)
# temp_ws.Print()
for value in values:
    shift = value + higgs_mass
    cat_datasets = []
    ws_new = ROOT.RooWorkspace('cms_hgg_13TeV')
    # for icat, cat in enumerate(nCat_list):
    for icat in range(5):
        print "ICAT ", icat
        print 'category:' ,icat
        dataset_name = 'H4G_Cat'+str(icat)
        dataset = (temp_ws.data(dataset_name)).Clone('H4G_'+str(shift)+'_13TeV_Cat'+str(icat))
        dataset.Print()
        print dataset.numEntries()
        dataset.changeObservableName('CMS_hgg_mass','tp_mass_old')
        higgs_old = dataset.get()['tp_mass_old']
        higgs_new = RooFormulaVar( 'CMS_hgg_mass', 'CMS_hgg_mass', "(@0+%.1f)"%value,RooArgList(higgs_old) );
        dataset.addColumn(higgs_new).setRange(105,140)
        dataset.Print()
        getattr(ws_new,'import')(dataset,RooCmdArg())
    output = TFile(opt.outDir+opt.i+'_'+str(shift)+'.root','RECREATE')
    output.mkdir("tagsDumper")
    output.cd("tagsDumper")
    ws_new.Write()
    output.Close()
