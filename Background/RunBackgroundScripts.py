# Script for running background fitting jobs for flashggFinalFit

import os, sys
from optparse import OptionParser

lumi = {'2016':'35.9', '2017':'41.5', '2018':'54.38', 'all':'131.78'} ## -- 1 refers to full run 2 (FIX LATER!)

def get_options():
  parser = OptionParser()

  # Take inputs from a config file: if this is used then ignore all other options
  parser.add_option('--inputConfig', dest='inputConfig', default='', help="Name of input config file (if specified will ignore other options)")

  # Setup
  parser.add_option('--inputWSDir', dest='inputWSDir', default='/vols/cms/es811/FinalFits/ws_ReweighAndNewggHweights', help="Directory storing flashgg workspaces" )
  parser.add_option('--cats', dest='cats', default='UntaggedTag_0,VBFTag_0', help="Define categories")
  parser.add_option('--ext', dest='ext', default='test', help="Extension: defines output dir which must matche xtension used for signal model building")
  parser.add_option('--year', dest='year', default='2016', help="Dataset year")
  parser.add_option('--unblind', dest='unblind', default=0, type='int', help="Unblind")
  # Options for running on the batch
  parser.add_option('--batch', dest='batch', default='IC', help="Batch")
  parser.add_option('--queue', dest='queue', default='hep.q', help="Queue")
  parser.add_option('--mass_a', dest='mass_a', default='', help="mass of pseudoscalar)")
  # Miscellaneous options: only performing single function
  parser.add_option('--mode', dest='mode', default='std', help="For performing single functions [std,fTestOnly,bkgPlotsOnly]")
  parser.add_option('--printOnly', dest='printOnly', default=0, type='int', help="Dry run: print command only")

  parser.add_option('--analysis', dest='analysis', default="", type='str', help="Analysis to run on. Currently just configuring for HHWWgg")
  # parser.add_option('--FinalState', dest='FinalState', default="", type='str', help="Final state particles for HHWWgg: qqlnu, lnulnu, or qqqq")


  return parser.parse_args()

(opt,args) = get_options()

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ RUNNING BACKGROUND SCRIPTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IF using config file then extract options:
if opt.inputConfig != '':
  if os.path.exists( opt.inputConfig ):

    # copy file to have common name and then import cfg options (dict)
    os.system("cp %s config.py"%opt.inputConfig)
    from config import backgroundScriptCfg
    _cfg = backgroundScriptCfg

    # Extract options
    inputWSDir   = _cfg['inputWSDir']
    cats         = _cfg['cats']
    ext          = _cfg['ext']
    year         = _cfg['year']
    unblind      = _cfg['unblind']
    batch        = _cfg['batch']
    queue        = _cfg['queue']
    mode         = _cfg['mode']
    printOnly    = opt.printOnly
    analysis     = _cfg['analysis']
    # FinalState   = _cfg['FinalState']

    # Delete copy of file
    os.system("rm config.py")

  else:
    print " --> [ERROR] %s config file does not exist. Leaving..."%opt.inputConfig
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ RUNNING BACKGROUND SCRIPTS (END) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    sys.exit(1)

# ELSE extract from the option parser
else:
  inputWSDir   = opt.inputWSDir
  cats         = opt.cats
  ext          = opt.ext
  year         = opt.year
  unblind      = opt.unblind
  batch        = opt.batch
  queue        = opt.queue
  mode         = opt.mode
  printOnly    = opt.printOnly
  analysis     = opt.analysis
  # FinalState   = opt.FinalState

ext = ext+"_M"+opt.mass_a
# Check if mode is allowed in options
if mode not in ['std','fTestOnly','bkgPlotsOnly']:
  print " --> [ERROR] mode %s is not allowed. Please use one of the following: [std,fTestOnly,bkgPlotsOnly]. Leaving..."%mode
  print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ RUNNING BACKGROUND SCRIPTS (END) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  sys.exit(1)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Extrct list of input ws filenames
ws_fileNames = []
for root, dirs, files in os.walk( inputWSDir+str(opt.mass_a)+"/Reduced_8Events_1Cats/WS_1Cats/" ):
  for fileName in files:
    if not fileName.startswith('all'): continue
    if not fileName.endswith('.root'): continue
    ws_fileNames.append( fileName )
# concatenate with input dir to get full list of complete file names
ws_fullFileNames = ''
for fileName in ws_fileNames: ws_fullFileNames+="%s/%s,"%(inputWSDir,fileName)
ws_fullFileNames = ws_fullFileNames[:-1]

# Extract list of procs
procs = ''
for fileName in ws_fileNames:
  if 'M125' not in fileName: continue
  procs += "%s,"%fileName.split('pythia8_')[1].split('.root')[0]
procs = procs[:-1]
if len(procs)==0: procs = 'arbitrary'

# Extract data file name and signal fit workspace filename
if(analysis == "H4G"):
    dataFile = "%s%s/Reduced_8Events_1Cats/WS_1Cats/allData.root"%(inputWSDir,opt.mass_a)
    #dataFile="%s/allData.root"%(inputWSDir)
else:  dataFile = "%s/allData.root"%inputWSDir

# signalFitWSFile = "%s/../Signal/outdir_%s/CMS-HGG_sigfit_%s.root"%(os.environ['PWD'],ext,ext)
if(analysis == "HHWWgg"):
  HHWWgg_SigExt = "%s_nodeSM_HHWWgg_%s"%(ext,FinalState) # SM --> more general eventually
  signalFitWSFile = "%s/../Signal/outdir_%s/CMS-HGG_sigfit_%s.root"%(os.environ['PWD'],HHWWgg_SigExt,HHWWgg_SigExt)
else:
  signalFitWSFile = "%s/../Signal/outdir_%s/CMS-HGG_sigfit_%s.root"%(os.environ['PWD'],ext,ext)

# want: sigFileName -s : Signal/outdir_HHWWgg_SM-SL_2016_AllCats_nodeSM_HHWWgg_qqnlu/CMS-HGG_sigfit_HHWWgg_SM-SL_2016_AllCats_nodeSM_HHWWgg_qqlnu.root


# if not os.path.exists( signalFitWSFile ):
#   print " --> [ERROR] signal fit workspace (%s) does not exists. Please run signal fitting first. Leaving..."%signalFitWSFile
#   print " --> [ERROR] Exiting"
#   exit(1)

# Print info to user
print " --> Input flashgg ws dir: %s"%inputWSDir
print " --> Processes: %s"%procs
print " --> Categories: %s"%cats
print " --> Extension: %s"%ext
print " --> Year: %s ::: Corresponds to intLumi = %s fb^-1"%(year,lumi[year])
print ""
print " --> Job information:"
print "     * Batch: %s"%batch
print "     * Queue: %s"%queue
print ""
if mode == "fTestOnly": print " --> Running background fTest only..."
elif mode == "bkgPlotsOnly": print " --> Running background plots only..."
print " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

# Construct input command
print " --> Constructing input command..."

cmdLine = "./runBackgroundScripts.sh -i %s -p %s -f %s --ext %s --intLumi %s --year %s --batch %s --queue %s --sigFile %s --isData "%(dataFile,procs,cats,ext,lumi[year],year,batch,queue,signalFitWSFile)
if mode == "fTestOnly": cmdLine += '--fTestOnly '
elif mode == "bkgPlotsOnly": cmdLine += '--bkgPlotsOnly '
if unblind and not fTestOnly: cmdLine += '--undblind '

if analysis != "": cmdLine += ' --analysis ' + analysis # for HHWWgg customization

# Either print command to screen or run
if printOnly: print "\n%s"%cmdLine
else: os.system( cmdLine )

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ RUNNING BACKGROUND SCRIPTS (END) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
