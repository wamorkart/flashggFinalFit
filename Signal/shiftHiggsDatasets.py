import ROOT
from ROOT import *

import sys
import os

mass = [10,15,20,25,30,35,40,45,50,55,60]

for m in mass:
    print "Looking at mass = ", m
    inDir = '/eos/cms/store/user/twamorka/HtoAAto4G/Signal/Jul16/'

    values = [-5,0,5]
    higgs_mass = 125

    ws_name = 'tagsDumper/cms_h4g_13TeV'
    dataset_name = 'h4g_13TeV_4photons'

    temp_ws = TFile(inDir+'/w_signal_'+str(m)+'.root').Get(ws_name)
    # temp_ws.Print()
    for value in values:
        shift = value + higgs_mass
        dataset = (temp_ws.data(dataset_name)).Clone('h4g_'+str(shift)+'_13TeV_4photons')
        dataset.Print()
        dataset.changeObservableName('dZ_bdtVtx','dZ')
        dataset.changeObservableName('tp_mass','tp_mass_old')
        higgs_old = dataset.get()['tp_mass_old']
        higgs_new = RooFormulaVar( 'tp_mass', 'tp_mass', "(@0+%.1f)"%value,RooArgList(higgs_old) );
        dataset.addColumn(higgs_new).setRange(100,180)
        dataset.Print()

        output = TFile(inDir+'/w_signal_'+str(m)+'_'+str(shift)+'.root','RECREATE')
        output.mkdir("tagsDumper")
        output.cd("tagsDumper")
        ws_new = ROOT.RooWorkspace("cms_h4g_13TeV_4photons")
        getattr(ws_new,'import')(dataset,RooCmdArg())
        ws_new.Write()
        output.Close()
