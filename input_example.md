
### Raw Data

An example of RAW data can be found here:

`/data/archive/hawcroot/data/hawc/data/2017/01/run006211/*.dat`

or any other similar path.

As you can notice, the extension of this data is .dat and we need to convert it to ROOT. For this, we use the instructions listed under the [data format documentation](http://private.hawc-observatory.org/hawc.umd.edu/internal/db/2266_08.pdf): 

Use online-hit-dump to process raw data files into ROOT trees:

Example on UMD cluster

```
user@sequoia $ eval `$HAWCSOFT/setup.sh`  
user@sequoia $ export CONFIG_HAWC=$HAWCSOFT/config-hawc 
user@sequoia $ online-hit-dump -c $CONFIG_HAWC -o raw_run006211_00007.root
--input $HAWCROOT/data/hawc/data/2017/01/run002196/raw_run006211_00007.dat 
```

### Reco Extended

For this we can find some simulated showers in XCDF format here:
` /data/archive/hawcroot/sim/reco/aerie_svn_27754/systematics/best_mc/test_nobroadpulse_10pctlogchargesmearing_0.63qe_25kHzNoise_run5481_curvature0/gamma/succeeded/`

