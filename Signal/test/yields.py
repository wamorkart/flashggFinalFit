import ROOT
from ROOT import *
from optparse import OptionParser, make_option
import sys
import os
from math import sqrt

filename = '/afs/cern.ch/work/n/nchernya/ETH/CMSSW_7_4_7/src/flashggFinalFit/Signal/CMS-HGG_sigfit_02_11_2018_20162017.root'
filename_bkg = '/afs/cern.ch/work/n/nchernya/ETH/CMSSW_7_4_7/src/flashggFinalFit/Background/CMS-HGG_multipdf_HHbbgg_data2016_2017_30_10_2018.root'
wsname = 'wsig_13TeV'
wsname_bkg = 'multipdf'

num_cat = 12
lumi_2016=35.9*1000
lumi_2017=41.5*1000
#lumi_2016=1000.
#lumi_2017=1000.
SMsignal=33.49*0.58*0.00227*2
#SMsignal=1
names='GluGluToHHTo2B2G_node_SM_13TeV_madgraph,GluGluHToGG_M_125_13TeV_powheg_pythia8,VBFHToGG_M_125_13TeV_powheg_pythia8,ttHToGG_M125_13TeV_powheg_pythia8_v2,VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8,GluGluToHHTo2B2G_node_SM_13TeV_madgraph_2017,GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8_2017,VBFHToGG_M125_13TeV_amcatnlo_pythia8_2017,ttHToGG_M125_13TeV_powheg_pythia8_2017,VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8_2017'.split(',')
tpMap = {"GluGluToHHTo2B2G_node_SM_13TeV_madgraph":"HHbbgg_2016","GluGluHToGG_M_125_13TeV_powheg_pythia8":"GF_2016","VBFHToGG_M_125_13TeV_powheg_pythia8":"VBF_2016","ttHToGG_M125_13TeV_powheg_pythia8_v2":"ttH_2016","VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8":"VH_2016","GluGluToHHTo2B2G_node_SM_13TeV_madgraph_2017":"HHbbgg_2017","GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8_2017":"GF_2017","VBFHToGG_M125_13TeV_amcatnlo_pythia8_2017":"VBF_2017","ttHToGG_M125_13TeV_powheg_pythia8_2017":"ttH_2017","VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8_2017":"VH_2017"}
sum_entries = dict()
sum_entries_bkg = dict()


tfile = TFile(filename)
ws = tfile.Get(wsname)
for name in names:
	print '%s\t'%(tpMap[name]),
	sum=0.
	lumi = 1.
	if '2017' in name : lumi = lumi_2017
	else : lumi = lumi_2016
	for cat in range(0,num_cat):
		ws_name = 'hggpdfsmrel_13TeV_%s_DoubleHTag_%d_norm'%(name,cat)
		var = (ws.var('MH'))
		var.setVal(125)
		entries = (ws.function(ws_name).getVal())
		sum_entries[name] = entries
		count = entries*lumi
		if 'HHbbgg' in tpMap[name] : count*=SMsignal
		sum+=count
	#	print '%.2f\t'%(count),
		print '%.4f\t'%(count),
	print '%.2f'%sum



tfile = TFile(filename_bkg)
ws_bkg = tfile.Get(wsname_bkg)
sum_bkg=0.
print 'Data 2016+2017\t',
for cat in range(0,num_cat):
	name = 'roohist_data_mass_DoubleHTag_%d'%(cat)
	entries = ws_bkg.data(name).sumEntries()
	sum_entries_bkg[name] = entries
	sum_bkg+=entries
	print '%.2f\t'%(entries),
print '%.2f'%sum_bkg

########################
filename_bkg_2016 = '/afs/cern.ch/work/n/nchernya/ETH/DiHiggs/root_file/02_11_2018/2016/output_DoubleEG_micheli-ReMiniAOD2016.root'
filename_bkg_2017 = '/afs/cern.ch/work/n/nchernya/ETH/DiHiggs/root_file/02_11_2018/2017/output_DoubleEG_spigazzi-RunIIFall17-3_2_0-RunIIFall17-3_2_0_all.root'
filename_bkg_total = '/afs/cern.ch/work/n/nchernya/ETH/DiHiggs/root_file/02_11_2018/output_DoubleEG_2016_2017_30_10_2018.root'
years=['2016','2017','Total']
for num,name in enumerate([filename_bkg_2016,filename_bkg_2017,filename_bkg_total]):
	tfile = TFile(name)
	wsname_bkg = 'tagsDumper/cms_hgg_13TeV'
	ws_bkg = tfile.Get(wsname_bkg)
	sum_bkg=0.
	print 'Data %s\t'%years[num],
	for cat in range(0,num_cat):
		name = 'Data_13TeV_DoubleHTag_%d'%(cat)
		entries = ws_bkg.data(name).sumEntries()
		sum_entries_bkg[name] = entries
		sum_bkg+=entries
		print '%.2f\t'%(entries),
	print '%.2f\t'%(sum_bkg)

