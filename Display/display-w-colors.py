#======================================================================/
# Author: Edna L. Ruiz Velasco    Hermes León Vargas                   /
# HAWC Collaboration                                                   /
# 2016                                                                 /
# Simple Display for RAW or extended preprocessed data                 /
#                                                                      /
#                                                                      /
#                                                                      /
#======================================================================/


#import necessary libraries

import matplotlib.pyplot as plt
import numpy as np
import argparse
from ROOT import *
import os
import pylab as P
import sys
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)

### ARGUMENT PARSER FOR OPTIONS

pars = argparse.ArgumentParser(description='Display for hits format file')

pars.add_argument('-i' , '--input' , help='input file' , dest="infile" , metavar="FILE")
pars.add_argument('-s' , '--start' , help='Start Entry' , dest="start")
pars.add_argument('-f' , '--final' , help='Final Entry' , dest="final")
pars.add_argument('--graphs', action="store_true" , dest="graphsf", help='Display with graphs flag', default=False)



args = pars.parse_args()
if len(sys.argv)==1:
    pars.print_help()
    sys.exit(1)

infile = args.infile
start = int(args.start)
final = int(args.final)
graphsf =args.graphsf

print "Infile: %s"%(infile)

rootf = TFile(infile)
mychain = rootf.Get("hits")
entries = mychain.GetEntriesFast()



# Tank and pmt-layout-03 is the infomration of x-y location of each tank/pmt in hawc
# necessary for buil the display
Tsurvey = np.loadtxt("tank-layout-03",usecols = (2 , 3) )
Psurvey = np.loadtxt("pmt-layout-03",usecols = (4 , 5) )


def FindEntry(tinit,tfin):
    tinit_F = int(tinit)
    tfin_F = int(tfin)
    chinit = 0
    chfin = 0 
    for i in range (0, entries):
        ientry = mychain.LoadTree( i )
        if ientry < 0:
            break
        
        # copy next entry into memory and verify
        nb = mychain.GetEntry( i )
        if nb <= 0:
            continue

        mychain.GetEntry(i)
        time =  int(mychain.CalibratedTime)
        print time,tinit_F,tfin_F
        
        if (time == tinit_F): 
          chinit = i-2
          print "CHINIT"
        if (time > tfin_F): 
          chfin = i + 2
          print "breaku"
          break
    #print chinit,chfin
    return chinit,chfin


def PlayDisplayWGraph( tinit, tfin ):

    pastT  = np.zeros(1200)
    pastCh = np.zeros(1200)

    C = "gray"

    steps = 10
    chinit,chfin = FindEntry(tinit,tfin)
    
    for jentry in np.arange(chinit+steps,chfin+steps,steps):
        fig ,ax = plt.subplots(num=None,  figsize=(12, 5), dpi=80, facecolor='w', edgecolor='k')
        plt.suptitle("HAWC Display")
        plt.subplot(121)
        plt.xlabel("Survey x [m]")
        plt.ylabel("Survey y [m]")
        plt.xlim(-90,160)
        plt.ylim(150,345)
        
 
        # get the next tree in the chain and verify
        ientry = mychain.LoadTree( jentry )
        if ientry < 0:
            break
        
        # copy next entry into memory and verify
        nb = mychain.GetEntry( jentry )
        if nb <= 0:
            continue
        

        ChargeT =  np.zeros(300)
        ChargeP =  np.zeros(1200)
        TimeP =  np.zeros(1200)
        ChannelP = np.zeros(1200)
        while ( mychain.GetEntry(i) and mychain.CalibratedTime<jentry):
            mychain.GetEntry(i)
            ichannel = mychain.Channel
            icharge  = mychain.CalibratedCharge
            itime = mychain.CalibratedTime
            ChargeT[int(floor((ichannel-1)/4))] = ChargeT[int(floor((ichannel-1)/4))] + icharge
            ChargeP[ichannel-1] = ChargeP[ichannel-1] + icharge
            TimeP[ichannel-1] = itime
            ChannelP[ichannel-1] = ichannel
            i = i+1
    
        #print ChargeT
        plt.scatter(Tsurvey[:,0]*0.01,Tsurvey[:,1]*0.01,s = 100, c = [ log(ich) for ich in ChargeT],cmap=plt.cm.jet , vmin=1, vmax = 10 , alpha=0.5)
        plt.scatter(Psurvey[:,0]*0.01,Psurvey[:,1]*0.01,s = 10, c = [ log(ich) for ich in ChargeP],cmap=plt.cm.jet , vmin=1, vmax = 10 , alpha=0.5)
        cbar = plt.colorbar()
        cbar.set_label('log(Charge) [PE]')

        plt.scatter(Tsurvey[:,0]*0.01,Tsurvey[:,1]*0.01,s = 100,color=C,alpha=0.2)
        plt.scatter(Psurvey[:,0]*0.01,Psurvey[:,1]*0.01,s = 10,color=C,alpha=0.2)

        plt.text(-85,330,"Time: %i - %i ns"%(jentry-steps,jentry),fontsize=10)

        plt.subplots_adjust( right=0.9)
        
        
        
        
        plt.subplot(222)

        n , bins , patches = P.hist([round(log(ich),2) for ich in ChargeP if ich != 0],30, histtype='stepfilled')

        P.setp(patches, 'facecolor', 'g', 'alpha', 0.35)
        plt.ylim(-0.01,10.01)
        plt.xlim(-1.01,10.01)
        plt.xlabel("log(Charge) [PE]")
        plt.ylabel("Number of events")

        plt.subplot(224)
        
        plt.scatter(pastCh,pastT,s = 5,color=C,alpha=0.3)
        plt.scatter(ChannelP,TimeP,s = 5,color=C,alpha=0.9)
        plt.axhline(y=jentry-steps, color='r', linestyle='-')
        plt.axhline(y=jentry, color='r', linestyle='-')
        ax = plt.gca()
        ax.ticklabel_format(useOffset=False)
        plt.ylim(jentry-(steps*2),jentry)
        plt.xlim(0.001,1200.001)
        plt.xlabel("PMT Channel")
        plt.ylabel("Time [ns]")
        
        plt.tight_layout()
        
        fig.subplots_adjust(top=0.88)
        
        
        plt.savefig("%i.png"%(jentry))
        print "Image %i.png generated"%(jentry)

        plt.close()

        pastCh = ChannelP
        pastT = TimeP



def PlayDisplay( tinit, tfin ):
    C = "gray
    steps = 10
    CHIN = []
    CHFIN = []
    TIN = []
    TFIN = []
    
    for it in np.arange(tinit,tfin,steps):
        chinit, chfin = FindEntry(it,it+steps)
        CHIN.append(chinit)
        CHFIN.append(chfin)
        TIN.append(it)
        TFIN.append(it+steps)
    
    for istep in range(0,len(CHIN)):
        fig, ax = plt.subplots(num=None,  figsize=(6, 5), dpi=80, facecolor='w', edgecolor='k')
        plt.title("HAWC Display")
        plt.xlabel("Survey x [m]")
        plt.ylabel("Survey y [m]")
        plt.xlim(-90,160)
        plt.ylim(150,345)
        
        for iCh in np.arange(CHIN[istep],CHFIN[istep],1):
          
            ientry = mychain.LoadTree( iCh )
            if ientry < 0:
                break
        
            # copy next entry into memory and verify
            nb = mychain.GetEntry( iCh )
            if nb <= 0:
                continue
            
            ChargeT =  np.zeros(300)
            ChargeP =  np.zeros(1200)
            TimeP =  np.zeros(1200)
            ChannelP = np.zeros(1200)
        
            mychain.GetEntry(iCh)
        
            ichannel = mychain.Channel
            icharge  = mychain.CalibratedCharge
            itime = mychain.CalibratedTime
            ChargeT[int(floor((ichannel-1)/4))] = ChargeT[int(floor((ichannel-1)/4))] + icharge
            ChargeP[ichannel-1] = ChargeP[ichannel-1] + icharge
            TimeP[ichannel-1] = itime
            ChannelP[ichannel-1] = ichannel
            i = i+1
    
            plt.scatter(Tsurvey[:,0]*0.01,Tsurvey[:,1]*0.01,s = 100, c = [ log(ich) for ich in ChargeT],cmap=plt.cm.jet , vmin=1, vmax = 10 , alpha=0.5)
            plt.scatter(Psurvey[:,0]*0.01,Psurvey[:,1]*0.01,s = 10, c = [ log(ich) for ich in ChargeP],cmap=plt.cm.jet , vmin=1, vmax = 10 , alpha=0.5)
            cbar = plt.colorbar()
            cbar.set_label('log(Charge) [PE]')
        
            plt.scatter(Tsurvey[:,0]*0.01,Tsurvey[:,1]*0.01,s = 100,color=C,alpha=0.2)
            plt.scatter(Psurvey[:,0]*0.01,Psurvey[:,1]*0.01,s = 10,color=C,alpha=0.2)

            plt.text(-85,330,"Time: %i - %i ns"%(TIN[istep],TFIN[istep]),fontsize=10)



        plt.savefig("%i.png"%(istep))
        print "Image %i.png generated"%(istep)
        plt.close()

def GenGif(start,final):
    print "Generating gif..."
    os.system('convert -delay 23 -loop 0 *.png %i-to-%i.gif'%(start,final))
    print "Deleting PNG images generated"
    os.system('rm *.png')

########     ----------------       MAIN         ----------------      ########

def main():
    
    if (graphsf == False):
        print "Finding entry"
        FindEntry(start , final )
        #PlayDisplay( start , final )
        #GenGif(start , final )

    else:
        PlayDisplayWGraph( start , final )
        GenGif(start , final )




if __name__ == "__main__":
    main()



#Test()



