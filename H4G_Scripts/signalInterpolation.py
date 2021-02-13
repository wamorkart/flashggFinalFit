import ROOT
from ROOT import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# matplotlib.use('Agg')
import math
import numpy as np
from numpy import array
from prettytable import PrettyTable
from root_numpy import root2array, tree2array
from scipy import stats

mass = [60,55,50,45,40,30,25,20,15]
year = [2016,2017,2018]

outDir = "/eos/user/t/twamorka/www/H4G_for_PreApp/PreApp_Checks/SignalInterpolation/"

def mkPlot(var_x,var_y,ylabel,year,outname):
    plt.figure()
    plt.grid()
    plt.plot(var_x,np.array(var_y,dtype=float),marker='o')
    plt.xlim(13,62)
    plt.ylabel(ylabel)
    plt.xlabel("m(a) [GeV]")
    plt.title(str(year))
    plt.savefig(outname+'.png')
    plt.savefig(outname+'.pdf')

for y in year:
    mean_dcb = []
    width_dcb = []
    alpha1_dcb = []
    alpha2_dcb = []
    n1_dcb = []
    n2_dcb = []
    sig_gaus = []
    norm = []
    for m in mass:
        inDir = "../Signal/outdir_H4G_23Jan2021_M"+str(m)+"_"+str(y)
        inFile = ROOT.TFile(inDir+"/CMS-HGG_mva_13TeV_sigfit.root","read")

        wsig_13TeV = inFile.Get("wsig_13TeV")
        wsig_13TeV.var("MH").setVal(125)

        mean_dcb.append(  wsig_13TeV.function("mean_dcb_H4G_Cat0_rv_13TeV").getVal() )
        width_dcb.append( wsig_13TeV.function("sig_dcb_H4G_Cat0_rv_13TeV").getVal())
        alpha1_dcb.append( wsig_13TeV.function("a1_dcb_H4G_Cat0_rv_13TeV").getVal())
        alpha2_dcb.append( wsig_13TeV.function("a2_dcb_H4G_Cat0_rv_13TeV").getVal())
        n1_dcb.append( wsig_13TeV.function("n1_dcb_H4G_Cat0_rv_13TeV").getVal())
        n2_dcb.append( wsig_13TeV.function("n2_dcb_H4G_Cat0_rv_13TeV").getVal())
        sig_gaus.append(wsig_13TeV.function("sig_gaus_H4G_Cat0_rv_13TeV").getVal())
        norm.append(wsig_13TeV.function("hggpdfsmrel_"+str(y)+"_13TeV_H4G_Cat0_norm").getVal())

    mkPlot(mass,mean_dcb,"Mean_DCB",y,outDir+"/Mean_DCB_"+str(y))
    mkPlot(mass,width_dcb,"Width_DCB",y,outDir+"/Width_DCB_"+str(y))
    mkPlot(mass,alpha1_dcb,"Alpha1_DCB",y,outDir+"/Alpha1_DCB_"+str(y))
    mkPlot(mass,alpha2_dcb,"Alpha2_DCB",y,outDir+"/Alpha2_DCB_"+str(y))
    mkPlot(mass,n1_dcb,"n1_DCB",y,outDir+"/n1_DCB_"+str(y))
    mkPlot(mass,n2_dcb,"n2_DCB",y,outDir+"/n2_DCB_"+str(y))
    mkPlot(mass,sig_gaus,"Sigma_Gaus",y,outDir+"/Sigma_Gaus_"+str(y))
    mkPlot(mass,norm,"Norm",y,outDir+"/Norm_"+str(y))

    # plt.figure()
    # plt.grid()
    # plt.plot(mass,np.array(mean_dcb,dtype=float),marker='o')
    # plt.savefig('test.pdf')
