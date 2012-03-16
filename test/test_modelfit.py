import unittest
from pybiosas import modelling
import json
import os.path

class TestSimpleFits(unittest.TestCase):

    def setUp(self):
        self.default_args = {'xml' : True,
                     'outpath' : 'test',
                     'command' : 'fit'}
        if os.path.isfile('testdata.xml'):
            self.test_data_dir = ''
        elif os.path.isfile('test/testdata.xml'):
            self.test_data_dir = 'test'
        else:
            print "Can't find data for test, run tests from root of package or test/"
            raise IOError
        self.params_json = [
            {"fixed" : True, "value": 0.01, "paramname": "scale"},
            {"fixed" : True, "value": 1e-05, "paramname": "sldSolv"}
            ]
        self.params_file = 'test.json'
        self.data_file = 'testdata.xml'

    def organise_parameters(self, list):
        """Utility method to pull parameter names and values into a single dict"""

        returndict = {}
        for param in list:
            returndict[param['paramname']] = param['value']
        return returndict


    def root_model_test(self, model, params, expected_values, test_data):
        self.args = self.default_args
        self.args['model'] = model
        self.args['dataset'] = os.path.join(self.test_data_dir, test_data)
        for param in params:
            self.params_json.append(param)
        self.args['parameters'] = json.dumps(self.params_json)
        modelrun = modelling.ModelWrapper(self.args)
        modelrun.execute()
        paramdict = self.organise_parameters(modelrun.parameters)

        print "\nTesting:", model
        #for key in iter(paramdict):


        for expected_value in expected_values:
            print (expected_value['paramname'] + ' ' +
                       'Found:' + str(paramdict[expected_value['paramname']]) + ' ' +
                       'Expected:' + str(expected_value['value']))

            self.assertAlmostEqual(expected_value['value'],
                                   paramdict[expected_value['paramname']],
                                   places = 2)
            
        return paramdict
        

    def testSphereFit(self):
        self.model = 'sphere'
        self.test_data = 'test_data_sphere.xml'
        self.params= [{"value": 60.0,
                       "paramname": "radius"}]

        self.expected_values = [{'paramname' : 'scale',
                                 'value'     : 0.01},
                                {'paramname' : 'radius',
                                 'value'     : 40.0},
                                {'paramname' : 'sldSph',
                                 'value'     : 2e-6},
                                {'paramname' : 'sldSolv',
                                 'value'     : 1e-5},
                                {'paramname' : 'background',
                                 'value'     : 0.1}]
        self.root_model_test(self.model, self.params, self.expected_values, self.test_data)
        
    def testEllipseFit(self):
        self.model = 'ellipse'
        self.test_data = 'test_data_ellipse.xml'
        self.params= [{"value" : 40,
                       "paramname" : "radius_a"},
                      {"value" : 100,
                       "paramname" : "radius_b"}]
                       

        self.expected_values = [{'paramname' : 'scale',
                                 'value'     : 0.01},
                                {'paramname' : 'radius_a',
                                 'value'     : 30.0},
                                {'paramname' : 'radius_b',
                                 'value'     : 200.0},
                                {'paramname' : 'sldEll',
                                 'value'     : 2e-6},
                                {'paramname' : 'sldSolv',
                                 'value'     : 1e-5},
                                {'paramname' : 'background',
                                 'value'     : 0.001}]
        self.root_model_test(self.model, self.params, self.expected_values, self.test_data)

    def testCylinderFit(self):
        self.model = 'cylinder'
        self.test_data = 'test_data_cylinder.xml'
        self.params= [{"value" : 20,
                       "paramname" : "radius"},
                      {"value" : 50,
                       "paramname" : "length"}]
                       

        self.expected_values = [{'paramname' : 'scale',
                                 'value'     : 0.01},
                                {'paramname' : 'radius',
                                 'value'     : 30.0},
                                {'paramname' : 'length',
                                 'value'     : 100.0},
                                {'paramname' : 'sldCyl',
                                 'value'     : 2e-6},
                                {'paramname' : 'sldSolv',
                                 'value'     : 1e-5},
                                {'paramname' : 'background',
                                 'value'     : 0.2}]
        self.root_model_test(self.model, self.params, self.expected_values, self.test_data)

if __name__ == '__main__':
    unittest.main()
