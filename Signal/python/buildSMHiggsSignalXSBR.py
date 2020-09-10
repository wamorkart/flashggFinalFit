from HiggsAnalysis.CombinedLimit.DatacardParser import *
from HiggsAnalysis.CombinedLimit.ModelTools import *
from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import *
import HiggsAnalysis.CombinedLimit.PhysicsModel as models 

class dummy_options:
  def __init__(self):
    self.physModel = "HiggsAnalysis.CombinedLimit.PhysicsModel:floatingHiggsMass"
    self.physOpt = ["higgsMassRange=90,250"]
    self.bin = True
    self.fileName = "eh.root"
    self.cexpr = False
    self.out = "wsdefault"
    self.verbose = 0
    self.mass = 125
    self.funcXSext = "13TeV" #default?
    # self.funcXSext = "8TeV" #default?

options=dummy_options()
DC = Datacard()
MB = ModelBuilder(DC, options)
physics = models.floatingHiggsMass
physics.setPhysicsOptions(options.physOpt)
MB.setPhysics(physics)
MB.physics.doParametersOfInterest()
SM = SMHiggsBuilder(MB)

# Make the x-section and BR Splines 
SM.makeBR("hgg")

# Pick the MH var and functions out of the ws
mhVar  = SM.modelBuilder.out.var("MH")
funcBR = SM.modelBuilder.out.function("SM_BR_hgg")

def Init7TeV():
  SM.makeXS("ggH","7TeV")
  SM.makeXS("qqH","7TeV")
  SM.makeXS("ttH","7TeV")
  SM.makeXS("WH","7TeV")
  SM.makeXS("ZH","7TeV")
  SM.makeXS("ggF","7TeV")
  options.funcXSext = "7TeV" 

def Init8TeV():
  SM.makeXS("ggH","8TeV")
  SM.makeXS("qqH","8TeV")
  SM.makeXS("ttH","8TeV")
  SM.makeXS("WH","8TeV")
  SM.makeXS("ZH","8TeV")
  SM.makeXS("ggF","8TeV")
  options.funcXSext = "8TeV" 

def Init13TeV():
  SM.makeXS("ggH","13TeV")
  SM.makeXS("qqH","13TeV")
  SM.makeXS("ttH","13TeV")
  SM.makeXS("tHq","13TeV")
  SM.makeXS("tHW","13TeV")
  SM.makeXS("ggZH","13TeV")
  SM.makeXS("bbH","13TeV")
  SM.makeXS("WH","13TeV") 
  SM.makeXS("ZH","13TeV") 
  SM.makeXS("ggF","13TeV")
  options.funcXSext = "13TeV" 

def getBR(mh): 
 mhVar.setVal(mh)
 return funcBR.getVal()
 
def getXS(mh,prod):
 mhVar.setVal(mh)
 #print'------------------------------------------------------------------------------'
 #print'prod: ',prod 
 funcXS = SM.modelBuilder.out.function("SM_XS_%s_%s"%(prod,options.funcXSext))
 #print'------------------------------------------------------------------------------'
 return funcXS.getVal()

