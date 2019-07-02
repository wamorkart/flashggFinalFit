import ROOT
from ROOT import *
import optparse
import argparse

parser = argparse.ArgumentParser(description='make WS')

parser.add_argument('--mass', metavar='mass', type=str, help='mass of a',required=True)
args = parser.parse_args()
#
mass  = args.mass
# print mass
# file = '/eos/cms/store/user/twamorka/NTuples_17Feb2019/Signal/signal_m_' + str(mass) + '.root'
# chain = ROOT.TChain('h4gCandidateDumper/trees/SUSYGluGluToHToAA_AToGG_M_'+ str(mass) +'_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons')
# file = '/eos/cms/store/user/torimoto/physics/4gamma/H4Gamma_2016Analysis/Signal_LowMassPreselOnly/signal_m_' + str(mass) + '.root'
# file = '/afs/cern.ch/work/t/twamorka/H4Gamma_BrandNew_2016/CMSSW_8_0_26_patch1/src/flashgg/TestBench/60/signal2_m_' + str(mass) + '.root'
# file = '/eos/cms/store/user/twamorka/H4G_2016_ntuples/Signal/signal_m_' + str(mass) + '.root'
file = '/eos/cms/store/user/twamorka/HtoAAto4G/Signal/ntuples/signal_m_' + str(mass) + '.root'
# file = '/eos/cms/store/user/twamorka/HtoAAto4G/Data/ntuples/data_2016_all.root'


chain = ROOT.TChain('h4gCandidateDumper/trees/SUSYGluGluToHToAA_AToGG_M_'+ str(mass) +'_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons')
# chain = ROOT.TChain('h4gCandidateDumper/trees/Data_13TeV_4photons')
chain.Add(file)

h = ROOT.TH1F("hist","Avg, Diphoton mass;Mass[GeV];# of events",100, 0, 500)
# h = ROOT.TH1F("hist","Avg, Diphoton mass;Mass[GeV];# of events",100, 0, 10)
chain.Draw('avg_dp_mass >> hist')
# chain.Draw('avg_dp_mass >> hist','pho1_pt > 30 && pho2_pt > 20 && pho3_pt > 10 && pho4_pt > 10 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) &&  (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_MVA > -0.9 && pho2_MVA > -0.9 && pho3_MVA > -0.6 && pho4_MVA > -0.6 && tp_mass > 110 && tp_mass < 180')
fitResultPtr = h.Fit("gaus","S")

mean =  fitResultPtr.GetParams()[1]
sigma = fitResultPtr.GetParams()[2]

# print "mean =",mean, " ", "mean + 2sigma =", mean + 2*sigma, " ", "mean - 2sigma =", mean - 2*sigma
# outputLoc = "/eos/cms/store/user/twamorka/NTuples_17Feb2019/Test_SignalWS/"
# outputLoc = "/eos/cms/store/user/torimoto/physics/4gamma/H4Gamma_2016Analysis/SignalFitOutput/"
# outputLoc = "/afs/cern.ch/work/t/twamorka/H4Gamma_BrandNew_2016/CMSSW_8_0_26_patch1/src/flashgg/TestBench/60/"
# outputLoc = '/eos/cms/store/user/twamorka/H4G_2016_ntuples/Signal/'
outputLoc = '/eos/cms/store/user/twamorka/HtoAAto4G/Signal/ntuples/Jul1/'
# outputLoc = '/eos/cms/store/user/twamorka/HtoAAto4G/Data/ntuples/'

name_root_file_with_workspace = outputLoc + "w_signal_"+ str(mass) +".root"

# name_root_file_with_workspace = outputLoc + "w_data.root"


root_file_with_workspace = ROOT.TFile (name_root_file_with_workspace, "RECREATE")
root_file_with_workspace.mkdir("tagsDumper")
root_file_with_workspace.cd("tagsDumper")

w = ROOT.RooWorkspace("cms_h4g_13TeV_4photons")
# w = ROOT.RooWorkspace("cms_h4g_13TeV")
IntLumi = 1000.0

w.factory("weight[0,7e-06]")
# w.factory("dZ[-100000,1000000]")
# w.factory("dZ[-100000,1000000]")
w.factory("dZ_zeroVtx[-100000,1000000]")
w.factory("dZ_hggVtx[-100000,1000000]")
w.factory("dZ_randomVtx[-100000,1000000]")

w.factory("IntLumi[1000.]")
w.factory("avg_dp_mass[0,1000]")
w.factory("tp_mass[100,180]")
w.factory("pho1_pt[0,1000]")
w.factory("pho2_pt[0,1000]")
w.factory("pho3_pt[0,1000]")
w.factory("pho4_pt[0,1000]")
w.factory("pho1_eta[-1000,1000]")
w.factory("pho2_eta[-1000,1000]")
w.factory("pho3_eta[-1000,1000]")
w.factory("pho4_eta[-1000,1000]")
w.factory("pho1_MVA[-1000,1000]")
w.factory("pho2_MVA[-1000,1000]")
w.factory("pho3_MVA[-1000,1000]")
w.factory("pho4_MVA[-1000,1000]")


wsVars = ROOT.RooArgSet()
wsVars.add(w.var("weight"))
# wsVars.add(w.var("dZ"))
wsVars.add(w.var("dZ_zeroVtx"))
wsVars.add(w.var("dZ_hggVtx"))
wsVars.add(w.var("dZ_randomVtx"))

wsVars.add(w.var("IntLumi"))
wsVars.add(w.var("avg_dp_mass"))
wsVars.add(w.var("tp_mass"))
wsVars.add(w.var("pho1_pt"))
wsVars.add(w.var("pho2_pt"))
wsVars.add(w.var("pho3_pt"))
wsVars.add(w.var("pho4_pt"))
wsVars.add(w.var("pho1_eta"))
wsVars.add(w.var("pho2_eta"))
wsVars.add(w.var("pho3_eta"))
wsVars.add(w.var("pho4_eta"))
wsVars.add(w.var("pho1_MVA"))
wsVars.add(w.var("pho2_MVA"))
wsVars.add(w.var("pho3_MVA"))
wsVars.add(w.var("pho4_MVA"))

# data_RooDataSet = ROOT.RooDataSet( "Data_13TeV_4photons", "Data_13TeV_4photons", chain, wsVars )

data_RooDataSet = ROOT.RooDataSet( "h4g_13TeV_4photons", "h4g_13TeV_4photons", chain, wsVars )
# data_reduced_RooDataSet = data_RooDataSet.reduce("pho1_pt > 30 && pho2_pt > 20 && pho3_pt > 10 && pho4_pt > 10 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) &&  (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_MVA > -0.9 && pho2_MVA > -0.9 && pho3_MVA > -0.6 && pho4_MVA > -0.6 && tp_mass > 100 && tp_mass < 180" )

data_reduced_RooDataSet = data_RooDataSet.reduce("(weight)*(avg_dp_mass >"+ str (mean - 2*sigma) + " && avg_dp_mass <"+ str (mean + 2*sigma)+")" )

getattr(w,'import')(data_reduced_RooDataSet,RooCmdArg())

w.Write()
