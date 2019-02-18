import ROOT
from ROOT import *
from optparse import OptionParser, make_option
import sys
import os
import json


parser = OptionParser(option_list=[
    make_option("--inp-files",type='string',dest='inp_files',default='GluGluToHHTo2B2G_12nodes_13TeV-madgraph_correctedcfg'),  #2017
   # make_option("--inp-files",type='string',dest='inp_files',default='GluGluToHHTo2B2G_12nodes_13TeV-madgraph'),  #2016
    make_option("--inp-dir",type='string',dest="inp_dir",default='/afs/cern.ch/work/n/nchernya/ETH/DiHiggs/root_file/13_12_2018/'),
    make_option("--out-dir",type='string',dest="out_dir",default='/afs/cern.ch/work/n/nchernya/ETH/DiHiggs/root_file/13_12_2018/'),
    make_option("--year",type='string',dest="year",default='2017'),
    make_option("--cats",type='string',dest="cats",default='DoubleHTag_0,DoubleHTag_1,DoubleHTag_2,DoubleHTag_3,DoubleHTag_4,DoubleHTag_5,DoubleHTag_6,DoubleHTag_7,DoubleHTag_8,DoubleHTag_9,DoubleHTag_10,DoubleHTag_11'),
    make_option("--config",type='string',dest="config",default='/afs/cern.ch/work/n/nchernya/ETH/DiHiggs/root_file/13_12_2018/reweighting_normalization_15_02_2018.json'),
])

(options, args) = parser.parse_args()
cats = options.cats.split(',')
input_files = options.inp_files.split(',')
input_names = []
for num,f in enumerate(input_files):
	input_names.append(f.replace('-','_') +'_13TeV') 
	input_files[num] = 'output_' + f 

options.inp_dir = options.inp_dir + options.year + '/'
options.out_dir = options.out_dir + options.year + '/'

normalization_file = open(options.config).read()
normalizations = json.loads(normalization_file)

wsname = "tagsDumper/cms_hgg_13TeV"

for num,f in enumerate(input_files):
	print 'doing file ',f
	tfile = TFile(options.inp_dir + f+".root")  
	ws = tfile.Get(wsname)
	for benchmark_num in range(0,12) :
			print 'doing benchmark ',benchmark_num
			ws.Print()
			cat_datasets=[]
			normalization_value = normalizations[options.year]["benchmark_%d_normalization"%benchmark_num]
			for cat in cats :
				print 'doing cat ',cat
				name = input_names[num]+'_'+cat
				name_new = name.replace('12nodes','node_%d'%benchmark_num)
				if '2017' in options.year : name_new = name_new.replace('13TeV_Do','2017_13TeV_Do').replace('_correctedcfg','')
				print 'name new ',name_new
				mass = RooRealVar("CMS_hgg_mass","CMS_hgg_mass",100,180) 
				dZ = RooRealVar("dZ","dZ",-20,20) 
				centralObjectWeight = RooRealVar("centralObjectWeight","centralObjectWeight",-999999.,999999.) 
				benchmark = RooRealVar("benchmark_reweight_%d"%benchmark_num,"benchmark_reweight_%d"%benchmark_num,0,100.) 
				dataset = (ws.data(name))
				dataset_new = (ws.data(name)).emptyClone(name_new,name_new).reduce(RooArgSet(mass,dZ,centralObjectWeight,benchmark))
				weight = RooRealVar("weight","weight",-100000,1000000);
				for i in range(0,dataset.numEntries()):
					mass.setVal(dataset.get(i).getRealValue("CMS_hgg_mass"))
					dZ.setVal(dataset.get(i).getRealValue("dZ"))
					centralObjectWeight.setVal(dataset.get(i).getRealValue("centralObjectWeight"))
					benchmark_value = dataset.get(i).getRealValue("benchmark_reweight_%d"%benchmark_num)
					benchmark.setVal(benchmark_value)
					weight.setVal(dataset.weight() * benchmark_value / normalization_value )
					dataset_new.add(RooArgSet(mass, dZ, centralObjectWeight, benchmark, weight), weight.getVal() )
				dataset_new.Print()
				cat_datasets.append(dataset_new)

			f_new = f.replace('12nodes','node_%d'%benchmark_num).replace('_correctedcfg','')
			if '2017' in options.year : f_new = f_new+'_2017'
			out = TFile(options.out_dir + f_new +".root","RECREATE")
			out.mkdir("tagsDumper")
			out.cd("tagsDumper")
			neww = RooWorkspace("cms_hgg_13TeV","cms_hgg_13TeV") ;
			for dat in cat_datasets:
				getattr(neww, 'import')(dat, RooCmdArg())
			neww.Write()
			out.Close()



