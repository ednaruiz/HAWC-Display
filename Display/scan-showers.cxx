#include <iostream>



#include <TTree.h>
#include <TH1F.h>
#include <TH2.h>
#include <TSystem.h>
#include <TChain.h>
#include <TFile.h>
#include <TStyle.h>

#include <hawcnest/CommandLineConfigurator.h>



using namespace std;

TChain* hits=new TChain("hits"); //name of the TTree in the input file

//Variables for the SetBranchAddress.
Double_t TCalibratedTime =0;
Double_t TCalibratedCharge=0;
UInt_t TChannel=0;


//-------------FUNCTIONS--------

unsigned chfin=1;
unsigned chinit=1;

void TInterval(Double_t tinit,Double_t tfin){//gives the number of entry (final and initial) corresponding to tinterval
    chfin = 1;
    chinit = 1;
    int i = 0;
    int skip = 0;
    while (hits->GetEntry(i) && skip == 0 )
        hits->GetEntry(i);
        if (TCalibratedTime == tinit){chinit=i;}
        if (TCalibratedTime == tfin){
            chfin=i;
            skip = 1}
        
    }
    chinit=chinit-2;
    chfin=chfin+2;
    cout<<"Chinit: "<<chinit<<" "<<"Chfin: "<<chfin<<"\n"<<endl;
}

void FINDSHOWERS(){//this function print the time interval for blocks of time given by stepfind where ther are 100 or more events.
    unsigned k=1;
    int stepfind=200;
    Double_t tinit = 0.0;
    Double_t tfin = 0.0;
    int contador=0;
    
    for ( unsigned j=1; j<(hits->GetEntries());j++ ){
        contador=0;
        unsigned kinit = k;
        while (hits->GetEntry(k) && TCalibratedTime<stepfind*j){
            hits->GetEntry(k);
            //cout<<stepfind*j<<" "<<TCalibratedTime<<endl;
            
            contador++;
            k++;
            //cout<<contador<<" "<<k<<" "<<kinit<<endl;
            
            
        }
        
        if (contador>50){
            hits->GetEntry(kinit);
            tinit = TCalibratedTime;
            hits->GetEntry(k);
            tfin = TCalibratedTime;
            
            cout<<"Tin: "<<tinit<<"  "<<"Tfin: "<<tfin<<endl;
            TInterval(tinit,tfin );
            
            
            
        }
        
        
    }
}

//---------------------MAIN---------------
int main(int argc,char**argv){
    // User interaction
    CommandLineConfigurator cl;
    cl.AddPositionalOption<string>("input","Input ROOT file with hits format to scan for showers");
    
    if (!cl.ParseCommandLine(argc, argv)) {
        return 1;
    }
    

    
    string fileList=cl.GetArgument<string>("input");//Input of the file
    hits->Add(fileList.c_str());//import the tree of the input file
    
    //Set the address to the variables in the ttree
    hits->SetBranchAddress("Channel", &TChannel);
    hits->SetBranchAddress("CalibratedTime", &TCalibratedTime);
    hits->SetBranchAddress("CalibratedCharge", &TCalibratedCharge);
    
    FINDSHOWERS();


}
