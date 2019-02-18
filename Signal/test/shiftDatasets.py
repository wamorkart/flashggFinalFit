import ROOT
from ROOT import *
from optparse import OptionParser, make_option
import sys
import os


parser = OptionParser(option_list=[
   # make_option("--inp-files",type='string',dest='inp_files',default='output_GluGluToHHTo2B2G_node_SM_13TeV-madgraph'),
   # make_option("--inp-files",type='string',dest='inp_files',default='VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8,ttHToGG_M125_13TeV_powheg_pythia8_v2,VBFHToGG_M-125_13TeV_powheg_pythia8,GluGluHToGG_M-125_13TeV_powheg_pythia8,GluGluToHHTo2B2G_node_SM_13TeV-madgraph,bbHToGG_M-125_4FS_ybyt_13TeV_amcatnlo,bbHToGG_M-125_4FS_yb2_13TeV_amcatnlo,GluGluToHHTo2B2G_node_box_13TeV-madgraph,GluGluToHHTo2B2G_node_2_13TeV-madgraph,GluGluToHHTo2B2G_node_3_13TeV-madgraph,GluGluToHHTo2B2G_node_4_13TeV-madgraph,GluGluToHHTo2B2G_node_5_13TeV-madgraph,GluGluToHHTo2B2G_node_6_13TeV-madgraph,GluGluToHHTo2B2G_node_7_13TeV-madgraph,GluGluToHHTo2B2G_node_8_13TeV-madgraph,GluGluToHHTo2B2G_node_9_13TeV-madgraph,GluGluToHHTo2B2G_node_10_13TeV-madgraph,GluGluToHHTo2B2G_node_11_13TeV-madgraph,GluGluToHHTo2B2G_node_11_13TeV-madgraph,GluGluToHHTo2B2G_node_12_13TeV-madgraph,GluGluToHHTo2B2G_node_13_13TeV-madgraph'),
   # make_option("--inp-files",type='string',dest='inp_files',default='VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8,ttHToGG_M125_13TeV_powheg_pythia8_v2,VBFHToGG_M-125_13TeV_powheg_pythia8,GluGluHToGG_M-125_13TeV_powheg_pythia8,GluGluToHHTo2B2G_node_SM_13TeV-madgraph'),  #2016
 #   make_option("--inp-files",type='string',dest='inp_files',default='ttHToGG_M125_13TeV_powheg_pythia8,GluGluHToGG_M-125_13TeV_powheg_pythia8,VBFHToGG_M125_13TeV_amcatnlo_pythia8,VHToGG_M125_13TeV_amcatnloFXFX_madspin_pythia8,GluGluToHHTo2B2G_node_SM_13TeV-madgraph'), #2017
    make_option("--inp-files",type='string',dest='inp_files',default=''),  #nodes
   # make_option("--inp-names",type='string',dest='inp_names',default='GluGluToHHTo2B2G_node_SM_13TeV_madgraph'),
   # make_option("--inp-dir",type='string',dest="inp_dir",default='/afs/cern.ch/work/n/nchernya/ETH/DiHiggs/root_file/13_12_2018/renamed2017/'),
   # make_option("--inp-dir",type='string',dest="inp_dir",default='/afs/cern.ch/work/n/nchernya/ETH/DiHiggs/root_file/13_12_2018/2016/'),
    make_option("--inp-dir",type='string',dest="inp_dir",default='/afs/cern.ch/work/n/nchernya/ETH/DiHiggs/root_file/13_12_2018/2017/'),
    make_option("--out-dir",type='string',dest="out_dir",default='/afs/cern.ch/work/n/nchernya/ETH/DiHiggs/root_file/13_12_2018/'),
    make_option("--cats",type='string',dest="cats",default='DoubleHTag_0,DoubleHTag_1,DoubleHTag_2,DoubleHTag_3,DoubleHTag_4,DoubleHTag_5,DoubleHTag_6,DoubleHTag_7,DoubleHTag_8,DoubleHTag_9,DoubleHTag_10,DoubleHTag_11'),
])

(options, args) = parser.parse_args()
cats = options.cats.split(',')
input_files = options.inp_files.split(',')

input_files=[]
for i in range(0,12):
	input_files.append('GluGluToHHTo2B2G_node_%d_13TeV-madgraph'%i)


input_names = []
for num,f in enumerate(input_files):
#	input_names.append(f.replace('-','_') +'_13TeV') #2016
	input_names.append(f.replace('-','_') +'_2017_13TeV')
	input_files[num] = 'output_' + f 

masses = [-5.,0.,5.]
higgs_mass = 125.
wsname = "tagsDumper/cms_hgg_13TeV"

for num,f in enumerate(input_files):
	print 'doing file ',f
#	tfile = TFile(options.inp_dir + f+".root")  #2016
	tfile = TFile(options.inp_dir + f+"_2017.root") 
	ws = tfile.Get(wsname)
	for mass in masses :
			value = mass + higgs_mass 
			ws.Print()
			print 'doing mass ',mass
			cat_datasets=[]
			for cat in cats :
				print 'doing cat ',cat
				name = input_names[num]+'_'+cat
				print 'name ',name
				dataset = (ws.data(name)).Clone(input_names[num]+"_%d_"%value+cat)
				dataset.Print()
				dataset.changeObservableName("CMS_hgg_mass","CMS_hgg_mass_old")
				oldmass = dataset.get()["CMS_hgg_mass_old"]
				mass_new = RooFormulaVar( "CMS_hgg_mass", "CMS_hgg_mass", "(@0+%.1f)"%mass,RooArgList(oldmass) );
			#	dataset.SetName(input_names[num]+"_%d_"%value+cat)
				dataset.addColumn(mass_new).setRange(100,180)
				dataset.Print()
				cat_datasets.append(dataset)

			out = TFile(options.out_dir + f +"_%d_2017.root"%value,"RECREATE")
#			out = TFile(options.out_dir + f +"_%d.root"%value,"RECREATE")
			out.mkdir("tagsDumper")
			out.cd("tagsDumper")
			neww = RooWorkspace("cms_hgg_13TeV","cms_hgg_13TeV") ;
			for dat in cat_datasets:
				getattr(neww, 'import')(dat, RooCmdArg())
			neww.Write()
			out.Close()
#			delete dataset
#			delete oldmass
#			delete mass_new
#			delete neww



