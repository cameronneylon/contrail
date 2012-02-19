# SansModel: A python library for interacting with SansView 
# implementation of the NIST SANS models at command line level
#
# Public Domain Waiver:
# To the extent possible under law, Cameron Neylon has waived all 
# copyright and related or neighboring rights to lablogpost.py
# This work is published from United Kingdom.
#
# See http://creativecommons.org/publicdomain/zero/1.0/
#
# Dependencies: The application requires a range of modules from the
# Python 2.7 standard library including json, sys, argparse, datetime,
# os.path. Python is Copyright 2001-2012 Python Software Foundation
# and used here under the PSF Licence for Python 2.7.2
#
# In addition it requires non-standard library elements including:
#     * Sansview (and all its dependencies)
#     * Numpy and Scipy
#     * sas (http://github.com/cameronneylon/######
#

import argparse
import json
import sys
import datetime
import os
import os.path
import sas
import scipy.optimize
import numpy as np
import copy

from pycml.conventions.simple_comp_chem import *

class ApplicationRun():
    """Command line app for running refinements and model calculations

    """

    def __init__(self):
        """Initialisation method for the app class"""

        self.parser = None
        self.command = None
        self.model = None
        self.parameters = None
        self.dataset = None
        self.datain = None
        self.outpath = None

        self.__init_parser()
        self._raw_args = self.parser.parse_args()
        self.args = vars(self._raw_args)
        
    def __init_parser(self):

        self.parser = argparse.ArgumentParser()
        
        # TODO System for monitoring and registering models automatically
        # The available models are just hard coded at the moment
        self._registered_models = {'cylinder' : {
                                     'library_name':'CylinderModel',
                                     'model_name'  :'CylinderModel'},
                                   'sphere'   : {
                                     'library_name':'SphereModel',
                                     'model_name'  :'SphereModel'},
                                   'ellipse'  : {
                                     'library_name':'EllipsoidModel',
                                     'model_name'  :'EllipsoidModel'}
                                   }

        self.parser.add_argument('command', type = str,
                                 choices = ['fit', 'calc', 'calculate'],
                                 help = """Fit a model or calculate data given
                                 a set of parameters and a model""")

        self.parser.add_argument('-dataset', type = str,
                                     help = "The dataset to fit in SasXML format")

        models = []
        for model in self._registered_models.iterkeys():
            models.append(model)
        self.parser.add_argument('-model', type=str,
                                 choices = models,
                                 help = ("""The model to fitted or calculated.
                                 Available models are""" +
                                     str(models)))
        
        self.parser.add_argument('-parameters', type = str,
                                 help = """The paramaters, as either a json
                          file or a list of dictionaries with structure as defined
                          for the parinfo option of mpfit.""")

        self.parser.add_argument('-q_vals', '-q_values', type = str,
                                 help = """A list of q values for calculating
                                 intensities from a model. Provide as a string
                                 or file containing either the list of q values
                                 [1st, 2nd...last] or [1st, last, step] where
                                 step is optional""",
                                 default = "[0.0, 0.5, 0.0005]")

        self.parser.add_argument('-outpath', type = str,
                                 help = """A path to a directory for the output
                                 files. If it is desired to name the output file
                                 then terminate the path with that filename.
                                 Otherwise terminate the path with a '/'.
                                 Default is to place output files in
                                 same directory as the input parameter file. The
                                 default output filename is 'outfile.json'. If
                                 parameters are passed as a string on the
                                 command line then outpath defaults to the
                                 current working directory.""")

        self.parser.add_argument('-xml', action = 'store_true',
                                 help = """Write output to CML file.""")


    def execute(self):
        """Generate Model Wrapper and Execute."""

        self.model_instance = ModelWrapper(self.args)
        self.model_instance.execute()

    def write_out(self):
        self.model_instance.write()
        

class ModelWrapper:
    def __init__(self, args):

        self.outfile = 'sansmodel_output'
        self.args = args
        self.__distribute_args()
        self._registered_models = {'cylinder' : {
                                     'library_name':'CylinderModel',
                                     'model_name'  :'CylinderModel'},
                                   'sphere'   : {
                                     'library_name':'SphereModel',
                                     'model_name'  :'SphereModel'},
                                   'ellipse'  : {
                                     'library_name':'EllipsoidModel',
                                     'model_name'  :'EllipsoidModel'}
                                   }


    def __distribute_args(self):
        """Initialiser to distribute commandline args to internal variables"""

        for key in self.args.iterkeys():
            self.__dict__[key] = self.args[key]
        if not 'q_vals' in self.args:
            self.q_vals = None
            
    def execute(self):
        """Routine to execute the calculation or fit"""

        self.__model_func = self.__model_importer()
        self.__load_files_from_args() # load data from files

        if self.command == 'fit':
            self.fit()
            self.calculate()
            
        elif self.command == ('calc' or 'calculate'):
            self.calculate()

    def fit(self):
        """Run the fit process for the given model

        The parameters list is set up from those parameters that are not set as
        fixed in self.parameters. As these parameters have already been set in
        the model in the __load_args function they do not need to be set again here.        If this library is being used in scripts it might be appropriate to reset
        parameters for the model here just to be safe.
        """
        
        parameters=[]
        self.q_vals = self.datain.q
        for par in self.parameters:
            if not par.get('fixed', False):
                parameters.append(Parameter(self.__model_func, par['paramname'],
                                                               value=par['value']))
            
        def f(params):
            i=0
            for p in parameters:
                p.set(params[i])
                i+=1

            residuals=[]
            for j in range(len(self.datain.q)):
                residuals.append(self.datain.i[j] -
                             self.__model_func.run(self.datain.q[j]))

            return residuals

        def chi2(params):
            sum = 0
            res = f(params)
            for item in res:
                sum += item * item
            return sum

        p = [param() for param in parameters]
        out, self.cov_x, info, mesg, success = scipy.optimize.leastsq(f, p, 
                                                                 full_output=1)
        # Calculate chi squared
        if len(parameters) > 1:
            self.chisqr = chi2(out)
        elif len(parameters) == 1:
            self.chisqr = chi2([out])
        
        # Update the main parameter list at self.parameters with finalised values
        paramlist = []
        for p in self.parameters:
            paramlist.append(p['paramname'])

        for p in parameters:
            self.parameters[paramlist.index(p.get_name())]['value'] = p.get()
        
    def __fit_func(self, qvec, ivec, err=None):
        
        qi = zip(qvec, ivec)
        def f(p, fjac = None):
            for n in range(len(self.parameters)):
                self.__model_func.setParam(self.parameters[n]['paramname'], p[n])

            residuals = map(self.__eval_residuals, qi)
            return [0, residuals]

        return f

    def __eval_residuals(self, qi):
        q, i = qi
        return self.__model_func.run(q) - i

        #if err == None:
            #return 0, (self.__model_func.run(q) - i)
        #else:
        #    return 0, ((self.__model_func.run(q) - i)/err)
        


    def calculate(self):
        """Calculate values of i for given model and q values

        The function first sets up the list of q values, either from an existing
        imported list of values, or from a list of three values (start, stop,
        numpts) or two values (start, stop, assumed 100 points). The function then
        sets the appropriate parameters for the model and evaluates the model for
        each value in q, setting self.i_vals_out and self.q_vals_out in preparation
        for writing out the results.
        """
        
        q_vals_list = self.q_vals
        if len(q_vals_list) == 2:
            q_vals = np.arange(q_vals_list[0], q_vals_list[1], 100)

        elif len(q_vals_list) == 3:
            q_vals = np.arange(q_vals_list[0], q_vals_list[1],
                                    q_vals_list[2]).tolist()

        else:
            q_vals = q_vals_list
            
        # Calculate i for each value of q
        i_vals_out = map(self.__model_func.run, q_vals)

        self.i_vals_out = i_vals_out
        self.q_vals_out = q_vals
        return True

    def write(self):
        outdict = {'model'            : self.model,
                   'data_out'         : {'q'       : json.dumps(self.q_vals_out),
                                         'i'       : json.dumps(self.i_vals_out),
                                         'units'   : 'A^-1'},
                   'run'              : {'command' : self.command,
                                         'date'    : str(datetime.date.today()),
                                         'time'    : str(datetime.time())},
                   'parameters_in'    : self.parameters_in}

        if self.dataset:
            outdict['dataset'] = {'q_in' : json.dumps(self.datain.q),
                                  'i_in' : json.dumps(self.datain.i)}
        if self.command == 'fit':
            outdict['fit'] = {'chi^2'          : self.chisqr,
                              'cov_x'          : np.array_repr(self.cov_x),
                              'parameters_out' : self.parameters}

        if os.path.isfile(os.path.split(self.outpath)[1]):
            path, filename = os.path.split(self.outpath)
        else:
            path = os.path.dirname(self.outpath)
            filename = self.outfile
        
        if not os.path.exists(path):
            os.mkdir(path)

        if self.xml:
            self.write_cml(path, filename)

        else:
            f = open(os.path.join(path, filename), 'w')
            json.dump(outdict, f)
            f.close()

    def write_cml(self, path, filename):
        """Write a CML output file to disc."""

        doc = SimpleCompChem()
        doc.initialisation().setTitle('SANSModel Input Parameters')
        doc.finalisation().setTitle('SANSModel output')

        # Setup the input parameter list and populate it
        in_param_list=[]
        if self.command == 'fit':
            for parameter in self.parameters_in:
                 in_param_list.append({'value' : parameter['value'],
                                       'attrib': { 'dictRef' :
                                                   parameter['paramname'],
                                                   'units'   : 'ang or 1/cm'}})

        if self.dataset:
            in_param_list.append({'value' : self.datain.q,
                                  'attrib': { 'dictRef' : 'experimentalQData',
                                              'units'   : 'ang^-1'}})
            in_param_list.append({'value' : self.datain.i,
                                  'attrib': { 'dictRef' : 'experimentalIData',
                                              'units'   : 'cm^-1'}})
                                                    
        doc.initialisation().populate(in_param_list)
 
        # Setup the input parameter list and populate it
        out_param_list=[]
        for parameter in self.parameters:
            out_param_list.append({'value' : parameter['value'],
                                  'attrib': { 'dictRef' : parameter['paramname'],
                                              'units'   : 'ang or 1/cm'}})

        out_param_list.append({'value' : self.chisqr,
                               'attrib' : { 'dictRef' : 'chi2',
                                            'units'  : 'variance'}})
        out_param_list.append({'value' : self.q_vals_out,
                                  'attrib': { 'dictRef' : 'modelQData',
                                              'units'   : 'ang^-1'}})
        out_param_list.append({'value' : self.i_vals_out,
                                  'attrib': { 'dictRef' : 'modelIData',
                                              'units'   : 'cm^-1'}})

        doc.finalisation().populate(out_param_list)

        doc.job().setTitle('SANSModel: ' + self.command)
        doc.jobslist().setTitle('SANSModel: ' + self.command)

        filename = filename.rstrip('.xml') + '.xml'
        f = open(os.path.join(path, filename), 'w')
        doc.write(f).close()
        
        

    def __load_files_from_args(self):
        """Load files in based on command arguments

        """

        if self.dataset:
            try:
                self.datain = sas.loadsasxml(self.dataset)
                self.datain.err = None
            except OSError:
                errmsg = "Unable to load file: " + self.dataset
                raise InputError, errmsg
                return False

        # Load and parse the parameters
        if self.parameters:
            if os.path.isfile(self.parameters):
                if not self.outpath:
                    self.outpath = os.path.dirname(self.parameters)
                    if self.outpath == '': self.outpath = os.getcwd()
                f = open(self.parameters, 'r')
                self.parameters = json.load(f)
                f.close()
            else:
                if not self.outpath:
                    self.outpath = os.getcwd()
                self.parameters = json.loads(self.parameters)

            self.parameters_in = copy.deepcopy(self.parameters)
            
        # Check we have all the parameters for model including those left as defaults
        input_param_list = []
        for param in self.parameters:
            input_param_list.append(param['paramname'])
        for paramname in self.__model_func.details.keys():
            if (paramname not in input_param_list) and (
                    paramname not in self.__model_func.orientation_params):
                self.parameters.append({'paramname' : paramname,
                                        'value' :
                                       self.__model_func.getParam(paramname)
                                        })

        # Set the parameters for the model
        for parameter in self.parameters:
            self.__model_func.setParam(parameter['paramname'], parameter['value'])
        
        if (self.q_vals and os.path.isfile(self.q_vals)):
            try:
                f = open(self.q_vals, 'r')
                q_in = json.load(f)
            except OSError:
                errmsg = "Failed to load q_vals in: " + self.q_vals
                raise InputError, errmsg
                return False
            self.q_vals = q_in

        elif self.q_vals:
            q_in = json.loads(self.q_vals)
            self.q_vals = q_in

        else:
            pass

        
            
    def __model_importer(self):
        """Function for importing correct model library and returning model function

        Because we don't know either the module name or the model function name
        until runtime (as it is selected by the user) we need to look it up in
        the dictionary of registered model (self._registered_models) and then
        use __import__ so that we can pass the import command the string with
        the module location. Having identified the library we then want to pass
        the actual model calculation function back to the data model. The
        function is available from the module __dict__ and if we know the model
        we know the function name, so can create a pointer to this function and
        return it to the main app execution thread.
        """
        
        model_location = self._registered_models[self.model]['library_name']
        library_location = 'sans.models.' + model_location
        __import__(library_location)
        model_func = getattr(sys.modules[library_location],
                             self._registered_models[self.model]['model_name'])()
        return model_func

class Parameter:
    """
    Convenience class to handle model parameters for a fit
    """

    def __init__(self, model, name, value=None, fixed=False):
            self.model = model
            self.name = name
            self.fixedparam = fixed
            if not value == None:
                self.model.setParam(self.name, value)
           
    def set(self, value):
        """
            Set the value of the parameter
        """
        self.model.setParam(self.name, value)

    def get(self):
        """ 
            Return the current value of the parameter
        """
        return self.model.getParam(self.name)

    def get_name(self):
        return self.name

    def fixed(self):
        """
            Return the value of the "fixedparam" internal variable

            self.fixedparam is used to toggle whether this parameter should be fixed
            in the subsequent fit. If self.fixed==True then the parameter is not
            included in the list for the fit.
        """

        return self.fixedparam

    def set_fixed(self, fix=True):
        """
            Set the parameter as being fixed for fit.

            Default after being set is True.
        """
        self.fixedparam = fix

    def __call__(self):
        """ 
            Return the current value of the parameter
        """
        return self.model.getParam(self.name)
        
if __name__ == '__main__':
    run = ApplicationRun()
    run.parser.parse_args()
    run.execute()
    run.write_out()
