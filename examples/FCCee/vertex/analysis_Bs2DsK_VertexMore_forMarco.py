import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
#ROOT.gSystem.Load("libFCCAnalysesFlavour")

ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader
#_bs  = ROOT.dummyLoaderFlavour


print ('edm4hep  ',_edm)
print ('podio    ',_pod)
#print ('fccana   ',_bs)


#
#       Example file:  (files produced for Marco) :
#       /eos/experiment/fcc/ee/generation/DelphesEvents/dev/IDEA/p8_ee_Zbb_ecm91_EvtGen_Bs2DsK/events_034379705.root
#

class analysis():

    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        #ROOT.ROOT.EnableImplicitMT(ncpu)

        self.df = ROOT.RDataFrame("events", inputlist)
        print (" done")
    #__________________________________________________________
    def run(self):
        df2 = (self.df.Range(10000)
        #df2 = (self.df

               .Alias("Particle1", "Particle#1.index")
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")


               # MC event primary vertex
               .Define("MC_PrimaryVertex",  "FCCAnalyses::MCParticle::get_EventPrimaryVertex(21)( Particle )" )

               # number of tracks
               .Define("ntracks","FCCAnalyses::ReconstructedParticle2Track::getTK_n(EFlowTrack_1)")


               # MC indices of the decay Bs -> Ds+ K-
               # In the file I process, only the Bs0 (not the Bsbar) has been forced to decay into Ds+ K-
               # Look for (Ds+ K-) in the list of unstable decays of a Bs - hence oscillations are
               # not accounted for. So there should be at most one such decay per event. In any case,
               # would there be > 1, the method gives the first one encountered.
               # Returns the indices of : mother Bs, Ds+, K-

               .Define("Bs2DsK_indices", "FCCAnalyses::MCParticle::get_indices_ExclusiveDecay( -531, {431, -321}, false, false) ( Particle, Particle1)" )


               # MC indices of (this) Ds+ -> K+ K- Pi+
               # Do not want *any* Ds here, hence use custom code in Bs2DsK.cc
               # Returns the indices of:  mother Ds+, K+ K- Pi+
               # comes from AdditionalCode
               .Define("Ds2KKPi_indices",  "getMC_indices_Ds2KKPi( Bs2DsK_indices, Particle, Particle1) ")

               # MC indices of Bs -> ( K+ K- Pi+ ) K-
               # Return the indices of:  mother Bs, ( K+ K- Pi+ ) K-
               # comes from AdditionalCode 
               .Define("Bs2KKPiK_indices",  "getMC_indices_Bs2KKPiK( Bs2DsK_indices,  Ds2KKPi_indices)" )


	       # ---------------------------------------------------------------------------------------
	       # -----    The MC Particles :

               # the MC Bs :
               # comes from AdditionalCode 
               .Define("Bs",  "selMC_leg(0) ( Bs2DsK_indices, Particle )")
               # the MC Ds :
               .Define("Ds",  "selMC_leg(1) ( Bs2DsK_indices, Particle )")
               # the MC bachelor K- from the Bs decay :
               .Define("BachelorK",  "selMC_leg(2) ( Bs2DsK_indices, Particle )")

               # The MC legs from the Ds decay
               .Define("Kplus",   "selMC_leg(1) ( Bs2KKPiK_indices, Particle )")
               .Define("Kminus",   "selMC_leg(2) ( Bs2KKPiK_indices, Particle )")
               .Define("Piplus",   "selMC_leg(3) ( Bs2KKPiK_indices, Particle )")

               # Example to retrieve the energy:
               .Define("Kplus_E",  "FCCAnalyses::MCParticle::get_e( Kplus)" )

               # ---------------------------------------------------------------------------------------



               # ---------------------------------------------------------------------------------------
               # -----    The MC Vertices of the Ds and the Bs :

               # MC Decay vertex of the Ds
               # This takes the production vertex of the 1st non mother particle in Bs2KKPiK_indices, i.e.
               # of the K+ from the Ds, that's what we want. Need to change the name of this method, give it a more general name !
               .Define("DsMCDecayVertex",  "BsMCDecayVertex( Ds2KKPi_indices, Particle ) ")

               # MC Decay vertex of the Bs :
               # Use the BsMCDecayVertex coded for Bs2JPsiPhi: take the production vertex of the Ds. 
               .Define("BsMCDecayVertex",  "BsMCDecayVertex( Bs2DsK_indices, Particle ) ")

               # ---------------------------------------------------------------------------------------


               # ---------------------------------------------------------------------------------------
               # -----    The RecoParticles that are MC-matched with the particles of the Ds decay

               # RecoParticles associated with the Ds decay
               # the size of this collection is always 3 provided that Ds2KKPi_indices is not empty.
               # In case one of the Ds legs did not make a RecoParticle, a "dummy" particle is inserted in the liat.
               # This is done on purpose, to maintain the mapping with the indices.
               .Define("DsRecoParticles",   " FCCAnalyses::ReconstructedParticle2MC::selRP_matched_to_list( Ds2KKPi_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")

               # the corresponding tracks - here, dummy particles, if any, are removed
               .Define("DsTracks",  "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK( DsRecoParticles, EFlowTrack_1)" )

               # number of tracks used to reconstruct the Ds vertex
               .Define("n_DsTracks", "FCCAnalyses::ReconstructedParticle2Track::getTK_n( DsTracks )")

               # the RecoParticles associated with the K+, K- and Pi+ of the Ds decay
               #.Define("RecoKplus",  "selRP_leg(0)( DsRecoParticles )" )
               #.Define("RecoKminus", "selRP_leg(1)( DsRecoParticles )" )
               #.Define("RecoPiplus", "selRP_leg(2)( DsRecoParticles )" )

               # ---------------------------------------------------------------------------------------
               # ------      Reco'ed vertex of the Ds

               .Define("DsVertexObject",  "FCCAnalyses::VertexFitterSimple::VertexFitter_Tk( 3, DsTracks)" )
               .Define("DsVertex",  "FCCAnalyses::VertexingUtils::get_VertexData( DsVertexObject )")


	       # -------------------------------------------------------------------------------------------------------
               # ----------  Reconstruction of the Bs vertex 

	       # The Ds pseudoTrack (TrackState) :
               .Define("Ds_PseudoTrack",  "FCCAnalyses::ana_Bs2DsK::ReconstructedDs_fromVertexMore( DsTracks )")

               # The momentum vector (TVector3) of the Ds :
               .Define("Ds_momentum",   "FCCAnalyses::ana_Bs2DsK::Momentum_ReconstructedDs_fromVertexMore( DsTracks )")


               # the  RecoParticle associated with  the bachelor K
               .Define("BsRecoParticles", "FCCAnalyses::ReconstructedParticle2MC::selRP_matched_to_list( Bs2KKPiK_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define("RecoBachelorK",  "selRP_leg(3)( BsRecoParticles )")
               # and the corresponding track
               .Define("BachelorKTrack",  "FCCAnalyses::ReconstructedParticle2Track::getRP2TRK(  RecoBachelorK, EFlowTrack_1)" )

	       # Now we have the two tracks that we need for the Bs vertex :
               .Define("BsTracks",  "tracks_for_fitting_the_Bs_vertex( Ds_PseudoTrack, BachelorKTrack) ")


               # ---------------------------------------------------------------------------------------
               # ------      Reco'ed vertex of the Bs

               .Define("BsVertexObject",  "FCCAnalyses::VertexFitterSimple::VertexFitter_Tk( 2, BsTracks, -1.)" )
               .Define("n_BsTracks", "FCCAnalyses::ReconstructedParticle2Track::getTK_n( BsTracks )")

               # This is the final Bs vertex
               .Define("BsVertex",  "FCCAnalyses::VertexingUtils::get_VertexData( BsVertexObject )")

        )


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "DsMCDecayVertex",
                "BsMCDecayVertex",
                "n_DsTracks",
                "DsVertex",
                "BsVertex",
                "n_BsTracks",
                ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)



if __name__ == "__main__":

    if len(sys.argv)==1:
        print ("usage:")
        print ("python ",sys.argv[0]," file.root")
        sys.exit(3)
    infile = sys.argv[1]
    #outDir = 'FCCee/'+sys.argv[0].split('/')[1]+'/'
    outDir = './'
    import os
    os.system("mkdir -p {}".format(outDir))
    outfile = outDir+infile.split('/')[-1]
    ncpus = 0
    analysis = analysis(infile, outfile, ncpus)
    analysis.run()

    tf = ROOT.TFile(infile)
    entries = tf.events.GetEntries()
    p = ROOT.TParameter(int)( "eventsProcessed", entries)
    outf=ROOT.TFile(outfile,"UPDATE")
    p.Write()
