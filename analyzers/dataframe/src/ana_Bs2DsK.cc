#include "FCCAnalyses/ana_Bs2DsK.h"


//using namespace MCParticle;
//using namespace VertexFitterSimple;

//using namespace VertexingUtils;


// ----------------------------------------------------------------------

// using VertexMOre
namespace FCCAnalyses{
  namespace ana_Bs2DsK{

ROOT::VecOps::RVec<edm4hep::TrackState>  ReconstructedDs_fromVertexMore( ROOT::VecOps::RVec<edm4hep::TrackState>  tracks) {

// This returns a vector by convenience - but the vector only contains at most one TrackState.
// tracks in input = the DsTracks

  //std::cout << " --- enter in ReconstructedDs_fromVertexMore  " <<  std::endl;

  ROOT::VecOps::RVec<edm4hep::TrackState > result;

  int Ntr = tracks.size();
  if ( Ntr != 3 ) return result;

  TVectorD** trkPar = new TVectorD*[Ntr];
  TMatrixDSym** trkCov = new TMatrixDSym*[Ntr];

  for (Int_t i = 0; i < Ntr; i++) {
    edm4hep::TrackState t = tracks[i] ;
    TVectorD par = FCCAnalyses::VertexingUtils::get_trackParam( t ) ;
    trkPar[i] = new TVectorD( par );
    TMatrixDSym Cov = FCCAnalyses::VertexingUtils::get_trackCov( t );
    trkCov[i] = new TMatrixDSym ( Cov );
  }

  VertexFit theVertexFit( Ntr, trkPar, trkCov );
  TVectorD  x = theVertexFit.GetVtx() ;   // this actually runs the fit

  VertexFit* vertexfit = &theVertexFit;
  VertexMore vertexmore( vertexfit );

  TVectorD  Ds_track_param  = vertexmore.GetVpar();
  TMatrixDSym cov = vertexmore.GetVcov();

  edm4hep::TrackState track;

    double scale0 = 1e-3;   //convert mm to m
    double scale1 = 1.;
    double scale2 = 0.5*1e3;  // C = rho/2, convert from mm-1 to m-1
    scale2 = -scale2 ;   // sign of omega
    double scale3 = 1e-3 ;  //convert mm to m
    double scale4 = 1.;

        track.D0        = Ds_track_param[0] / scale0 ; // from meters to mm
        track.phi       = Ds_track_param[1] / scale1 ;
        track.omega     = Ds_track_param[2] / scale2 ; // C from Franco = rho/2, and convert from m-1 to mm-1
        track.Z0        = Ds_track_param[3] / scale3  ;   // from meters to mm
        track.tanLambda = Ds_track_param[4] / scale4 ;

  // now the covariance matrix - lower-triangle :

  TMatrixDSym covM(5);
  std::array<float, 15> covMatrix ;

  covMatrix[0]  = cov[0][0] / ( scale0 * scale0) ;
  covMatrix[1]  = cov[1][0] / ( scale1 * scale0 );
  covMatrix[2]  = cov[1][1] / ( scale1 * scale1 );
  covMatrix[3]  = cov[2][0] / ( scale0 * scale2 );
  covMatrix[4]  = cov[2][1] / ( scale1 * scale2 );
  covMatrix[5]  = cov[2][2] / ( scale2 * scale2 ) ;
  covMatrix[6]  = cov[3][0] / ( scale3 * scale0 );
  covMatrix[7]  = cov[3][1] / ( scale3 * scale1 );
  covMatrix[8]  = cov[3][2] / ( scale3 * scale2 );
  covMatrix[9]  = cov[3][3] / ( scale3 * scale3 );
  covMatrix[10]  = cov[4][0] / ( scale4 * scale0 );
  covMatrix[11]  = cov[4][1] / ( scale4 * scale1 );
  covMatrix[12]  = cov[4][2] / ( scale4 * scale2 );
  covMatrix[13]  = cov[4][3] / ( scale4 * scale3 );
  covMatrix[14]  = cov[4][4] / ( scale4 * scale4 );

  track.covMatrix = covMatrix ;

  result.push_back(  track );

  return result;

}



// ------------------------------------------------------------------------------------

TVector3 Momentum_ReconstructedDs_fromVertexMore( ROOT::VecOps::RVec<edm4hep::TrackState>  tracks) {

// returns the momentum (at the Ds vertex) of the Ds
// tracks = the DsTracks

  TVector3 result;

  int Ntr = tracks.size();
  if ( Ntr != 3 ) return result;

  TVectorD** trkPar = new TVectorD*[Ntr];
  TMatrixDSym** trkCov = new TMatrixDSym*[Ntr];

  for (Int_t i = 0; i < Ntr; i++) {
    edm4hep::TrackState t = tracks[i] ;
    TVectorD par = FCCAnalyses::VertexingUtils::get_trackParam( t ) ;
    trkPar[i] = new TVectorD( par );
    TMatrixDSym Cov = FCCAnalyses::VertexingUtils::get_trackCov( t );
    trkCov[i] = new TMatrixDSym ( Cov );
  }

  VertexFit theVertexFit( Ntr, trkPar, trkCov );
  TVectorD  x = theVertexFit.GetVtx() ;   // this actually runs the fit

  VertexFit* vertexfit = &theVertexFit;
  VertexMore vertexmore( vertexfit );

  TVector3 Ds_momentum = vertexmore.GetTotalP(); 
  result = Ds_momentum;

  return result;
}

  }
}
