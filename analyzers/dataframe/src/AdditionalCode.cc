#include "FCCAnalyses/AdditionalCode.h"

using namespace FCCAnalyses;
using namespace MCParticle;

// To retrieve a given MC leg corresponding to the Bs decay

selMC_leg::selMC_leg( int idx ) {
  m_idx = idx;
};

// I return a vector instead of a single particle :
//   - such that the vector is empty when there is no such decay mode (instead
//     of returning a dummy particle)
//   - such that I can use the getMC_theta etc functions, which work with a
//     ROOT::VecOps::RVec of particles, and not a single particle

ROOT::VecOps::RVec<edm4hep::MCParticleData> selMC_leg::operator() ( ROOT::VecOps::RVec<int> list_of_indices,  ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::MCParticleData>  res;
  if ( list_of_indices.size() == 0) return res;
  if ( m_idx < list_of_indices.size() ) {
        res.push_back( sel_byIndex( list_of_indices[m_idx], in ) );
        return res;
  }
  else {
        std::cout << "   !!!  in selMC_leg:  idx = " << m_idx << " but size of list_of_indices = " << list_of_indices.size() << std::endl;
  }
  return res;
}




// some specific code needed to run the Bs2DsK example :


ROOT::VecOps::RVec<int>  getMC_indices_Ds2KKPi ( ROOT::VecOps::RVec<int> Bs2DsK_indices,
                                                  ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {

 ROOT::VecOps::RVec<int>  result;

 if ( Bs2DsK_indices.size() == 0) return result;
 if ( Bs2DsK_indices.size() != 3) {
        std::cout << "  !!!!  getMC_indices_Bs2DsK: size of Bs2DsK_indices != 3: " << Bs2DsK_indices.size() << std::endl;
        return result;
 }

 //std::cout << " ... in getMC_indices_Ds2KKPi, found a Bs to Ds K " << std::endl;

 int idx_Ds = Bs2DsK_indices[1];  // by construction  ( [0] = index of the mpther Bs )

 // get the indices of the Ds+ daughters :
 std::vector<int> pdg_daughters = { 321, -321, 211 } ;  //  K+, K-, Pi+
 bool stable = true;    // look among the list of *stable* daughters of the Ds+
 ROOT::VecOps::RVec<int> Ds_daughters = get_indices_ExclusiveDecay_MotherByIndex( idx_Ds, pdg_daughters, stable, in, ind);

 // Ds_daughters contains the indices of : the mother Ds, the K+, K-, Pi+
 if ( Ds_daughters.size() != 4 ) return result;   // this is not the decay searched for. Return an empty vector

 //std::cout << " ... Found the Ds daughters " << std::endl;
 //check:
 //std::cout << " end of getMC_indices_Ds2KKPi " << std::endl;
 //for (int i=0; i < Ds_daughters.size(); i++) {
 //std::cout << " index = " << Ds_daughters[i] << " PDG = " << in.at( Ds_daughters[i] ).PDG << std::endl;
 //}

 return Ds_daughters ;
}


// ---------------------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<int>  getMC_indices_Bs2KKPiK ( ROOT::VecOps::RVec<int> Bs2DsK_indices,
                                                  ROOT::VecOps::RVec<int> Ds2KKPi_indices ) {

// returns a vector with the indices of the Bs, (K+ K- Pi+ ) ,  K- , in this order,
// where the first 3 particles are the daughters from the Ds+
// the input lists: Bs2DsK_indices  contains the indices of: the Bs, the Ds+, the K- (in this order)
//                  Ds2KKPi_indices contains the indices of: the Ds+, the K+,K-, Pi+

 ROOT::VecOps::RVec<int>  result;

 if ( Bs2DsK_indices.size() != 3) return result;
 if ( Ds2KKPi_indices.size() != 4) return result;

 // Now fill in the indices:

 result.push_back(  Bs2DsK_indices[0] );   // the mother Bs

 // the Ds daughters :
 for (int i=1; i< Ds2KKPi_indices.size(); i++) {  // do not include the Ds !
   result.push_back( Ds2KKPi_indices[i] );
 }

 result.push_back(  Bs2DsK_indices[2] );  // the bachelor K-
 //std::cout << " ... in getMC_indices_Bs2DsK, found all daughters " << std::endl;

 return result;

}




// ---------------------------------------------------------------------------------------

// this code, despite the name of the method, is actually more general:

edm4hep::Vector3d BsMCDecayVertex(  ROOT::VecOps::RVec<int>  mcParticles_indices, ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {

   edm4hep::Vector3d vertex(1e12, 1e12, 1e12);
   if ( mcParticles_indices.size() == 0 ) return vertex;

   int idx_muplus = mcParticles_indices[1];
   if ( idx_muplus < in.size() ) {
     vertex = in.at( idx_muplus ).vertex;
   }

 //std::cout << " in MCDecayVertex, vertex = " << vertex.x << " " << vertex.y << " " << vertex.z << std::endl;
  return vertex;

}




// ----------------------------------------------------------------------------------------------------------------------------

ROOT::VecOps::RVec<edm4hep::TrackState>  tracks_for_fitting_the_Bs_vertex(
                                ROOT::VecOps::RVec<edm4hep::TrackState>  ReconstructedDs_atVertex_TrackState_withCovariance,
				ROOT::VecOps::RVec<edm4hep::TrackState> BachelorKTrack) {

 ROOT::VecOps::RVec<edm4hep::TrackState>  result;
 if ( ReconstructedDs_atVertex_TrackState_withCovariance.size() != 1 ) return result;
 if ( BachelorKTrack.size() != 1 )  return result;

 result.push_back( ReconstructedDs_atVertex_TrackState_withCovariance[0])  ;  // the pseudo-Ds track
 result.push_back( BachelorKTrack[0] );        // the bachelor K

 return result;
}



selRP_leg::selRP_leg(int idx) {
  m_idx = idx;
};

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> selRP_leg::operator() ( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> BsRecoParticles ) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> res;
  if ( BsRecoParticles.size() == 0) return res;
  if ( m_idx < BsRecoParticles.size() ) {
    res.push_back( BsRecoParticles[m_idx] ) ;
    return res;
  }
  else {
    std::cout << "   !!!  in selRP_leg: idx = " << m_idx << " but size of BsRecoParticles = " << BsRecoParticles.size() << std::endl;
  }
  return res;
}
