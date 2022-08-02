#ifndef ADDITIONALCODE_H
#define ADDITIONALCODE_H

#include <cmath>
#include <vector>
#include <iostream>

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/TrackState.h"
#include "podio/ObjectID.h"
#include "TLorentzVector.h"


#include "MCParticle.h"
#include "ReconstructedParticle2MC.h"

// return one MC leg corresponding to the Bs decay
// note: the sizxe of the vector is always zero or one. I return a ROOT::VecOps::RVec for convenience

struct selMC_leg{
  selMC_leg( int idx );
  int m_idx;
  ROOT::VecOps::RVec<edm4hep::MCParticleData> operator() (ROOT::VecOps::RVec<int> list_of_indices,
                                                          ROOT::VecOps::RVec<edm4hep::MCParticleData> in) ;
};



// specific code to run the Bs2DsK example :

ROOT::VecOps::RVec<int>  getMC_indices_Ds2KKPi (ROOT::VecOps::RVec<int> Bs2DsK_indices,
                                                ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) ;

ROOT::VecOps::RVec<int>  getMC_indices_Bs2KKPiK (ROOT::VecOps::RVec<int> Bs2DsK_indices,
                                                 ROOT::VecOps::RVec<int> Ds2KKPi_indices ) ;


edm4hep::Vector3d BsMCDecayVertex(ROOT::VecOps::RVec<int>  mcParticles_indices,
                                  ROOT::VecOps::RVec<edm4hep::MCParticleData> in) ;



ROOT::VecOps::RVec<edm4hep::TrackState>  
tracks_for_fitting_the_Bs_vertex(ROOT::VecOps::RVec<edm4hep::TrackState>  ReconstructedDs_atVertex_TrackState_withCovariance,
				 ROOT::VecOps::RVec<edm4hep::TrackState> BachelorKTrack);


struct selRP_leg{
  selRP_leg( int idx );
  int m_idx;
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> BsRecoParticles);
};

#endif

