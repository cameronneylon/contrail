import unittest
import cli

class TestParams(unittest.TestCase):

    def setUp(self):
        self.testFitSet = cli.SingleModelFitSet()
        self.testParam = {'paramname' : 'test-param',
                          'value'     : [0,1,2]}
        self.testParamSingle = {'paramname' : 'test-param-float',
                                'value'     : 1.}
        self.testParamList = [self.testParam, self.testParam, self.testParam]
        self.testdataset = 'test-datafile-name'
        self.testoutpath = 'test-outfile-name'
        self.testbagpath = 'test.bot'
        self.testprogpath = 'test-progpath'
        self.testmodel = 'test-model'
        self.testFitSet.params = self.testParamList
        self.testFitSet.set_arg('model', self.testmodel)
        self.testFitSet.set_arg('dataset',  self.testdataset)
        self.testFitSet.set_arg('outpath', self.testoutpath)
        self.testFitSet.set_arg('bagpath', self.testbagpath)
        self.testFitSet.set_arg('progpath', self.testprogpath)
        self.testFitSet.set_arg('xml', True)
        
        self.testargslist = [{'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 0, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000000', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 0, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000001', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 0, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000002', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 0, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000003', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 0, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000004', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 0, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000005', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 0, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000006', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 0, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000007', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 0, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000008', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 1, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000009', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 1, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000010', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 1, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000011', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 1, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000012', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 1, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000013', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 1, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000014', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 1, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000015', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 1, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000016', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 1, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000017', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 2, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000018', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 2, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000019', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 2, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000020', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 2, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000021', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 2, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000022', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 2, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000023', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 2, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}, {'value': 0, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000024', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 2, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000025', 'progpath': 'test-progpath', 'model': 'test-model'}, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 2, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000026', 'progpath': 'test-progpath', 'model': 'test-model'}]


    def test_build_args(self):
        test = self.testFitSet._build_args([0,[3,2,1]])
        self.assertEqual(test, {'xml': True, 'dataset': 'test-datafile-name', 'params': [{'value': 3, 'paramname': 'test-param'}, {'value': 2, 'paramname': 'test-param'}, {'value': 1, 'paramname': 'test-param'}], 'outpath': 'test-outfile-name/000000', 'progpath': 'test-progpath', 'model': 'test-model'})

    def test_enumerate(self):
        test = self.testFitSet.enumerate_tasks()
        self.assertEqual(test, self.testargslist)

    def test_write_bag(self):
        self.testFitSet.write_bag()

    def test_set_params(self):
        self.testFitSet.set_arg('model', 'sphere')
        self.testFitSet.params.append({'paramname' : 'radius', 'value' : 10.})
        
        self.testFitSet.set_param('radius', 5.)
        self.assertEqual(self.testFitSet.params[3]['value'], [5.])

        # Test setting parameter to a list
        self.testFitSet.set_param('radius', [0,1,2,3])
        self.assertEqual(self.testFitSet.params[3]['value'], [0,1,2,3])
        self.testFitSet.enumerate_tasks()

    def test_validate_fail(self):
        self.testFitSet.args['model'] = None
        self.assertRaises(IOError, self.testFitSet.validate_ready)

        

        

if __name__ == "__main__":
    unittest.main()
