#ifndef ANABS2DSK_ANALYZERS_H
#define ANABS2DSK_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "podio/ObjectID.h"
#include "TLorentzVector.h"


#include "FCCAnalyses/MCParticle.h"
#include "FCCAnalyses/ReconstructedParticle2MC.h"
#include "FCCAnalyses/VertexFitterSimple.h"
#include "FCCAnalyses/VertexingUtils.h"

namespace FCCAnalyses{
  namespace ana_Bs2DsK{
ROOT::VecOps::RVec<edm4hep::TrackState>  ReconstructedDs_fromVertexMore( ROOT::VecOps::RVec<edm4hep::TrackState> DsTracks );
TVector3 Momentum_ReconstructedDs_fromVertexMore( ROOT::VecOps::RVec<edm4hep::TrackState>  DsTracks) ;

  }
}

#endif


