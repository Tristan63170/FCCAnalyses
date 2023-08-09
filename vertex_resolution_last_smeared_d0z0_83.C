#define vertex_resolution_last_cxx
#include "vertex_resolution_last_smeared_d0z0_83.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

void vertex_resolution_last::Loop()
{
    if (fChain == 0) return;

    TFile *f = new TFile("/afs/cern.ch/work/t/tmiralle/public/FCCAnalyses/vertexing_output_smeared_d0z0_83/p8_ee_Zbb_ecm91_EvtGen_Bd2KstarTauTau/vertex_resolution_last_smeared_d0z0_83.root", "RECREATE");
    f -> cd();

    TTree *t = new TTree("tree", "event wise vertex resolution container");

    vector<Double_t  > PV_rec_x, PV_rec_y, PV_rec_z;
    vector<Double_t  > PV_mc_x, PV_mc_y, PV_mc_z;
    vector<Double_t  > PV_dx, PV_dy, PV_dz;
    vector<Double_t  > PV_rec_chi2;

    vector<Double_t  > Kst_rec_x, Kst_rec_y, Kst_rec_z;
    vector<Double_t  > Kst_mc_x, Kst_mc_y, Kst_mc_z;
    vector<Double_t  > Kst_dx, Kst_dy, Kst_dz;
    vector<Double_t  > Kst_uLx, Kst_uLy, Kst_uLz;

    vector<Double_t  > Tau_rec_x, Tau_rec_y, Tau_rec_z;
    vector<Double_t  > Tau_mc_x, Tau_mc_y, Tau_mc_z;
    vector<Double_t  > Tau_dx, Tau_dy, Tau_dz;
    vector<Double_t  > Tau_uLx, Tau_uLy, Tau_uLz;

    vector<Double_t  > displacement_Kst_l, displacement_Kst_t;
    vector<Double_t  > displacement_Tau_l, displacement_Tau_t;

    vector<Double_t  > Kst_rec_chi2;
    vector<Double_t  > Tau_rec_chi2;

    t -> Branch("PV_rec_x", &PV_rec_x);
    t -> Branch("PV_rec_y", &PV_rec_y);
    t -> Branch("PV_rec_z", &PV_rec_z);
    t -> Branch("PV_mc_x", &PV_mc_x);
    t -> Branch("PV_mc_y", &PV_mc_y);
    t -> Branch("PV_mc_z", &PV_mc_z);
    t -> Branch("PV_dx", &PV_dx);
    t -> Branch("PV_dy", &PV_dy);
    t -> Branch("PV_dz", &PV_dz);
    t -> Branch("PV_rec_chi2", &PV_rec_chi2);

    t -> Branch("Kst_rec_x", &Kst_rec_x);
    t -> Branch("Kst_rec_y", &Kst_rec_y);
    t -> Branch("Kst_rec_z", &Kst_rec_z);
    t -> Branch("Kst_rec_chi2", &Kst_rec_chi2);
    t -> Branch("Kst_mc_x", &Kst_mc_x);
    t -> Branch("Kst_mc_y", &Kst_mc_y);
    t -> Branch("Kst_mc_z", &Kst_mc_z);
    t -> Branch("Kst_dx", &Kst_dx);
    t -> Branch("Kst_dy", &Kst_dy);
    t -> Branch("Kst_dz", &Kst_dz);
    t -> Branch("Kst_uLx", &Kst_uLx);
    t -> Branch("Kst_uLy", &Kst_uLy);
    t -> Branch("Kst_uLz", &Kst_uLz);

    t -> Branch("Tau_rec_x", &Tau_rec_x);
    t -> Branch("Tau_rec_y", &Tau_rec_y);
    t -> Branch("Tau_rec_z", &Tau_rec_z);
    t -> Branch("Tau_rec_chi2", &Tau_rec_chi2);
    t -> Branch("Tau_mc_x", &Tau_mc_x);
    t -> Branch("Tau_mc_y", &Tau_mc_y);
    t -> Branch("Tau_mc_z", &Tau_mc_z);
    t -> Branch("Tau_dx", &Tau_dx);
    t -> Branch("Tau_dy", &Tau_dy);
    t -> Branch("Tau_dz", &Tau_dz);
    t -> Branch("Tau_uLx", &Tau_uLx);
    t -> Branch("Tau_uLy", &Tau_uLy);
    t -> Branch("Tau_uLz", &Tau_uLz);

    t -> Branch("displacement_Kst_l", &displacement_Kst_l);
    t -> Branch("displacement_Kst_t", &displacement_Kst_t);

    t -> Branch("displacement_Tau_l", &displacement_Tau_l);
    t -> Branch("displacement_Tau_t", &displacement_Tau_t);



    Long64_t nentries = fChain -> GetEntries();

    Long64_t nbytes = 0, nb = 0, step_size = nentries / 10;

    for (Long64_t jentry=0; jentry < nentries;jentry++) {
        Long64_t ientry = LoadTree(jentry);
        if (ientry < 0) break;
        nb = fChain->GetEntry(jentry);   nbytes += nb;
        
        if (jentry % step_size == 0) {
            cout << "--- Info: reading event (" << jentry << "-" << jentry + step_size << ") of " << nentries << " ---" << endl;
        }

        PV_rec_x.clear(), PV_rec_y.clear(), PV_rec_z.clear();
        PV_mc_x.clear(), PV_mc_y.clear(), PV_mc_z.clear();
        PV_dx.clear(), PV_dy.clear(), PV_dz.clear();
        PV_rec_chi2.clear();

        Kst_rec_x.clear(), Kst_rec_y.clear(), Kst_rec_z.clear(), Kst_rec_chi2.clear();
        Kst_mc_x.clear(), Kst_mc_y.clear(), Kst_mc_z.clear();
        Kst_dx.clear(), Kst_dy.clear(), Kst_dz.clear();
        Kst_uLx.clear(), Kst_uLy.clear(), Kst_uLz.clear();

        Tau_rec_x.clear(), Tau_rec_y.clear(), Tau_rec_z.clear(), Tau_rec_chi2.clear();
        Tau_mc_x.clear(), Tau_mc_y.clear(), Tau_mc_z.clear();
        Tau_dx.clear(), Tau_dy.clear(), Tau_dz.clear();
        Tau_uLx.clear(), Tau_uLy.clear(), Tau_uLz.clear();

        displacement_Kst_l.clear(), displacement_Kst_t.clear();

        displacement_Tau_l.clear(), displacement_Tau_t.clear();

        // PV
        TVector3 primary_vertex_mc, primary_vertex_rec;
        primary_vertex_mc.SetXYZ(MC_PV_x, MC_PV_y, MC_PV_z);
        primary_vertex_rec.SetXYZ(RP_primary_vertex_x, RP_primary_vertex_y, RP_primary_vertex_z);

        PV_rec_x.push_back(primary_vertex_rec.X()), PV_rec_y.push_back(primary_vertex_rec.Y()), PV_rec_z.push_back(primary_vertex_rec.Z());
        PV_mc_x.push_back(primary_vertex_mc.X()), PV_mc_y.push_back(primary_vertex_mc.Y()), PV_mc_z.push_back(primary_vertex_mc.Z());
        PV_dx.push_back(primary_vertex_rec.X()-primary_vertex_mc.X()), PV_dy.push_back(primary_vertex_rec.Y()-primary_vertex_mc.Y()), PV_dz.push_back(primary_vertex_rec.Z()-primary_vertex_mc.Z());
        PV_rec_chi2.push_back(RP_primary_vertex_chi2);

        // Kstar to KPi
        TVector3 Kst_vertex_mc, Kst_vertex_rec;
        Kst_vertex_mc.SetXYZ(MC_Kst_vertex_x, MC_Kst_vertex_y, MC_Kst_vertex_z);
        Kst_vertex_rec.SetXYZ(RP_Kst_vertex_x, RP_Kst_vertex_y, RP_Kst_vertex_z);

        Kst_rec_x.push_back(Kst_vertex_rec.X()), Kst_rec_y.push_back(Kst_vertex_rec.Y()), Kst_rec_z.push_back(Kst_vertex_rec.Z());
        Kst_mc_x.push_back(Kst_vertex_mc.X()), Kst_mc_y.push_back(Kst_vertex_mc.Y()), Kst_mc_z.push_back(Kst_vertex_mc.Z());
        Kst_rec_chi2.push_back(RP_Kst_vertex_chi2);
        Kst_dx.push_back(Kst_vertex_rec.X()-Kst_vertex_mc.X()), Kst_dy.push_back(Kst_vertex_rec.Y()-Kst_vertex_mc.Y()), Kst_dz.push_back(Kst_vertex_rec.Z()-Kst_vertex_mc.Z());

        TVector3 displacement_Kst = Kst_vertex_rec - Kst_vertex_mc;
        TVector3 reference_axis_PV_Kst = (Kst_vertex_mc - primary_vertex_mc).Unit();
        Kst_uLx.push_back(reference_axis_PV_Kst.X()), Kst_uLy.push_back(reference_axis_PV_Kst.Y()), Kst_uLz.push_back(reference_axis_PV_Kst.Z());
        Double_t   Dl_Kst = displacement_Kst.Dot(reference_axis_PV_Kst);
        Double_t   Dt_Kst = sqrt(displacement_Kst.Mag2() - Dl_Kst*Dl_Kst);
        displacement_Kst_l.push_back(Dl_Kst), displacement_Kst_t.push_back(Dt_Kst);

        // Tau- to 3Pi
        TVector3 Taum_vertex_mc, Taum_vertex_rec;
        Taum_vertex_mc.SetXYZ(MC_Taum_vertex_x, MC_Taum_vertex_y, MC_Taum_vertex_z);
        Taum_vertex_rec.SetXYZ(RP_Taum_vertex_x, RP_Taum_vertex_y, RP_Taum_vertex_z);

        Tau_rec_x.push_back(Taum_vertex_rec.X()), Tau_rec_y.push_back(Taum_vertex_rec.Y()), Tau_rec_z.push_back(Taum_vertex_rec.Z());
        Tau_mc_x.push_back(Taum_vertex_mc.X()), Tau_mc_y.push_back(Taum_vertex_mc.Y()), Tau_mc_z.push_back(Taum_vertex_mc.Z());
        Tau_rec_chi2.push_back(RP_Taum_vertex_chi2);
        Tau_dx.push_back(Taum_vertex_rec.X()-Taum_vertex_mc.X()), Tau_dy.push_back(Taum_vertex_rec.Y()-Taum_vertex_mc.Y()), Tau_dz.push_back(Taum_vertex_rec.Z()-Taum_vertex_mc.Z());

        TVector3 displacement_Taum = Taum_vertex_rec - Taum_vertex_mc;
        TVector3 reference_axis_Kst_Taum = (Taum_vertex_mc - Kst_vertex_mc).Unit();
        Tau_uLx.push_back(reference_axis_Kst_Taum.X()), Tau_uLy.push_back(reference_axis_Kst_Taum.Y()), Tau_uLz.push_back(reference_axis_Kst_Taum.Z());
        Double_t   Dl_Taum = displacement_Taum.Dot(reference_axis_Kst_Taum);
        Double_t   Dt_Taum= sqrt(displacement_Taum.Mag2() - Dl_Taum*Dl_Taum);
        displacement_Tau_l.push_back(Dl_Taum), displacement_Tau_t.push_back(Dt_Taum);

        // Tau+ to 3Pi
        TVector3 Taup_vertex_mc, Taup_vertex_rec;
        Taup_vertex_mc.SetXYZ(MC_Taup_vertex_x, MC_Taup_vertex_y, MC_Taup_vertex_z);
        Taup_vertex_rec.SetXYZ(RP_Taup_vertex_x, RP_Taup_vertex_y, RP_Taup_vertex_z);

        Tau_rec_x.push_back(Taup_vertex_rec.X()), Tau_rec_y.push_back(Taup_vertex_rec.Y()), Tau_rec_z.push_back(Taup_vertex_rec.Z());
        Tau_mc_x.push_back(Taup_vertex_mc.X()), Tau_mc_y.push_back(Taup_vertex_mc.Y()), Tau_mc_z.push_back(Taup_vertex_mc.Z());
        Tau_rec_chi2.push_back(RP_Taup_vertex_chi2);
        Tau_dx.push_back(Taup_vertex_rec.X()-Taup_vertex_mc.X()), Tau_dy.push_back(Taup_vertex_rec.Y()-Taup_vertex_mc.Y()), Tau_dz.push_back(Taup_vertex_rec.Z()-Taup_vertex_mc.Z());

        TVector3 displacement_Taup = Taup_vertex_rec - Taup_vertex_mc;
        TVector3 reference_axis_Kst_Taup = (Taup_vertex_mc - Kst_vertex_mc).Unit();
        Tau_uLx.push_back(reference_axis_Kst_Taup.X()), Tau_uLy.push_back(reference_axis_Kst_Taup.Y()), Tau_uLz.push_back(reference_axis_Kst_Taup.Z());
        Double_t   Dl_Taup = displacement_Taup.Dot(reference_axis_Kst_Taup);
        Double_t   Dt_Taup= sqrt(displacement_Taup.Mag2() - Dl_Taup*Dl_Taup);
        displacement_Tau_l.push_back(Dl_Taup), displacement_Tau_t.push_back(Dt_Taup);
        

        t -> Fill();
    }
    t -> Write();
    f -> Close();
}


void run() {
   vertex_resolution_last a = vertex_resolution_last();
   a.Loop();
}