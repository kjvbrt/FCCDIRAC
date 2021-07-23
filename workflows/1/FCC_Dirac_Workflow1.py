
# Create sandbox files
import os
from shutil import copy2
import array

# Utility function
def copywithreplace(filein, fileout, repls):

    # If no replacements, just copy the file
    if len(repls) == 0:
        copy2(filein, fileout)
        return

    #input file
    fin = open(filein, "rt")
    #output file to write the result to
    fout = open(fileout, "wt")
    #for each line in the input file
    for line in fin:
        # Apply each requested replacement
        ltmp = line
        for r in repls:
            lout = ltmp.replace(str(r[0]), str(r[1]))
            ltmp = lout
        fout.write(lout)
        
    #close input and output files
    fin.close()
    fout.close()

from DIRAC.Core.Base import Script
Script.parseCommandLine()

from ILCDIRAC.Interfaces.API.DiracILC import DiracILC
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications import KKMC, GenericApplication

dIlc = DiracILC()

job = UserJob()
job.setOutputSandbox(['*.log', '*.sh', '*.py', '*.xml'])
job.setOutputData( 'edm4hep_test_output.root', '','CERN-DST-EOS' )
job.setInputSandbox(['./delphes_card_IDEA.tcl',
                     './edm4hep_output_config.tcl',
                     './Pythia_LHEinput.cmd'])

job.setJobGroup( "KKMC_EDM4HEP_Run" )
job.setName( "KKMC_EDM4HEP" )
job.setLogLevel("DEBUG")

kkmc = KKMC ()
# kkmc.setVersion('latest')  # Set your exact version in here
kkmc.setVersion('Key4hep-2021-04-30')
kkmc.setEvtType('Tau')
kkmc.setEnergy(91.2)
nevts = 10000
outputfile = 'kkmu_delphes_' + str(nevts) + '.LHE'
kkmc.setNumberOfEvents(nevts)
kkmc.setOutputFile(outputfile)

job.append(kkmc)

# Delphes card
delphescardpath=os.path.expandvars('$DELPHES/cards/delphes_card_IDEA.tcl')
delphescard=os.path.basename(delphescardpath)
copy2(delphescardpath, delphescard)
# EDM4hep output definition
edm4hepoutdefpath=os.path.expandvars('$K4SIMDELPHES/edm4hep_output_config.tcl')
edm4hepoutdef=os.path.basename(edm4hepoutdefpath)
copy2(edm4hepoutdefpath, edm4hepoutdef)
# Pythia card
pythiacardpath=os.path.expandvars('$K4GEN/Pythia_LHEinput.cmd')
pythiacard=os.path.basename(pythiacardpath)
replacements = [['Main:numberOfEvents = 100','Main:numberOfEvents = ' + str(nevts)],
                ['Beams:LHEF = Generation/data/events.lhe','Beams:LHEF = ' + outputfile]]
copywithreplace(pythiacardpath, pythiacard, replacements)

ga = GenericApplication()
ga.setSetupScript("/cvmfs/sw.hsf.org/spackages2/key4hep-stack/2021-04-30/x86_64-centos7-gcc8.3.0-opt/t5gcd6ltt2ikybap2ndoztsg5uyorxzg/setup.sh")
ga.setScript("/cvmfs/sw.hsf.org/spackages2/k4simdelphes/00-01-05/x86_64-centos7-gcc8.3.0-opt/beesqo4r5wuqrrijyz57kxbqcdp5pp4v/bin/DelphesPythia8_EDM4HEP")
# ga.setSetupScript("/cvmfs/sw.hsf.org/key4hep/setup.sh") # Put the exact full path of a given exact version, if that is required
# ga.setScript("DelphesPythia8_EDM4HEP")

ga.setArguments(delphescard + ' ' + edm4hepoutdef + ' ' + pythiacard + ' ' + "edm4hep_test_output.root")

job.append(ga)

# print job.submit(dIlc, mode='wms')  
print job.submit(dIlc, mode='local')  
