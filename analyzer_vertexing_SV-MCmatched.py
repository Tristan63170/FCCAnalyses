processList = {'p8_ee_Zbb_ecm91_EvtGen_Bd2KstarTauTau':{
    'fraction':1, 
    'output':'p8_ee_Zbb_ecm91_EvtGen_Bd2KstarTauTau_output',
    'chunks': 10}
} 
# 1: 10^7
# 0.1: 10^6
# 0.01: 10^5
# 0.001: 10^4
prodTag     = "FCCee/winter2023/IDEA"

outputDir   = "/afs/cern.ch/work/t/tmiralle/public/FCCAnalyses/vertexing_output"
nCPUS       = 2
runBatch    = True
batchQueue  = "testmatch"
compGroup   = "group_u_LHCB.u_z5"

import ROOT

ROOT.gInterpreter.Declare("""
int count_Kst_tracks_in_PTracks(ROOT::VecOps::RVec<int> MC_pdg, ROOT::VecOps::RVec<int> RP_MC_parentindex, ROOT::VecOps::RVec<int> RP_MC_grandparentindex, ROOT::VecOps::RVec<int> RP_primary_vertex_RP_index){
int result = 0;
    for (int i = 0; i<RP_primary_vertex_RP_index.size(); i++){
        if (abs(MC_pdg[RP_MC_parentindex[RP_primary_vertex_RP_index[i]]])==313 && abs(MC_pdg[RP_MC_grandparentindex[RP_primary_vertex_RP_index[i]]])==511) result +=1;
    }
    return result;
}
""")

ROOT.gInterpreter.Declare("""
int count_Tau_tracks_in_PTracks(ROOT::VecOps::RVec<int> MC_pdg, ROOT::VecOps::RVec<int> RP_MC_parentindex, ROOT::VecOps::RVec<int> RP_MC_grandparentindex, ROOT::VecOps::RVec<int> RP_primary_vertex_RP_index){
int result = 0;
    for (int i = 0; i<RP_primary_vertex_RP_index.size(); i++){
        if (abs(MC_pdg[RP_MC_parentindex[RP_primary_vertex_RP_index[i]]])==15 && abs(MC_pdg[RP_MC_grandparentindex[RP_primary_vertex_RP_index[i]]])==511) result +=1;
    }
    return result;
}
""")

ROOT.gInterpreter.Declare("""
int count_Kst_tracks_in_STracks(ROOT::VecOps::RVec<int> MC_pdg, ROOT::VecOps::RVec<int> RP_MC_parentindex, ROOT::VecOps::RVec<int> RP_MC_grandparentindex, ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> RP_secondary_vertex_RP_index){
    int result = 0;
    for (int i = 0; i<RP_secondary_vertex_RP_index.size(); i++){
        if (result==0){
            for (int j = 0; j<RP_secondary_vertex_RP_index[i].size(); j++){
                if (RP_secondary_vertex_RP_index[i].size()==2 && abs(MC_pdg[RP_MC_parentindex[RP_secondary_vertex_RP_index[i][j]]])==313 && abs(MC_pdg[RP_MC_grandparentindex[RP_secondary_vertex_RP_index[i][j]]])==511) result +=1;
            }
        }
    }
    return result;
}
""")

ROOT.gInterpreter.Declare("""
int count_Taum_tracks_in_STracks(ROOT::VecOps::RVec<int> MC_pdg, ROOT::VecOps::RVec<int> RP_MC_parentindex, ROOT::VecOps::RVec<int> RP_MC_grandparentindex, ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>> RP_secondary_vertex_RP_index){
    int result = 0;
    for (int i = 0; i<RP_secondary_vertex_RP_index.size(); i++){
        if (result==0){
            for (int j = 0; j<RP_secondary_vertex_RP_index[i].size(); j++){
                if (RP_secondary_vertex_RP_index[i].size()==3 && MC_pdg[RP_MC_parentindex[RP_secondary_vertex_RP_index[i][j]]]==15 && abs(MC_pdg[RP_MC_grandparentindex[RP_secondary_vertex_RP_index[i][j]]])==511) result +=1;
            }
        }
    }
    return result;
}
""")
                          
class RDFanalysis():
    def analysers(df):
        df2 = (
            df
                .Alias("MCRecoAssociations0",   "MCRecoAssociations#0.index")
                .Alias("MCRecoAssociations1",   "MCRecoAssociations#1.index")
                .Alias("Particle0",             "Particle#0.index")
                .Alias("Particle1", "Particle#1.index")

                .Define("MC_px",                "FCCAnalyses::MCParticle::get_px(Particle)")
                .Define("MC_py",                "FCCAnalyses::MCParticle::get_py(Particle)")
                .Define("MC_pz",                "FCCAnalyses::MCParticle::get_pz(Particle)")
                .Define("MC_p",                 "FCCAnalyses::MCParticle::get_p(Particle)")
                .Define("MC_e",                 "FCCAnalyses::MCParticle::get_e(Particle)")
                .Define("MC_pdg",               "FCCAnalyses::MCParticle::get_pdg(Particle)")
                .Define("MC_charge",            "FCCAnalyses::MCParticle::get_charge(Particle)")
                .Define("MC_mass",              "FCCAnalyses::MCParticle::get_mass(Particle)")
                .Define("MC_status",            "FCCAnalyses::MCParticle::get_genStatus(Particle)")
                .Define('MC_index',             "ROOT::VecOps::RVec<int> v; for(size_t i=0; i<Particle.size(); i++) v.push_back(i);return v;")
                .Define('MC_parentindex',       "FCCAnalyses::MCParticle::get_parentid(MC_index,Particle, Particle0)")
                .Define('MC_grandparentindex',  "FCCAnalyses::MCParticle::get_parentid(MC_parentindex,Particle, Particle0)")
                .Define('MC_greatgrandparentindex', "FCCAnalyses::MCParticle::get_parentid(MC_grandparentindex,Particle, Particle0)")
                .Define('MC_greatgreatgrandparentindex', "FCCAnalyses::MCParticle::get_parentid(MC_greatgrandparentindex, Particle, Particle0)")

                # MC vertex
                .Define("MC_vertex_x",          "FCCAnalyses::MCParticle::get_vertex_x(Particle)")
                .Define("MC_vertex_y",          "FCCAnalyses::MCParticle::get_vertex_y(Particle)")
                .Define("MC_vertex_z",          "FCCAnalyses::MCParticle::get_vertex_z(Particle)")
                .Define("MC_primary_vertex",    "FCCAnalyses::MCParticle::get_EventPrimaryVertex(21)(Particle)")
                .Define("MC_PV_x", "MC_primary_vertex.x()")
                .Define("MC_PV_y", "MC_primary_vertex.y()")
                .Define("MC_PV_z", "MC_primary_vertex.z()")

                .Define("RPs",                  "ReconstructedParticles")
                .Define("RP_p",                 "FCCAnalyses::ReconstructedParticle::get_p(ReconstructedParticles)")
                .Define("RP_e",                 "FCCAnalyses::ReconstructedParticle::get_e(ReconstructedParticles)")
                .Define("RP_px",                "FCCAnalyses::ReconstructedParticle::get_px(ReconstructedParticles)")
                .Define("RP_py",                "FCCAnalyses::ReconstructedParticle::get_py(ReconstructedParticles)")
                .Define("RP_pz",                "FCCAnalyses::ReconstructedParticle::get_pz(ReconstructedParticles)")
                .Define("RP_charge",            "FCCAnalyses::ReconstructedParticle::get_charge(ReconstructedParticles)")
                .Define("RP_mass",              "FCCAnalyses::ReconstructedParticle::get_mass(ReconstructedParticles)")
                .Define('RP_index',             "ROOT::VecOps::RVec<int> v; for(size_t i=0; i<ReconstructedParticles.size(); i++) v.push_back(i);return v;")
                .Define('RP_MC_index',          "FCCAnalyses::ReconstructedParticle2MC::getRP2MC_index(MCRecoAssociations0, MCRecoAssociations1,ReconstructedParticles)") 
                .Define('RP_MC_parentindex',    "FCCAnalyses::MCParticle::get_parentid(RP_MC_index, Particle, Particle0)")
                .Define('RP_MC_grandparentindex',   "FCCAnalyses::MCParticle::get_parentid(RP_MC_parentindex, Particle, Particle0)")
                .Define('RP_MC_greatgrandparentindex', "FCCAnalyses::MCParticle::get_parentid(RP_MC_grandparentindex, Particle, Particle0)")
                .Define('RP_MC_greatgreatgrandparentindex', "FCCAnalyses::MCParticle::get_parentid(RP_MC_greatgrandparentindex, Particle, Particle0)")


                # Track information (and covariance matrix)
                .Define("ReconstructedTracks",      "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK(ReconstructedParticles, EFlowTrack_1)")

                # Build the PV
                # My own solution
                # .Define("VertexObject_allTracks",   "VertexFitterSimple::VertexFitter_Tk(1, ReconstructedTracks, true, 4.5, 20e-3, 300)")
                # .Define("PrimaryTracks",            "VertexFitterSimple::get_PrimaryTracks(VertexObject_allTracks, ReconstructedTracks, true, 4.5, 20e-3, 300, 0.0, 0.0, 0.0, 0)")
                # .Define("PrimaryVertex",            "VertexFitterSimple::VertexFitter(1, ReconstructedParticles, ReconstructedTracks, PrimaryTracks, true, 4.5, 20e-3, 300)")
                # .Define("IsPrimary_based_on_reco",  "VertexFitterSimple::IsPrimary_forTracks(ReconstructedTracks,  PrimaryTracks)")

                # Cross-check for Emmanuel's method to retrieve the reco_indices
                .Define("PrimaryTracks",              "VertexFitterSimple::get_PrimaryTracks( EFlowTrack_1, true, 4.5, 20e-3, 300, 0., 0., 0.)")
                .Define("PrimaryVertex",              "VertexFitterSimple::VertexFitter_Tk(1, PrimaryTracks, EFlowTrack_1, true, 4.5, 20e-3, 300)")

                .Define("IsPrimary_based_on_reco",    "VertexFitterSimple::IsPrimary_forTracks(ReconstructedTracks, PrimaryTracks)")
                # Derive quantities from the PV
                .Define("RP_primary_vertex_x",        "PrimaryVertex.vertex.position.x")
                .Define("RP_primary_vertex_y",        "PrimaryVertex.vertex.position.y")
                .Define("RP_primary_vertex_z",        "PrimaryVertex.vertex.position.z")
                .Define("RP_is_primary_vertex",       "PrimaryVertex.vertex.primary")
                .Define("RP_primary_vertex_chi2",     "PrimaryVertex.vertex.chi2")
                .Define("RP_primary_vertex_ntracks",  "PrimaryVertex.ntracks")
                .Define("RP_primary_vertex_RP_index", "VertexingUtils::get_VertexRecoParticlesInd(PrimaryVertex, ReconstructedParticles)")
                .Define("RP_primary_Kst_tracks_count", "count_Kst_tracks_in_PTracks(MC_pdg,RP_MC_parentindex,RP_MC_grandparentindex,RP_primary_vertex_RP_index)")
                .Define("RP_primary_Tau_tracks_count", "count_Tau_tracks_in_PTracks(MC_pdg,RP_MC_parentindex,RP_MC_grandparentindex,RP_primary_vertex_RP_index)")
               
                # MC indices of the decay Bd -> K* tau tau
                # Retrieves a vector of int's which correspond to indices in the Particle block
                # vector[0] = the mother, and then the daughters in the order specified, i.e. here
                #       [1] = the K*, [2] = the tau-, [3] = the tau+
                # Boolean arguments :
                #        1st: stableDaughters. when set to true, the daughters specified in the list are looked
                #             for among the final, stable particles that come out from the mother, i.e. the decay tree is
                #             explored recursively if needed.
                #        2nd: chargeConjugateMother
                #        3rd: chargeConjugateDaughters
                #        4th: inclusiveDecay: when set to false, if a mother is found, that decays
                #             into the particles specified in the list plus other particle(s), this decay is not selected.
                # If the event contains more than one such decays,only the first one is kept.
                .Define("Bd2KstTauTau_indices",   "MCParticle::get_indices(  511, { 313, 15, -15}, false, true, true, false) ( Particle, Particle1)" )

                # to recover events with a FSR photon on one leg:
                .Define("Bd2KstTauTau_rad_indices",   "MCParticle::get_indices(  511, { 313, 15, -15, 22}, false, true, true, false) ( Particle, Particle1)" )

                # select events for which the requested decay chain has been found:
                .Filter("Bd2KstTauTau_indices.size() > 0 || Bd2KstTauTau_rad_indices.size() > 0")

                .Define("the_Bd2KstTauTau_indices", " if ( Bd2KstTauTau_indices.size() > 0 ) return Bd2KstTauTau_indices; else return Bd2KstTauTau_rad_indices; ")

                .Define("Bd_MCindex",   "return the_Bd2KstTauTau_indices[0];" )
                .Define("Kstar_MCindex",  "return the_Bd2KstTauTau_indices[1];")
                # Note: with chargeConjugateMother and chargeConjugateDaughters set to true in get_indices above (in order to select
                # not only Bd, but also Bd_bar decays, the "taum" does not always correspond to the tau-minus leg, it could be the tau-plus.
                .Define("taum_MCindex",  "return the_Bd2KstTauTau_indices[2] ;")
                .Define("taup_MCindex",  "return the_Bd2KstTauTau_indices[3] ;")


                # the MC Particles of the selected decay :
                .Define("Bd",  "return Particle[Bd_MCindex] ; " )
                .Define("Kstar",  "return  Particle[Kstar_MCindex] ;")
                .Define("taum",  "return Particle[taum_MCindex] ;")
                .Define("taup",  "return Particle[taup_MCindex] ;")

                # Example that shows how to retrieve e.g. the px and theta of one MC particle:
                .Define("taum_px",  "return taum.momentum.x; ")
                .Define("v_taum", "ROOT::VecOps::RVec<edm4hep::MCParticleData> v; v.push_back( taum ); return v; ")
                .Define("v_taum_theta",  "MCParticle::get_theta( v_taum )")
                .Define("taum_theta", "return v_taum_theta[0] ;")

                # -------------------------------------------------------------------------------------------------------
                #
                # ----------   the Kstar -> K Pi decay 


                # the daughters from the K*:
                # from the K* index, one gets a vector with the indices of: mother K*, K, Pi, in this order:
                # Boolean arguments :
                #        1st: stableDaughters. when set to true, the daughters specified in the list are looked
                #             for among the final, stable particles that come out from the mother, i.e. the decay tree is
                #             explored recursively if needed.
                #        2nd: chargeConjugateDaughters
                #        3rd: inclusiveDecay
                .Define("Kst2KPi_indices",    "MCParticle::get_indices_MotherByIndex( Kstar_MCindex, { 321, -211 }, true, true, false, Particle, Particle1)" )

                .Define("K_from_Kstar_MCindex",  "return Kst2KPi_indices[1]; ")
                .Define("Pi_from_Kstar_MCindex",  "return Kst2KPi_indices[2]; ")

                # This is the MC Kaon from the Kstar decay :
                .Define("K_from_Kstar", " return Particle[K_from_Kstar_MCindex]; ")
                # and the MC pion :
                .Define("Pi_from_Kstar",  "return Particle[Pi_from_Kstar_MCindex]; ")

                # -------------------------------------------------------------------------------------------------------
                #
                # ----------  RecoParticles associated with the K+ and Pi- from the Kstar

                # the size of this collection is always 2 provided that Kst2KPi_indices  is not empty.
                # In case one of the Kstar legs did not make a RecoParticle, a "dummy" particle is inserted in the liat.
                # This is done on purpose, to maintain the mapping with the indices.
                # the list KstRecoParticles is the kaon, then the pion.
                # (selRP_matched_to_list ignores the unstable MC particles that are in the input list of indices
                # hence the mother particle, which is the [0] element of the Kst2KPi_indices vector).
                #
                # The matching between RecoParticles and MCParticles requires 4 collections. For more
                # detail, see https://github.com/HEP-FCC/FCCAnalyses/tree/master/examples/basics


                .Define("KstRecoParticles",   " ReconstructedParticle2MC::selRP_matched_to_list( Kst2KPi_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")

                # the corresponding tracks - here, dummy particles, if any, are removed
                .Define("KstTracks",  "ReconstructedParticle2Track::getRP2TRK( KstRecoParticles, EFlowTrack_1)" )

                # number of tracks used to reconstruct the Ds vertex
                .Define("n_KstTracks", "ReconstructedParticle2Track::getTK_n( KstTracks )")

                # Reco'ed vertex of the Kstar  ( = reco'ed decay vertex of the Bd from the K+ and Pi- tracks only)
                .Define("KstVertexObject",  "VertexFitterSimple::VertexFitter_Tk( 2, KstTracks)" )
                .Define("KstVertex",  "VertexingUtils::get_VertexData( KstVertexObject )")

                # MC production vertex of the Kstar ( = MC decay vertex of the Bd, = MC decay vertex of the Kstar)
                .Define("KstMCDecayVertex", " return Kstar.vertex; ")
                .Define("MC_Kst_vertex_x",          "KstMCDecayVertex.x")
                .Define("MC_Kst_vertex_y",          "KstMCDecayVertex.y")
                .Define("MC_Kst_vertex_z",          "KstMCDecayVertex.z")


                # Derive SV quantity
                .Define("RP_Kst_vertex_x",        "KstVertexObject.vertex.position.x")
                .Define("RP_Kst_vertex_y",        "KstVertexObject.vertex.position.y")
                .Define("RP_Kst_vertex_z",        "KstVertexObject.vertex.position.z")
                .Define("RP_Kst_vertex_chi2",     "KstVertexObject.vertex.chi2")

                # -------------------------------------------------------------------------------------------------------



                # -------------------------------------------------------------------------------------------------------
                #
                # ----------   the pions from the tau- decay

                # the daughters from the tau-
                .Define("Taum2Pions_indices",  " MCParticle::get_indices_MotherByIndex( taum_MCindex,  {16, -211, 211, -211  }, true, true, false, Particle, Particle1)" )

                # RecoParticles associated with the pions from the tau decau
                .Define("TaumRecoParticles",   " ReconstructedParticle2MC::selRP_matched_to_list( Taum2Pions_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
                # the corresponding tracks - here, dummy particles, if any, are removed
                .Define("TaumTracks",   "ReconstructedParticle2Track::getRP2TRK( TaumRecoParticles, EFlowTrack_1)" )

                # number of tracks used to reconstruct the Taum vertex
                .Define("n_TaumTracks", "ReconstructedParticle2Track::getTK_n( TaumTracks )")

                # Reco'ed decay vertex of the Taum
                .Define("TaumVertexObject",  "VertexFitterSimple::VertexFitter_Tk( 3, TaumTracks)" )
                .Define("TaumVertex",  "VertexingUtils::get_VertexData( TaumVertexObject ) ")
                
                # MC decay vertex of the Taum:
                # first, get one of the pions from the tau decay ( 0 = the mother tau, 1 = the nu, 2 = a pion)
                .Define("PiFromTaum_MCindex", "return Taum2Pions_indices[1];")
                .Define("PiFromTaum", "return Particle[ PiFromTaum_MCindex ] ;")

                # MC production vertex of this pion:
                .Define("TaumMCDecayVertex",  " return PiFromTaum.vertex; ")
                
                .Define("MC_Taum_vertex_x",          "TaumMCDecayVertex.x")
                .Define("MC_Taum_vertex_y",          "TaumMCDecayVertex.y")
                .Define("MC_Taum_vertex_z",          "TaumMCDecayVertex.z")


                # Derive SV quantity
                .Define("RP_Taum_vertex_x",        "TaumVertexObject.vertex.position.x")
                .Define("RP_Taum_vertex_y",        "TaumVertexObject.vertex.position.y")
                .Define("RP_Taum_vertex_z",        "TaumVertexObject.vertex.position.z")
                .Define("RP_Taum_vertex_chi2",     "TaumVertexObject.vertex.chi2")

                # ----------   the pions from the tau+ decay

                # the daughters from the tau+
                .Define("Taup2Pions_indices",  " MCParticle::get_indices_MotherByIndex( taup_MCindex,  {-16, 211, -211, 211  }, true, true, false, Particle, Particle1)" )

                # RecoParticles associated with the pions from the tau decau
                .Define("TaupRecoParticles",   " ReconstructedParticle2MC::selRP_matched_to_list( Taup2Pions_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
                # the corresponding tracks - here, dummy particles, if any, are removed
                .Define("TaupTracks",   "ReconstructedParticle2Track::getRP2TRK( TaupRecoParticles, EFlowTrack_1)" )

                # number of tracks used to reconstruct the Taup vertex
                .Define("n_TaupTracks", "ReconstructedParticle2Track::getTK_n( TaupTracks )")

                # Reco'ed decay vertex of the Taup
                .Define("TaupVertexObject",  "VertexFitterSimple::VertexFitter_Tk( 3, TaupTracks)" )
                .Define("TaupVertex",  "VertexingUtils::get_VertexData( TaupVertexObject ) ")

                # MC decay vertex of the Taup:
                # first, get one of the pions from the tau decay ( 0 = the mother tau, 1 = the nu, 2 = a pion)
                .Define("PiFromTaup_MCindex", "return Taup2Pions_indices[1];")
                .Define("PiFromTaup", "return Particle[ PiFromTaup_MCindex ] ;")

                # MC production vertex of this pion:
                .Define("TaupMCDecayVertex",  " return PiFromTaup.vertex; ")

                .Define("MC_Taup_vertex_x",          "TaupMCDecayVertex.x")
                .Define("MC_Taup_vertex_y",          "TaupMCDecayVertex.y")
                .Define("MC_Taup_vertex_z",          "TaupMCDecayVertex.z")


                # Derive SV quantity
                .Define("RP_Taup_vertex_x",        "TaupVertexObject.vertex.position.x")
                .Define("RP_Taup_vertex_y",        "TaupVertexObject.vertex.position.y")
                .Define("RP_Taup_vertex_z",        "TaupVertexObject.vertex.position.z")
                .Define("RP_Taup_vertex_chi2",     "TaupVertexObject.vertex.chi2")

                # Build the SVs
                # .Define("SecondaryTracks",            "VertexFitterSimple::get_NonPrimaryTracks(ReconstructedTracks, PrimaryTracks)")
                # # .Define("SecondaryVertices",            "VertexFinderLCFIPlus::get_SV_event(ReconstructedParticles, ReconstructedTracks, SecondaryTracks, PrimaryVertex, IsPrimary_based_on_reco)")

                # # Cross-check for Emmanuel's method to retrieve the reco_indices
                # # .Define("SecondaryVertices",            "VertexFinderLCFIPlus::get_SV_event(SecondaryTracks, ReconstructedTracks, PrimaryVertex, true, 9., 10., 25.)")
                # .Define("SecondaryVertices",            "VertexFinderLCFIPlus::get_SV_event(SecondaryTracks, ReconstructedTracks, PrimaryVertex)")
                # # Derive quantities from the SVs
                # .Define("RP_secondary_vertex_position", "VertexingUtils::get_position_SV(SecondaryVertices)")
                # .Define("RP_secondary_vertex_x",        "VertexingUtils::get_vertex_x(SecondaryVertices)")
                # .Define("RP_secondary_vertex_y",        "VertexingUtils::get_vertex_y(SecondaryVertices)")
                # .Define("RP_secondary_vertex_z",        "VertexingUtils::get_vertex_z(SecondaryVertices)")
                # .Define("RP_secondary_vertex_px",       "VertexingUtils::get_updated_momentum_at_vertex_x(SecondaryVertices)")
                # .Define("RP_secondary_vertex_py",       "VertexingUtils::get_updated_momentum_at_vertex_y(SecondaryVertices)")
                # .Define("RP_secondary_vertex_pz",       "VertexingUtils::get_updated_momentum_at_vertex_z(SecondaryVertices)")
                # .Define("RP_secondary_vertex_n",        "VertexingUtils::get_n_SV(SecondaryVertices)")
                # .Define("RP_secondary_vertex_mass",     "VertexingUtils::get_invM(SecondaryVertices)")
                # .Define("RP_secondary_vertex_ntracks",  "VertexingUtils::get_VertexNtrk(SecondaryVertices)")
                # .Define("RP_secondary_vertex_RP_index", "VertexingUtils::get_VerticesRecoParticlesInd(SecondaryVertices, ReconstructedParticles)")
                # .Define("RP_secondary_vertex_norm_chi2","VertexingUtils::get_norm_chi2_SV(SecondaryVertices)")
                # .Define("RP_secondary_vertex_chi2",     "VertexingUtils::get_chi2_SV(SecondaryVertices)")
                # .Define("RP_secondary_tracks_RP_index", "VertexingUtils::get_TracksRecoParticlesInd(ReconstructedTracks, RP_primary_vertex_RP_index, RP_secondary_vertex_RP_index)")
                # .Define("RP_secondary_Kst_tracks_count", "count_Kst_tracks_in_STracks(MC_pdg,RP_MC_parentindex,RP_MC_grandparentindex,RP_secondary_vertex_RP_index)")
                # .Define("RP_secondary_Taum_tracks_count", "count_Taum_tracks_in_STracks(MC_pdg,RP_MC_parentindex,RP_MC_grandparentindex,RP_secondary_vertex_RP_index)")

                .Define('EVT_thrust',               'FCCAnalyses::Algorithms::minimize_thrust("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
                # .Define('EVT_sphericity',           'FCCAnalyses::Algorithms::minimize_sphericity("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
                .Define('RP_thrustangle',           'FCCAnalyses::Algorithms::getAxisCosTheta(EVT_thrust, RP_px, RP_py, RP_pz)')
                # .Define('RP_sphericityangle',       'FCCAnalyses::Algorithms::getAxisCosTheta(EVT_sphericity, RP_px, RP_py, RP_pz)')

                .Define('MC_EVT_thrust',               'FCCAnalyses::Algorithms::minimize_thrust("Minuit2","Migrad")(MC_px, MC_py, MC_pz)')
                .Define('MC_thrustangle',           'FCCAnalyses::Algorithms::getAxisCosTheta(MC_EVT_thrust, MC_px, MC_py, MC_pz)')
        )
        return df2


    def output():
        branchList = [
            "MC_EVT_thrust", "MC_thrustangle", "MC_px","MC_py","MC_pz","MC_p","MC_e","MC_pdg","MC_charge","MC_mass", "MC_status", "MC_vertex_x", "MC_vertex_y", "MC_vertex_z", "MC_primary_vertex", "MC_index", "MC_parentindex","MC_grandparentindex","MC_greatgrandparentindex", "MC_greatgreatgrandparentindex",

            "RP_thrustangle","RP_p","RP_px","RP_py","RP_pz","RP_charge","RP_mass","RP_index","RP_e", "RP_MC_index","RP_MC_parentindex","RP_MC_grandparentindex","RP_MC_greatgrandparentindex", "RP_MC_greatgreatgrandparentindex",

            "MC_PV_x","MC_PV_y","MC_PV_z","RP_primary_vertex_x", "RP_primary_vertex_y", "RP_primary_vertex_z", "RP_is_primary_vertex", "RP_primary_vertex_chi2", "RP_primary_vertex_RP_index",

            "MC_Kst_vertex_x", "MC_Kst_vertex_y", "MC_Kst_vertex_z", "RP_Kst_vertex_x", "RP_Kst_vertex_y", "RP_Kst_vertex_z", "RP_Kst_vertex_chi2",

            "MC_Taum_vertex_x", "MC_Taum_vertex_y", "MC_Taum_vertex_z", "RP_Taum_vertex_x", "RP_Taum_vertex_y", "RP_Taum_vertex_z", "RP_Taum_vertex_chi2",

            "MC_Taup_vertex_x", "MC_Taup_vertex_y", "MC_Taup_vertex_z", "RP_Taup_vertex_x", "RP_Taup_vertex_y", "RP_Taup_vertex_z", "RP_Taup_vertex_chi2"



        ]
        return branchList
