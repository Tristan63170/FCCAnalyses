#!/bin/bash
cd /afs/cern.ch/work/t/tmiralle/public/delphes
export LD_LIBRARY_PATH=$PWD/install/lib:$LD_LIBRARY_PATH
export CMAKE_PREFIX_PATH=$PWD/install:$CMAKE_PREFIX_PATH
export DELPHES_DIR=$PWD/install
cd /afs/cern.ch/work/t/tmiralle/public/FCCAnalyses
