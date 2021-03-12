#!/usr/bin/env python

import ROOT as r
import argparse

parser =  argparse.ArgumentParser(description='hist')
parser.add_argument('-i','--i',dest='i',required=True,type=str)
parser.add_argument('-e', '--e', dest='e', required=True, type=str)
parser.add_argument('-m', '--m', dest='m', required=True, type=str)

opt = parser.parse_args()

fName = opt.i+"/Parametrized_DataMix_M"+str(opt.m)+"_"+str(opt.e)+"_TurnOn_12Mar2021/CMS-HGG_multipdf_H4G_Parametrized_DataMix_"+str(opt.e)+"_TurnOn_M"+str(opt.m)+".root"
wsName = 'multipdf' 
dataName = 'roohist_data_mass_H4GTag_Cat0'
varName = 'CMS_hgg_mass'
ext = '_TH1'

inFile = r.TFile(fName)
ws   = inFile.Get(wsName)
data = ws.obj(dataName)
mass = ws.var(varName)
hist = data.createHistogram(dataName+ext, mass)
hist.Sumw2()

outFile = r.TFile(fName.replace('.root','%s.root'%ext), 'RECREATE')
outFile.cd()
hist.Write()
