//Edna Ruiz-Velasco
#include <xcdf/utility/XCDFUtility.h>
#include <xcdf/utility/Expression.h>

#include <TTree.h>
#include <TFile.h>

#include <fstream>
#include <set>
#include <iostream>

#include <hawcnest/CommandLineConfigurator.h>


using namespace std;

void CopyComments(XCDFFile& destination,
                  XCDFFile& source) {
  for (std::vector<std::string>::const_iterator
                             it = source.CommentsBegin();
                             it != source.CommentsEnd(); ++it) {

    destination.AddComment(*it);
  }
}

struct hit{
  unsigned gridId;
  double time;
  double channel;
};


bool operator<(const hit& lhs, const hit& rhs){
  return lhs.time < rhs.time;
}

int main(int argc, char** argv){
  CommandLineConfigurator cl;
  cl.AddPositionalOption<string>("input","Input XCDF file name of a reconstructed extended file");
  cl.AddOption<string> ("out,o","hits_out.root","output ROOT file of reco showers");
    
  if (!cl.ParseCommandLine(argc, argv)) {
    return 1;
  }
    
  string recfile = cl.GetArgument<string>("input");
  string foutfile    = cl.GetArgument<string>("out");


  XCDFFile f(recfile.c_str(),"r");
  
  XCDFUnsignedIntegerField gridId = f.GetUnsignedIntegerField("event.hit.gridId");
  XCDFFloatingPointField t = f.GetFloatingPointField("event.hit.time");
  XCDFUnsignedIntegerField nHit = f.GetUnsignedIntegerField("event.nHit");
  XCDFFloatingPointField ch = f.GetFloatingPointField("event.hit.charge");

  TFile* fout = new TFile(foutfile.c_str(),"RECREATE");
  TTree* hits_tree = new TTree("hits","hits");
  
  ULong64_t gridId_tree;
  Double_t time_tree;
  Double_t channel_tree;
  
  hits_tree->Branch("Channel",&gridId_tree);
  hits_tree->Branch("CalibratedTime",&time_tree);
  hits_tree->Branch("CalibratedCharge",&channel_tree);
  
  while (f.Read()){
  
    vector<hit> hits;
    for(unsigned i = 0 ; i < nHit.At(0) ; i++){
      cout<<gridId.At(i)<<" "<<t.At(i)<<endl;
      hit h;
      h.gridId = gridId.At(i);
      h.time = t.At(i);
      h.channel=ch.At(i);
      
      hits.push_back(h);
    }
    
    sort(hits.begin(),hits.end());
    
    for(unsigned i = 0 ; i < hits.size() ; i++){
      gridId_tree = hits[i].gridId;
      time_tree = hits[i].time;
      channel_tree = hits[i].channel;
      hits_tree->Fill();
    }
    
  }
  
  hits_tree->Write();
  fout->Close();
  
}





