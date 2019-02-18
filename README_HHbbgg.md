flashggFinalFit for HHbbgg
=======
Instuctions how to run FinalFit specifically for HHbbgg code.

Main readme for flashgg can be found here : flashggFinalFit/README.md.

#### The most recent branch : nchernya

For 7_4_7 CMSSW, starting from a clean area and checking out Nadya's branch :
```
cmsrel CMSSW_7_4_7
cd CMSSW_7_4_7/src
cmsenv
git cms-init
# Install Combine as per Twiki: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit#ROOT6_SLC6_release_CMSSW_7_4_X
# They recently migrated to 81X; we will follow shortly, but checkout 74X branch for now
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd ${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout origin/74x-root6
git checkout -b mybranch
cd ${CMSSW_BASE}/src
# Install the GBRLikelihood package which contains the RooDoubleCBFast implementation
git clone git@github.com:bendavid/GBRLikelihood.git HiggsAnalysis/GBRLikelihood
# Compile external libraries
cd ${CMSSW_BASE}/src/HiggsAnalysis
cmsenv
scram b -j9
# Install Flashgg Final Fit packages
cd ${CMSSW_BASE}/src/
#Git checkout Nadya's branch 
git clone https://github.com/chernyavskaya/flashggFinalFit flashggFinalFit
git remote add nchernyavskaya https://github.com/chernyavskaya/flashggFinalFit.git
git fetch nchernyavskaya
git checkout -b branch_name --track nchernyavskaya/nchernya
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
## Contents
The FLASHgg Finals Fits package contains several subfolders which are used for the following steps:

* Create the Signal Model (see `Signal` dir)
* Create the Background Model (see `Background` dir)
* Generate a Datacard (see `Datacard` dir)
* Run `combine` and generate statistical interpretation plots. (see `Plots/FinalResults` dir)

Each of the relevant folders are documented with specific `README.md` files (inherited from the main code).

#### Signal Model
__All scipts for Signal and resonant bkg models are in flashggFinalFit/Signal folder__.

* By construction FinalFit requires several mass points to build a signal model, as it does extrapolation between the mass points.
We do not need this, but since the code relies on it and it is very hardcoded and difficult to change, we create these mass points 
simply by copying the workspaces and renaming them. 
* 2016 and 2017 (2018 in future) are treated as independent signals and resonant bkgs,
but in the datacard in the end we will only have one signal - HHbbgg
* Since different years of data taking are treated differently, we need to rename the workspaces to have a year in the name

Two short scipts are needed to do this renaming and shifting of the mass : renameDatasets.py and  shiftDatasets.py.
Options have to be specified when running these scripts, otherwise defults directories and signal names will be used.
```
cd flashggFinalFit/Signal/test/
python renameDatasets.py
python shiftDatasets.py
```
Once workspaces are prepared, we can start building a signal model.

First we run *signalFtest* to determine the number of gausians needed to describe signal 
(for more info see general README in Signal directory). Beware that this script is not perfect and one has to look at the plots produced 
and maybe adjust the *config.dat* file that was written in flashggFinalFit/Signal/dat with more accurate number of gaussians.

After the config file is prepared, we can the script to create a Signal and Resonant Single Higgs bkg models 
(for now it is counted as signal, but in final datacards we specify it is background).

To make plots of the signal/resonant bkg model script is available : *./bin/makeParametricSignalModelPlots*

To make life easier I have prepared *run.sh* script in Signal folder with the exact commands written.
Folders, names of the files, processes you want to run on have to be modified.
```
cd FlashggFinalFit/Signal/
source run.sh
```

### Background Model 
__All scipts for non-resonant background model are in flashggFinalFit/Background folder__.

Background model is taken from data 
(2016+2017 - do not forget to hadd workspaces from flashgg for data : hadd_workspaces all_data.root 2016.root 2017.root)

Envelope method is run by
```
cd flashggFinalFit/Background
./bin/fTest -i options...
```
Plots with signal model can be created using the script *scripts/subBkgPlots.py*

To make life easier I have prepared run.sh script in Bakcground folder with the exact commands written.
Folders, names of the files, processes you want to run on have to be modified.
```
cd flashggFinalFit/Background
source run.sh
```

### Datacards
__Datacards commands are in folder flashggFinalFit/Datacard.__

Datacard is created by running the scipt : *makeParametricModelDatacardFLASHgg.py*.
**Beware** for lumi there are two options , one for 2016, another one for 2017 : *--intLumi*,*--intLumi2017*

Again, example of commands that I run can be found in *Datacard/run.sh*

### Limits
__The scripts for final results are given in flashggFinalFit/Plots/FinalResults.__

You have to copy your bkg,signal model workspaces and datacard to this folder (instruction from FinalFit readme), 
otherwise give full pathes to root workspaces in the datacard.

Scipts *run.sh* is availble with example command.

### Yields table
For the moment, I am using a very simple script to get yields. The luminosities, SM singal xsec x BR, as well as pathes to files are hardcoded. Can be easily modified  in options.
```
python Signal/test/yields.py
```

