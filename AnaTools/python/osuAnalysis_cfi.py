import FWCore.ParameterSet.Config as cms
import math
import os

import OSUT3Analysis.DBTools.osusub_cfg as osusub
from OSUT3Analysis.Configuration.processingUtilities import *
from OSUT3Analysis.Configuration.configurationOptions import *
from OSUT3Analysis.AnaTools.MyTreeBranchSets import *

###########################################################
##### Set up process #####
###########################################################

process = cms.Process ('OSUAnalysis')
process.load ('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.source = cms.Source ('PoolSource',
    fileNames = cms.untracked.vstring ()
)

#output file name when running interactively
process.TFileService = cms.Service ('TFileService',
    fileName = cms.string ('hist.root')
)
process.maxEvents = cms.untracked.PSet (
    input = cms.untracked.int32 (-1)
)

###########################################################
##### Set up the analyzer #####
###########################################################


process.OSUAnalysis = cms.EDProducer ('OSUAnalysis',
    jets = cms.InputTag ('BNproducer', 'selectedPatJetsPFlow'),
    muons    = cms.InputTag ('BNproducer', 'selectedPatMuonsLoosePFlow'),
    secMuons = cms.InputTag ('BNproducer', 'selectedPatMuonsLoosePFlow'),
    electrons = cms.InputTag ('BNproducer', 'selectedPatElectronsLoosePFlow'),
    events = cms.InputTag ('BNproducer', ''),
    taus = cms.InputTag ('BNproducer', 'selectedPatTaus'),
    mets = cms.InputTag ('BNproducer', 'patMETsPFlow'),
    tracks = cms.InputTag ('BNproducer', 'generalTracks'),
    genjets = cms.InputTag ('BNproducer', 'ak5GenJets'),
    mcparticles = cms.InputTag ('BNproducer', 'MCstatus3'),
    stops = cms.InputTag ('BNproducer', 'MCstop'),
    primaryvertexs = cms.InputTag ('BNproducer', 'offlinePrimaryVertices'),
    bxlumis = cms.InputTag ('BNproducer', 'BXlumi'),
    photons = cms.InputTag ('BNproducer', 'none'),
    superclusters = cms.InputTag ('BNproducer', 'corHybridSCandMulti5x5WithPreshower'),
    triggers = cms.InputTag('BNproducer','HLT'),
    trigobjs = cms.InputTag('BNproducer','HLT'),

    dataset = cms.string ('TTbar_Lep'),#dummy variable
    datasetType = cms.string ('bgMC'),#dummy variable
    channels = cms.VPSet (),
    histogramSets = cms.VPSet (),
    useEDMFormat = cms.bool (False),
    treeBranchSets = cms.VPSet (),  
#    treeBranchSets = AllTreeBranchSets,

    #deadEcalFile = cms.string (os.environ['CMSSW_BASE']+'/src/OSUT3Analysis/Configuration/data/DeadEcalChannels.txt'),
    deadEcalFile = cms.string (os.environ['CMSSW_BASE']+'/src/OSUT3Analysis/Configuration/data/ecalDpgMapCutPlusHotSpots.txt'),
#    deadEcalFile = cms.string (os.environ['CMSSW_BASE']+'/src/OSUT3Analysis/Configuration/data/federicoMapCut.txt'),
    badCSCFile   = cms.string (os.environ['CMSSW_BASE']+'/src/OSUT3Analysis/Configuration/data/BadCSCChambers.txt'),  
    printAllTriggers = cms.bool(False),  # prints all available triggers (for first event only)  
    printEventInfo   = cms.bool(False),  # produces a lot of output, recommend using only with few channels and histograms
    GetPlotsAfterEachCut = cms.bool(False),
    useTrackCaloRhoCorr = cms.bool(False),  # Only needed for PU correction of BNtrack isolation energy
    stopCTau = cms.vdouble(100.0, 50.0),  # Original and target stop <c*tau> values; only used if
                                          # datasetType_ == "signalMC" and dataset_ matches "stop.*to.*_.*mm.*"
    plotAllObjectsInPassingEvents = cms.bool(False),
    verbose = cms.int32(0),

# Parameters for event weighting, including systematics  
    doPileupReweighting = cms.bool(True),
    puFile = cms.string (os.environ['CMSSW_BASE']+'/src/OSUT3Analysis/Configuration/data/pu.root'),
    dataPU = cms.string ('PU_data_190456_208686_69300xSec'),
    flagJESJERCorr = cms.bool(False),
    jESJERCorr = cms.string(''),
    targetTriggers = cms.vstring(''),
    applyLeptonSF = cms.bool(False),  #  multiplies scale factors in the case of multiple leptons
    applyGentoRecoEfficiency = cms.bool(False),  # 
    electronSFFile = cms.string (''), # if blank, will attempt to use the SFs hard-coded in SFWeight.cc
    electronSFID = cms.string ('mvaTrig0p9'), # ID label for using hard-coded SFs in SFWeight.cc
    electronSF = cms.string (''), # histogram name if using SFs from a histogram
    electronSFShift = cms.string('central'), # change to 'up' to shift factors up 1 sigma, to 'down' to shift factors down 1
    muonSFFile = cms.string (os.environ['CMSSW_BASE']+'/src/OSUT3Analysis/Configuration/data/MuonSF_ID_ISO_2D.root'),
    muonSF = cms.string ('Combined_TOT'),
    muonSFShift = cms.string('central'), # change to 'up' to shift factors up 1 sigma, to 'down' to shift factors down 1 sigma
    triggerMetSFFile = cms.string (''),  # filename 
    triggerMetSF = cms.string (''),      # histogram name 
    triggerMetSFShift = cms.string('central'), # change to 'up' to shift factors up 1 sigma, to 'down' to shift factors down 1 sigma
    trackNMissOutSFFile = cms.string (''),  # filename 
    trackNMissOutSF = cms.string (''),      # histogram name
    trackNMissOutSFShift = cms.string('central'), # change to 'up' to shift factors up 1 sigma, to 'down' to shift factors down 1 sigma
    EcaloVarySFFile = cms.string (''),  # filename 
    EcaloVarySF = cms.string (''),      # histogram name 
    EcaloVarySFShift = cms.string('central'), # change to 'up' to shift factors up 1 sigma, to 'down' to shift factors down 1 sigma
    recoElectronFile = cms.string (os.environ['CMSSW_BASE']+'/src/OSUT3Analysis/Configuration/data/pu.root'),  # filename
    recoElectron = cms.string ('PU_data_190456_208686_69300xSec'),      # histogram name
    recoMuonFile = cms.string (os.environ['CMSSW_BASE']+'/src/OSUT3Analysis/Configuration/data/pu.root'),  # filename
    recoMuon = cms.string ('PU_data_190456_208686_69300xSec'),      # histogram name
    electronCutFile = cms.string (os.environ['CMSSW_BASE']+'/src/OSUT3Analysis/Configuration/data/pu.root'),  # filename
    electronCut = cms.string ('PU_data_190456_208686_69300xSec'),      # histogram name
    muonCutFile = cms.string (os.environ['CMSSW_BASE']+'/src/OSUT3Analysis/Configuration/data/pu.root'),  # filename
    muonCut = cms.string ('PU_data_190456_208686_69300xSec'),      # histogram name
    isrVarySFFile = cms.string (''),  # filename 
    isrVarySF  = cms.string (''),      # histogram name 
    isrVarySFShift = cms.string('central'), # change to 'up' to shift factors up 1 sigma, to 'down' to shift factors down 1 sigma
    applyTriggerSF = cms.bool(False),
    triggerScaleFactor = cms.double(0.985),#0.985+0.004 #ONLY RELEVANT FOR DISPLACED SUSY ANALYSIS                                      
    applyTrackingSF = cms.bool(False),
    trackSFShift = cms.string('central'), # change to 'up' to shift factors up 1 sigma, to 'down' to shift factors down 1 sigma                                       
    doTopPtReweighting = cms.bool(True),
    applyBtagSF = cms.bool(False),
    minBtag = cms.int32(1),
    maxBtag = cms.int32(5),
    calcPdfWeights = cms.bool(False),      # If setting this to true, recompile with: src> touch OSUT3Analysis/AnaTools/BuildFile.xml; scram setup lhapdffull; scram b -j 9 
    pdfSet = cms.string('cteq66.LHgrid'),  # only used if calcPdfWeights is True
    pdfSetFlag = cms.int32(1),             # only used if calcPdfWeights is True

)


process.myPath = cms.Path (process.OSUAnalysis)

###########################################################################################

if osusub.batchMode:
  dataset = osusub.dataset
  sourceLabel = get_short_name (dataset, dataset_names)
  if sourceLabel=="Unknown":
    print "Error[osuAnalysis_cfi.py]:  Could not find short name for dataset: %s; this will cause job to crash." % dataset  
  label = osusub.datasetLabel
  process.OSUAnalysis.dataset = cms.string (sourceLabel)
  process.OSUAnalysis.datasetType = cms.string (types[sourceLabel])

  if process.OSUAnalysis.datasetType == cms.string ("signalMC") and re.match (r"stop[^_]*to[^_]*_[^_]*mm.*", label):
    stopCTau = stop_ctau (label)
    sourceStopCTau = source_stop_ctau (stopCTau)
    process.OSUAnalysis.stopCTau = cms.vdouble (sourceStopCTau / 10.0, stopCTau / 10.0)
  
  if process.OSUAnalysis.datasetType == cms.string ("signalMC") and re.match (r"AMSB*", label):
    charginoCTau =  chargino_ctau (label)
    sourceCharginoCTau = source_chargino_ctau (charginoCTau)
    process.OSUAnalysis.stopCTau = cms.vdouble (sourceCharginoCTau, charginoCTau)  
#    print "Setting stopCTau = (" + str(sourceCharginoCTau) + ", " + str(charginoCTau) + ") for label = " + label + ", datasetType = " + str(process.OSUAnalysis.datasetType) + ", dataset = " + str(process.OSUAnalysis.dataset) 
    



