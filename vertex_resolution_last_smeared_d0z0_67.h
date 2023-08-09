#ifndef vertex_resolution_last_smeared_d0z0_67_h
#define vertex_resolution_last_smeared_d0z0_67_h

#include <iostream>
#include <vector>

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

#include "ROOT/RVec.hxx"

#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TLorentzVector.h>
#include <numeric>
#include <math.h>
#include <algorithm>
#include <iterator>

using namespace std;

class vertex_resolution_last {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   ROOT::VecOps::RVec<float> *MC_EVT_thrust;
   ROOT::VecOps::RVec<float> *MC_thrustangle;
   ROOT::VecOps::RVec<float> *MC_px;
   ROOT::VecOps::RVec<float> *MC_py;
   ROOT::VecOps::RVec<float> *MC_pz;
   ROOT::VecOps::RVec<float> *MC_p;
   ROOT::VecOps::RVec<float> *MC_e;
   ROOT::VecOps::RVec<float> *MC_pdg;
   ROOT::VecOps::RVec<float> *MC_charge;
   ROOT::VecOps::RVec<float> *MC_mass;
   ROOT::VecOps::RVec<float> *MC_status;
   ROOT::VecOps::RVec<float> *MC_vertex_x;
   ROOT::VecOps::RVec<float> *MC_vertex_y;
   ROOT::VecOps::RVec<float> *MC_vertex_z;
   TVector3        *MC_primary_vertex;
   ROOT::VecOps::RVec<int> *MC_index;
   ROOT::VecOps::RVec<int> *MC_parentindex;
   ROOT::VecOps::RVec<int> *MC_grandparentindex;
   ROOT::VecOps::RVec<int> *MC_greatgrandparentindex;
   ROOT::VecOps::RVec<int> *MC_greatgreatgrandparentindex;
   ROOT::VecOps::RVec<float> *RP_thrustangle;
   ROOT::VecOps::RVec<float> *RP_p;
   ROOT::VecOps::RVec<float> *RP_px;
   ROOT::VecOps::RVec<float> *RP_py;
   ROOT::VecOps::RVec<float> *RP_pz;
   ROOT::VecOps::RVec<float> *RP_charge;
   ROOT::VecOps::RVec<float> *RP_mass;
   ROOT::VecOps::RVec<int> *RP_index;
   ROOT::VecOps::RVec<float> *RP_e;
   ROOT::VecOps::RVec<int> *RP_MC_index;
   ROOT::VecOps::RVec<int> *RP_MC_parentindex;
   ROOT::VecOps::RVec<int> *RP_MC_grandparentindex;
   ROOT::VecOps::RVec<int> *RP_MC_greatgrandparentindex;
   ROOT::VecOps::RVec<int> *RP_MC_greatgreatgrandparentindex;
   float_t         RP_primary_vertex_x;
   float_t         RP_primary_vertex_y;
   float_t         RP_primary_vertex_z;
   Int_t           RP_is_primary_vertex;
   float_t         RP_primary_vertex_chi2;
   ROOT::VecOps::RVec<int> *RP_primary_vertex_RP_index;
   double_t         MC_PV_x;
   double_t         MC_PV_y;
   double_t         MC_PV_z;
   double_t         MC_Kst_vertex_x;
   double_t         MC_Kst_vertex_y;
   double_t         MC_Kst_vertex_z;
   float_t         RP_Kst_vertex_x;
   float_t         RP_Kst_vertex_y;
   float_t         RP_Kst_vertex_z;
   float_t         RP_Kst_vertex_chi2;
   double_t         MC_Taum_vertex_x;
   double_t         MC_Taum_vertex_y;
   double_t         MC_Taum_vertex_z;
   float_t         RP_Taum_vertex_x;
   float_t         RP_Taum_vertex_y;
   float_t         RP_Taum_vertex_z;
   float_t         RP_Taum_vertex_chi2;
   double_t         MC_Taup_vertex_x;
   double_t         MC_Taup_vertex_y;
   double_t         MC_Taup_vertex_z;
   float_t         RP_Taup_vertex_x;
   float_t         RP_Taup_vertex_y;
   float_t         RP_Taup_vertex_z;
   float_t         RP_Taup_vertex_chi2;

   // List of branches
   TBranch        *b_MC_EVT_thrust;   //!
   TBranch        *b_MC_thrustangle;   //!
   TBranch        *b_MC_px;   //!
   TBranch        *b_MC_py;   //!
   TBranch        *b_MC_pz;   //!
   TBranch        *b_MC_p;   //!
   TBranch        *b_MC_e;   //!
   TBranch        *b_MC_pdg;   //!
   TBranch        *b_MC_charge;   //!
   TBranch        *b_MC_mass;   //!
   TBranch        *b_MC_status;   //!
   TBranch        *b_MC_vertex_x;   //!
   TBranch        *b_MC_vertex_y;   //!
   TBranch        *b_MC_vertex_z;   //!
   TBranch        *b_MC_primary_vertex;   //!
   TBranch        *b_MC_index;   //!
   TBranch        *b_MC_parentindex;   //!
   TBranch        *b_MC_grandparentindex;   //!
   TBranch        *b_MC_greatgrandparentindex;   //!
   TBranch        *b_MC_greatgreatgrandparentindex;   //!
   TBranch        *b_RP_thrustangle;   //!
   TBranch        *b_RP_p;   //!
   TBranch        *b_RP_px;   //!
   TBranch        *b_RP_py;   //!
   TBranch        *b_RP_pz;   //!
   TBranch        *b_RP_charge;   //!
   TBranch        *b_RP_mass;   //!
   TBranch        *b_RP_index;   //!
   TBranch        *b_RP_e;   //!
   TBranch        *b_RP_MC_index;   //!
   TBranch        *b_RP_MC_parentindex;   //!
   TBranch        *b_RP_MC_grandparentindex;   //!
   TBranch        *b_RP_MC_greatgrandparentindex;   //!
   TBranch        *b_RP_MC_greatgreatgrandparentindex;   //!
   TBranch        *b_RP_primary_vertex_x;   //!
   TBranch        *b_RP_primary_vertex_y;   //!
   TBranch        *b_RP_primary_vertex_z;   //!
   TBranch        *b_RP_is_primary_vertex;   //!
   TBranch        *b_RP_primary_vertex_chi2;   //!
   TBranch        *b_RP_primary_vertex_RP_index;   //!
   TBranch        *b_MC_PV_x; //!
   TBranch        *b_MC_PV_y; //!
   TBranch        *b_MC_PV_z; //!
   TBranch        *b_MC_Kst_vertex_x;  //!
   TBranch        *b_MC_Kst_vertex_y;  //!
   TBranch        *b_MC_Kst_vertex_z;  //!
   TBranch        *b_RP_Kst_vertex_x;  //!
   TBranch        *b_RP_Kst_vertex_y;  //!
   TBranch        *b_RP_Kst_vertex_z;  //!
   TBranch        *b_RP_Kst_vertex_chi2;  //!
   TBranch        *b_MC_Taum_vertex_x; //!
   TBranch        *b_MC_Taum_vertex_y; //!
   TBranch        *b_MC_Taum_vertex_z; //!
   TBranch        *b_RP_Taum_vertex_x; //!
   TBranch        *b_RP_Taum_vertex_y; //!
   TBranch        *b_RP_Taum_vertex_z; //!
   TBranch        *b_RP_Taum_vertex_chi2; //!
   TBranch        *b_MC_Taup_vertex_x; //!
   TBranch        *b_MC_Taup_vertex_y; //!
   TBranch        *b_MC_Taup_vertex_z; //!
   TBranch        *b_RP_Taup_vertex_x; //!
   TBranch        *b_RP_Taup_vertex_y; //!
   TBranch        *b_RP_Taup_vertex_z; //!
   TBranch        *b_RP_Taup_vertex_chi2; //!

   vertex_resolution_last(TTree *tree=0);
   virtual ~vertex_resolution_last();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef vertex_resolution_last_cxx
vertex_resolution_last::vertex_resolution_last(TTree *tree) : fChain(0) 
{
   if (tree == 0) {
      #ifdef SINGLE_TREE
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("/afs/cern.ch/work/t/tmiralle/public/FCCAnalyses/vertexing_output_smeared_d0z0_67/p8_ee_Zbb_ecm91_EvtGen_Bd2KstarTauTau/chunk0.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("/afs/cern.ch/work/t/tmiralle/public/FCCAnalyses/vertexing_output_smeared_d0z0_67/p8_ee_Zbb_ecm91_EvtGen_Bd2KstarTauTau/chunk0.root");
      }
      f->GetObject("events",tree);

      #else 
      TChain * chain = new TChain("events", "");
      for (int i = 0; i < 10; i++) {
         string file_number = to_string(i);
         // string file_name = "/afs/cern.ch/work/t/tmiralle/public/FCCAnalyses/vertexing_output/p8_ee_Zbb_ecm91_EvtGen_Bd2KstarTauTau/chunk" + file_number + ".root/events";
         string file_name = "/afs/cern.ch/work/t/tmiralle/public/FCCAnalyses/vertexing_output_smeared_d0z0_67/p8_ee_Zbb_ecm91_EvtGen_Bd2KstarTauTau/chunk" + file_number + ".root/events";
         const char *c = file_name.c_str();
         chain -> Add(c);
         
         tree = chain;
         #endif // SINGLE_TREE
      }
      // string file_name = "/afs/cern.ch/work/t/tmiralle/public/FCCAnalyses/vertexing_output_smeared_tracks/vertexing_test_SVMCmatched_smeared.root/events";
      // const char *c = file_name.c_str();
      // chain -> Add(c);
      
      // tree = chain;
      // #endif // SINGLE_TREE
   }
   Init(tree);
}

vertex_resolution_last::~vertex_resolution_last()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t vertex_resolution_last::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t vertex_resolution_last::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void vertex_resolution_last::Init(TTree *tree)
{
   MC_EVT_thrust = 0;
   MC_thrustangle = 0;
   MC_px = 0;
   MC_py = 0;
   MC_pz = 0;
   MC_p = 0;
   MC_e = 0;
   MC_pdg = 0;
   MC_charge = 0;
   MC_mass = 0;
   MC_status = 0;
   MC_vertex_x = 0;
   MC_vertex_y = 0;
   MC_vertex_z = 0;
   MC_primary_vertex = 0;
   MC_index = 0;
   MC_parentindex = 0;
   MC_grandparentindex = 0;
   MC_greatgrandparentindex = 0;
   MC_greatgreatgrandparentindex = 0;
   RP_thrustangle = 0;
   RP_p = 0;
   RP_px = 0;
   RP_py = 0;
   RP_pz = 0;
   RP_charge = 0;
   RP_mass = 0;
   RP_index = 0;
   RP_e = 0;
   RP_MC_index = 0;
   RP_MC_parentindex = 0;
   RP_MC_grandparentindex = 0;
   RP_MC_greatgrandparentindex = 0;
   RP_MC_greatgreatgrandparentindex = 0;
   RP_primary_vertex_RP_index = 0;
   MC_PV_x=0;
   MC_PV_y=0;
   MC_PV_z=0;
   MC_Kst_vertex_x=0;
   MC_Kst_vertex_y=0;
   MC_Kst_vertex_z=0;
   RP_Kst_vertex_x=0;
   RP_Kst_vertex_y=0;
   RP_Kst_vertex_z=0;
   RP_Kst_vertex_chi2=0;
   MC_Taum_vertex_x=0;
   MC_Taum_vertex_y=0;
   MC_Taum_vertex_z=0;
   RP_Taum_vertex_x=0;
   RP_Taum_vertex_y=0;
   RP_Taum_vertex_z=0;
   RP_Taum_vertex_chi2=0;
   MC_Taup_vertex_x=0;
   MC_Taup_vertex_y=0;
   MC_Taup_vertex_z=0;
   RP_Taup_vertex_x=0;
   RP_Taup_vertex_y=0;
   RP_Taup_vertex_z=0;
   RP_Taup_vertex_chi2=0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("MC_EVT_thrust", &MC_EVT_thrust, &b_MC_EVT_thrust);
   fChain->SetBranchAddress("MC_thrustangle", &MC_thrustangle, &b_MC_thrustangle);
   fChain->SetBranchAddress("MC_px", &MC_px, &b_MC_px);
   fChain->SetBranchAddress("MC_py", &MC_py, &b_MC_py);
   fChain->SetBranchAddress("MC_pz", &MC_pz, &b_MC_pz);
   fChain->SetBranchAddress("MC_p", &MC_p, &b_MC_p);
   fChain->SetBranchAddress("MC_e", &MC_e, &b_MC_e);
   fChain->SetBranchAddress("MC_pdg", &MC_pdg, &b_MC_pdg);
   fChain->SetBranchAddress("MC_charge", &MC_charge, &b_MC_charge);
   fChain->SetBranchAddress("MC_mass", &MC_mass, &b_MC_mass);
   fChain->SetBranchAddress("MC_status", &MC_status, &b_MC_status);
   fChain->SetBranchAddress("MC_vertex_x", &MC_vertex_x, &b_MC_vertex_x);
   fChain->SetBranchAddress("MC_vertex_y", &MC_vertex_y, &b_MC_vertex_y);
   fChain->SetBranchAddress("MC_vertex_z", &MC_vertex_z, &b_MC_vertex_z);
   fChain->SetBranchAddress("MC_primary_vertex", &MC_primary_vertex, &b_MC_primary_vertex);
   fChain->SetBranchAddress("MC_index", &MC_index, &b_MC_index);
   fChain->SetBranchAddress("MC_parentindex", &MC_parentindex, &b_MC_parentindex);
   fChain->SetBranchAddress("MC_grandparentindex", &MC_grandparentindex, &b_MC_grandparentindex);
   fChain->SetBranchAddress("MC_greatgrandparentindex", &MC_greatgrandparentindex, &b_MC_greatgrandparentindex);
   fChain->SetBranchAddress("MC_greatgreatgrandparentindex", &MC_greatgreatgrandparentindex, &b_MC_greatgreatgrandparentindex);
   fChain->SetBranchAddress("RP_thrustangle", &RP_thrustangle, &b_RP_thrustangle);
   fChain->SetBranchAddress("RP_p", &RP_p, &b_RP_p);
   fChain->SetBranchAddress("RP_px", &RP_px, &b_RP_px);
   fChain->SetBranchAddress("RP_py", &RP_py, &b_RP_py);
   fChain->SetBranchAddress("RP_pz", &RP_pz, &b_RP_pz);
   fChain->SetBranchAddress("RP_charge", &RP_charge, &b_RP_charge);
   fChain->SetBranchAddress("RP_mass", &RP_mass, &b_RP_mass);
   fChain->SetBranchAddress("RP_index", &RP_index, &b_RP_index);
   fChain->SetBranchAddress("RP_e", &RP_e, &b_RP_e);
   fChain->SetBranchAddress("RP_MC_index", &RP_MC_index, &b_RP_MC_index);
   fChain->SetBranchAddress("RP_MC_parentindex", &RP_MC_parentindex, &b_RP_MC_parentindex);
   fChain->SetBranchAddress("RP_MC_grandparentindex", &RP_MC_grandparentindex, &b_RP_MC_grandparentindex);
   fChain->SetBranchAddress("RP_MC_greatgrandparentindex", &RP_MC_greatgrandparentindex, &b_RP_MC_greatgrandparentindex);
   fChain->SetBranchAddress("RP_MC_greatgreatgrandparentindex", &RP_MC_greatgreatgrandparentindex, &b_RP_MC_greatgreatgrandparentindex);
   fChain->SetBranchAddress("RP_primary_vertex_x", &RP_primary_vertex_x, &b_RP_primary_vertex_x);
   fChain->SetBranchAddress("RP_primary_vertex_y", &RP_primary_vertex_y, &b_RP_primary_vertex_y);
   fChain->SetBranchAddress("RP_primary_vertex_z", &RP_primary_vertex_z, &b_RP_primary_vertex_z);
   fChain->SetBranchAddress("RP_is_primary_vertex", &RP_is_primary_vertex, &b_RP_is_primary_vertex);
   fChain->SetBranchAddress("RP_primary_vertex_chi2", &RP_primary_vertex_chi2, &b_RP_primary_vertex_chi2);
   fChain->SetBranchAddress("RP_primary_vertex_RP_index", &RP_primary_vertex_RP_index, &b_RP_primary_vertex_RP_index);
   fChain->SetBranchAddress("MC_PV_x", &MC_PV_x, &b_MC_PV_x);
   fChain->SetBranchAddress("MC_PV_y", &MC_PV_y, &b_MC_PV_y);
   fChain->SetBranchAddress("MC_PV_z", &MC_PV_z, &b_MC_PV_z);
   fChain->SetBranchAddress("MC_Kst_vertex_x", &MC_Kst_vertex_x, &b_MC_Kst_vertex_x);
   fChain->SetBranchAddress("MC_Kst_vertex_y", &MC_Kst_vertex_y, &b_MC_Kst_vertex_y);
   fChain->SetBranchAddress("MC_Kst_vertex_z", &MC_Kst_vertex_z, &b_MC_Kst_vertex_z);
   fChain->SetBranchAddress("RP_Kst_vertex_x", &RP_Kst_vertex_x, &b_RP_Kst_vertex_x);
   fChain->SetBranchAddress("RP_Kst_vertex_y", &RP_Kst_vertex_y, &b_RP_Kst_vertex_y);
   fChain->SetBranchAddress("RP_Kst_vertex_z", &RP_Kst_vertex_z, &b_RP_Kst_vertex_z);
   fChain->SetBranchAddress("RP_Kst_vertex_chi2", &RP_Kst_vertex_chi2, &b_RP_Kst_vertex_chi2);
   fChain->SetBranchAddress("MC_Taum_vertex_x", &MC_Taum_vertex_x, &b_MC_Taum_vertex_x);
   fChain->SetBranchAddress("MC_Taum_vertex_y", &MC_Taum_vertex_y, &b_MC_Taum_vertex_y);
   fChain->SetBranchAddress("MC_Taum_vertex_z", &MC_Taum_vertex_z, &b_MC_Taum_vertex_z);
   fChain->SetBranchAddress("RP_Taum_vertex_x", &RP_Taum_vertex_x, &b_RP_Taum_vertex_x);
   fChain->SetBranchAddress("RP_Taum_vertex_y", &RP_Taum_vertex_y, &b_RP_Taum_vertex_y);
   fChain->SetBranchAddress("RP_Taum_vertex_z", &RP_Taum_vertex_z, &b_RP_Taum_vertex_z);
   fChain->SetBranchAddress("RP_Taum_vertex_chi2", &RP_Taum_vertex_chi2, &b_RP_Taum_vertex_chi2);
   fChain->SetBranchAddress("MC_Taup_vertex_x", &MC_Taup_vertex_x, &b_MC_Taup_vertex_x);
   fChain->SetBranchAddress("MC_Taup_vertex_y", &MC_Taup_vertex_y, &b_MC_Taup_vertex_y);
   fChain->SetBranchAddress("MC_Taup_vertex_z", &MC_Taup_vertex_z, &b_MC_Taup_vertex_z);
   fChain->SetBranchAddress("RP_Taup_vertex_x", &RP_Taup_vertex_x, &b_RP_Taup_vertex_x);
   fChain->SetBranchAddress("RP_Taup_vertex_y", &RP_Taup_vertex_y, &b_RP_Taup_vertex_y);
   fChain->SetBranchAddress("RP_Taup_vertex_z", &RP_Taup_vertex_z, &b_RP_Taup_vertex_z);
   fChain->SetBranchAddress("RP_Taup_vertex_chi2", &RP_Taup_vertex_chi2, &b_RP_Taup_vertex_chi2);

   Notify();
}

Bool_t vertex_resolution_last::Notify()
{
   return kTRUE;
}

void vertex_resolution_last::Show(Long64_t entry)
{
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t vertex_resolution_last::Cut(Long64_t entry)
{
   return 1;
}
#endif
