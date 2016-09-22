# strata-cars

These are the files that interface to the Scalextric track as used at Strata London.  An overview of the initial, single car demo can be read [here:](http://basho.com/posts/technical/how-we-built-an-electric-racing-demo-showcasing-the-potential-of-riak-ts/).

*  race.py:  the script used to capture lap times and write them to the Riak TS instance
*  test6a.py:  the script used to test the limit switch set-up
*  test-connection.py: the script used to test connection to Riak TS from the RPi
*  create-table.py:  the script to create the table and set up the primary keys
*  Strata Lap Times.ipynb:  The jupyter notebook to show the leader board

In response to request to use the demo at the Erlang Users Conference in Stockholm, September 2016, added the file EUC-race.py which handles cars on both lanes.
