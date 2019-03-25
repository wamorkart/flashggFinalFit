import ROOT
from ROOT import *
import argparse
import optparse
# from optparse import OptionParser, make_option
import sys
import os

parser = argparse.ArgumentParser(description='shift higgs')

parser.add_argument('--mass', metavar='mass', type=str, nargs = '+', help='pseudoscalar mass',required=True)
args = parser.parse_args()


mass = args.mass
print "pseudoscalar mass =",mass

inputFiles = []
for m in mass:
    inputFiles.append('/eos/cms/store/user/twamorka/NTuples_17Feb2019/Test_SignalWS/w_signal_'+str(m))#+'.root')

values = [-5.,0.,5.]
higgs_mass = 125.

ws_name = 'tagsDumper/cms_h4g_13TeV_4photons'
dataset_name = 'Data_13TeV_4photons'

for fi, f in enumerate(inputFiles):
    print "Looking at ", f
    temp_ws = TFile(f+'.root').Get(ws_name)
    for value in values:
        shift = value + higgs_mass
        # temp_ws.Print()
        dataset = (temp_ws.data(dataset_name)).Clone(dataset_name+'_'+str(value))
        dataset.Print()
        dataset.changeObservableName('tp_mass','tp_mass_old')
        higgs_old = dataset.get()['tp_mass_old']
        higgs_new = RooFormulaVar( 'tp_mass', 'tp_mass', "(@0+%.1f)"%value,RooArgList(higgs_old) );
        dataset.addColumn(higgs_new).setRange(100,180)
        dataset.Print()

        output = TFile(f+'_'+str(value)+'.root','RECREATE')
        output.mkdir("tagsDumper")
        output.cd("tagsDumper")
        ws_new = ROOT.RooWorkspace("cms_h4g_13TeV_4photons")#,'cms_h4g_13TeV_4photons')
        getattr(ws_new,'import')(dataset,RooCmdArg())
        ws_new.Write()
        output.Close()
