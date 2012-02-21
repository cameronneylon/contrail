import unittest
from pybiosas import modelling
import json
import os.path

class TestSimpleFits(unittest.TestCase):

    def setUp(self):
        self.default_args = {'xml' : True,
                     'dataset' : 'test/testdata.xml',
                     'outpath' : 'test',
                     'command' : 'fit'}
        if os.path.isfile('testdata.xml'):
            self.default_args['dataset'] = 'testdata.xml'
        elif os.path.isfile('test/testdata.xml'):
            self.default_args['dataset'] = 'test/testdata.xml'
        else:
            print "Can't find data for test, run tests from root of package or test/"
            raise IOError
        self.params_json = [
            {"fixed": True, "value": 2.0, "paramname": "scale"},
            {"fixed": True, "value": 6e-06, "paramname": "sldSolv"}
            ]
        self.params_file = 'test.json'
        self.data_file = 'testdata.xml'

    def organise_parameters(self, list):
        """Utility method to pull parameter names and values into a single dict"""

        returndict = {}
        for param in list:
            returndict[param['paramname']] = param['value']
        return returndict


    def root_model_test(self, model, params, expected_values):
        self.args = self.default_args
        self.args['model'] = model
        for param in params:
            self.params_json.append(param)
        self.args['parameters'] = json.dumps(self.params_json)
        modelrun = modelling.ModelWrapper(self.args)
        modelrun.execute()
        paramdict = self.organise_parameters(modelrun.parameters)

        for expected_value in expected_values:
            self.assertAlmostEqual(expected_value['value'],
                                   paramdict[expected_value['paramname']],
                                   places = 3)

        return paramdict
        

    def testSphereFit(self):
        self.model = 'sphere'
        self.params= [{"value": 40.0,
                       "paramname": "radius"}]

        self.expected_values = [{'paramname' : 'radius',
                                 'value'     : 52.93727},
                                {'paramname' : 'sldSph',
                                 'value'     : 5.840343e-6}]
        self.root_model_test(self.model, self.params, self.expected_values)
        
    def testEllipseFit(self):
        self.model = 'ellipse'
        self.params= [{"value" : 40,
                       "paramname" : "radius_a"},
                      {"value" : 60,
                       "paramname" : "radius_b"}]
                       

        self.expected_values = [{'paramname' : 'radius_a',
                                 'value'     : 0.5870366},
                                {'paramname' : 'radius_b',
                                 'value'     : 77.94983},
                                {'paramname' : 'sldEll',
                                 'value'     : 4.896173e-6}]
        self.root_model_test(self.model, self.params, self.expected_values)

    def testCylinderFit(self):
        self.model = 'cylinder'
        self.params= [{"value" : 40,
                       "paramname" : "radius"},
                      {"value" : 60,
                       "paramname" : "length"}]
                       

        self.expected_values = [{'paramname' : 'radius',
                                 'value'     : 69.390798},
                                {'paramname' : 'length',
                                 'value'     : 5.937745},
                                {'paramname' : 'sldCyl',
                                 'value'     : 4.896173e-6}]
        self.root_model_test(self.model, self.params, self.expected_values)

if __name__ == '__main__':
    unittest.main()
