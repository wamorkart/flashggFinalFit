#include <iostream>
#include <fstream>
#include <TH1F.h>
#include <TTree.h>
#include <TPaveText.h>
#include <TStyle.h>
#include <TCanvas.h>
#include "TLorentzVector.h"
#include <iomanip>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <vector>
#include "TFile.h"
#include "TROOT.h"
#include "TLatex.h"
#include "TLegend.h"
#include "TGraph.h"
#include <algorithm>    // std::min_element, std::max_element

using namespace std;

void optimize_cats_modifiedSig(const int NCATS, bool scaleBkgSideband, bool verbose, double xcutoff, double bin_width_, int mass_) {

	// Misc
	gROOT->SetBatch("kTrue");

	// Parameters
	TString scaleOpt;
	if(scaleBkgSideband) scaleOpt = "withSidebandScale";
	else scaleOpt = "noSidebandScale";
	TString inDir = "/eos/user/t/twamorka/h4g_fullRun2/withSystematics/";
	// TString inDir = "/eos/user/t/twamorka/h4g_fullRun2/withSystematics/Training_CombinedMass_PerYear/BDTTransformation_Checks/20000_withSelectionsselection/";
	//TString outDir = "/eos/user/t/twamorka/www/H4G_Training_CombinedMass_PerYear/Transformation_20000Bins/";
	// TString outDir = "/afs/cern.ch/work/t/twamorka/fggfinalfit_h4g_run2/CMSSW_10_2_13/src/flashggFinalFit/100kTransform_5Oct2020_modifiedSignificance_highStatDataMix_bdtVar/";
	// TString outDir = "/afs/cern.ch/work/t/twamorka/fggfinalfit_h4g_run2/CMSSW_10_2_13/src/flashggFinalFit/100kTransform_5Oct2020_modifiedSignificance_bdtVar/";
	// TString outDir = "/eos/user/t/twamorka/www/H4G_Pre_PreApp/Significance_Optimization_Plots/CatTrain_Standard_M"+mass+"_PerYear_Optimization_Run2/";

	TString what_to_opt = "bdt";
	double minevents = 8.;
	// double xmin = 0.0;
	double xmin = xcutoff;
	double xmax = 1.0000; // to include values that == 1
	// Double_t bin_width=0.01; // course binning
	// Double_t bin_width=0.0025;
	Double_t bin_width = bin_width_;
	TString xmin_str = to_string(xcutoff);
	TString binWidth_str = to_string(bin_width_);
	TString mass = to_string(mass_);
	// TString outDir = "/eos/user/t/twamorka/www/H4G_Pre_PreApp/Significance_Optimization_Plots/19Oct2020/CatTrain_Standard_AllMasses_M"+mass+"_PerYear_Optimization_Run2/";
	// TString outDir="/eos/user/t/twamorka/www/H4G_Pre_PreApp/Significance_Optimization_Plots/19Oct2020/CatTrain_Standard_M60_Run2_Optimization_Run2/";
	// TString outDir="/eos/user/t/twamorka/www/H4G_Pre_PreApp/Significance_Optimization_Plots/2Nov2020/CatTrain_GenMass_AllMasses_ExceptM15_Run2/";
  // TString outDir = "/eos/user/t/twamorka/www/H4G_Pre_PreApp/DataMix_v4_OldNormalization/";
	TString outDir = "/eos/user/t/twamorka/www/H4G_Pre_PreApp/DataMix_v4_OldNormalization/";

	// TString extraSelection = "*(1)";
	// TString extraSelection = "*(N_goodMuons == 1)";

	TString Mgg_window = "*((tp_mass>115)&&(tp_mass<135))";
	TString Mgg_sideband = "*((tp_mass<=115)||(tp_mass>=135))";
	// TString selection_sig = "1*weight*(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass < 180)" ; // normalize signal properly with cross section

	//TString selection_sig = "131.78*weight*(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass < 180)" ; // normalize signal properly with cross section

	TString selection_sig_2016 = "35.9*weight*(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass < 180)" ; // normalize signal properly with cross section
	TString selection_sig_2017 = "41.5*weight*(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass < 180)" ; // normalize signal properly with cross section
	TString selection_sig_2018 = "54.38*weight*(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass < 180)" ; // normalize signal properly with cross section
	TString selection_bg = "(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass < 180)" ;
	TString selection_data = "(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass < 180)";
	TString s; TString sel;
	TString outname = s.Format("Categorization_%s_%dcats",what_to_opt.Data(),NCATS);

	// Combine Signal Trees
	cout << "nBins: " << int((xmax-xmin)/bin_width) << endl;
	cout << "xmin: " << xmin << endl;
	cout << "xmax: " << xmax << endl;

	TChain *file_s_2016 =  new TChain("file_s_2016");
	file_s_2016->Add(inDir+"CatTrain_Standard_M60_Run2_2016/signal_m_60_2016.root/SUSYGluGluToHToAA_AToGG_M_"+mass+"_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0");

  TChain *file_s_2017 =  new TChain("file_s_2017");
	file_s_2016->Add(inDir+"CatTrain_Standard_M60_Run2_2017/signal_m_60_2017.root/SUSYGluGluToHToAA_AToGG_M_"+mass+"_TuneCP5_13TeV_pythia8_13TeV_H4GTag_0");

  TChain *file_s_2018 =  new TChain("file_s_2018");
	file_s_2018->Add(inDir+"CatTrain_Standard_M60_Run2_2018/signal_m_60_2018.root/HAHMHToAA_AToGG_MA_"+mass+"GeV_TuneCP5_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0");

  // TChain *file_s_2016_eval =  new TChain("file_s_2016_eval");
	// TChain *file_s_2017_eval =  new TChain("file_s_2017_eval");
	// TChain *file_s_2018_eval =  new TChain("file_s_2018_eval");
	// file_s_2016_eval->Add(inDir+"CatTrain_Standard_AllMasses_2016/signal_m_15_2016_transform.root/SUSYGluGluToHToAA_AToGG_M_15_TuneCUETP8M1_13TeV_pythia8_13TeV_H4GTag_0");
	// file_s_2017_eval->Add(inDir+"CatTrain_Standard_AllMasses_2017/signal_m_15_2017_transform.root/SUSYGluGluToHToAA_AToGG_M_15_TuneCP5_13TeV_pythia8_13TeV_H4GTag_0");
	// file_s_2018_eval->Add(inDir+"CatTrain_Standard_AllMasses_2018/signal_m_15_2018_transform.root/HAHMHToAA_AToGG_MA_15GeV_TuneCP5_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0");


	TH1F *hist_S_2016 = new TH1F("hist_S_2016","hist_S_2016",int((xmax-xmin)/bin_width),xmin,xmax);
  s.Form("%s>>hist_S_2016",what_to_opt.Data());
  sel.Form("%s",(selection_sig_2016+Mgg_window).Data());
	file_s_2016->Draw(s,sel,"goff");

	TH1F *hist_S_2017 = new TH1F("hist_S_2017","hist_S_2017",int((xmax-xmin)/bin_width),xmin,xmax);
  s.Form("%s>>hist_S_2017",what_to_opt.Data());
  sel.Form("%s",(selection_sig_2017+Mgg_window).Data());
	file_s_2017->Draw(s,sel,"goff");

	TH1F *hist_S_2018 = new TH1F("hist_S_2018","hist_S_2018",int((xmax-xmin)/bin_width),xmin,xmax);
  s.Form("%s>>hist_S_2018",what_to_opt.Data());
  sel.Form("%s",(selection_sig_2018+Mgg_window).Data());
	file_s_2018->Draw(s,sel,"goff");

	hist_S_2016->Add(hist_S_2017);
	hist_S_2016->Add(hist_S_2018);

	// TH1F *hist_S_2016_eval = new TH1F("hist_S_2016_eval","hist_S_2016_eval",int((xmax-xmin)/bin_width),xmin,xmax);
  // s.Form("%s>>hist_S_2016_eval",what_to_opt.Data());
  // sel.Form("%s",(selection_sig_2016+Mgg_window).Data());
	// file_s_2016_eval->Draw(s,sel,"goff");
	//
	// TH1F *hist_S_2017_eval = new TH1F("hist_S_2017_eval","hist_S_2017_eval",int((xmax-xmin)/bin_width),xmin,xmax);
  // s.Form("%s>>hist_S_2017_eval",what_to_opt.Data());
  // sel.Form("%s",(selection_sig_2017+Mgg_window).Data());
	// file_s_2017_eval->Draw(s,sel,"goff");
	//
	// TH1F *hist_S_2018_eval = new TH1F("hist_S_2018_eval","hist_S_2018_eval",int((xmax-xmin)/bin_width),xmin,xmax);
  // s.Form("%s>>hist_S_2018_eval",what_to_opt.Data());
  // sel.Form("%s",(selection_sig_2018+Mgg_window).Data());
	// file_s_2018_eval->Draw(s,sel,"goff");
	//
	// hist_S_2016_eval->Add(hist_S_2017_eval);
	// hist_S_2016_eval->Add(hist_S_2018_eval);


	// Combine Background Trees
	// TChain *tree_bg =  new TChain("tree_bg");
	// // tree_bg->Add(inDir+"data_mix_2016_highstat_wBDT_transformedMVA.root/Data_13TeV_H4GTag_0");
	// // tree_bg->Add(inDir+"data_mix_2017_highstat_wBDT_transformedMVA.root/Data_13TeV_H4GTag_0");
	// // tree_bg->Add(inDir+"data_mix_2018_highstat_wBDT_transformedMVA.root/Data_13TeV_H4GTag_0");
	// tree_bg->Add(inDir+"CatTrain_Standard_M15_Run2_2016/data_mix_weight_v4_genMass_"+mass+"_2016.root/Data_13TeV_H4GTag_0");
	// tree_bg->Add(inDir+"CatTrain_Standard_M15_Run2_2017/data_mix_weight_v4_genMass_"+mass+"_2017.root/Data_13TeV_H4GTag_0");
	// tree_bg->Add(inDir+"CatTrain_Standard_M15_Run2_2018/data_mix_weight_v4_genMass_"+mass+"_2018.root/Data_13TeV_H4GTag_0");

	TChain *tree_bg_2016 =  new TChain("tree_bg_2016");
	tree_bg_2016->Add(inDir+"CatTrain_Standard_M60_Run2_2016/data_mix_weight_v4_genMass_"+mass+"_2016.root/Data_13TeV_H4GTag_0");

	TChain *tree_bg_2017 =  new TChain("tree_bg_2017");
	tree_bg_2017->Add(inDir+"CatTrain_Standard_M60_Run2_2017/data_mix_weight_v4_genMass_"+mass+"_2017.root/Data_13TeV_H4GTag_0");

	TChain *tree_bg_2018 =  new TChain("tree_bg_2018");
	tree_bg_2018->Add(inDir+"CatTrain_Standard_M60_Run2_2018/data_mix_weight_v4_genMass_"+mass+"_2018.root/Data_13TeV_H4GTag_0");


	// Combine Data Trees
	// TChain *tree_data =  new TChain("tree_data");
	// tree_data->Add(inDir+"CatTrain_Standard_M60_Run2_2016/data_"+mass+"_2016.root/Data_13TeV_H4GTag_0");
	// tree_data->Add(inDir+"CatTrain_Standard_M60_Run2_2017/data_"+mass+"_2017.root/Data_13TeV_H4GTag_0");
	// tree_data->Add(inDir+"CatTrain_Standard_M60_Run2_2018/data_"+mass+"_2018.root/Data_13TeV_H4GTag_0");

	TChain *tree_data_2016 =  new TChain("tree_data_2016");
	tree_data_2016->Add(inDir+"CatTrain_Standard_M60_Run2_2016/data_"+mass+"_2016.root/Data_13TeV_H4GTag_0");

	TChain *tree_data_2017 =  new TChain("tree_data_2017");
	tree_data_2017->Add(inDir+"CatTrain_Standard_M60_Run2_2017/data_"+mass+"_2017.root/Data_13TeV_H4GTag_0");

	TChain *tree_data_2018 =  new TChain("tree_data_2018");
	tree_data_2018->Add(inDir+"CatTrain_Standard_M60_Run2_2018/data_"+mass+"_2018.root/Data_13TeV_H4GTag_0");

	cout << "[tree_data]->GetEntries(): " << tree_data->GetEntries() << endl;

	// Get Data over Background in sidebands scale factor
	// TH1F* hist_background_sideband = new TH1F("hist_background_sideband","hist_background_sideband",100,-1,1);
	TH1F* hist_background_sideband_2016 = new TH1F("hist_background_sideband_2016","hist_background_sideband_2016",100,-1,1);
	TH1F* hist_background_sideband_2017 = new TH1F("hist_background_sideband_2017","hist_background_sideband_2017",100,-1,1);
	TH1F* hist_background_sideband_2018 = new TH1F("hist_background_sideband_2018","hist_background_sideband_2018",100,-1,1);
	// TH1F* hist_data_sideband = new TH1F("hist_data_sideband","hist_data_sideband",100,-1,1);

	TH1F* hist_data_sideband_2016 = new TH1F("hist_data_sideband_2016","hist_data_sideband_2016",100,-1,1);
	TH1F* hist_data_sideband_2017 = new TH1F("hist_data_sideband_2017","hist_data_sideband_2017",100,-1,1);
	TH1F* hist_data_sideband_2018 = new TH1F("hist_data_sideband_2018","hist_data_sideband_2018",100,-1,1);

	s.Form("bdt >> hist_background_sideband_2016");
	sel.Form("%s",(selection_bg+Mgg_sideband).Data());
	tree_bg_2016->Draw(s,sel,"goff");
  hist_background_sideband_2016->Scale(35.9/hist_background_sideband_2016->Integral());

	s.Form("bdt >> hist_background_sideband_2017");
	sel.Form("%s",(selection_bg+Mgg_sideband).Data());
	tree_bg_2017->Draw(s,sel,"goff");
	hist_background_sideband_2017->Scale(41.5/hist_background_sideband_2017->Integral());

	s.Form("bdt >> hist_background_sideband_2018");
	sel.Form("%s",(selection_bg+Mgg_sideband).Data());
	tree_bg_2018->Draw(s,sel,"goff");
	hist_background_sideband_2018->Scale(54.38/hist_background_sideband_2018->Integral());

	hist_background_sideband_2016->Add(hist_background_sideband_2017);
	hist_background_sideband_2016->Add(hist_background_sideband_2018);

	TH1F *hist_background_sideband = (TH1F*)hist_background_sideband_2016->Clone("b_new_sideband");

	// s.Form("bdt >> hist_data_sideband");
	// sel.Form("%s",(selection_data+Mgg_sideband).Data());
	// tree_data->Draw(s,sel,"goff");

	s.Form("bdt >> hist_data_sideband_2016");
	sel.Form("%s",(selection_data+Mgg_sideband).Data());
	tree_data_2016->Draw(s,sel,"goff");

	s.Form("bdt >> hist_data_sideband_2017");
	sel.Form("%s",(selection_data+Mgg_sideband).Data());
	tree_data_2017->Draw(s,sel,"goff");

	s.Form("bdt >> hist_data_sideband_2018");
	sel.Form("%s",(selection_data+Mgg_sideband).Data());
	tree_data_2018->Draw(s,sel,"goff");

	// if(verbose){
	// 	cout << " " << endl;
	// 	cout << "Background sideband Integral: " << hist_background_sideband->Integral() << endl;
	// 	cout << "Data sideband Integral: " << hist_data_sideband->Integral() << endl;
	// }

	// double scale = 1;

	double scale_2016 = 1;
	double scale_2017 = 1;
	double scale_2018 = 1;

	if(scaleBkgSideband)
		// scale = hist_data_sideband->Integral() / hist_background_sideband->Integral();
		scale_2016 = hist_data_sideband_2016->Integral() / hist_background_sideband_2016->Integral();
    scale_2017 = hist_data_sideband_2017->Integral() / hist_background_sideband_2017->Integral();
		scale_2018 = hist_data_sideband_2018->Integral() / hist_background_sideband_2018->Integral();

	// Create Background Hists
	// TH1F *hist_B = new TH1F("hist_B","hist_B",int((xmax-xmin)/bin_width),xmin,xmax); //200 bins  -- background signal region
  // s.Form("%s>>hist_B",what_to_opt.Data());
  // sel.Form("%s",(selection_bg+Mgg_window).Data());
	// tree_bg->Draw(s,sel,"goff");

	TH1F *hist_B_2016 = new TH1F("hist_B_2016","hist_B_2016",int((xmax-xmin)/bin_width),xmin,xmax); //200 bins  -- background signal region
  s.Form("%s>>hist_B_2016",what_to_opt.Data());
  sel.Form("%s",(selection_bg+Mgg_window).Data());
	tree_bg_2016->Draw(s,sel,"goff");
  hist_B_2016->Scale(35.9/hist_B_2016->Integral());

	TH1F *hist_B_2017 = new TH1F("hist_B_2017","hist_B_2017",int((xmax-xmin)/bin_width),xmin,xmax); //200 bins  -- background signal region
  s.Form("%s>>hist_B_2017",what_to_opt.Data());
  sel.Form("%s",(selection_bg+Mgg_window).Data());
	tree_bg_2017->Draw(s,sel,"goff");
  hist_B_2017->Scale(41.5/hist_B_2017->Integral());

	TH1F *hist_B_2018 = new TH1F("hist_B_2018","hist_B_2018",int((xmax-xmin)/bin_width),xmin,xmax); //200 bins  -- background signal region
  s.Form("%s>>hist_B_2018",what_to_opt.Data());
  sel.Form("%s",(selection_bg+Mgg_window).Data());
	tree_bg_2018->Draw(s,sel,"goff");
  hist_B_2018->Scale(54.38/hist_B_2018->Integral());

	// hist_B_2016->Add(hist_B_2017);
	// hist_B_2016->Add(hist_B_2018);

	hist_B_2016->Scale(scale_2016);
	hist_B_2017->Scale(scale_2017);
	hist_B_2018->Scale(scale_2018);

	hist_B_2016->Add(hist_B_2017);
	hist_B_2016->Add(hist_B_2018);

	TH1F *hist_B = (TH1F*)hist_B_2016->Clone("b_new_1");

	// hist_B->Scale(scale);
	// hist_B->Scale(scale/hist_B->Integral());
	if(verbose){
		cout << " " << endl;
		cout << "BG integral under Mgg "<< hist_B->Integral() << endl;
	}
	// TH1F *hist_B_sideband = new TH1F("hist_B_sideband","hist_B_sideband",int((xmax-xmin)/bin_width),xmin,xmax); // background sideband region
  // s.Form("%s>>hist_B_sideband",what_to_opt.Data());
  // sel.Form("(1)*%s",(selection_bg+Mgg_sideband).Data());
	TH1F *hist_B_sideband_2016 = new TH1F("hist_B_sideband_2016","hist_B_sideband_2016",int((xmax-xmin)/bin_width),xmin,xmax); // background sideband region
  s.Form("%s>>hist_B_sideband_2016",what_to_opt.Data());
  sel.Form("(1)*%s",(selection_bg+Mgg_sideband).Data());
	tree_bg_2016->Draw(s,sel,"goff");
  hist_B_sideband_2016->Scale(35.9/hist_B_sideband_2016->Integral());

	TH1F *hist_B_sideband_2017 = new TH1F("hist_B_sideband_2017","hist_B_sideband_2017",int((xmax-xmin)/bin_width),xmin,xmax); // background sideband region
  s.Form("%s>>hist_B_sideband_2017",what_to_opt.Data());
  sel.Form("(1)*%s",(selection_bg+Mgg_sideband).Data());
	tree_bg_2017->Draw(s,sel,"goff");
  hist_B_sideband_2017->Scale(41.5/hist_B_sideband_2017->Integral());

	TH1F *hist_B_sideband_2018 = new TH1F("hist_B_sideband_2018","hist_B_sideband_2018",int((xmax-xmin)/bin_width),xmin,xmax); // background sideband region
  s.Form("%s>>hist_B_sideband_2018",what_to_opt.Data());
  sel.Form("(1)*%s",(selection_bg+Mgg_sideband).Data());
	tree_bg_2018->Draw(s,sel,"goff");
  hist_B_sideband_2018->Scale(54.38/hist_B_sideband_2018->Integral());

	// hist_B_sideband_2016->Add(hist_B_sideband_2017);
	// hist_B_sideband_2016->Add(hist_B_sideband_2018);

	hist_B_sideband_2016->Scale(scale_2016);
	hist_B_sideband_2017->Scale(scale_2017);
	hist_B_sideband_2018->Scale(scale_2018);

	// hist_B_sideband_2016->Add(hist_B_sideband_2017);
	// hist_B_sideband_2016->Add(hist_B_sideband_2018);

	TH1F *hist_B_sideband = (TH1F*)hist_B_sideband_2016->Clone("b_new_sideband_1");
	// hist_B_sideband->Scale(scale);
	if(verbose){
		cout << " " << endl;
		cout << "Sidebands SF: " << scale << endl;
		cout << "BG integral sidebands AFTER scaling " << hist_B_sideband->Integral() << endl;
	}

	// Create Data hist
	// TH1F *hist_D_sideband = new TH1F("hist_D_sideband","hist_D_sideband",int((xmax-xmin)/bin_width),xmin,xmax); //200 bins -- data sideband region
	//
  // s.Form("%s>>hist_D_sideband",what_to_opt.Data());
  // sel.Form("%s",(selection_data+Mgg_sideband).Data());
	// tree_data->Draw(s,sel,"goff");

	TH1F *hist_D_sideband_2016 = new TH1F("hist_D_sideband_2016","hist_D_sideband_2016",int((xmax-xmin)/bin_width),xmin,xmax); //200 bins -- data sideband region

  s.Form("%s>>hist_D_sideband_2016",what_to_opt.Data());
  sel.Form("%s",(selection_data+Mgg_sideband).Data());
	tree_data_2016->Draw(s,sel,"goff");

	TH1F *hist_D_sideband_2017 = new TH1F("hist_D_sideband_2017","hist_D_sideband_2017",int((xmax-xmin)/bin_width),xmin,xmax); //200 bins -- data sideband region

  s.Form("%s>>hist_D_sideband_2017",what_to_opt.Data());
  sel.Form("%s",(selection_data+Mgg_sideband).Data());
	tree_data_2017->Draw(s,sel,"goff");

	TH1F *hist_D_sideband_2018 = new TH1F("hist_D_sideband_2018","hist_D_sideband_2018",int((xmax-xmin)/bin_width),xmin,xmax); //200 bins -- data sideband region

  s.Form("%s>>hist_D_sideband_2018",what_to_opt.Data());
  sel.Form("%s",(selection_data+Mgg_sideband).Data());
	tree_data_2018->Draw(s,sel,"goff");

	// if(verbose){
	// 	cout << " " << endl;
	// 	cout << "Data integral sidebands " << hist_D_sideband->Integral() << endl;
	// }

	// Get Start and Ends of Optimization Range
	double END = hist_B->GetBinCenter(hist_B->FindLastBinAbove(-1.)) + hist_B->GetBinWidth(1)/2.; // Left end of BDT distibution
	double START = hist_B->GetBinCenter(hist_B->FindFirstBinAbove(-1.)) - hist_B->GetBinWidth(1)/2.; // Right end of BDT distibution
	if(verbose){
		cout << " " << endl;
		cout << "start = " << START << " , end = " << END << endl;
	}

	// hist_S_2016->SetFillStyle(4050);
	hist_S_2016->SetLineColor(kRed);
	// hist_S_2016->SetFillColor(kRed-7);
	hist_S_2016->SetLineWidth(2);
	// hist_B->SetFillStyle(4050);
	hist_B->SetLineColor(kBlue+1);
	// hist_B->SetFillColor(kBlue-10);
	hist_B->SetLineWidth(2);

	// Make Copies of Background and Signal Histograms
	TH1F *hist_B2 = (TH1F*)hist_B->Clone("b_new");
	TH1F *hist_S2 = (TH1F*)hist_S_2016->Clone("s_new");
  // hist_S2->Scale(1./131.78);
	// CMS info
	float left2 = gStyle->GetPadLeftMargin();
	float right2 = gStyle->GetPadRightMargin();
	float top2 = gStyle->GetPadTopMargin();
	float bottom2 = gStyle->GetPadBottomMargin();
	TPaveText pCMS1(left2,1.-top2,0.4,1.,"NDC");
	pCMS1.SetTextFont(62);
	pCMS1.SetTextSize(top2*0.75);
	pCMS1.SetTextAlign(12);
	pCMS1.SetFillStyle(-1);
	pCMS1.SetBorderSize(0);
	pCMS1.AddText("CMS");
	TPaveText pCMS12(left2+0.1,1.-top2*1.1,0.6,1.,"NDC");
	pCMS12.SetTextFont(52);
	pCMS12.SetTextSize(top2*0.75);
	pCMS12.SetTextAlign(12);
	pCMS12.SetFillStyle(-1);
	pCMS12.SetBorderSize(0);
	pCMS12.AddText("Preliminary");
	TPaveText pCMS2(0.5,1.-top2,1.-right2*0.5,1.,"NDC");
	pCMS2.SetTextFont(42);
	pCMS2.SetTextSize(top2*0.75);
	pCMS2.SetTextAlign(32);
	pCMS2.SetFillStyle(-1);
	pCMS2.SetBorderSize(0);
	pCMS2.AddText("(13 TeV)");
	TPaveText pave22(0.2,0.8,0.4,1.-top2*1.666,"NDC");
	pave22.SetTextAlign(11);
	pave22.SetFillStyle(-1);
	pave22.SetBorderSize(0);
	pave22.SetTextFont(62);
	pave22.SetTextSize(top2*0.5);
	pave22.AddText("HHbbgg");
	TPaveText pave33(0.2,0.75,0.4,0.8,"NDC");
	pave33.SetTextAlign(11);
	pave33.SetFillStyle(-1);
	pave33.SetBorderSize(0);
	pave33.SetTextFont(42);
	pave33.SetTextColor(kBlue);
	pave33.SetTextSize(top2*0.5);
	TLegend *leg = new TLegend(0.72,0.755,0.85,0.875);
	leg->SetFillColor(0);
	leg->SetBorderSize(0);
	leg->SetTextFont(42);
	leg->SetTextSize(0.025);
	leg->AddEntry(hist_S2,"Sig","F");
	leg->AddEntry(hist_B2,"BG","F");

	double bin=0.;
	double s1=0; double b1=0;
	int i=0;
	float TOTAL_S2OB = 0;

	for(int i = 0; i < (int) hist_S2->GetEntries(); i++){
		s1 = hist_S2->GetBinContent(i+1); // +1 to skip underflow bin
		b1 = hist_B2->GetBinContent(i+1);
		// if(b1 != 0) TOTAL_S2OB += pow(s1,2) / (b1);
		if(b1 != 0) TOTAL_S2OB += ((2*(s1+b1)*log(1+(s1/b1))) - 2*s1);
	}

	// Do these indices with a max of 10 corresond to a max of 10 categories?
	double max = 0;
	double borders[10] = {};   // including START and END
	borders[0] = START;
	double sig_n[10] = {0,0,0,0,0,0,0,0,0,0};
	double bkg_n[10] = {0,0,0,0,0,0,0,0,0,0};
	double data_n[10] = {0,0,0,0,0,0,0,0,0,0};
	double bkg_sideband_n[10] = {0,0,0,0,0,0,0,0,0,0};
	double data_sideband_n[10] = {0,0,0,0,0,0,0,0,0,0};
	double max_n[10] = {0,0,0,0,0,0,0,0,0,0};
	double max_final[10] = {0,0,0,0,0,0,0,0,0,0};
	double max_total = 0;
	double start_n[10] = {0,0,0,0,0,0,0,0,0,0};
	double bkg_yields[10] = {0,0,0,0,0,0,0,0,0,0};
	double bkg_yields_sideband[10] = {0,0,0,0,0,0,0,0,0,0};
	double data_yields[10] = {0,0,0,0,0,0,0,0,0,0};
	double data_yields_sideband[10] = {0,0,0,0,0,0,0,0,0,0};
	double sig_yields[10] = {0,0,0,0,0,0,0,0,0,0};

	for (int index = 0; index < NCATS; index++){
		start_n[index]=START+(index+1)*bin_width; // what is start_n? Initial CAT Minimum maybe
		// cout << "start_n[" << index << "] = " << start_n[index] << endl;
	}
	int minevt_cond_n[10] = {};

	std::vector<double> categories_scans;
	std::vector<double> significance_scans;

	// Categorization
	do {
		max_n[0] = 0; // I think S^2 / B for one or all categories
		sig_n[0] = hist_S_2016->Integral(1,hist_S_2016->FindBin(start_n[0])-1); // Optimize cats based on integral of Signifiance?
		bkg_n[0] = hist_B->Integral(1,hist_B->FindBin(start_n[0])-1);

		// Sidebands
		bkg_sideband_n[0] = hist_B_sideband->Integral(1,hist_B_sideband->FindBin(start_n[0])-1);
		data_sideband_n[0] = hist_D_sideband->Integral(1,hist_D_sideband->FindBin(start_n[0])-1);

		// if (bkg_n[0]!=0) max_n[0]=pow(sig_n[0],2)/bkg_n[0];
		if (bkg_n[0]!=0) max_n[0]=(2*(sig_n[0]+bkg_n[0])*log(1+(sig_n[0]/bkg_n[0]))) - 2*sig_n[0];
		start_n[1]=start_n[0]+bin_width; // initial min for second category?

		bkg_sideband_n[1] = hist_B_sideband->Integral(hist_B_sideband->FindBin(start_n[0]),hist_B_sideband->GetNbinsX()+1);
		data_sideband_n[1] = hist_D_sideband->Integral(hist_D_sideband->FindBin(start_n[0]),hist_D_sideband->GetNbinsX()+1);

		// cout << "#1 BIN " << start_n[0] << endl;

		// if (bkg_n[1]!=0) max_n[1]=pow(sig_n[1],2)/bkg_n[1];
		if (bkg_n[1]!=0) max_n[1]=(2*(sig_n[1]+bkg_n[1])*log(1+(sig_n[1]/bkg_n[1]))) - 2*sig_n[1];

		categories_scans.push_back(start_n[0]);
		significance_scans.push_back(sqrt(max_n[1]));

		do {
			max_n[1]=0;
			sig_n[1] = hist_S_2016->Integral(hist_S_2016->FindBin(start_n[0]),hist_S_2016->FindBin(start_n[1])-1);
			bkg_n[1] = hist_B->Integral(hist_B->FindBin(start_n[0]),hist_B->FindBin(start_n[1])-1);
			bkg_sideband_n[1] = hist_B_sideband->Integral(hist_B_sideband->FindBin(start_n[0]),hist_B_sideband->FindBin(start_n[1])-1);
			data_sideband_n[1] = hist_D_sideband->Integral(hist_D_sideband->FindBin(start_n[0]),hist_D_sideband->FindBin(start_n[1])-1);

			// cout << "#2 BIN " << start_n[0] << endl;

			// if (bkg_n[1]!=0) max_n[1]=pow(sig_n[1],2)/bkg_n[1];
			if (bkg_n[1]!=0) max_n[1]=(2*(sig_n[1]+bkg_n[1])*log(1+(sig_n[1]/bkg_n[1]))) - 2*sig_n[1];

			start_n[2]=start_n[1]+bin_width;
			do{
				max_n[2]=0;
				if (NCATS<=2) {
					sig_n[2] = 0;
					bkg_n[2] = 1;
					bkg_sideband_n[2] = 1;
					data_n[2] = 1;
					data_sideband_n[2] = 1;
				} else {
					sig_n[2] = hist_S_2016->Integral(hist_S_2016->FindBin(start_n[1]),hist_S_2016->FindBin(start_n[2])-1);
					bkg_n[2] = hist_B->Integral(hist_B->FindBin(start_n[1]),hist_B->FindBin(start_n[2])-1);
					bkg_sideband_n[2] = hist_B_sideband->Integral(hist_B_sideband->FindBin(start_n[1]),hist_B_sideband->FindBin(start_n[2])-1);
					data_sideband_n[2] = hist_D_sideband->Integral(hist_D_sideband->FindBin(start_n[1]),hist_D_sideband->FindBin(start_n[2])-1);

					// cout << "#3 BIN " << start_n[1] << endl;

				}
				// if (bkg_n[2]!=0) max_n[2]=pow(sig_n[2],2)/bkg_n[2];
				if (bkg_n[2]!=0) max_n[2]=(2*(sig_n[2]+bkg_n[2])*log(1+(sig_n[2]/bkg_n[2]))) - 2*sig_n[2];

				start_n[3]=start_n[2]+bin_width;
				do{
					max_n[3]=0;
					if (NCATS<=3) {
						sig_n[3] = 0;
						bkg_n[3] = 1;
						bkg_sideband_n[3] = 1;
						data_sideband_n[3] = 1;
					}

					else {
						sig_n[3] = hist_S_2016->Integral(hist_S_2016->FindBin(start_n[2]),hist_S_2016->FindBin(start_n[3])-1);
						bkg_n[3] = hist_B->Integral(hist_B->FindBin(start_n[2]),hist_B->FindBin(start_n[3])-1);
						bkg_sideband_n[3] = hist_B_sideband->Integral(hist_B_sideband->FindBin(start_n[2]),hist_B_sideband->FindBin(start_n[3])-1);
						data_sideband_n[3] = hist_D_sideband->Integral(hist_D_sideband->FindBin(start_n[2]),hist_D_sideband->FindBin(start_n[3])-1);

					}
					// if (bkg_n[3]!=0) max_n[3]=pow(sig_n[3],2)/bkg_n[3];
					if (bkg_n[3]!=0) max_n[3]=(2*(sig_n[3]+bkg_n[3])*log(1+(sig_n[3]/bkg_n[3]))) - 2*sig_n[3];

					max_n[4]=0;

					if (NCATS<=4)
					{
						sig_n[4] = 0.;
						bkg_n[4] = 1.;
						bkg_sideband_n[4] = 1.;
						data_sideband_n[4] = 1.;
					}

					else
					{
						// cout << "[5 CATEGORIES]" << endl;
						sig_n[4] = hist_S_2016->Integral(hist_S_2016->FindBin(start_n[3]),hist_S_2016->GetNbinsX()+1); // FindBin returns the bin number corresponding to the x value
						bkg_n[4] = hist_B->Integral(hist_B->FindBin(start_n[3]),hist_B->GetNbinsX()+1); //

						// Sidebands
						bkg_sideband_n[4] = hist_B_sideband->Integral(hist_B_sideband->FindBin(start_n[3]),hist_B_sideband->GetNbinsX()+1);
						data_sideband_n[4] = hist_D_sideband->Integral(hist_D_sideband->FindBin(start_n[3]),hist_D_sideband->GetNbinsX()+1);

						// cout << "#5 BIN " << start_n[3] << endl;

					}

					// cout << "[bkg_sideband_n[4]]: " << bkg_sideband_n[4] <<   " [data_sideband_n[4]]: " << data_sideband_n[4] << " [sig_n[4]]: " << sig_n[4] <<  " [bkg_n[4]]: " << bkg_n[4] << endl;

					// if (bkg_n[4]!=0) max_n[4]=pow(sig_n[4],2)/bkg_n[4];
					if (bkg_n[4]!=0) max_n[4]=(2*(sig_n[4]+bkg_n[4])*log(1+(sig_n[4]/bkg_n[4]))) - 2*sig_n[4];

					double max_sum = 0;
					int minevt_cond = 0; //condition is false
					for (int index=0;index<NCATS;index++){ //start from 1 for tth only when optimizing separately
						max_sum+=max_n[index];
						// minevt_cond_n[index] = ( (data_sideband_n[index] >= 1));
						 // minevt_cond_n[index] = (bkg_sideband_n[index]>=minevents );
						minevt_cond_n[index] = (bkg_sideband_n[index]>=minevents && data_sideband_n[index] >= minevents);
					}
					minevt_cond = std::accumulate(minevt_cond_n, minevt_cond_n + NCATS, 0); // minevt_cond_n+1 for tth only when optimizing separately
					if (((max_sum)>=max) && (minevt_cond==(NCATS))) { //NCATS-1 for tth
						max = max_sum;
						for (int index=0;index<NCATS;index++){
							borders[index+1] = start_n[index]; // first and last are START and END
							max_final[index] = max_n[index];
							bkg_yields[index] = bkg_n[index];
							bkg_yields_sideband[index] = bkg_sideband_n[index];
							data_yields_sideband[index] = data_sideband_n[index];
							// cout << "[data_sideband_n[index]] = " << data_sideband_n[index] << endl;
							sig_yields[index] = sig_n[index];
							max_total = max_sum;
						}
					}
					start_n[3]+=bin_width;
				} while (start_n[3]<=(END-(NCATS-4)*bin_width)); // probably max at num cats - NCATS because you can't determine the significance integral for the 1st category so high that cats can't be added at bins starting above it
				start_n[2]+=bin_width;
			} while (start_n[2]<=(END-(NCATS-3)*bin_width));
			start_n[1]+=bin_width;
		} while (start_n[1]<=(END-(NCATS-2)*bin_width));
		start_n[0]+=bin_width;
	} while (start_n[0]<=(END-(NCATS-1)*bin_width));

	borders[NCATS] = END;

	// // Save Border Values to Text File
	// ofstream outborder;
	// outborder.open(s.Format("test.txt"));

	// outborder.open(s.Format("%s%s_%s.txt",outDir.Data(),outnameborder.Data(),scaleOpt.Data()));
	for (int index=0;index<NCATS+1;index++)
	     cout << "borders[index]" << borders[index] << endl;
		// outborder<<borders[index] << "\t";
	// outborder<<endl;
	// outborder.close();

	// Write Output Text File
	ofstream out;
	out.open(s.Format("%s%s_%s_xmin-%s_binWidth-%s.txt",outDir.Data(),outname.Data(),scaleOpt.Data(),xmin_str.Data(),binWidth_str.Data()));
	out << "(S**2)tot/Btot over all bins: " << TOTAL_S2OB << endl;
	out << endl;
	out << "sqrt((S**2)tot/Btot) over all bins: " << sqrt(TOTAL_S2OB) << endl;
	out << endl;
	out << "S**2/B total over the chosen categories : " << max_total << "  , S/sqrt(B) =  " << sqrt(max_total) << endl;
	out << endl;
	out << "borders of categories : ";
	for (int index=0;index<NCATS+1;index++)
		out << borders[index] << "\t";
	out << endl;
	out << endl;
	out << "S**2/B in each category : ";
	for (int index=0;index<NCATS;index++)
		out << max_final[index] << "\t";
	out << endl;
	out << endl;
	out << "sqrt(S**2/B) in each category : ";
	for (int index=0;index<NCATS;index++)
		out << sqrt(max_final[index]) << "\t";
	out << endl;
	out << endl;
	out << "Mgg sidebands bkg yields in categories : ";
	for (int index=0;index<NCATS;index++)
		out << bkg_yields_sideband[index] << "\t";
	out << endl;
	out << "bkg yields in categories : ";
	for (int index=0;index<NCATS;index++)
		out << bkg_yields[index] << "\t";
	out << endl;
	out << "sig yields in categories : ";
	for (int index=0;index<NCATS;index++)
		out << sig_yields[index] << "\t";
	out << endl;
	out << "Mgg sidebands data yields in categories : ";
	for (int index=0;index<NCATS;index++)
		out << data_yields_sideband[index] << "\t";
	out << endl;
	out.close();

	string line;
	ifstream outfile(s.Format("%s%s_fineBinning_combined.txt",outDir.Data(),outname.Data()));
	if (outfile.is_open()){
		while ( getline (outfile,line) )
		cout << line << '\n';
		outfile.close();
	}

	// float ymin=hist_B2->GetBinContent(hist_B2->FindFirstBinAbove(0.))*0.1;
	// float ymin=hist_S2->GetBinContent(hist_S2->FindFirstBinAbove(0.))*0.1;
	float ymin = 0.0001;
	// float ymin = 0.0001;
	float ymax=hist_B2->GetMaximum()*1e02;

	TLine* lines[10];
	for (int index=0;index<NCATS-1;index++){
		lines[index] = new TLine(borders[index+1],ymin,borders[index+1],hist_B2->GetBinContent(hist_B2->FindBin(borders[index+1]))+5);
		lines[index]->SetLineStyle(9);
		lines[index]->SetLineColor(1);
		lines[index]->SetLineWidth(3);
	}

	TCanvas *c1 = new TCanvas("Fit","",800,800);
	c1->SetLogy();
	c1->cd();
	TH1F *frame2 = new TH1F("frame2","",50,xmin,xmax);

	frame2->GetXaxis()->SetNdivisions(505);
	frame2->GetYaxis()->SetRangeUser(80,150);
	frame2->SetStats(0);
	frame2->SetYTitle("Events");
	frame2->SetXTitle(s.Format("%s",what_to_opt.Data()));
	frame2->SetMinimum(ymin);
	frame2->SetMaximum(ymax);
	frame2->Draw();

	// hist_B2->GetXaxis()->SetRange(0,1);
	// hist_S2->GetXaxis()->SetRange(0,1);
	hist_B2->Draw("HISTsame");
	float hist_B2_max = hist_B2->GetMaximum();
	// cout << "[Max bkg]: " << hist_B2_max << endl;
	// hist_S2->Scale(100./hist_B2_max);
	hist_S2->Draw("HISTsame");
	// hist_S2->Scale(131.78);
	// hist_B_cut_tth->Draw("HISTsame")
	TLatex latex;
	latex.SetTextSize(0.025);
	latex.SetTextAlign(13);  //align at top
	// for (int index=0;index<NCATS;index++)
		// latex.DrawLatex(-1,100000,std::to_string(sig_yields[index]).c_str());
    // latex.DrawLatex(-1,100000,"K_{S}");
	// latex.Draw();
	// leg->AddEntry(hist_B_cut_tth,"ttH","L");

	gPad->Update();
	// pCMS1.Draw("same");
	// pCMS2.Draw("same");
	// pCMS12.Draw("same");
	// pave22.Draw("same");
	// pave33.Draw("same");
	leg->Draw("same");
	for (int index=0;index<NCATS-1;index++)
		lines[index]->Draw("same");
	gPad->RedrawAxis();
	c1->Print(s.Format("%s/%s_%s_xMin-%s_binWidth-%s.png",outDir.Data(),scaleOpt.Data(),outname.Data(),xmin_str.Data(),binWidth_str.Data()));
	// c1->Print(s.Format("%s/%s_%s_xMin-%s_binIwdth-%s.pdf",outDir.Data(),scaleOpt.Data(),outname.Data(),xmin_str.Data(),binWidth_str.Data()));

	double* cat_scan = &categories_scans[0];
	double* sign_scan = &significance_scans[0];
	int counter = significance_scans.size();

	// TGraph *gr = new TGraph(counter,cat_scan,sign_scan); // significance plot

	// cout << sign_scan << endl;
	// cout << "ymin: " << *std::max_element(sign_scan,sign_scan+counter) << endl;
	// old end of ymin: * 0.01
	ymin = *std::max_element(sign_scan,sign_scan+counter) * 0.01;
	ymax = *std::max_element(sign_scan,sign_scan+counter) * 1.1;
	// gr->SetMarkerStyle(20);
	int max_pos = std::distance(sign_scan, std::max_element(sign_scan,sign_scan+counter));

	TCanvas *c2 = new TCanvas("B","",800,800);
	c2->cd();
	TH1F *frame3 = new TH1F("frame3","",50,xmin,xmax);
	frame3->GetXaxis()->SetNdivisions(505);
	frame3->SetStats(0);
	frame3->SetYTitle("S/#sqrt{B}");
	frame3->GetYaxis()->SetTitleOffset(1.32);
	frame3->SetXTitle(s.Format("%s",what_to_opt.Data()));
	frame3->SetMinimum(ymin);
	frame3->SetMaximum(ymax);
	frame3->Draw();
	// gr->Draw("Psame");
	gPad->Update();
	// pCMS1.Draw("same");
	// pCMS2.Draw("same");
	// pCMS12.Draw("same");
	// pave22.Draw("same");
	// pave33.Draw("same");
	gPad->RedrawAxis();

	// Make Significance Plots
	cout << "Signal integral: " << hist_S2->Integral() << endl;;
	cout << "Background integral: " << hist_B2->Integral() << endl;;

	cout << "Total Significance integral: " << hist_S2->Integral() / sqrt(hist_B2->Integral()) << endl;

	gStyle->SetOptStat(0000);
	int bin_i = 0;
	double sig, bkg = 0.;
	double sigOverSqrtb = 0;
	double maxsigOverSqrtb = -99;
	TH1F * Significance_h = new TH1F("Significance_h","S/#sqrt{B} vs. DNN Score " + scaleOpt,int((xmax-xmin)/bin_width),xmin,xmax);
	for(int i = 0; i < (int) hist_S2->GetNbinsX(); i++){
		bin_i = i + 1; // +1 to skip underflow bin
		sig = hist_S2->GetBinContent(bin_i);
		bkg = hist_B2->GetBinContent(bin_i);

		// if(verbose){
			// cout << "evalDNN bin x min: " << Significance_h->GetBinLowEdge(bin_i) << endl;
			// cout << "S : " << sig << endl;
			// cout << "B : " << bkg << endl;
		// }


		if(bkg > 0){
			sigOverSqrtb = sig / sqrt(bkg);
			Significance_h->SetBinContent(bin_i, sigOverSqrtb);
			if(sigOverSqrtb > maxsigOverSqrtb) maxsigOverSqrtb = sigOverSqrtb;
			// cout << "evalDNN bin x min: " << Significance_h->GetBinLowEdge(bin_i) << endl;
			// cout << "S : " << sig << endl;
			// cout << "B : " << bkg << endl;
			// cout << "significance: " << sigOverSqrtb << endl;
		}
		else{
			// cout << "for DNN val: " << Significance_h->GetBinLowEdge(bin_i) << ", Background Yield < 0: " << bkg << endl;
			Significance_h->SetBinContent(bin_i, 0);

		}
	}

	// TH1F * Shaded_Area = new TH1F("Shaded_Area","S/#sqrt{B} vs. DNN Score " + scaleOpt,1,xmin,xcutoff);
	// Shaded_Area->SetFillColorAlpha(kRed,0.5);

	// Get Total Significance for each category
	ofstream catSigOut;
	catSigOut.open(s.Format("%s%s_%s_xmin-%s_binWidth-%s_CatSignificances.txt",outDir.Data(),outname.Data(),scaleOpt.Data(),xmin_str.Data(),binWidth_str.Data()));

	ofstream catSigOut_p1Bin;
	catSigOut_p1Bin.open(s.Format("%s%s_%s_xmin-%s_binWidth-%s_CatSignificances_p1Bin.txt",outDir.Data(),outname.Data(),scaleOpt.Data(),xmin_str.Data(),binWidth_str.Data()));

	ofstream catSigOut_m1Bin;
	catSigOut_m1Bin.open(s.Format("%s%s_%s_xmin-%s_binWidth-%s_CatSignificances_m1Bin.txt",outDir.Data(),outname.Data(),scaleOpt.Data(),xmin_str.Data(),binWidth_str.Data()));

	ofstream catSigOut_p2Bin;
	catSigOut_p2Bin.open(s.Format("%s%s_%s_xmin-%s_binWidth-%s_CatSignificances_p2Bin.txt",outDir.Data(),outname.Data(),scaleOpt.Data(),xmin_str.Data(),binWidth_str.Data()));

	ofstream catSigOut_m2Bin;
	catSigOut_m2Bin.open(s.Format("%s%s_%s_xmin-%s_binWidth-%s_CatSignificances_m2Bin.txt",outDir.Data(),outname.Data(),scaleOpt.Data(),xmin_str.Data(),binWidth_str.Data()));


	double cat_min, cat_max, cat_min_p1Bin, cat_max_p1Bin, cat_min_m1Bin, cat_max_m1Bin,cat_min_p2Bin, cat_max_p2Bin, cat_min_m2Bin, cat_max_m2Bin  = 0.;
	double Cat_significance, Cat_significance_p1Bin, Cat_significance_m1Bin, Cat_significance_p2Bin, Cat_significance_m2Bin = 0.;
	int min_bin, max_bin, min_bin_p1Bin, max_bin_p1Bin, min_bin_m1Bin, max_bin_m1Bin,min_bin_p2Bin, max_bin_p2Bin, min_bin_m2Bin, max_bin_m2Bin = 0;
	double S_total, B_total,S_total_p1Bin, B_total_p1Bin, S_total_p2Bin, B_total_p2Bin,S_total_m1Bin, B_total_m1Bin, S_total_m2Bin, B_total_m2Bin  = 0;
	double data_sideband_total;
	int numBins = int((xmax-xmin)/bin_width);
	double tot_sig, tot_sig_p1Bin, tot_sig_p2Bin, tot_sig_m1Bin, tot_sig_m2Bin = 0;

	catSigOut << "Category boundary: " <<   "Significance:  "  << "Signal events:  "  << "Bkg events:  "  << "Data sideband" << "\n";
	catSigOut_p1Bin << "Category boundary: " <<   "Significance:  "  << "Signal events:  "  << "Bkg events"  << "\n";
	catSigOut_m1Bin << "Category boundary: " <<   "Significance:  "  << "Signal events:  "  << "Bkg events"  << "\n";
	catSigOut_p2Bin << "Category boundary: " <<   "Significance:  "  << "Signal events:  "  << "Bkg events"  << "\n";
	catSigOut_m2Bin << "Category boundary: " <<   "Significance:  "  << "Signal events:  "  << "Bkg events"  << "\n";
        cout << "[NCATS]: " << NCATS << endl;
	for(int i = 0; i < NCATS; i++){
        cout << "[i]: " << i << endl;
		if(i == 0){
			cat_min = xcutoff;
			cat_max = borders[i+1];

			cat_min_p1Bin = xcutoff;
			cat_max_p1Bin = borders[i+1] + bin_width;

			cat_min_p2Bin = xcutoff;
			cat_max_p2Bin = borders[i+1] + 2*bin_width;

			cat_min_m1Bin = xcutoff;
			cat_max_m1Bin = borders[i+1] - bin_width;

			cat_min_m2Bin = xcutoff;
			cat_max_m2Bin = borders[i+1] - 2*bin_width;


		}
		else if (i>0 and i!=NCATS-1 ){
			cat_min = borders[i];
			cat_max = borders[i+1];

			cat_min_p1Bin = borders[i] + bin_width;
			cat_max_p1Bin = borders[i+1] + bin_width;

			cat_min_m1Bin = borders[i] - bin_width;
			cat_max_m1Bin = borders[i+1] - bin_width;

			cat_min_p2Bin = borders[i] + 2*bin_width;
			cat_max_p2Bin = borders[i+1] + 2*bin_width;

			cat_min_m2Bin = borders[i] - 2*bin_width;
			cat_max_m2Bin = borders[i+1] - 2*bin_width;


		}
               else if (i==NCATS-1){
                        cat_min = borders[i];
                        cat_max = borders[i+1];

                        cat_min_p1Bin = borders[i] + bin_width;
                        cat_max_p1Bin = borders[i+1] + bin_width;

                        cat_min_m1Bin = borders[i] - bin_width;
                        cat_max_m1Bin=1;

                        cat_min_p2Bin = borders[i] + 2*bin_width;
                        cat_max_p2Bin = borders[i+1] + 2*bin_width;

                        cat_min_m2Bin = borders[i] - 2*bin_width;
                        cat_max_m2Bin =1;
                }

		cout << "Cat min: " << cat_min << endl;
		cout << "Cat max: " << cat_max << endl;

		min_bin = (cat_min - xmin) / bin_width + 1;
		max_bin = (cat_max - xmin) / bin_width;

		min_bin_p1Bin = (cat_min_p1Bin - xmin) / bin_width + 1;
		max_bin_p1Bin = (cat_max_p1Bin - xmin) / bin_width;

		min_bin_p2Bin = (cat_min_p2Bin - xmin) / bin_width + 1;
		max_bin_p2Bin = (cat_max_p2Bin - xmin) / bin_width;

		min_bin_m1Bin = (cat_min_m1Bin - xmin) / bin_width + 1;
		max_bin_m1Bin = (cat_max_m1Bin - xmin) / bin_width;

		min_bin_m2Bin = (cat_min_m2Bin - xmin) / bin_width + 1;
		max_bin_m2Bin = (cat_max_m2Bin - xmin) / bin_width;

		cout << "min_bin low edge: " << hist_S2->GetBinLowEdge(min_bin) << endl;
		cout << "max_bin low edge: " << hist_S2->GetBinLowEdge(max_bin) << endl;

		Cat_significance = Significance_h->Integral(min_bin,max_bin); // significance for all signal region events in this category
		S_total = hist_S2->Integral(min_bin, max_bin);
		B_total = hist_B2->Integral(min_bin, max_bin);
		data_sideband_total = hist_D_sideband->Integral(min_bin, max_bin);

		S_total_p1Bin = hist_S2->Integral(min_bin_p1Bin, max_bin_p1Bin);
		B_total_p1Bin = hist_B2->Integral(min_bin_p1Bin, max_bin_p1Bin);

		S_total_p2Bin = hist_S2->Integral(min_bin_p2Bin, max_bin_p2Bin);
		B_total_p2Bin = hist_B2->Integral(min_bin_p2Bin, max_bin_p2Bin);

		S_total_m1Bin = hist_S2->Integral(min_bin_m1Bin, max_bin_m1Bin);
		B_total_m1Bin = hist_B2->Integral(min_bin_m1Bin, max_bin_m1Bin);

		S_total_m2Bin = hist_S2->Integral(min_bin_m2Bin, max_bin_m2Bin);
		B_total_m2Bin = hist_B2->Integral(min_bin_m2Bin, max_bin_m2Bin);

		// S_total = hist_S_2016_eval->Integral(min_bin, max_bin);
		// B_total = hist_B2->Integral(min_bin, max_bin);
		// data_sideband_total = hist_D_sideband->Integral(min_bin, max_bin);
		//
		// S_total_p1Bin = hist_S_2016_eval->Integral(min_bin_p1Bin, max_bin_p1Bin);
		// B_total_p1Bin = hist_B2->Integral(min_bin_p1Bin, max_bin_p1Bin);
		//
		// S_total_p2Bin = hist_S_2016_eval->Integral(min_bin_p2Bin, max_bin_p2Bin);
		// B_total_p2Bin = hist_B2->Integral(min_bin_p2Bin, max_bin_p2Bin);
		//
		// S_total_m1Bin = hist_S_2016_eval->Integral(min_bin_m1Bin, max_bin_m1Bin);
		// B_total_m1Bin = hist_B2->Integral(min_bin_m1Bin, max_bin_m1Bin);
		//
		// S_total_m2Bin = hist_S_2016_eval->Integral(min_bin_m2Bin, max_bin_m2Bin);
		// B_total_m2Bin = hist_B2->Integral(min_bin_m2Bin, max_bin_m2Bin);



		cout << "S: " << S_total << endl;
		cout << "B: " << B_total << endl;

		// Cat_significance = S_total / sqrt(B_total);
		Cat_significance = sqrt( (2*(S_total+B_total)*log(1+(S_total/B_total))) - 2*S_total );
		tot_sig += Cat_significance*Cat_significance;
		cout << "Significance in the signal region events: " << Cat_significance << endl;

		Cat_significance_p1Bin = sqrt( (2*(S_total_p1Bin+B_total_p1Bin)*log(1+(S_total_p1Bin/B_total_p1Bin))) - 2*S_total_p1Bin );
		tot_sig_p1Bin += Cat_significance_p1Bin*Cat_significance_p1Bin;

		Cat_significance_p2Bin = sqrt( (2*(S_total_p2Bin+B_total_p2Bin)*log(1+(S_total_p2Bin/B_total_p2Bin))) - 2*S_total_p2Bin );
		tot_sig_p2Bin += Cat_significance_p2Bin*Cat_significance_p2Bin;

		Cat_significance_m1Bin = sqrt( (2*(S_total_m1Bin+B_total_m1Bin)*log(1+(S_total_m1Bin/B_total_m1Bin))) - 2*S_total_m1Bin );
		tot_sig_m1Bin += Cat_significance_m1Bin*Cat_significance_m1Bin;

		Cat_significance_m2Bin = sqrt( (2*(S_total_m2Bin+B_total_m2Bin)*log(1+(S_total_m2Bin/B_total_m2Bin))) - 2*S_total_m2Bin );
		tot_sig_m2Bin += Cat_significance_m2Bin*Cat_significance_m2Bin;

		catSigOut << "Cat: [" << cat_min << ", " << cat_max << "]: " << Cat_significance << " :" <<  S_total << " :" << B_total << " :" << data_sideband_total << "\n";
		catSigOut_p1Bin << "Cat: [" << cat_min_p1Bin << ", " << cat_max_p1Bin << "]: " << Cat_significance_p1Bin << " :" <<  S_total_p1Bin << " :" << B_total_p1Bin << "\n";
		catSigOut_p2Bin << "Cat: [" << cat_min_p2Bin << ", " << cat_max_p2Bin << "]: " << Cat_significance_p2Bin << " :" <<  S_total_p2Bin << " :" << B_total_p2Bin << "\n";
		catSigOut_m1Bin << "Cat: [" << cat_min_m1Bin << ", " << cat_max_m1Bin << "]: " << Cat_significance_m1Bin << " :" <<  S_total_m1Bin << " :" << B_total_m1Bin << "\n";
		catSigOut_m2Bin << "Cat: [" << cat_min_m2Bin << ", " << cat_max_m2Bin << "]: " << Cat_significance_m2Bin << " :" <<  S_total_m2Bin << " :" << B_total_m2Bin << "\n";

	}
  catSigOut << "Total Significance: " << sqrt(tot_sig) << "\n";
	catSigOut.close();

	catSigOut_p1Bin << "Total Significance: " << sqrt(tot_sig_p1Bin) << "\n";
	catSigOut_p1Bin.close();

	catSigOut_p2Bin << "Total Significance: " << sqrt(tot_sig_p2Bin) << "\n";
	catSigOut_p2Bin.close();

	catSigOut_m1Bin << "Total Significance: " << sqrt(tot_sig_m1Bin) << "\n";
	catSigOut_m1Bin.close();

	catSigOut_m2Bin << "Total Significance: " << sqrt(tot_sig_m2Bin) << "\n";
	catSigOut_m2Bin.close();


	TCanvas * sig_c = new TCanvas("sig_c","sig_c",800,600);
	sig_c->cd();
	Significance_h->SetMarkerStyle(kFullCircle);
	Significance_h->GetXaxis()->SetTitle(what_to_opt);
	Significance_h->GetYaxis()->SetTitle("S/#sqrt{B}");
	Significance_h->Draw("P");

	TLine* CatLines[10];
	double canvas_ymin, canvas_ymax = 0.;
	sig_c->Update(); // https://root-forum.cern.ch/t/drawing-tline-over-a-histogram/10279/3
	canvas_ymin = sig_c->GetUymin();
	canvas_ymax = sig_c->GetUymax();
	// double cat_min, cat_max = 0.;
	for (int i = 0; i < NCATS-1; i++){
		CatLines[i] = new TLine(borders[i+1],canvas_ymin,borders[i+1],canvas_ymax);
		CatLines[i]->SetLineStyle(9);
		CatLines[i]->SetLineColor(1);
		CatLines[i]->SetLineWidth(3);
		CatLines[i]->Draw("same");
	}

	// Shaded_Area->Fill(0.00001,canvas_ymax);
	// Shaded_Area->Draw("hist same");

	sig_c->SaveAs(outDir + "Significance_" + scaleOpt + "_xmin-" + xmin_str + "_binWidth-" + binWidth_str + ".png");

	TCanvas * sig_c_log = new TCanvas("sig_c_log","sig_c_log",800,600);
	sig_c_log->cd();
	Significance_h->Draw("P");
	sig_c_log->SetLogy();
	gPad->Update();
	TLine* CatLinesLog[10];
	canvas_ymin = sig_c->GetUymin();
	canvas_ymax = sig_c->GetUymax();
	for (int i = 0; i < NCATS-1; i++){
		Double_t lm = gPad->GetLeftMargin();
		Double_t rm = 1.-gPad->GetRightMargin();
		Double_t tm = 1.-gPad->GetTopMargin();
		Double_t bm = gPad->GetBottomMargin();
		Double_t xndc = (rm-lm)*((borders[i+1]-gPad->GetUxmin())/(gPad->GetUxmax()-gPad->GetUxmin()))+lm;
		CatLinesLog[i] = new TLine(borders[i+1],bm,borders[i+1],tm);
		CatLinesLog[i]->SetLineStyle(9);
		CatLinesLog[i]->SetLineColor(1);
		CatLinesLog[i]->SetLineWidth(3);
		CatLinesLog[i]->DrawLineNDC(xndc,bm,xndc,tm);
	}

	// Shaded_Area->SetBinContent(1,100);
	// Shaded_Area->Draw("hist same");
	sig_c_log->SaveAs(outDir + "Significance_" + scaleOpt + "_xmin-" + xmin_str + "_binWidth-" + binWidth_str + "_log.png");
}
