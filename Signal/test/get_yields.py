import ROOT
from ROOT import *
from optparse import OptionParser, make_option
import sys
import os
from math import sqrt

filename = '/afs/cern.ch/work/n/nchernya/ETH/CMSSW_7_4_7/src/flashggFinalFit/Signal/CMS-HGG_sigfit_28_09_2018.root'
filename_bkg = '/afs/cern.ch/work/n/nchernya/ETH/CMSSW_7_4_7/src/flashggFinalFit/Background/CMS-HGG_multipdf_HHbbgg_data_28_09_2018.root'
wsname = 'wsig_13TeV'
wsname_bkg = 'multipdf'

num_cat = 12
sum_entries = dict()
sum_entries_bkg = dict()


tfile = TFile(filename)
ws = tfile.Get(wsname)
sum=0.
for cat in range(0,num_cat):
	name = 'hggpdfsmrel_13TeV_GluGluToHHTo2B2G_node_SM_13TeV_madgraph_DoubleHTag_%d_normThisLumi'%(cat)
	var = (ws.var('MH'))
	var.setVal(125)
	entries = (ws.function(name).getVal())
	sum_entries[name] = entries
	sum+=entries


for cat in range(0,num_cat):
	name = 'hggpdfsmrel_13TeV_GluGluToHHTo2B2G_node_SM_13TeV_madgraph_DoubleHTag_%d_normThisLumi'%(cat) 
	print name , '%.3f'%sum_entries[name]
print 'sum = ','%.3f'%sum


tfile = TFile(filename_bkg)
ws_bkg = tfile.Get(wsname_bkg)
sum_bkg=0.
for cat in range(0,num_cat):
	name = 'roohist_data_mass_DoubleHTag_%d'%(cat)
	entries = ws_bkg.data(name).sumEntries()
	sum_entries_bkg[name] = entries
	sum_bkg+=entries

for cat in range(0,num_cat):
	name = 'roohist_data_mass_DoubleHTag_%d'%(cat)
	print name , '%.3f'%sum_entries_bkg[name]
print 'sum_bkg = ','%.3f'%sum_bkg

sum2 = 0.
for cat in range(0,num_cat):
	name_bkg = 'roohist_data_mass_DoubleHTag_%d'%(cat)
	name = 'hggpdfsmrel_13TeV_GluGluToHHTo2B2G_node_SM_13TeV_madgraph_DoubleHTag_%d_normThisLumi'%(cat) 
	sig = sum_entries[name]/sqrt(sum_entries[name]+sum_entries_bkg[name_bkg])
	sum2 +=sig**2
	print 'DoubleHTag %d'%cat , '%.4f'%sig
print 'sqrt(sum Sig^2) = ','%.3f'%(sqrt(sum2))
