# :mount_fuji:HAWC_display
HAWC display using reco extended or raw data

### Prerequisites:

- HAWC soft
- Imagemagic convert

### Usage:

This is divided in two steps, fist you have to *prepare* the data which should contain shower hits (charge, time, channel). 
The code for this is in under the directory FilePrep. 

This hits format constrain kid of data to use, for instance, only raw and reco (with extended format) can be *prepared*.

After this, the display-w-colors.py is used to make the GIF animation of the events.

For more details please check the memo in: 


A list of some input data as example can be found [here](input_example.md). I recommend to take a look first at the [data format docummentation](http://private.hawc-observatory.org/hawc.umd.edu/internal/db/2266_08.pdf). 



