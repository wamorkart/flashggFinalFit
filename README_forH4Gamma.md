flashggFinalFit for H-->aa-->4gamma analysis
=======

How to run flashgg final fit package for the H-->aa-->4gamma analysis (currently working on 2016 samples and data)

#### The most recent branch is Tanvi_H4G

flashgg final fit package works with CMSSW 7_4_7, so start from a clean area and checkout the Tanvi_H4G branch :
```
cmsrel CMSSW_7_4_7
cd CMSSW_7_4_7/src/
cmsenv
git cms-init
# First get the higgs analysis combined limit package
git clone git@github.com:cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit/
git fetch origin
git checkout origin/74x-root6
# create your own branch
git checkout -b Tanvi_H4G
cd ${CMSSW_BASE}/src
git clone git@github.com:bendavid/GBRLikelihood.git HiggsAnalysis/GBRLikelihood
cd ${CMSSW_BASE}/src/HiggsAnalysis
cmsenv
scram b -j9
cd ${CMSSW_BASE}/src/

# Get the flashggfinalfit package now (Tanvi's fork of the repository)
git clone git@github.com:wamorkart/flashggFinalFit.git
cd flashggFinalFit/
# Checkout Tanvi's branch
git checkout -b Tanvi_H4G
cd ${CMSSW_BASE}/src/flashggFinalFit/
```
Two packages need to be built with their own makefiles, if needed.
Please note that there will be verbose warnings from BOOST etc, which can be ignored.
So long as the make commands finish without error, then the compilation happened fine.:
```
cd ${CMSSW_BASE}/src/flashggFinalFit/Background
make
cd ${CMSSW_BASE}/src/flashggFinalFit/Signal
make
```
Moving on...
## Flashggfinalfit details
The package contains different folder to create the background model and signal model, generate the datacards and run "combine " for performing the statistical interpretation.
Instructions for each of the steps are available in the readme section of the respective folders.
Any special instructions needed to run on the H4gamma analysis will also be specified.

## Signal Model
1. We have several mass points in the H4Gamma analysis i.e, several values of m(a). We want to scan the values of m(a) and for each value, fit the m(h) distribution.
   * The way we do this (may need to be revised in the future) is by performing a Gaussian fit to the average diphoton mass distribution, acquiring the mean and sigma of the fit, and applying a selection on diphoton mass such that we only look at the higgs mass in a 2 sigma m(a) window.
   * We do this for each m(a), thereby scanning the m(a) values. The script that does this fitting and produces workspaces for signal MC is here __https://github.com/wamorkart/flashggFinalFit/blob/Tanvi_H4G/Signal/mkSignalWS_h4g.py__
   * It reads a signal ntuple (output of the H4Gamma tagger of flashgg); the ntuples are currently stored here **/eos/cms/store/user/twamorka/NTuples_17Feb2019/Signal/**
   * Sample ntuple for m(a) = 60 GeV  is stored here **/afs/cern.ch/work/t/twamorka/public/forBadder/signal_m_60.root**  (would need to change the input file location in the script)
   * How to run? `python mkSignalWS_h4g.py --mass 60`
   * Sample output file **/afs/cern.ch/work/t/twamorka/public/forBadder/w_signal_60.root**
2. flashggfinalfit requires several mass points in order to create a signal model, and then it proceeds with interpolating between the different mass points. We get around this by creating    "fake" signal points at m(h) = 120 and 130 GeV. We do this by copying the roodataset for m(h) = 125 GeV, and shifting all points up and down by 5 GeV.
  * The script for that is here __https://github.com/wamorkart/flashggFinalFit/blob/Tanvi_H4G/Signal/shiftHiggsDatasets.py__
  * This takes an input the signal WS that was produced in step 1 and produces three WS's as output, one each for m(h) value at 120, 125, 130 GeV.
  * How to run? `python shiftHiggsDatasets.py --mass 60`
  * Sample input file **/afs/cern.ch/work/t/twamorka/public/forBadder/w_signal_60.root**
  * Sample output files **/afs/cern.ch/work/t/twamorka/public/forBadder/w_signal_60_120.root**, **/afs/cern.ch/work/t/twamorka/public/forBadder/w_signal_60_125.root** and **/afs/cern.ch/work/t/twamorka/public/forBadder/w_signal_60_130.root**

Once the workspaces are created, we can proceed with building the signal model.
`Issue: flashggfinalfit requires several mass points in order to create a signal model, and then it proceeds with interpolating between the different mass points`
How do we get around this? :confused:

* First step is to determine the number of gaussians needed to fit the higgs mass distribution, in both the right vertex (RV) and the wrong vertex (WV) case (this is determined by a `dZ < 1` cut)
