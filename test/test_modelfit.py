import unittest
from pybiosas import modelling, models
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
        self.params_json = []
        self.params_file = 'test.json'
        self.data_file = 'testdata.xml'

    def organise_parameters(self, list):
        """Utility method to pull parameter names and values into a single dict"""

        returndict = {}
        for param in list:
            returndict[param['paramname']] = param['value']
        return returndict

    def testRegisteredModels(self):
        for model in iter(models.models):
            self.setUp()
            self.args = self.default_args
            self.args['model'] = model
            self.args['dataset'] = os.path.join(self.test_data_dir,
                                                models.models[model]['test_data'])
            for param in models.models[model]['test_params']:
                self.params_json.append(param)
            self.args['parameters'] = json.dumps(self.params_json)
            modelrun = modelling.ModelWrapper(self.args)
            modelrun.execute()

            paramdict = self.organise_parameters(modelrun.parameters)

            print "\nTesting:", model
            for expected_value in models.models[model]['exp_vals']:
                print (expected_value['paramname'] + ' ' +
                       'Found:' + str(paramdict[expected_value['paramname']]) + ' ' +
                       'Expected:' + str(expected_value['value']))

                self.assertAlmostEqual(expected_value['value'],
                                   paramdict[expected_value['paramname']],
                                   places = 1)
        
            # print "Covariance:", modelrun.cov_x
            # print "Fit info:", modelrun.fit_info
            
if __name__ == '__main__':
    unittest.main()
