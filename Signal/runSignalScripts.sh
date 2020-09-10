#!/bin/bash

#bash variables
FILE="";
EXT="auto"; #extensiom for all folders and files created by this script
PROCS="H4G"
CATS="UntaggedTag_0,UntaggedTag_1,UntaggedTag_2,UntaggedTag_3,UntaggedTag_4,VBFTag_0,VBFTag_1,VBFTag_2"
SCALES="HighR9EE,LowR9EE,HighR9EB,LowR9EB"
#SCALESCORR="MaterialCentral,MaterialForward,FNUFEE,FNUFEB,ShowerShapeHighR9EE,ShowerShapeHighR9EB,ShowerShapeLowR9EE,ShowerShapeLowR9EB"
SCALESCORR="MaterialCentral,MaterialForward"
#SCALESGLOBAL="NonLinearity:0:2.6"
SCALESGLOBAL="NonLinearity,Geant4,LightYield,Absolute"
SMEARS="HighR9EE,LowR9EE,HighR9EB,LowR9EB" #DRY RUN
MASSLIST="120,125,130"
ANALYSIS="hig-16-040"
ANALYSIS_TYPE=""
FINALSTATE="" # for HHWWgg
YEAR="2016"
FTESTONLY=0
CALCPHOSYSTONLY=0
SIMULATENOUSMASSPOINTFITTING=0
USEDCBP1G=1
SIGFITONLY=0
DONTPACKAGE=0
PACKAGEONLY=0
SIGPLOTSONLY=0
INTLUMI=131.78
BATCH=""
QUEUE=""
VERBOSITY=""
BS=""
SYSTEMATICS="1"

usage(){
	echo "The script runs three signal scripts in this order:"
		echo "signalFTest --> determines number of gaussians to use for fits of each Tag/Process"
		echo "calcPhotonSystConsts --> scale and smear ets of photons systematic variations"
		echo "SignalFit --> actually determine the number of gaussians to fit"
		echo "options:"
		echo "-h|--help) "
		echo "-i|--inputFile) "
		echo "-p|--procs) "
		echo "-f|--flashggCats) (default UntaggedTag_0,UntaggedTag_1,UntaggedTag_2,UntaggedTag_3,UntaggedTag_4,VBFTag_0,VBFTag_1,VBFTag_2,TTHHadronicTag,TTHLeptonicTag,VHHadronicTag,VHTightTag,VHLooseTag,VHEtTag)"
		echo "--analysis) Specifies the replacement dataset to use"
                echo "--useDCB_1G) Use the functional form ofi a Double Crystal Ball + one Gaussian (same mean) (default $USEDCBP1G)"
                echo "--useSSF) SSF = Simultaneous Signal Fitting. Do a fit where the mass points are all fitted at once where the parameters have MH dependence (default $SIMULATENOUSMASSPOINTFITTING)"
		echo "--analysis_type) Analysis type used for HHWWgg. Ex) Res, EFT, NMSSM"
    echo "--FinalState) Final state used for HHWWgg. Ex) qqlnu, lnulnu, qqqq"
    echo "--ext)  (default auto)"
		echo "--fTestOnly) "
		echo "--calcPhoSystOnly) "
		echo "--sigFitOnly) "
		echo "--dontPackage) "
		echo "--packageOnly) "
		echo "--sigPlotsOnly) "
		echo "--intLumi) specified in fb^-{1} (default $INTLUMI)) "
		echo "--year) Dataset year (default $YEAR)) "
		echo "--batch) which batch system to use (None (''),LSF,IC) (default '$BATCH')) "
		echo "--queue) queue to submit jobs to (specific to batch)) "
    echo "--systematics) 0: run with empty dat file for systematics. 1: run with properly written and filled dat file for photon systematics"
}


#------------------------------ parsing


# options may be followed by one colon to indicate they have a required argument
if ! options=$(getopt -u -o hi:p:f: -l help,inputFile:,procs:,bs:,smears:,massList:,scales:,scalesCorr:,useSSF:,useDCB_1G:,scalesGlobal:,flashggCats:,analysis:,analysis_type:,FinalState:,ext:,fTestOnly,calcPhoSystOnly,sigFitOnly,dontPackage,packageOnly,sigPlotsOnly,intLumi:,year:,batch:,queue:,verbosity:,systematics:, -- "$@")
then
# something went wrong, getopt will put out an error message for us
exit 1
fi
set -- $options

while [ $# -gt 0 ]
do
case $1 in
-h|--help) usage; exit 0;;
-i|--inputFile) FILE=$2; shift ;;
-p|--procs) PROCS=$2; shift ;;
--massList) MASSLIST=$2; shift ;;
--smears) SMEARS=$2; shift ;;
--scales) SCALES=$2; shift ;;
--scalesCorr) SCALESCORR=$2; shift ;;
--scalesGlobal) SCALESGLOBAL=$2; shift ;;
--bs) BS=$2; shift ;;
-f|--flashggCats) CATS=$2; shift ;;
--analysis) ANALYSIS=$2; shift ;;
--analysis_type) ANALYSIS_TYPE=$2; shift ;;
--FinalState) FINALSTATE=$2; shift ;;
--ext) EXT=$2 ; shift ;;
--useSSF) SIMULATENOUSMASSPOINTFITTING=$2 ; shift;;
--useDCB_1G) USEDCBP1G=$2 ; shift;;
--fTestOnly) FTESTONLY=1 ;;
--calcPhoSystOnly) CALCPHOSYSTONLY=1;;
--sigFitOnly) SIGFITONLY=1;;
--dontPackage) DONTPACKAGE=1;;
--packageOnly) PACKAGEONLY=1;;
--sigPlotsOnly) SIGPLOTSONLY=1;;
--intLumi) INTLUMI=$2; shift ;;
--year) YEAR=$2; shift ;;
--batch) BATCH=$2; shift;;
--queue) QUEUE=$2; shift;;
--verbosity) VERBOSITY=$2; shift;;
--systematics) SYSTEMATICS=$2; shift;;

(--) shift; break;;
(-*) usage; echo "$0: [ERROR] - unrecognized option $1" 1>&2; usage >> /dev/stderr; exit 1;;
(*) break;;
esac
shift
done

#temp for batch submission - std::bad_alloc errors...
#cd /vols/build/cms/es811/FreshStart/Pass6/CMSSW_7_4_7/src/flashggFinalFit/Signal
#eval `scramv1 runtime -sh`

echo "[INFO] processing signal model for INTLUMI $INTLUMI"

OUTDIR="outdir_$EXT"
echo "[INFO] outdir is $OUTDIR"
if [[ $FILE == "" ]];then
echo "[ERROR], input file (--inputFile or -i) is mandatory!"
exit 0
fi

if [ $FTESTONLY == 0 -a $CALCPHOSYSTONLY == 0 -a $SIGFITONLY == 0 -a $SIGPLOTSONLY == 0 -a $PACKAGEONLY == 0 ]; then
#IF not particular script specified, run all!
FTESTONLY=1
CALCPHOSYSTONLY=1
SIGFITONLY=1
SIGPLOTSONLY=1
PACKAGEONLY=1
fi
echo "FTESTONLY       = $FTESTONLY"
echo "CALCPHOSYSTONLY = $CALCPHOSYSTONLY"
echo "SIGFITONLY      = $SIGFITONLY"
echo "SIGPLOTSONLY    =  $SIGPLOTSONLY"
echo "PACKAGEONLY     =  $PACKAGEONLY"

echo "BATCH           =  $BATCH"
echo "VERBOSITY       =  $VERBOSITY"

if [[ $BATCH == "IC" ]]; then
QUEUE=hep.q
echo "[INFO] Batch = $BATCH, using QUEUE = $QUEUE"
fi
if [[ $BATCH == "HTCONDOR" ]]; then
  if [[ $QUEUE == "" ]]; then
    QUEUE=espresso
    echo "[INFO] Batch = $BATCH, QUEUE not specified. Using QUEUE = $QUEUE"
  fi
  else
    echo "[INFO] Batch = $BATCH, Using QUEUE = $QUEUE"
fi

BSOPT=""
if [[ $BS == "" ]]; then
echo "[INFO] NO BeamSpot SIZE SPECIFIED - DEFAULT FROM MC WILL BE USED"
else
echo "[INFO] BeamSpot Size is to be reweighted to $BS"
BSOPT=" --bs $BS"
fi


if [ $USEDCBP1G == 0 ]; then

####################################################
################## SIGNAL F-TEST ###################
####################################################
#ls dat/newConfig_${EXT}.dat
if [ -e dat/newConfig_${EXT}.dat ]; then
  echo "[INFO] sigFTest dat file $OUTDIR/dat/copy_newConfig_${EXT}.dat already exists, so SKIPPING SIGNAL FTEST"
else
  if [ $FTESTONLY == 1 ]; then
    mkdir -p $OUTDIR/fTest
    echo "=============================="
    echo "Running Signal F-Test"
    echo "-->Determine Number of gaussians"
    echo "=============================="

    # If it's HHWWgg need to run signalFTest for each file

    if [ -z $BATCH ]; then
      echo "./bin/signalFTest -i $FILE -d dat/newConfig_$EXT.dat -p $PROCS -f $CATS -o $OUTDIR --analysis $ANALYSIS --verbose $VERBOSITY --analysis_type $ANALYSIS_TYPE --FinalState $FINALSTATE"
      ./bin/signalFTest -i $FILE -d dat/newConfig_$EXT.dat -p $PROCS -f $CATS -o $OUTDIR --analysis $ANALYSIS --verbose $VERBOSITY --analysis_type $ANALYSIS_TYPE --FinalState $FINALSTATE
    else
      echo "./python/submitSignalFTest.py --procs $PROCS --flashggCats $CATS --outDir $OUTDIR --i $FILE --batch $BATCH -q $QUEUE --analysis $ANALYSIS --verbose $VERBOSITY"
      ./python/submitSignalFTest.py --procs $PROCS --flashggCats $CATS --outDir $OUTDIR --i $FILE --batch $BATCH -q $QUEUE --analysis $ANALYSIS --verbose $VERBOSITY
      PEND=`ls -l $OUTDIR/fTestJobs/sub*| grep -v "\.run" | grep -v "\.done" | grep -v "\.fail" | grep -v "\.err" |grep -v "\.log" | grep -v "\.out" | grep -v "\.sub" | wc -l`
      echo "PEND $PEND"
      while (( $PEND > 0 )) ; do
        PEND=`ls -l $OUTDIR/fTestJobs/sub* | grep -v "\.run" | grep -v "\.done" | grep -v "\.fail" | grep -v "\.err" | grep -v "\.log" | grep -v "\.out" | grep -v "\.sub" | wc -l`
        RUN=`ls -l $OUTDIR/fTestJobs/sub* | grep "\.run" | wc -l`
        FAIL=`ls -l $OUTDIR/fTestJobs/sub* | grep "\.fail" | wc -l`
        DONE=`ls -l $OUTDIR/fTestJobs/sub* | grep "\.done" | wc -l`
        (( PEND=$PEND-$RUN-$FAIL-$DONE ))
        echo " PEND $PEND - RUN $RUN - DONE $DONE - FAIL $FAIL"
        if (( $RUN > 0 )) ; then PEND=1 ; fi
        if (( $FAIL > 0 )) ; then
          echo "[ERROR] at least one job failed :"
          ls -l $OUTDIR/fTestJobs/sub* | grep "\.fail"
          exit 1
        fi
        sleep 10
      done
    fi
    mkdir -p $OUTDIR/dat
    cat $OUTDIR/fTestJobs/outputs/* > dat/newConfig_${EXT}_temp.dat
    sort -u dat/newConfig_${EXT}_temp.dat  > dat/tmp_newConfig_${EXT}_temp.dat
    mv dat/tmp_newConfig_${EXT}_temp.dat dat/newConfig_${EXT}_temp.dat
    cp dat/newConfig_${EXT}_temp.dat $OUTDIR/dat/copy_newConfig_${EXT}_temp.dat
    rm -rf $OUTDIR/sigfTest
    mv $OUTDIR/fTest $OUTDIR/sigfTest
  fi
  echo "[INFO] SUCCESS sigFTest jobs completed, check output and do:"
  echo "cp $PWD/dat/newConfig_${EXT}_temp.dat $PWD/dat/newConfig_${EXT}.dat"
  echo "and manually amend chosen number of gaussians using the output pdfs here:"
	echo "Signal/outdir_${EXT}/sigfTest/"
  echo "then re-run the same command to continue !"
  CALCPHOSYSTONLY=0
  SIGFITONLY=0
  SIGPLOTSONLY=0
	exit 1
fi
fi
####################################################
################## CALCPHOSYSTCONSTS ###################
####################################################

if [ $CALCPHOSYSTONLY == 1 ]; then

  echo "=============================="
  echo "Running calcPho"
  echo "-->Determine effect of photon systematics"
  echo "=============================="

  echo "./bin/calcPhotonSystConsts -i $FILE -o dat/photonCatSyst_$EXT.dat -p $PROCS -s $SCALES -S $SCALESCORR -g $SCALESGLOBAL -r $SMEARS -D $OUTDIR -f $CATS --analysis $ANALYSIS --analysis_type $ANALYSIS_TYPE --FinalState $FINALSTATE"
  ./bin/calcPhotonSystConsts -i $FILE -o dat/photonCatSyst_$EXT.dat -p $PROCS -s $SCALES -S $SCALESCORR -g $SCALESGLOBAL -r $SMEARS -D $OUTDIR -f $CATS --analysis $ANALYSIS --analysis_type $ANALYSIS_TYPE --FinalState $FINALSTATE
  mkdir -p $OUTDIR/dat
  cp dat/photonCatSyst_$EXT.dat $OUTDIR/dat/copy_photonCatSyst_$EXT.dat
fi
####################################################
####################### SIGFIT #####################
####################################################
if [ $SIGFITONLY == 1 ]; then

  echo "=============================="
  echo "Running SignalFit"
  echo "-->Create actual signal model"
  echo "=============================="

	# if H4G analysis, need to artificially create 120, 130 GeV mass points by shifting 125 dataset
	if [[ $ANALYSIS == "H4G" ]]; then

		 fileDir="${FILE%/*}" # get directory
		 fileEnd="${FILE##*/}"
		 fileID=${fileEnd::-5} # remove .root

		 ID="Run2"
		 mass="60"
		 python DirecShiftHiggsDatasets.py $fileDir $ID $mass $CATS
		 sigFiles=""
     for m in 120 125 130
     do
			 sigFiles+="${fileDir}_interpolation/H4G_signal_m${mass}_${ID}_${m}.root,"
		 done
     sigFiles=${sigFiles: : -1} # remove extra ","
     FILE=$sigFiles
   fi



  # if HHWWgg analysis, need to artificially create 120, 130 GeV mass points by shifting 125 dataset
  if [[ $ANALYSIS == "HHWWgg" ]]; then

    fileDir="${FILE%/*}" # get directory
    fileEnd="${FILE##*/}"
    fileID=${fileEnd::-5} # remove .root

    ## Get HHWWgg label from file name
    if [[ $ANALYSIS_TYPE == "Res" ]]; then
      # For res analysis, ID = SM, X250, ...
      ID="$(cut -d'_' -f1 <<<$fileID)" # get text before first '_'. ex: SM, X250, X260, ...
      # echo "fileDir: $fileDir"
      # echo "mass: $mass"
      HHWWggLabel="${ID}_WWgg_${FINALSTATE}gg"
      proc="ggF"
    elif [[ $ANALYSIS_TYPE == "EFT" ]];
    then
      ## --EFT:
      # File name format: nodeX_HHWWgg_<FinalState>
      # RooAbsData name format: GluGluToHHTo_WWgg_<FinalState>_nodeX_13TeV_HHWWggTag_Y
      # proc = GluGluToHHTo, 13TeV_HHWWggTag_Y already included
      # HHWWgg_Label = WWgg_<FinalState>_nodeX

      # For EFT analysis, ID = node2, node9, ...
      ID="$(cut -d'_' -f1 <<<$fileID)"
      HHWWggLabel="WWgg_${FINALSTATE}_${ID}"
      proc="GluGluToHHTo"

    elif [[ $ANALYSIS_TYPE == "NMSSM" ]];
    then
      # // file name format: MX<massX>_MY<massY>_HHWWgg_<FinalState>.root
      # // RooAbsData name format: NMSSM_XYHWWgg<FinalState>_MX<massX>_MY<massY>_13TeV_HHWWggTag_Y
      # vector<string> tmpV;
      # split(tmpV,filename_[0],boost::is_any_of("/"));
      # unsigned int N = tmpV.size();
      # string endPath = tmpV[N-1];
      # vector<string> tmpV2;
      # split(tmpV2,endPath,boost::is_any_of("_"));
      # string XmassString = tmpV2[0];
      # string YmassString = tmpV2[1];
      # HHWWgg_Label = Form("XYHWWgg<FinalState>_%s_%s",XmassString.c_str(),YmassString.c_str());
      # cout << "Going to look for: " << HHWWgg_Label.c_str() << endl;
      echo "Doing NMSSM analysis"
      mX="$(cut -d'_' -f1 <<<$fileID)"
      mY="$(cut -d'_' -f2 <<<$fileID)"
      ID="${mX}_${mY}"
      HHWWggLabel="NMSSM_XYHWWgg${FINALSTATE}_${ID}"
      proc="ggF"
      # echo "
      # ID="$(cut -d'_' -f1 <<<$fileID)"
    fi

    # python DirecShiftHiggsDatasets.py $fileDir $mass $HHWWggLabel # create 120 and 130 points
    echo "COMMAND: python DirecShiftHiggsDatasets.py $fileDir $ID $HHWWggLabel $CATS $ANALYSIS_TYPE $proc $FINALSTATE"
    python DirecShiftHiggsDatasets.py $fileDir $ID $HHWWggLabel $CATS $ANALYSIS_TYPE $proc $FINALSTATE # create 120 and 130 points
    sigFiles=""
    for m in 120 125 130
    do
      sigFiles+="${fileDir}_interpolation/X_signal_${ID}_${m}_HHWWgg_${FINALSTATE}.root,"

      # if [[ $ANALYSIS_TYPE == "Res" ]]; then
      #   sigFiles+="${fileDir}_interpolation/X_signal_${ID}_${m}_HHWWgg_<FinalState>.root,"
      # elif [[ $ANALYSIS_TYPE == "EFT" ]];
      # then
      #   sigFiles+="${fileDir}_interpolation/X_signal_${ID}_${m}_HHWWgg_<FinalState>.root,"
      # elif [[ $ANALYSIS_TYPE == "NMSSM" ]];
      # then
      #   sigFiles+="${fileDir}_interpolation/X_signal_${ID}_${m}_HHWWgg_<FinalState>.root,"
      # fi

    done
    sigFiles=${sigFiles: : -1} # remove extra ","
    FILE=$sigFiles
  fi

  if [[ $BATCH == "" ]]; then
    echo "ANALYSIS: $ANALYSIS"
    echo "SYSTEMATICS: $SYSTEMATICS"
    sysdatOption="-s dat/photonCatSyst_$EXT.dat"
    if [ $SYSTEMATICS == 0 ]; then
      sysdatOption="-s dat/empty.dat"
    fi
    echo "./bin/SignalFit -i $FILE -d dat/newConfig_$EXT.dat  --mhLow=120 --mhHigh=130 ${sysdatOption} --procs $PROCS -o $OUTDIR/CMS-HGG_mva_13TeV_sigfit.root -p $OUTDIR/sigfit -f $CATS --changeIntLumi $INTLUMI  --useDCBplusGaus $USEDCBP1G --useSSF $SIMULATENOUSMASSPOINTFITTING --massList $MASSLIST --analysis $ANALYSIS --year $YEAR --analysis_type $ANALYSIS_TYPE --FinalState $FINALSTATE "
    ./bin/SignalFit -i $FILE -d dat/newConfig_$EXT.dat  --mhLow=120 --mhHigh=130 ${sysdatOption} --procs $PROCS -o $OUTDIR/CMS-HGG_mva_13TeV_sigfit.root -p $OUTDIR/sigfit -f $CATS --changeIntLumi $INTLUMI  --useDCBplusGaus $USEDCBP1G --useSSF $SIMULATENOUSMASSPOINTFITTING --massList $MASSLIST --analysis $ANALYSIS --year 2016 --analysis_type $ANALYSIS_TYPE --FinalState $FINALSTATE
  else
    echo "./python/submitSignalFit.py -i $FILE -d dat/newConfig_$EXT.dat  --mhLow=120 --mhHigh=130 -s dat/photonCatSyst_$EXT.dat --procs $PROCS -o $OUTDIR/CMS-HGG_sigfit_$EXT.root -p $OUTDIR/sigfit -f $CATS --changeIntLumi $INTLUMI --batch $BATCH --massList $MASSLIST -q $QUEUE $BSOPT --useSSF $SIMULATENOUSMASSPOINTFITTING --useDCB_1G $USEDCBP1G --analysis $ANALYSIS --year $YEAR"
    ./python/submitSignalFit.py -i $FILE -d dat/newConfig_$EXT.dat  --mhLow=120 --mhHigh=130 -s dat/photonCatSyst_$EXT.dat --procs $PROCS -o $OUTDIR/CMS-HGG_sigfit_$EXT.root -p $OUTDIR/sigfit -f $CATS --changeIntLumi $INTLUMI --batch $BATCH --massList $MASSLIST -q $QUEUE $BSOPT --useSSF $SIMULATENOUSMASSPOINTFITTING --useDCB_1G $USEDCBP1G --analysis $ANALYSIS --year $YEAR

    PEND=`ls -l $OUTDIR/sigfit/SignalFitJobs/sub*| grep -v "\.run" | grep -v "\.done" | grep -v "\.fail" | grep -v "\.err" |grep -v "\.log" | grep -v "\.out" | grep -v "\.sub" | wc -l`
    echo "PEND $PEND"

    # Don't want this for HHWWgg because need to submit job for each mass point
    if [[ $ANALYSIS != "HHWWgg" ]]; then
      while (( $PEND > 0 )) ; do
        PEND=`ls -l $OUTDIR/sigfit/SignalFitJobs/sub* | grep -v "\.run" | grep -v "\.done" | grep -v "\.fail" | grep -v "\.err" | grep -v "\.log" | grep -v "\.out" | grep -v "\.sub" | wc -l`
        RUN=`ls -l $OUTDIR/sigfit/SignalFitJobs/sub* | grep "\.run" | wc -l`
        FAIL=`ls -l $OUTDIR/sigfit/SignalFitJobs/sub* | grep "\.fail" | wc -l`
        DONE=`ls -l $OUTDIR/sigfit/SignalFitJobs/sub* | grep "\.done" | wc -l`
        (( PEND=$PEND-$RUN-$FAIL-$DONE ))
        echo " PEND $PEND - RUN $RUN - DONE $DONE - FAIL $FAIL"
        if (( $RUN > 0 )) ; then PEND=1 ; fi
        if (( $FAIL > 0 )) ; then
          echo "[ERROR] at least one job failed :"
          ls -l $OUTDIR/sigfit/SignalFitJobs/sub* | grep "\.fail"
          exit 1
        fi
        sleep 10
      done
    fi

    #ls $PWD/$OUTDIR/CMS-HGG_sigfit_${EXT}_*.root > out.txt
    # CMS-HGG_mva_13TeV_sigfit.root
    # ls $OUTDIR/CMS-HGG_sigfit_${EXT}_*.root > out.txt
    # echo "ls ../Signal/$OUTDIR/CMS-HGG_sigfit_${EXT}_*.root > out.txt"
    counter=0
    while read p ; do
      if (($counter==0)); then
        SIGFILES="$p"
      else
        SIGFILES="$SIGFILES,$p"
      fi
      ((counter=$counter+1))
    done < out.txt
    echo "SIGFILES $SIGFILES"

    #./makeSlides.sh $OUTDIR
    #scp fullslides.pdf lcorpe@lxplus.cern.ch:www/scratch/fullslides.pdf
    #exit 1
    if [ $DONTPACKAGE == 0 ]; then
      echo "./bin/PackageOutput -i $SIGFILES --procs $PROCS -l $INTLUMI -p $OUTDIR/sigfit -W wsig_13TeV -f $CATS -L 120 -H 130 -o $OUTDIR/CMS-HGG_sigfit_$EXT.root --year $YEAR --FinalState $FINALSTATE"
      ./bin/PackageOutput -i $SIGFILES --procs $PROCS -l $INTLUMI -p $OUTDIR/sigfit -W wsig_13TeV -f $CATS -L 120 -H 130 -o $OUTDIR/CMS-HGG_sigfit_$EXT.root --year $YEAR --FinalState $FINALSTATE > package.out
    fi
  fi

fi

if [ $PACKAGEONLY == 1 ]; then

  echo "ANALYSIS: $ANALYSIS"
  if [[ $ANALYSIS == "HHWWgg" ]]; then
    ls $OUTDIR/CMS-HGG_mva_13TeV_sigfit.root > out.txt
    echo "ls ../Signal/$OUTDIR/CMS-HGG_mva_13TeV_sigfit.root > out.txt"
	elif [[ $ANALYSIS == "H4G" ]]; then
		ls $OUTDIR/CMS-HGG_mva_13TeV_sigfit.root > out.txt
    echo "ls ../Signal/$OUTDIR/CMS-HGG_mva_13TeV_sigfit.root > out.txt"
  else
    ls $OUTDIR/CMS-HGG_sigfit_${EXT}_*.root > out.txt
    echo "HERE ls ../Signal/$OUTDIR/CMS-HGG_sigfit_${EXT}_*.root > out.txt"
  fi

  # ls $OUTDIR/CMS-HGG_sigfit_${EXT}_*.root > out.txt
  # echo "ls ../Signal/$OUTDIR/CMS-HGG_sigfit_${EXT}_*.root > out.txt"

  counter=0
  while read p ; do
    if (($counter==0)); then
      #SIGFILES="$PWD/$p"
      SIGFILES="$p"
    else
      #SIGFILES="$SIGFILES,$PWD/$p"
      SIGFILES="$SIGFILES,$p"
    fi
    ((counter=$counter+1))
  done < out.txt
  echo "SIGFILES $SIGFILES"
  echo ""
  if [[ $BATCH == "" ]]; then
    echo "./bin/PackageOutput -i $SIGFILES --procs $PROCS -l $INTLUMI -p $OUTDIR/sigfit -W wsig_13TeV -f $CATS -L 120 -H 130 -o $OUTDIR/CMS-HGG_sigfit_$EXT.root --year $YEAR --FinalState $FINALSTATE"
    ./bin/PackageOutput -i $SIGFILES --procs $PROCS -l $INTLUMI -p $OUTDIR/sigfit -W wsig_13TeV -f $CATS -L 120 -H 130 -o $OUTDIR/CMS-HGG_sigfit_$EXT.root --year 2016 --FinalState $FINALSTATE > package.out
  else
    echo "./python/submitPackager.py -i $SIGFILES --basepath $PWD --procs $PROCS -l $INTLUMI -p $OUTDIR/sigfit -W wsig_13TeV -f $CATS -L 120 -H 130 -o $OUTDIR/CMS-HGG_sigfit_$EXT.root --batch $BATCH -q $QUEUE --year $YEAR"
    ./python/submitPackager.py -i $SIGFILES --basepath $PWD --procs $PROCS -l $INTLUMI -p $OUTDIR/sigfit -W wsig_13TeV -f $CATS -L 120 -H 130 -o $OUTDIR/CMS-HGG_sigfit_$EXT.root --batch $BATCH -q $QUEUE --year $YEAR

    PEND=`ls -l $OUTDIR/sigfit/PackagerJobs/sub*| grep -v "\.run" | grep -v "\.done" | grep -v "\.fail" | grep -v "\.err" |grep -v "\.log" | grep -v "\.out" | grep -v "\.sub" | wc -l`
    echo "PEND $PEND"
    while (( $PEND > 0 )) ; do
      PEND=`ls -l $OUTDIR/sigfit/PackagerJobs/sub* | grep -v "\.run" | grep -v "\.done" | grep -v "\.fail" | grep -v "\.err" | grep -v "\.log" | grep -v "\.out" | grep -v "\.sub" | wc -l`
      RUN=`ls -l $OUTDIR/sigfit/PackagerJobs/sub* | grep "\.run" | wc -l`
      FAIL=`ls -l $OUTDIR/sigfit/PackagerJobs/sub* | grep "\.fail" | wc -l`
      DONE=`ls -l $OUTDIR/sigfit/PackagerJobs/sub* | grep "\.done" | wc -l`
      (( PEND=$PEND-$RUN-$FAIL-$DONE ))
      echo " PEND $PEND - RUN $RUN - DONE $DONE - FAIL $FAIL"
      if (( $RUN > 0 )) ; then PEND=1 ; fi
      if (( $FAIL > 0 )) ; then
        echo "[ERROR] at least one job failed :"
        ls -l $OUTDIR/sigfit/PackagerJobs/sub* | grep "\.fail"
        exit 1
      fi
      sleep 10
    done
  fi
fi

#####################################################
#################### SIGNAL PLOTS ###################
#####################################################

if [ $SIGPLOTSONLY == 1 ]; then
  echo "=============================="
  echo "Make Signal Plots"
  echo "-->Create Validation plots"
  echo "=============================="

  if [ -z $BATCH ]; then

    inFile="${OUTDIR}/CMS-HGG_sigfit_${EXT}.root" #packaged
    # if [[ $ANALYSIS == "HHWWgg" ]]; then
    #   inFile="${OUTDIR}/CMS-HGG_mva_13TeV_sigfit.root" # non-packaged
    # fi
    # sysOption="1"
    # if [ $SYSTEMATICS == 0 ]; then
    #   sysOption="-s dat/empty.dat"
    # fi
    echo " ./bin/makeParametricSignalModelPlots -i ${inFile}  -o $OUTDIR -p $PROCS -f $CATS --analysis $ANALYSIS --year $YEAR --systematics $SYSTEMATICS --analysis_type $ANALYSIS_TYPE --FinalState $FINALSTATE"
    ./bin/makeParametricSignalModelPlots -i ${inFile}  -o $OUTDIR/sigplots -p $PROCS -f $CATS --analysis $ANALYSIS --year 2016 --systematics $SYSTEMATICS --analysis_type $ANALYSIS_TYPE --FinalState $FINALSTATE # Need to not output to .txt file in order to debug
    # ./bin/makeParametricSignalModelPlots -i ${inFile}  -o $OUTDIR/sigplots -p $PROCS -f $CATS --analysis $ANALYSIS --year $YEAR --systematics $SYSTEMATICS > signumbers_${EXT}.txt

    # if [[ $ANALYSIS != "HHWWgg" ]]; then
    #   # should add HHWWgg feature here :)
    #   ./makeSlides.sh $OUTDIR
    #   mv fullslides.pdf $OUTDIR/fullslides_${EXT}.pdf
    # fi

  else
    echo "./python/submitSignalPlots.py -i $OUTDIR/CMS-HGG_sigfit_$EXT.root -o $OUTDIR/sigplots -p $PROCS -f $CATS --batch $BATCH -q $QUEUE --year $YEAR"
    ./python/submitSignalPlots.py -i $OUTDIR/CMS-HGG_sigfit_$EXT.root -o $OUTDIR/sigplots -p $PROCS -f $CATS --batch $BATCH -q $QUEUE --year $YEAR

    PEND=`ls -l $OUTDIR/sigplots/PlottingJobs/sub*| grep -v "\.run" | grep -v "\.done" | grep -v "\.fail" | grep -v "\.err" |grep -v "\.log" | grep -v "\.out" | grep -v "\.sub" | wc -l`
    echo "PEND $PEND"
    while (( $PEND > 0 )) ; do
      PEND=`ls -l $OUTDIR/sigplots/PlottingJobs/sub* | grep -v "\.run" | grep -v "\.done" | grep -v "\.fail" | grep -v "\.err" | grep -v "\.log" | grep -v "\.out" | grep -v "\.sub" | wc -l`
      RUN=`ls -l $OUTDIR/sigplots/PlottingJobs/sub* | grep "\.run" | wc -l`
      FAIL=`ls -l $OUTDIR/sigplots/PlottingJobs/sub* | grep "\.fail" | wc -l`
      DONE=`ls -l $OUTDIR/sigplots/PlottingJobs/sub* | grep "\.done" | wc -l`
      (( PEND=$PEND-$RUN-$FAIL-$DONE ))
      echo " PEND $PEND - RUN $RUN - DONE $DONE - FAIL $FAIL"
      if (( $RUN > 0 )) ; then PEND=1 ; fi
      if (( $FAIL > 0 )) ; then
        echo "[ERROR] at least one job failed :"
        ls -l $OUTDIR/sigplots/PlottingJobs/sub* | grep "\.fail"
        exit 1
      fi
      sleep 10
    done
    cat $OUTDIR/sigplots/PlottingJobs/sub*.log > signumbers_${EXT}.txt
  fi

fi
