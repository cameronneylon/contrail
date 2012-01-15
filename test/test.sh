# Fit a model to a file of test data given a dictionary of starting parameters on the command line.
# Parameters are REQUIRED to be a dictionary that matches a subset of the parameters of the relevant
# SansView model (i.e. that returned by model.params)
echo 'Testing a fit to a model with parameters passed on command line'
python ../sansmodel.py fit -m cylinder -d testdata.xml -p '[{"fixed": true, "value": 2.0, "paramname": "scale"}, {"value": 40.0, "paramname": "radius"}, {"fixed": false, "value": 200.0, "paramname": "length"}, {"fixed": true, "value": 6e-06, "paramname": "sldSolv"}]'

# Fit a model to a file of test data given a file of starting parameters
echo 'Testing a fit to a model with a parmeter file'
python ../sansmodel.py fit -m cylinder -d testdata.xml -p test.json 

# Output parameters that contains predicted data for given model given start parameters. If the 
# test directory is there from previous tests, remove it and any files it holds.
echo 'Testing calculation of a model with parameters from a file, writing to new directory'
if [ -d testdir ]; then rm -R testdir; fi
python ../sansmodel.py calc -m cylinder -p test.json -o 'testdir/testout.json'

# Return an object ###how? where?### that contains predicted data for given model given 
# start parameters on the command line
echo 'Testing calculation of a model from parameters on command line'
python ../sansmodel.py calc -m cylinder -p '[{"fixed": true, "value": 2.0, "paramname": "scale"}, {"value": 40.0, "paramname": "radius"}, {"fixed": false, "value": 200.0, "paramname": "length"}, {"fixed": true, "value": 6e-06, "paramname": "sldSolv"}]' 