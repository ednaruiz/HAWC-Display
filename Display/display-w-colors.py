#======================================================================/
# Author: Edna L. Ruiz Velasco    Hermes Leon Vargas                   /
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
        #print time,tinit_F,tfin_F
        
        if (time <= tinit_F): 
          chinit = i
          #print "CHINIT"
        if (time >= tfin_F): 
          chfin = i 
        #print "breaku"
          break
    #print chinit,chfin
    return chinit,chfin


def PlayDisplayWGraph( tinit, tfin ):
    
    C = "gray"
    steps = 10

    chinit, chfin = FindEntry(tinit,tfin)
    
    ChargeP =  np.zeros(1200)
    TimeP = np.zeros(1200)
    
    j = 1.
    tstep = tinit + j*steps
    cont = 0
    
    CHARGE = []
    TIME = []
    for iCh in np.arange(chinit,chfin+2,1):
      ientry = mychain.LoadTree( iCh )
      if ientry < 0:
        break
        
      # copy next entry into memory and verify
      nb = mychain.GetEntry( iCh )
      if nb <= 0:
        continue
            
      
      mychain.GetEntry(iCh)
        
      ichannel = mychain.Channel
      icharge  = mychain.CalibratedCharge
      itime = mychain.CalibratedTime
      
      if (int(itime)<tstep):
        ChargeP[ichannel]=icharge
        TimeP[ichannel]=itime
        print itime
        #print itime,tstep,j
      else:
        print [i for i in TimeP if i !=0]
        CHARGE.append(ChargeP)
        TIME.append(TimeP)
        j=j+1
        tstep = tinit + j*steps
        iCh = iCh - 1
        cont = 0
        ChargeP =  np.zeros(1200)
        TimeP = np.zeros(1200)
        
    print len(TIME)
    print len(CHARGE)
    for iEvent in range (0,len(CHARGE)):
      ChargeT = np.zeros(300)
      
      for i in range(0,1200):
        ChargeT[int(floor((i)/4))] = ChargeT[int(floor((i)/4))] + CHARGE[iEvent][i]

      fig, ax = plt.subplots(num=None,  figsize=(12, 5), dpi=80, facecolor='w', edgecolor='k')
      plt.suptitle("HAWC Display")
      plt.subplot(121)
      plt.title("HAWC Display")
      plt.xlabel("Survey x [m]")
      plt.ylabel("Survey y [m]")
      plt.xlim(-90,160)
      plt.ylim(150,345)
      
      t0 = tinit + iEvent*steps
      tf = tinit + (iEvent+1)*steps
      
      plt.scatter(Tsurvey[:,0]*0.01,Tsurvey[:,1]*0.01,s = 100,color=C,alpha=0.2)
      plt.scatter(Psurvey[:,0]*0.01,Psurvey[:,1]*0.01,s = 10,color=C,alpha=0.2)
      plt.scatter(Tsurvey[:,0]*0.01,Tsurvey[:,1]*0.01,s = 100, c = [ log(ich) for ich in ChargeT ],cmap=plt.cm.jet , vmin=1, vmax = 10 , alpha=0.5)
      plt.scatter(Psurvey[:,0]*0.01,Psurvey[:,1]*0.01,s = 10, c = [ log(ich) for ich in CHARGE[iEvent] ],cmap=plt.cm.jet , vmin=1, vmax = 10 , alpha=0.5)
      cbar = plt.colorbar()
      cbar.set_label('log(Charge) [PE]')
      plt.text(-85,330,"Time: %i - %i ns"%(t0,tf),fontsize=10)

      plt.subplots_adjust( right=0.9)
      
      plt.subplot(222)

      n , bins , patches = P.hist([round(log(ich),2) for ich in CHARGE[iEvent] if ich != 0],30, histtype='stepfilled')

      P.setp(patches, 'facecolor', 'g', 'alpha', 0.35)
      plt.ylim(-0.01,10.01)
      plt.xlim(-1.01,10.01)
      plt.xlabel("log(Charge) [PE]")
      plt.ylabel("Number of events")

      plt.subplot(224)
      print sum(TIME[iEvent])

      plt.scatter(TIME[iEvent],TIME[iEvent],s = 5,color=C,alpha=0.3)
      #plt.scatter(TIME[iEvent+1],TIME[iEvent+1],s = 5,color=C,alpha=0.9)      
      #plt.scatter(TIME[iEvent+2],TIME[iEvent+2],s = 5,color=C,alpha=0.3)
      
      plt.axhline(y=t0, color='r', linestyle='-')
      plt.axhline(y=tf, color='r', linestyle='-')
      ax = plt.gca()
      ax.ticklabel_format(useOffset=False)
      plt.ylim(t0-(steps),tf+(steps))
      plt.xlim(0.001,1200.001)
      plt.xlabel("PMT Channel")
      plt.ylabel("Time [ns]")
      plt.tight_layout()
        
      fig.subplots_adjust(top=0.88)

      plt.savefig("%i.png"%(iEvent))
      print "Image %i.png generated"%(iEvent)
      plt.close()
      

def PlayDisplay( tinit, tfin ):
    C = "gray"
    steps = 10

    chinit, chfin = FindEntry(tinit,tfin)
    
    ChargeP =  np.zeros(1200)
    
    j = 1.
    tstep = tinit + j*steps
    cont = 0
    
    CHARGE = []
    for iCh in np.arange(chinit,chfin+2,1):
      ientry = mychain.LoadTree( iCh )
      if ientry < 0:
        break
        
      # copy next entry into memory and verify
      nb = mychain.GetEntry( iCh )
      if nb <= 0:
        continue
            
      
      mychain.GetEntry(iCh)
        
      ichannel = mychain.Channel
      icharge  = mychain.CalibratedCharge
      itime = int(mychain.CalibratedTime)
      
      if (itime<tstep):
        ChargeP[ichannel]=icharge
        #print itime,tstep,j
      else:
        CHARGE.append(ChargeP)
        j=j+1
        tstep = tinit + j*steps
        iCh = iCh - 1
        cont = 0
        ChargeP =  np.zeros(1200)
    
    for iEvent in range (0,len(CHARGE)):
      ChargeT = np.zeros(300)
      
      for i in range(0,1200):
        ChargeT[int(floor((i)/4))] = ChargeT[int(floor((i)/4))] + CHARGE[iEvent][i]

      fig, ax = plt.subplots(num=None,  figsize=(6, 5), dpi=80, facecolor='w', edgecolor='k')
      plt.title("HAWC Display")
      plt.xlabel("Survey x [m]")
      plt.ylabel("Survey y [m]")
      plt.xlim(-90,160)
      plt.ylim(150,345)
      
      t0 = tinit + iEvent*steps
      tf = tinit + (iEvent+1)*steps
      
      plt.scatter(Tsurvey[:,0]*0.01,Tsurvey[:,1]*0.01,s = 100,color=C,alpha=0.2)
      plt.scatter(Psurvey[:,0]*0.01,Psurvey[:,1]*0.01,s = 10,color=C,alpha=0.2)
      plt.scatter(Tsurvey[:,0]*0.01,Tsurvey[:,1]*0.01,s = 100, c = [ log(ich) for ich in ChargeT ],cmap=plt.cm.jet , vmin=1, vmax = 10 , alpha=0.5)
      plt.scatter(Psurvey[:,0]*0.01,Psurvey[:,1]*0.01,s = 10, c = [ log(ich) for ich in CHARGE[iEvent] ],cmap=plt.cm.jet , vmin=1, vmax = 10 , alpha=0.5)
      cbar = plt.colorbar()
      cbar.set_label('log(Charge) [PE]')
      plt.text(-85,330,"Time: %i - %i ns"%(t0,tf),fontsize=10)



      plt.savefig("%i.png"%(iEvent))
      print "Image %i.png generated"%(iEvent)
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
        PlayDisplay( start , final )
        GenGif(start , final )

    else:
        PlayDisplayWGraph( start , final )
        GenGif(start , final )




if __name__ == "__main__":
    main()



#Test()



