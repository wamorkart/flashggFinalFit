import ROOT
from ROOT import *

mass = [10,15,20,25,30,35,40,45,50,55,60]

for m in mass:
    print "Looking at mass = ", m
    inFile = '/afs/cern.ch/work/t/twamorka/ThesisAnalysis/CMSSW_10_5_0/src/flashgg/Signal_Jul15_ver5/signal_'+str(m)+'/signal_m_'+str(m)+'.root'
    chain = TChain('h4gCandidateDumper/trees/SUSYGluGluToHToAA_AToGG_M_'+str(m)+'_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons')
    chain.Add(inFile)
    h = ROOT.TH1F("hist","Avg, Diphoton mass;Mass[GeV];# of events",100, 0, 500)
    chain.Draw('avg_dp_mass >> hist','pho1_pt > 30 && pho2_pt > 20 && pho3_pt > 10 && pho4_pt > 10 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) &&  (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_MVA > -0.9 && pho2_MVA > -0.9 && pho3_MVA > -0.6 && pho4_MVA > -0.6 && tp_mass > 110 && tp_mass < 180')

    fitResultPtr = h.Fit("gaus","S")
    mean = fitResultPtr.GetParams()[1]
    sigma = fitResultPtr.GetParams()[2]

    print "mean =",mean, " ", "mean + 2sigma =", mean + 2*sigma, " ", "mean - 2sigma =", mean - 2*sigma

    inFileWS = '/afs/cern.ch/work/t/twamorka/ThesisAnalysis/CMSSW_10_5_0/src/flashgg/Signal_Jul15_ver5/signal_'+str(m)+'/output_SUSYGluGluToHToAA_AToGG_M-'+str(m)+'_TuneCUETP8M1_13TeV_pythia8.root'

    ws_name = 'h4gCandidateDumper/cms_h4g_13TeV'
    dataset_name = 'SUSYGluGluToHToAA_AToGG_M_'+str(m)+'_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons'

    temp_ws = TFile(inFileWS).Get(ws_name)
    # temp_ws.Print()
    temp_dataset = temp_ws.data(dataset_name).Clone('h4g_13TeV_4photons')
    # temp_dataset.Print()
    print temp_dataset.numEntries()
    temp_dataset_reduced = temp_dataset.reduce('pho1_pt > 30 && pho2_pt > 20 && pho3_pt > 10 && pho4_pt > 10 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) &&  (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_MVA > -0.9 && pho2_MVA > -0.9 && pho3_MVA > -0.6 && pho4_MVA > -0.6 && tp_mass > 100 && tp_mass < 180 && (avg_dp_mass > '+str(mean-2*sigma) + '&& avg_dp_mass < ' + str(mean+2*sigma)+')')
    print temp_dataset_reduced.numEntries()

    outFileWS = '/eos/cms/store/user/twamorka/HtoAAto4G/Signal/Jul16/w_signal_'+str(m)+'.root'
    output = TFile(outFileWS,'Recreate')
    output.mkdir('tagsDumper')
    output.cd('tagsDumper')
    ws_new = RooWorkspace('cms_h4g_13TeV')
    getattr(ws_new,'import')(temp_dataset_reduced,RooCmdArg())
    ws_new.Write()
    output.Close()
    print "Created reduced workspace for mass point = ", str(m)
