processList = {
    'p8_ee_Zbb_ecm91_EvtGen_Bd2KstarTauTau':{ 
    'output':'lighterVXD_50pc'}
} 
# 1: 10^7
# 0.1: 10^6
# 0.01: 10^5
# 0.001: 10^4
#prodTag     = "FCCee/winter2023/IDEA"

inputDir    = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023_variations/IDEA/lighterVXD_50pc"

outputDir   = "/afs/cern.ch/work/t/tmiralle/public/FCCAnalyses/IP_resolutions_exploration/vertexing_output"
nCPUS       = 2
runBatch    = False
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

ROOT.gInterpreter.Declare("""
    ROOT::VecOps::RVec<int> get_daughters(int parent_index, std::vector<int> daughter_pdgs,ROOT::VecOps::RVec<int> mc_pdgs,ROOT::VecOps::RVec<int> mc_parentindices, ROOT::VecOps::RVec<float> mc_es) {
        ROOT::VecOps::RVec<int> result;
        int parent_pdg = mc_pdgs.at(parent_index);
        vector<int> particle_parentindex;
        
        /*
        if(count(mc_parentindices.begin(),mc_parentindices.end(),parent_index) != daughter_pdgs.size()){
            std::cout<<count(mc_parentindices.begin(),mc_parentindices.end(),parent_index)<< " daughters in place of "<< daughter_pdgs.size() <<std::endl;
            for (int i_mc_particle = 0; i_mc_particle < mc_parentindices.size(); i_mc_particle++){
                if (mc_parentindices.at(i_mc_particle) == parent_index){
                          std::cout << "Daughter pdg = " << mc_pdgs.at(i_mc_particle) << " and index " << i_mc_particle << " and E = " << mc_es.at(i_mc_particle) << std::endl;
                }
            }
        }
        // due to the use of photos in EvtGen, the decays can have additionnal photons but this has no impact regarding their low energy comparing to the regular daughters
        */
        for (int i = 0; i < daughter_pdgs.size(); i++) {
            int particle_index;
            int particle_pdg;
            for (int i_mc_particle = 0; i_mc_particle < mc_parentindices.size(); i_mc_particle++) {
                if (abs(mc_pdgs.at(i_mc_particle)) == abs(daughter_pdgs.at(i)) & 
                    mc_parentindices.at(i_mc_particle) == parent_index &
                    particle_parentindex.size() == 0 &            
                    result.size()==0) {
                    particle_pdg=mc_pdgs.at(i_mc_particle);
                    particle_index = i_mc_particle;
                    particle_parentindex.push_back(mc_parentindices.at(i_mc_particle));
                }
                else if (abs(mc_pdgs.at(i_mc_particle)) == abs(daughter_pdgs.at(i)) &
                    mc_parentindices.at(i_mc_particle) == parent_index &
                    particle_parentindex.size() != 0 &
                    count(particle_parentindex.begin(), particle_parentindex.end(), mc_parentindices.at(i_mc_particle)) == particle_parentindex.size() &
                    result.size()!=0 & 
                    count(result.begin(), result.end(), i_mc_particle) == 0) {
                    particle_pdg=mc_pdgs.at(i_mc_particle);
                    particle_index = i_mc_particle;
                    particle_parentindex.push_back(mc_parentindices.at(i_mc_particle));
                }
            }
            //std::cout<<"Particle pdg = " << particle_pdg<<std::endl;
            //std::cout<<"Particle index = "<< particle_index<<std::endl;
            result.push_back(particle_index);
        }
        //std::cout<<std::endl;
        return result;
    }
""")

ROOT.gInterpreter.Declare("""
            ROOT::VecOps::RVec<float> TrackParamFromMC_DelphesConvV2(edm4hep::MCParticleData aMCParticle) {

            TVector3 p(aMCParticle.momentum.x, aMCParticle.momentum.y,
                        aMCParticle.momentum.z);
            TVector3 x(aMCParticle.vertex.x,aMCParticle.vertex.y,
                        aMCParticle.vertex.z); // mm to m
            float Q = aMCParticle.charge;
            TVectorD param = FCCAnalyses::VertexingUtils::XPtoPar(x, p, Q); // convention Franco
                          
            ROOT::VecOps::RVec<float> result;
                          
            result.push_back(param[0]);
            result.push_back(param[1]);
            result.push_back(param[2]);
            result.push_back(param[3]);
            result.push_back(param[4]);
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

                # # Cross-check for Emmanuel's method to retrieve the reco_indices
                # .Define("PrimaryTracks",              "VertexFitterSimple::get_PrimaryTracks( EFlowTrack_1, true, 4.5, 20e-3, 300, 0., 0., 0.)")
                # .Define("PrimaryVertex",              "VertexFitterSimple::VertexFitter_Tk(1, PrimaryTracks, EFlowTrack_1, true, 4.5, 20e-3, 300)")

                # .Define("IsPrimary_based_on_reco",    "VertexFitterSimple::IsPrimary_forTracks(ReconstructedTracks, PrimaryTracks)")
                # # Derive quantities from the PV
                # .Define("RP_primary_vertex_x",        "PrimaryVertex.vertex.position.x")
                # .Define("RP_primary_vertex_y",        "PrimaryVertex.vertex.position.y")
                # .Define("RP_primary_vertex_z",        "PrimaryVertex.vertex.position.z")
                # .Define("RP_is_primary_vertex",       "PrimaryVertex.vertex.primary")
                # .Define("RP_primary_vertex_chi2",     "PrimaryVertex.vertex.chi2")
                # .Define("RP_primary_vertex_ntracks",  "PrimaryVertex.ntracks")
                # .Define("RP_primary_vertex_RP_index", "VertexingUtils::get_VertexRecoParticlesInd(PrimaryVertex, ReconstructedParticles)")
                # .Define("RP_primary_Kst_tracks_count", "count_Kst_tracks_in_PTracks(MC_pdg,RP_MC_parentindex,RP_MC_grandparentindex,RP_primary_vertex_RP_index)")
                # .Define("RP_primary_Tau_tracks_count", "count_Tau_tracks_in_PTracks(MC_pdg,RP_MC_parentindex,RP_MC_grandparentindex,RP_primary_vertex_RP_index)")
               
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

                .Define("Bd_PDG", "return Bd.PDG;")
                .Define("Kstar_PDG", "return Kstar.PDG;")
                .Define("taum_PDG", "return taum.PDG;")
                .Define("taup_PDG", "return taup.PDG;")

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
                #.Define("Kst2KPi_indices",    "MCParticle::get_indices_MotherByIndex( Kstar_MCindex, { 321, -211 }, true, true, false, Particle, Particle1)" )
                .Define("Kst2KPi_indices",    "get_daughters( Kstar_MCindex, { 321, -211 }, MC_pdg, MC_parentindex, MC_e)" )

                .Define("K_from_Kstar_MCindex",  "return Kst2KPi_indices[0]; ")
                .Define("Pi_from_Kstar_MCindex",  "return Kst2KPi_indices[1]; ")

                # This is the MC Kaon from the Kstar decay :
                .Define("K_from_Kstar", " return Particle[K_from_Kstar_MCindex]; ")
                # and the MC pion :
                .Define("Pi_from_Kstar",  "return Particle[Pi_from_Kstar_MCindex]; ")

                # get p and pT MC
                .Define("MC_p_K_from_Kstar", "return sqrt(K_from_Kstar.momentum.x*K_from_Kstar.momentum.x+K_from_Kstar.momentum.y*K_from_Kstar.momentum.y+K_from_Kstar.momentum.z*K_from_Kstar.momentum.z) ;")
                .Define("MC_pT_K_from_Kstar", "return sqrt(K_from_Kstar.momentum.x*K_from_Kstar.momentum.x+K_from_Kstar.momentum.y*K_from_Kstar.momentum.y)")
                .Define("MC_p_Pi_from_Kstar", "return sqrt(Pi_from_Kstar.momentum.x*Pi_from_Kstar.momentum.x+Pi_from_Kstar.momentum.y*Pi_from_Kstar.momentum.y+Pi_from_Kstar.momentum.z*Pi_from_Kstar.momentum.z)")
                .Define("MC_pT_Pi_from_Kstar", "return sqrt(Pi_from_Kstar.momentum.x*Pi_from_Kstar.momentum.x+Pi_from_Kstar.momentum.y*Pi_from_Kstar.momentum.y)")

                # get production vertex of each track and derive MC IP's
                .Define("K_from_Kstar_MCVertex", "return K_from_Kstar.vertex;")
                .Define("MC_K_from_Kstar_vertex_x", "K_from_Kstar_MCVertex.x")
                .Define("MC_K_from_Kstar_vertex_y", "K_from_Kstar_MCVertex.y")
                .Define("MC_K_from_Kstar_vertex_z", "K_from_Kstar_MCVertex.z")
                # .Define("MC_K_from_Kstar_z0", "MC_K_from_Kstar_vertex_z")
                # .Define("MC_K_from_Kstar_d0", "return sqrt(MC_K_from_Kstar_vertex_x*MC_K_from_Kstar_vertex_x+MC_K_from_Kstar_vertex_y*MC_K_from_Kstar_vertex_y);")

                .Define("Pi_from_Kstar_MCVertex", "return Pi_from_Kstar.vertex;")
                .Define("MC_Pi_from_Kstar_vertex_x", "Pi_from_Kstar_MCVertex.x")
                .Define("MC_Pi_from_Kstar_vertex_y", "Pi_from_Kstar_MCVertex.y")
                .Define("MC_Pi_from_Kstar_vertex_z", "Pi_from_Kstar_MCVertex.z")
                # .Define("MC_Pi_from_Kstar_z0", "MC_Pi_from_Kstar_vertex_z")
                # .Define("MC_Pi_from_Kstar_d0", "return sqrt(MC_Pi_from_Kstar_vertex_x*MC_Pi_from_Kstar_vertex_x+MC_Pi_from_Kstar_vertex_y*MC_Pi_from_Kstar_vertex_y);")


                # .Define("vertex_K", "TVector3(K_from_Kstar.vertex.x,K_from_Kstar.vertex.y,K_from_Kstar.vertex.z)")
                # .Define("p_K","TVector3(K_from_Kstar.momentum.x,K_from_Kstar.momentum.y,K_from_Kstar.momentum.z)")
                # .Define("Q_K","K_from_Kstar.charge")

                #.Define("MC_par_K_from_Kst", "FCCAnalyses::VertexingUtils::XPtoPar(TVector3(K_from_Kstar.vertex[0],K_from_Kstar.vertex[1],K_from_Kstar.vertex[2]),TVector3(K_from_Kstar.momentum[0],K_from_Kstar.momentum[1],K_from_Kstar.momentum[2]),K_from_Kstar.charge)")
                .Define("MC_par_K_from_Kst", "TrackParamFromMC_DelphesConvV2(K_from_Kstar)")
                .Define("MC_K_from_Kstar_z0", "return MC_par_K_from_Kst[3];")
                .Define("MC_K_from_Kstar_d0", "return MC_par_K_from_Kst[0];")

                .Define("MC_par_Pi_from_Kst", "TrackParamFromMC_DelphesConvV2(Pi_from_Kstar)")
                .Define("MC_Pi_from_Kstar_z0", "return MC_par_Pi_from_Kst[3];")
                .Define("MC_Pi_from_Kstar_d0", "return MC_par_Pi_from_Kst[0];")

                .Define("K_from_Kstar_PDG", "return K_from_Kstar.PDG;")
                .Define("Pi_from_Kstar_PDG", "return Pi_from_Kstar.PDG;")
                # get reco IP of each track
                .Define("KstRecoParticles",   " ReconstructedParticle2MC::selRP_matched_to_list( Kst2KPi_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
                .Define("KstRecoParticles_d0", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0(KstRecoParticles,EFlowTrack_1)")
                .Define("KstRecoParticles_z0", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_Z0(KstRecoParticles,EFlowTrack_1)")
                .Define("reco_K_from_Kstar_d0", "return KstRecoParticles_d0[0];")
                .Define("reco_K_from_Kstar_z0", "return KstRecoParticles_z0[0];")
                .Define("reco_Pi_from_Kstar_d0", "return KstRecoParticles_d0[1];")
                .Define("reco_Pi_from_Kstar_z0", "return KstRecoParticles_z0[1];")

                .Define("reco_minus_MC_K_from_Kstar_d0", "return reco_K_from_Kstar_d0-MC_K_from_Kstar_d0;")
                .Define("reco_minus_MC_K_from_Kstar_z0", "return reco_K_from_Kstar_z0-MC_K_from_Kstar_z0;")
                .Define("reco_minus_MC_Pi_from_Kstar_d0", "return reco_Pi_from_Kstar_d0-MC_Pi_from_Kstar_d0;")
                .Define("reco_minus_MC_Pi_from_Kstar_z0", "return reco_Pi_from_Kstar_z0-MC_Pi_from_Kstar_z0;")

                # -------------------------------------------------------------------------------------------------------
                #
                # ----------   the pions from the tau- decay

                #.Define("Taum23Pi_indices",     " MCParticle::get_indices_MotherByIndex( taum_MCindex,  {16, -211, 211, -211  }, true, true, false, Particle, Particle1)"  )
                .Define("Taum23Pi_indices",    "get_daughters( taum_MCindex,  {16, -211, 211, -211  }, MC_pdg, MC_parentindex, MC_e)" )

                .Define("Pi1_from_taum_MCindex",  "return Taum23Pi_indices[1]; ")
                .Define("Pi2_from_taum_MCindex",  "return Taum23Pi_indices[2]; ")
                .Define("Pi3_from_taum_MCindex",  "return Taum23Pi_indices[3]; ")

                # This is the MC pions from tau :
                .Define("Pi1_from_taum",  "return Particle[Pi1_from_taum_MCindex]; ")
                .Define("Pi2_from_taum",  "return Particle[Pi2_from_taum_MCindex]; ")
                .Define("Pi3_from_taum",  "return Particle[Pi3_from_taum_MCindex]; ")

                # get p and pT MC
                .Define("MC_p_Pi1_from_taum", "return sqrt(Pi1_from_taum.momentum.x*Pi1_from_taum.momentum.x+Pi1_from_taum.momentum.y*Pi1_from_taum.momentum.y+Pi1_from_taum.momentum.z*Pi1_from_taum.momentum.z) ;")
                .Define("MC_pT_Pi1_from_taum", "return sqrt(Pi1_from_taum.momentum.x*Pi1_from_taum.momentum.x+Pi1_from_taum.momentum.y*Pi1_from_taum.momentum.y)")
                .Define("MC_p_Pi2_from_taum", "return sqrt(Pi2_from_taum.momentum.x*Pi2_from_taum.momentum.x+Pi2_from_taum.momentum.y*Pi2_from_taum.momentum.y+Pi2_from_taum.momentum.z*Pi2_from_taum.momentum.z) ;")
                .Define("MC_pT_Pi2_from_taum", "return sqrt(Pi2_from_taum.momentum.x*Pi2_from_taum.momentum.x+Pi2_from_taum.momentum.y*Pi2_from_taum.momentum.y)")
                .Define("MC_p_Pi3_from_taum", "return sqrt(Pi3_from_taum.momentum.x*Pi3_from_taum.momentum.x+Pi3_from_taum.momentum.y*Pi3_from_taum.momentum.y+Pi3_from_taum.momentum.z*Pi3_from_taum.momentum.z) ;")
                .Define("MC_pT_Pi3_from_taum", "return sqrt(Pi3_from_taum.momentum.x*Pi3_from_taum.momentum.x+Pi3_from_taum.momentum.y*Pi3_from_taum.momentum.y)")

                # get production vertex of each track and derive MC IP's
                .Define("Pi1_from_taum_MCVertex", "return Pi1_from_taum.vertex;")
                .Define("MC_Pi1_from_taum_vertex_x", "Pi1_from_taum_MCVertex.x")
                .Define("MC_Pi1_from_taum_vertex_y", "Pi1_from_taum_MCVertex.y")
                .Define("MC_Pi1_from_taum_vertex_z", "Pi1_from_taum_MCVertex.z")
                #.Define("MC_Pi1_from_taum_z0", "MC_Pi1_from_taum_vertex_z")
                #.Define("MC_Pi1_from_taum_d0", "return sqrt(MC_Pi1_from_taum_vertex_x*MC_Pi1_from_taum_vertex_x+MC_Pi1_from_taum_vertex_y*MC_Pi1_from_taum_vertex_y);")

                .Define("Pi2_from_taum_MCVertex", "return Pi2_from_taum.vertex;")
                .Define("MC_Pi2_from_taum_vertex_x", "Pi2_from_taum_MCVertex.x")
                .Define("MC_Pi2_from_taum_vertex_y", "Pi2_from_taum_MCVertex.y")
                .Define("MC_Pi2_from_taum_vertex_z", "Pi2_from_taum_MCVertex.z")
                #.Define("MC_Pi2_from_taum_z0", "MC_Pi2_from_taum_vertex_z")
                #.Define("MC_Pi2_from_taum_d0", "return sqrt(MC_Pi2_from_taum_vertex_x*MC_Pi2_from_taum_vertex_x+MC_Pi2_from_taum_vertex_y*MC_Pi2_from_taum_vertex_y);")

                .Define("Pi3_from_taum_MCVertex", "return Pi3_from_taum.vertex;")
                .Define("MC_Pi3_from_taum_vertex_x", "Pi3_from_taum_MCVertex.x")
                .Define("MC_Pi3_from_taum_vertex_y", "Pi3_from_taum_MCVertex.y")
                .Define("MC_Pi3_from_taum_vertex_z", "Pi3_from_taum_MCVertex.z")
                #.Define("MC_Pi3_from_taum_z0", "MC_Pi3_from_taum_vertex_z")
                #.Define("MC_Pi3_from_taum_d0", "return sqrt(MC_Pi3_from_taum_vertex_x*MC_Pi3_from_taum_vertex_x+MC_Pi3_from_taum_vertex_y*MC_Pi3_from_taum_vertex_y);")

                .Define("MC_par_Pi1_from_taum", "TrackParamFromMC_DelphesConvV2(Pi1_from_taum)")
                .Define("MC_Pi1_from_taum_z0", "return MC_par_Pi1_from_taum[3];")
                .Define("MC_Pi1_from_taum_d0", "return MC_par_Pi1_from_taum[0];")

                .Define("MC_par_Pi2_from_taum", "TrackParamFromMC_DelphesConvV2(Pi2_from_taum)")
                .Define("MC_Pi2_from_taum_z0", "return MC_par_Pi2_from_taum[3];")
                .Define("MC_Pi2_from_taum_d0", "return MC_par_Pi2_from_taum[0];")

                .Define("MC_par_Pi3_from_taum", "TrackParamFromMC_DelphesConvV2(Pi3_from_taum)")
                .Define("MC_Pi3_from_taum_z0", "return MC_par_Pi3_from_taum[3];")
                .Define("MC_Pi3_from_taum_d0", "return MC_par_Pi3_from_taum[0];")

                .Define("Pi1_from_taum_PDG", "return Pi1_from_taum.PDG;")
                .Define("Pi2_from_taum_PDG", "return Pi2_from_taum.PDG;")
                .Define("Pi3_from_taum_PDG", "return Pi3_from_taum.PDG;")
                # get reco IP of each track
                .Define("taumRecoParticles",   " ReconstructedParticle2MC::selRP_matched_to_list( Taum23Pi_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
                .Define("taumRecoParticles_d0", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0(taumRecoParticles,EFlowTrack_1)")
                .Define("taumRecoParticles_z0", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_Z0(taumRecoParticles,EFlowTrack_1)")
                
                .Define("reco_Pi1_from_taum_d0", "return taumRecoParticles_d0[1];")
                .Define("reco_Pi1_from_taum_z0", "return taumRecoParticles_z0[1];")
                .Define("reco_Pi2_from_taum_d0", "return taumRecoParticles_d0[2];")
                .Define("reco_Pi2_from_taum_z0", "return taumRecoParticles_z0[2];")
                .Define("reco_Pi3_from_taum_d0", "return taumRecoParticles_d0[3];")
                .Define("reco_Pi3_from_taum_z0", "return taumRecoParticles_z0[3];")

                .Define("reco_minus_MC_Pi1_from_taum_d0", "return reco_Pi1_from_taum_d0-MC_Pi1_from_taum_d0;")
                .Define("reco_minus_MC_Pi1_from_taum_z0", "return reco_Pi1_from_taum_z0-MC_Pi1_from_taum_z0;")
                .Define("reco_minus_MC_Pi2_from_taum_d0", "return reco_Pi2_from_taum_d0-MC_Pi2_from_taum_d0;")
                .Define("reco_minus_MC_Pi2_from_taum_z0", "return reco_Pi2_from_taum_z0-MC_Pi2_from_taum_z0;")
                .Define("reco_minus_MC_Pi3_from_taum_d0", "return reco_Pi3_from_taum_d0-MC_Pi3_from_taum_d0;")
                .Define("reco_minus_MC_Pi3_from_taum_z0", "return reco_Pi3_from_taum_z0-MC_Pi3_from_taum_z0;")

                # ----------   the pions from the tau+ decay

                #.Define("Taup23Pi_indices",     " MCParticle::get_indices_MotherByIndex( taup_MCindex,  {-16, 211, -211, 211  }, true, true, false, Particle, Particle1)"  )
                .Define("Taup23Pi_indices",    "get_daughters( taup_MCindex,  {-16, 211, -211, 211  }, MC_pdg, MC_parentindex, MC_e)" )

                .Define("Pi1_from_taup_MCindex",  "return Taup23Pi_indices[1]; ")
                .Define("Pi2_from_taup_MCindex",  "return Taup23Pi_indices[2]; ")
                .Define("Pi3_from_taup_MCindex",  "return Taup23Pi_indices[3]; ")

                # This is the MC pions from tau :
                .Define("Pi1_from_taup",  "return Particle[Pi1_from_taup_MCindex]; ")
                .Define("Pi2_from_taup",  "return Particle[Pi2_from_taup_MCindex]; ")
                .Define("Pi3_from_taup",  "return Particle[Pi3_from_taup_MCindex]; ")

                # get p and pT MC
                .Define("MC_p_Pi1_from_taup", "return sqrt(Pi1_from_taup.momentum.x*Pi1_from_taup.momentum.x+Pi1_from_taup.momentum.y*Pi1_from_taup.momentum.y+Pi1_from_taup.momentum.z*Pi1_from_taup.momentum.z) ;")
                .Define("MC_pT_Pi1_from_taup", "return sqrt(Pi1_from_taup.momentum.x*Pi1_from_taup.momentum.x+Pi1_from_taup.momentum.y*Pi1_from_taup.momentum.y)")
                .Define("MC_p_Pi2_from_taup", "return sqrt(Pi2_from_taup.momentum.x*Pi2_from_taup.momentum.x+Pi2_from_taup.momentum.y*Pi2_from_taup.momentum.y+Pi2_from_taup.momentum.z*Pi2_from_taup.momentum.z) ;")
                .Define("MC_pT_Pi2_from_taup", "return sqrt(Pi2_from_taup.momentum.x*Pi2_from_taup.momentum.x+Pi2_from_taup.momentum.y*Pi2_from_taup.momentum.y)")
                .Define("MC_p_Pi3_from_taup", "return sqrt(Pi3_from_taup.momentum.x*Pi3_from_taup.momentum.x+Pi3_from_taup.momentum.y*Pi3_from_taup.momentum.y+Pi3_from_taup.momentum.z*Pi3_from_taup.momentum.z) ;")
                .Define("MC_pT_Pi3_from_taup", "return sqrt(Pi3_from_taup.momentum.x*Pi3_from_taup.momentum.x+Pi3_from_taup.momentum.y*Pi3_from_taup.momentum.y)")

                # get production vertex of each track and derive MC IP's
                .Define("Pi1_from_taup_MCVertex", "return Pi1_from_taup.vertex;")
                .Define("MC_Pi1_from_taup_vertex_x", "Pi1_from_taup_MCVertex.x")
                .Define("MC_Pi1_from_taup_vertex_y", "Pi1_from_taup_MCVertex.y")
                .Define("MC_Pi1_from_taup_vertex_z", "Pi1_from_taup_MCVertex.z")
                #.Define("MC_Pi1_from_taup_z0", "MC_Pi1_from_taup_vertex_z")
                #.Define("MC_Pi1_from_taup_d0", "return sqrt(MC_Pi1_from_taup_vertex_x*MC_Pi1_from_taup_vertex_x+MC_Pi1_from_taup_vertex_y*MC_Pi1_from_taup_vertex_y);")

                .Define("Pi2_from_taup_MCVertex", "return Pi2_from_taup.vertex;")
                .Define("MC_Pi2_from_taup_vertex_x", "Pi2_from_taup_MCVertex.x")
                .Define("MC_Pi2_from_taup_vertex_y", "Pi2_from_taup_MCVertex.y")
                .Define("MC_Pi2_from_taup_vertex_z", "Pi2_from_taup_MCVertex.z")
                #.Define("MC_Pi2_from_taup_z0", "MC_Pi2_from_taup_vertex_z")
                #.Define("MC_Pi2_from_taup_d0", "return sqrt(MC_Pi2_from_taup_vertex_x*MC_Pi2_from_taup_vertex_x+MC_Pi2_from_taup_vertex_y*MC_Pi2_from_taup_vertex_y);")

                .Define("Pi3_from_taup_MCVertex", "return Pi3_from_taup.vertex;")
                .Define("MC_Pi3_from_taup_vertex_x", "Pi3_from_taup_MCVertex.x")
                .Define("MC_Pi3_from_taup_vertex_y", "Pi3_from_taup_MCVertex.y")
                .Define("MC_Pi3_from_taup_vertex_z", "Pi3_from_taup_MCVertex.z")
                #.Define("MC_Pi3_from_taup_z0", "MC_Pi3_from_taup_vertex_z")
                #.Define("MC_Pi3_from_taup_d0", "return sqrt(MC_Pi3_from_taup_vertex_x*MC_Pi3_from_taup_vertex_x+MC_Pi3_from_taup_vertex_y*MC_Pi3_from_taup_vertex_y);")

                .Define("MC_par_Pi1_from_taup", "TrackParamFromMC_DelphesConvV2(Pi1_from_taup)")
                .Define("MC_Pi1_from_taup_z0", "return MC_par_Pi1_from_taup[3];")
                .Define("MC_Pi1_from_taup_d0", "return MC_par_Pi1_from_taup[0];")

                .Define("MC_par_Pi2_from_taup", "TrackParamFromMC_DelphesConvV2(Pi2_from_taup)")
                .Define("MC_Pi2_from_taup_z0", "return MC_par_Pi2_from_taup[3];")
                .Define("MC_Pi2_from_taup_d0", "return MC_par_Pi2_from_taup[0];")

                .Define("MC_par_Pi3_from_taup", "TrackParamFromMC_DelphesConvV2(Pi3_from_taup)")
                .Define("MC_Pi3_from_taup_z0", "return MC_par_Pi3_from_taup[3];")
                .Define("MC_Pi3_from_taup_d0", "return MC_par_Pi3_from_taup[0];")

                .Define("Pi1_from_taup_PDG", "return Pi1_from_taup.PDG;")
                .Define("Pi2_from_taup_PDG", "return Pi2_from_taup.PDG;")
                .Define("Pi3_from_taup_PDG", "return Pi3_from_taup.PDG;")
                # get reco IP of each track
                .Define("taupRecoParticles",   " ReconstructedParticle2MC::selRP_matched_to_list( Taup23Pi_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
                .Define("taupRecoParticles_d0", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_D0(taupRecoParticles,EFlowTrack_1)")
                .Define("taupRecoParticles_z0", "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK_Z0(taupRecoParticles,EFlowTrack_1)")
                
                .Define("reco_Pi1_from_taup_d0", "return taupRecoParticles_d0[1];")
                .Define("reco_Pi1_from_taup_z0", "return taupRecoParticles_z0[1];")
                .Define("reco_Pi2_from_taup_d0", "return taupRecoParticles_d0[2];")
                .Define("reco_Pi2_from_taup_z0", "return taupRecoParticles_z0[2];")
                .Define("reco_Pi3_from_taup_d0", "return taupRecoParticles_d0[3];")
                .Define("reco_Pi3_from_taup_z0", "return taupRecoParticles_z0[3];")

                .Define("reco_minus_MC_Pi1_from_taup_d0", "return reco_Pi1_from_taup_d0-MC_Pi1_from_taup_d0;")
                .Define("reco_minus_MC_Pi1_from_taup_z0", "return reco_Pi1_from_taup_z0-MC_Pi1_from_taup_z0;")
                .Define("reco_minus_MC_Pi2_from_taup_d0", "return reco_Pi2_from_taup_d0-MC_Pi2_from_taup_d0;")
                .Define("reco_minus_MC_Pi2_from_taup_z0", "return reco_Pi2_from_taup_z0-MC_Pi2_from_taup_z0;")
                .Define("reco_minus_MC_Pi3_from_taup_d0", "return reco_Pi3_from_taup_d0-MC_Pi3_from_taup_d0;")
                .Define("reco_minus_MC_Pi3_from_taup_z0", "return reco_Pi3_from_taup_z0-MC_Pi3_from_taup_z0;")
        )
        return df2


    def output():
        branchList = [
            "K_from_Kstar_PDG", "Pi_from_Kstar_PDG", "Pi1_from_taum_PDG", "Pi2_from_taum_PDG", "Pi3_from_taum_PDG", "Pi1_from_taup_PDG", "Pi2_from_taup_PDG", "Pi3_from_taup_PDG",
            "MC_p_K_from_Kstar", "MC_pT_K_from_Kstar", "MC_K_from_Kstar_z0", "MC_K_from_Kstar_d0", "reco_K_from_Kstar_z0", "reco_K_from_Kstar_d0", "reco_minus_MC_K_from_Kstar_z0", "reco_minus_MC_K_from_Kstar_d0",
            "MC_p_Pi_from_Kstar", "MC_pT_Pi_from_Kstar", "MC_Pi_from_Kstar_z0", "MC_Pi_from_Kstar_d0", "reco_Pi_from_Kstar_z0", "reco_Pi_from_Kstar_d0", "reco_minus_MC_Pi_from_Kstar_z0", "reco_minus_MC_Pi_from_Kstar_d0",

            "MC_p_Pi1_from_taum", "MC_pT_Pi1_from_taum", "MC_Pi1_from_taum_z0", "MC_Pi1_from_taum_d0", "reco_Pi1_from_taum_z0", "reco_Pi1_from_taum_d0", "reco_minus_MC_Pi1_from_taum_z0", "reco_minus_MC_Pi1_from_taum_d0",
            "MC_p_Pi2_from_taum", "MC_pT_Pi2_from_taum", "MC_Pi2_from_taum_z0", "MC_Pi2_from_taum_d0", "reco_Pi2_from_taum_z0", "reco_Pi2_from_taum_d0", "reco_minus_MC_Pi2_from_taum_z0", "reco_minus_MC_Pi2_from_taum_d0",
            "MC_p_Pi3_from_taum", "MC_pT_Pi3_from_taum", "MC_Pi3_from_taum_z0", "MC_Pi3_from_taum_d0", "reco_Pi3_from_taum_z0", "reco_Pi3_from_taum_d0", "reco_minus_MC_Pi3_from_taum_z0", "reco_minus_MC_Pi3_from_taum_d0",

            "MC_p_Pi1_from_taup", "MC_pT_Pi1_from_taup", "MC_Pi1_from_taup_z0", "MC_Pi1_from_taup_d0", "reco_Pi1_from_taup_z0", "reco_Pi1_from_taup_d0", "reco_minus_MC_Pi1_from_taup_z0", "reco_minus_MC_Pi1_from_taup_d0",
            "MC_p_Pi2_from_taup", "MC_pT_Pi2_from_taup", "MC_Pi2_from_taup_z0", "MC_Pi2_from_taup_d0", "reco_Pi2_from_taup_z0", "reco_Pi2_from_taup_d0", "reco_minus_MC_Pi2_from_taup_z0", "reco_minus_MC_Pi2_from_taup_d0",
            "MC_p_Pi3_from_taup", "MC_pT_Pi3_from_taup", "MC_Pi3_from_taup_z0", "MC_Pi3_from_taup_d0", "reco_Pi3_from_taup_z0", "reco_Pi3_from_taup_d0", "reco_minus_MC_Pi3_from_taup_z0", "reco_minus_MC_Pi3_from_taup_d0"



        ]
        return branchList
