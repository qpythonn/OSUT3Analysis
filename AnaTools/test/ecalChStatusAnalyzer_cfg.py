###########################################################
## * Description: Creates a text file with eta, phi coordinates of all dead channels in the Ecal (DeadEcalChannels.txt); Makes plots of dead Ecal channels in the barrel and in the endcap (deadEcalMap.root)

## * Implementation:
##      cmsRun ecalChStatusAnalyzer_cfg.py
############################################################    

import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
### Conditions
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:startup', '')

#process.GlobalTag.globaltag = 'GR_R_61_V5::All'
process.GlobalTag.globaltag = 'FT53_V21A_AN6::All'
#process.GlobalTag.globaltag = 'START53_V27::All'


print "Using global tag:  " + str(process.GlobalTag.globaltag)

process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi")
process.load("Geometry.CaloEventSetup.CaloGeometry_cfi")
process.load("Geometry.CaloEventSetup.CaloTopology_cfi")
process.load("Geometry.CaloEventSetup.EcalTrigTowerConstituents_cfi")


#There is no need to run over more than one event to create the map   
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

###Choose input file  
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
#    'file:/store/user/ahart/BN_WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_Summer12_DR53X-PU_S10_START53_V7A-v2_AODSIM_0/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_Summer12_DR53X-PU_S10_START53_V7A-v2_AODSIM_9_1_Xd3.root'


    #'file:/store/user/biliu/BN_MET_Run2012A-22Jan2013-v1_AOD_0/MET_Run2012A-22Jan2013-v1_AOD_33_1_wb0.root'
#'file:/store/user/biliu/BN_MET_Run2012B-22Jan2013-v1_AOD_0/MET_Run2012B-22Jan2013-v1_AOD_397_1_kQi.root'
#'file:/store/user/jbrinson/MET/BEAN2012-v4/66b7c0b77dff84935489342550a9cb3e/METParked_Run2012D-22Jan2013-v1_AOD_381_1_8xR.root'
    'file:/mnt/hadoop/se/store/user/jbrinson/BN_METParked_Run2012D-22Jan2013-v1_AOD_0/METParked_Run2012D-22Jan2013-v1_AOD_347_1_eBz.root'
    )
)

#refer https://twiki.cern.ch/twiki/bin/viewauth/CMS/EcalChannelStatus for value of maskedEcalChannelStatusThreshold
#Any channel with value over threshold will be considered a 'dead' channel
process.demo = cms.EDAnalyzer("ecalChStatusAnalyzer",
                              maskedEcalChannelStatusThreshold = cms.untracked.int32(3),
                              )
###Output file name
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('deadEcalMap.root')
                                   )

process.p = cms.Path(process.demo)
