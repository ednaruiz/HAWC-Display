//Program for ordering raw data in ascending time
//Edna Ruiz hacking John Pretz script
#include <iostream>
#include <algorithm>
#include <string>
#include <fstream>
#include <set>

#include <TTree.h>
#include <TH1F.h>
#include <TChain.h>
#include <TFile.h>

#include <hawcnest/CommandLineConfigurator.h>

using namespace std;


struct hit{ //Create the structure of hits
    Double_t time;
    Double_t charge;
    UInt_t chan;
};

bool operator<(const hit& lhs,const hit& rhs){//ordering time
    return lhs.time<rhs.time;
}

int main(int argc, char** argv){
    // User interaction
    CommandLineConfigurator cl;
    cl.AddPositionalOption<string>("input","Input ROOT raw file name to order by ascending time");
    cl.AddOption<string> ("out,o","sorted_out.root","output ROOT file ordered by ascending time");
    
    if (!cl.ParseCommandLine(argc, argv)) {
        return 1;
    }
    
    //open input raw file
    string rawfile = cl.GetArgument<string>("input");
    string foutfile    = cl.GetArgument<string>("out");

    
    TChain* hits = new TChain("hits");
    hits->Add(rawfile.c_str());
    
    UInt_t ChannelInfo = 0;
    UInt_t FLAGSInfo = 0;
    Double_t CalibratedTimeInfo = 0;
    Double_t CalibratedChargeInfo = 0;
    
    //this variables are stored by default inside each raw root file
    //here we load them from the hits tree
    hits->SetBranchAddress("Channel",&ChannelInfo);
    hits->SetBranchAddress("FLAGS",&FLAGSInfo);
    hits->SetBranchAddress("CalibratedTime",&CalibratedTimeInfo);
    hits->SetBranchAddress("CalibratedCharge",&CalibratedChargeInfo);

    vector<hit> TIMES;
    
    for(unsigned i=0; i<(hits->GetEntries());i++){//loop over all the entries
    
        hits->GetEntry(i);
        if (FLAGSInfo==0 && CalibratedTimeInfo > 0 ){
            hit h;
            h.chan=ChannelInfo;
            h.time= CalibratedTimeInfo;
            h.charge= CalibratedChargeInfo;
            TIMES.push_back(h); //Fill the vector with the hits structure
        }
        
    }
    sort(TIMES.begin(),TIMES.end());//sort them
    
    
    //Generate the new tree with sorted 
    TFile* fout = new TFile(foutfile.c_str(),"RECREATE");
    TTree* hits_tree = new TTree("hits","hits");
    ULong64_t gridId_tree;
    Double_t time_tree;
    Double_t time_charge;
    hits_tree->Branch("Channel",&gridId_tree);
    hits_tree->Branch("CalibratedTime",&time_tree);
    hits_tree->Branch("CalibratedCharge",&time_charge);
    
    for(unsigned i = 0 ; i < TIMES.size() ; i++){
        gridId_tree=TIMES[i].chan;
        time_tree=TIMES[i].time;
        time_charge=TIMES[i].charge;
        //cout<<gridId_tree<<" "<<time_tree<<" "<<time_charge<<endl;
        hits_tree->Fill();
    }
    hits_tree->Write();

    fout->Close();
}




