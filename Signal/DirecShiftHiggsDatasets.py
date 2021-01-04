####################################################################################################################################
# Abe Tishelman-Charny
#
# The purpose of this python module is to artificially shift the HHWWgg CMS_hgg_mass distribution left and right 5 GeV
# in order to be compatabile with the fggfinalfit framework, as the standard Hgg analysis
# uses an interpolation technique with Hgg mass points ~ 110->130 GeV
#
# We only have a 125 GeV Higgs mass point for HHWWgg, so we must do this artifial shift.
#
####################################################################################################################################

import ROOT
from ROOT import *

import sys
import os

inDir = sys.argv[1]
cats_ = sys.argv[2]
proc = sys.argv[3]
mass = sys.argv[4]
year = sys.argv[5]

cats = cats_.split(",") # turn to list

outDir = inDir + '_' + 'interpolation/'
if not os.path.exists(outDir):
    os.makedirs(outDir)
values = [-5,0,5]
higgs_mass = 125

ws_name = 'tagsDumper/cms_hgg_13TeV'

temp_ws = TFile("%s/signal_m_%s_%s_even_skim_WS.root"%(inDir,str(mass),str(year))).Get(ws_name)

for value in values:
	print'mass shift:',value
	shift = value + higgs_mass

        output = TFile("%s/signal_m_%s_%s_%s.root"%(outDir,str(mass),str(shift),str(year)),'RECREATE')

	output.mkdir("tagsDumper")
	output.cd("tagsDumper")
	ws_new = ROOT.RooWorkspace("cms_hgg_13TeV")

	for cat in cats:
                dataset_name = str(proc)+'Tag_'+str(cat)+'_13TeV_'+str(year)#H4GTag_Cat4_13TeV_2016
		dataset = (temp_ws.data(dataset_name)).Clone(dataset_name + '_' + str(shift)) # includes process and category
		dataset.Print()
		dataset.changeObservableName('CMS_hgg_mass','CMS_hgg_mass_old')
		higgs_old = dataset.get()['CMS_hgg_mass_old']
		higgs_new = RooFormulaVar( 'CMS_hgg_mass', 'CMS_hgg_mass', "(@0+%.1f)"%value,RooArgList(higgs_old) );
		dataset.addColumn(higgs_new).setRange(105,145)
		dataset.Print()

		getattr(ws_new,'import')(dataset,RooCmdArg())

	ws_new.Write()

	output.Close()
	print'finished mass shift: ',value
