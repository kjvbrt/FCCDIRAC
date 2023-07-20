#!/bin/env python
"""script to do X"""
from DIRAC.Core.Base.Script import parseCommandLine
parseCommandLine()

from ILCDIRAC.Interfaces.API.NewInterface.Applications import DelphesApp
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC


def run():
  """Run The Job."""
  job = UserJob()
  job.setConfigPackage("fccConfig", 'key4hep-devel-2')

  delphes = DelphesApp()
  delphes.setVersion('key4hep-latest')
  delphes.setExecutableName("DelphesPythia8_EDM4HEP")
  delphes.setDetectorCard('card_IDEA.tcl')
  delphes.setOutputCard('edm4hep_IDEA.tcl')
  delphes.setPythia8Card('p8_ee_Zbb_ecm91.cmd')
  delphes.setRandomSeed(36)
  delphes.setEnergy(91.188)
  delphes.setNumberOfEvents(100)
  delphes.setOutputFile('output.root')

  job.append(delphes)
  job.submit(DiracILC(), mode='local')

  

if __name__ =="__main__":
  run()
