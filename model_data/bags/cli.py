# A command line interface for interacting with pybiosas and Contrail
#
# Either fire off a set of fits, or generate a bag of tasks as required
# by Contrail and Conpaas

import models
REGISTERED_MODELS = models.models
import cli_app_template
import optparse
import itertools
import copy
import json
import os.path
from string import Template
import re

class CLIApp:
    """A class representing the command line interface"""

    def __init__(self):
        self.parser = None
        self.command = None
        self.model = None
        self.params = None
        self.dataset = None
        self.outpath = None
        self.bagpath = None
        self.script = None
        self.xml = None

        self.process_args()
        print self.command, self.model, self.dataset

        self._init_fitset()
        self._prep_regex()

    def process_args(self):
        self.__init_parser()
        (temp, args) = self.parser.parse_args()
        self.command = temp.command
        self.model = temp.model
        self.params = temp.params
        self.dataset = temp.dataset
        self.outpath = temp.outpath
        self.bagpath = temp.bagpath
        self.script = temp.script
        self.xml = temp.xml

    def __init_parser(self):
        """Command line parser for taking in optional arguments"""

        self.parser = optparse.OptionParser()
        
        self._registered_models = REGISTERED_MODELS

        self.parser.add_option('-c','--command', 
                                 dest='command', default=None,
                                 help = """Fit models or write out a bag of
                                 tasks given a parameter space to sweep""")

        self.parser.add_option('-s','--script', 
                                 dest='script', default=None,
                                 help = """Location of the python script to
                                 run the model fit on this system""")

        self.parser.add_option('-d', '--dataset', dest="dataset",
                                     default=None,
                                     help = "The dataset to use in SasXML format")

        models = [model for model in iter(self._registered_models)]
        self.parser.add_option('-m', '--model', type=str,
                                 dest = "model", default=None,
                                 help = ("""The model to be fitted.
                                 Available models are""" +
                                     str(models)))
        
        self.parser.add_option('-p', '--parameters', type = str,
                                 dest = 'params', default=None,
                                 help = """The parameters, as either a json
                          file or a list of dictionaries with structure as defined
                          for the parinfo option of mpfit. Parameter sweeps should
                          be defined as lists, 3-tuples (lowest, highest, step)""")

        self.parser.add_option('-o', '--outpath', type = str,
                                 dest="outpath", default=None,
                                 help = """A path to a directory for the output
                                 files. If it is desired to name the output file
                                 then terminate the path with that filename.
                                 Otherwise terminate the path with a '/'.
                                 Default is to place output files in
                                 same directory as the input data file.""")

        self.parser.add_option('-b', '--bagpath', type = str,
                                 dest="bagpath", default=None,
                                 help = """Path for writing out the bag of tasks.
                                 This is expected to be set by a calling shell
                                 script in most cases as user will not be aware
                                 of where bag should go on the client VMs""")


        self.parser.add_option('-x', '--xml', action = 'store_true',
                                 dest="xml", default=None,
                                 help = """Write output to CML file.""")


    def _init_fitset(self):
        """Initialise a FitSet instance as the document

        The CLI App is a Model-View application where the FitSet acts as
        document(model) and the App class is the view.
        """

        print self.command, self.model, self.dataset
        self.fitset = SingleModelFitSet(self.params, self.command,
                                        self.model, self.dataset,
                                        self.outpath, self.bagpath,
                                        self.script,self.xml)
        print self.fitset.args

    def main(self):
        """Main loop for the CLI App

        The loop runs over a template document that is stored separately.
        For each cycle a dictionary is created that inserts current values
        into the line to present as query to user as default values to
        re-use.
        """

        # Print the "splash screen"
        print cli_app_template.app_header

        rerun = True
        # The main program loop
        # Collect the main parameters that will stay fixed
        for line in cli_app_template.main_params.splitlines():
            argname, value, app_text = self._app_line_process(line)
            if not value:
                input = raw_input(app_text)
                self.fitset.set_arg(argname, self._process_input(argname,input))
            else:
                pass

        # Collect the starting fit parameters for this set
        param_template = Template(cli_app_template.param_entry)
        if self.fitset.params == None:
            self.fitset._init_params()


        
        while rerun:           
            for param in self.fitset.params:
                print '\n'
                app_text = param_template.substitute(param)
                raw_value = raw_input(app_text.splitlines()[0])
                raw_fixed = raw_input(app_text.splitlines()[1])

                value, fixed = self._process_param(param['paramname'],
                                                   raw_value, raw_fixed)

                self.fitset.set_param(param['paramname'], value, fixed)
                
            self.fitset.write_bag()
            cont = raw_input('(Q)uit or (M)odify parameters?')
            if cont in ['Q', 'q', 'Quit', 'quit']:
                rerun = False
            
        exit()

    def _app_line_process(self, line):
        """Take a line from the CLI template and populate it

        Accepts a string sourced from cli_app_template.main_params and
        searches for ${name} where name corresponds to an argument
        name in the TestFit object. The text is processed to send
        to the CLI and name, current value, and modified text are
        returned.
        """
        
        processed = self.rg.search(line)
        paramname = processed.group(2)

        value = self.fitset.get_arg(paramname)
        app_text = re.sub(self.rg, str(value), line)

        return paramname, value, app_text


    def _process_input(self, argname, input):
        """Convenience function for processing inputs to correct form"""

        # If user hits return keep the existing value
        if input == '':
            return self.fitset.get_arg(argname)

        if input in ['True', 'true', 'T', 't']:
            if argname == 'xml':
                return True
            else:
                return input

        if input in ['False', 'false', 'F', 'f']:
            if argname == 'xml':
                return False
            else:
                return input

        if argname == 'command':
            if input in ['F', 'f', 'Fit', 'fit']:
                return 'fit'

            elif input in ['W', 'w', 'write', 'Write']:
                return 'write'

            else:
                raise ValueError

        return input

    def _process_param(self, paramname, raw_value, raw_fixed):
        """Convenience function for processing parameters to right form

        The FitSet Class takes floats, ints or lists of floats along
        as parameters. The CLI input will come in as strings which need
        to be processed.
        """

        if raw_value == '':
            value = self.fitset.get_param(paramname)

        elif ',' in raw_value:
            value = self._process_param_list(raw_value)

        else:
            value = float(raw_value)

        if raw_fixed == '':
            fixed = self.fitset.get_param_fixed(paramname)

        elif raw_fixed in ['False', 'false', 'F', 'f']:
            fixed = False

        elif raw_fixed in ['True', 'true', 'T', 't']:
            fixed = True

        else:
            raise ValueError

        return value, fixed

    def _process_param_list(self, raw_value):
        list = raw_value.split(',')
        value = []

        # If all vals are numbers this works
        try:
            for val in list:
                value.append(float(val))

        # If val contains other character treat as first, last, interval
        except ValueError:
            if len(list) == 3:
                first = float(list[0])
                last = float(list[1])
                interval = float(self.float_rg.search(list[2]).group())

                value = [first]
                while first < last:
                    first = first + interval
                    value.append(first)

            else:
                raise ValueError

        return value

    def _prep_regex(self):
        """Set up a regex for processing of CLI text lines"""

        re1='(\\$\\{)'	# Any Single Character 1
        re2='((?:[a-z][a-z]+))'	# Word 1
        re3='(\\})'	# Any Single Character 3

        self.rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)

        re5='([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)'
                    
        self.float_rg = re.compile(re5, re.IGNORECASE|re.DOTALL)
        
class SingleModelFitSet:
    """A class representing a set of fits using a single model

    The core of the class is a data model representing a set of fit
    tasks to be carried out using a single dataset and a single
    model. The data model is populated against the set of parameters
    that can be obtained from pybiosas.models.models[model]['exp_vals']

    For each variable it is possible for the fit set to have a single
    starting value, or a list (iterator) of values. For each individual
    fit the starting values can be fixed or not.

    The data model consists of a set of internal variarbles that
    correspond to the requirements for the arguments of a
    pybiosas.ModelWrapper except that the parameter values can be
    set to lists or iterators.

      'params' : [{'paramname' : parameter name,
                   'value'     : int, float, list or iterator,
                   'fixed'     : True/False or missing (False)},
                  {'paramname' : second parameter....}]
    }

    The class on calling of the enumerate function will generate a list
    of dictionaries in the form of arguments as required by the
    pybiosas.ModelWrapper class as follows:

    { 'model'  : model name,
      'params' : dictionary of the specified starting parameters as above
      'xml'    : true or false,
      'dataset': path to the dataset to be fitted,
      'outpath': output path and filename}
      
    """

    def __init__(self, params=[], command = None, model=None,
                 dataset=None, outpath = None, bagpath = None,
                 progpath=None, xml=True):

        self.args = {}
        self._registered_models = REGISTERED_MODELS
        self.params = params
        if command:
            self.set_arg('command', command)
        if model:
            self.set_arg('model', model)
        if dataset:
            self.set_arg('dataset', dataset)
        if outpath:
            self.set_arg('outpath', outpath)
        if bagpath:
            self.set_arg('bagpath', bagpath)
        if progpath:
            self.set_arg('progpath', progpath)
        if xml:
            self.set_arg('xml', xml)

    def set_arg(self, arg, value):
        """Set any of the main fit parameters

        This is not intended to be used to set params but for all other
        fitset arguments.

        :param :arg The name of the argument to be set
        :type :arg str
        :param :value The value the argument is to be set to
        :type :value str except for the argument 'xml' which is bool
        """

        assert (type(value) == str or type(value) == bool)
        assert arg in ['command', 'model', 'dataset', 'outpath', 'bagpath', 'progpath', 'xml']

        self.args[arg] = value

    def get_arg(self, arg):
        """Return the value of a given argument"""

        return self.args.get(arg)

    def set_param(self, paramname, value, fixed=None):
        """Set any of the model fit parameters

        Will accept either a single int, float or a list.

        :param :paramname The name of the parameter to be set
        :type :paramname str
        :param :value The value the parameter is to be set to
        :type :value int, float, str
        """

        if self.params == []:
            self._init_params()
 
        assert type(value) in [int, float, list]
        assert ((type(fixed) == bool) or (fixed == None))
        if type(value) == int or type(value) == float:
            value = [value]
        #try:
        #    assert (param_name in iter(
        #    pybiosas.models.models[self.get_arg('model')]['exp_values']))
        #except KeyError:
        #    raise IOError, ('No such registered model:' + self.get_arg('model'))

        i = self._get_param_list_index(paramname)
        self.params[i]['value'] = value
        if fixed:
            self.params[i]['fixed'] = fixed

    def get_param(self, paramname):
        """Get the value of a specific parameter"""

        i = self._get_param_list_index(paramname)
        return self.params[i]['value']

    def get_param_fixed(self, paramname):
        """Return whether a given fit parameter is fixed or not"""

        i = self._get_param_list_index(paramname)
        return self.params[i]['fixed']

    def _get_param_list_index(self, paramname):
        """Get the index for the paramname parameter in self.params list"""
        
        model_param_names = [param['paramname'] for param in self.params]
        i = model_param_names.index(paramname)
        return i
        

    def _init_params(self):
        """Initialise the parameters list from registered models"""

        self.params = []
        for param in self._registered_models[self.get_arg('model')]['exp_vals']:
            self.params.append({'paramname' : param['paramname'],
                                'value'     : None,
                                'fixed'     : False})
            
        
        
    def enumerate_tasks(self):
        """Enumerate the full set of parameter combinations

        Each parameter has been provided with a range or list of
        values. We need to obtain the set of values for each
        parameter from params['value'] and then create the
        iterator of all possible values using itertools.product

        We then need to reconstruct the set of dictionaries for
        each of the required set of starting parameters. This is
        fine because we started with a list and the ordering in
        each enumerated set of values will be consistent.
        """

        param_list = []
        for i, value in enumerate(self.params):
            param_list.append(self.params[i]['value'])

        enumerated_parameters = itertools.product(*param_list)

        buildlist = []
        for i, argset in enumerate(enumerated_parameters):
            buildlist.append([i, argset])
        args_list = map(self._build_args, buildlist)

        return args_list

    def _build_args(self, arglist):
        """Build the dictionary object args for a single fit

        The method builds a dictionary from the common values
        that have already been obtained. Then for each parameter
        the fitset parameter is copied across, including the
        'fixed' key and value and the value for the 'value' key
        is then over written.
        """

        file = '%06d' % arglist[0]
        outpath = os.path.join(self.get_arg('outpath'), file)

        args = {'model'   : self.get_arg('model'),
                'dataset' : self.get_arg('dataset'),
                'outpath' : outpath,
                'progpath': self.get_arg('progpath'),
                'xml'     : self.get_arg('xml'),
                'params'  : []}

        param_list = arglist[1]
        for i,value in enumerate(param_list):
            args['params'].append(copy.copy(self.params[i]))
            args['params'][i]['value'] = value

        return args


    def write_bag(self):
        """Write out a bag of tasks with all parameters set"""
        
        t = Template("""/usr/bin/python ${progpath} fit -m ${model} -o ${outpath} -d ${dataset} -x -p '${params}'\n""")
        
        self.validate_ready()
        tasks = self.enumerate_tasks()
        f = open(self.get_arg('bagpath'), 'w')
        for task in tasks:
            task['params'] = json.dumps(task['params'])
            command = t.substitute(task)
            f.write(command)

        f.close()

    def validate_ready(self):
        try:
            assert type(self.get_arg('model')) == str
            assert type(self.get_arg('dataset')) == str
            assert type(self.params) == list and len(self.params)>0

        except AssertionError:
            raise IOError, "Fit set not ready to run"

        

if __name__ == "__main__":
    app = CLIApp()
    app.main()
