from pybiosas import modelling
import json

solvent_sld=6.3e-6
background=0

scales = [(float(i)/1e9) for i in range(2,20,2)]
radii = range(30,200,20)
rim_thicks = range(2,20,2)
face_thicks = range(2,20,2)
lengths = range(10, 20, 5)
core_slds = [float(i/1e-6) for i in range(0,3,1)]
face_slds = [float(i/1e-6) for i in range(1,4,1)]
rim_slds = [float(i/1e-6) for i in range(0,3,1)]

args = {'xml' : True,
        'dataset' : 'data/100DPPC_D2O_20C.xml',
        'command' : 'fit'}
i=1
for model in ['coreShellBicelle']:
    for start_r in radii:
	    #for rim_thick in rim_thicks:
            #for scale in scales:
                try:
                    dict = {'coreShellBicelle' :
			      { 'radius' : {'value' : start_r,
                                            'paramname' : 'radius'},
                                'length' : {'value' : 20.,
                                            'paramname' : 'length'},
                                'solvent_sld' : {'value' : solvent_sld,
                                                 'paramname' : 'solvent_sld',
                                                 'fixed' : True},
                                'scale'  : {'value' : 1e-9,
                                   'paramname' : 'scale'},
                                'rim_thick' : {'value' : 10.,
                                            'paramname': 'rim_thick'},
                                'background' : {'value' : background,
                                                'paramname' : 'background'}}}
                    parameters=[]
                    for key in dict[model].iterkeys():
                        parameters.append(dict[model][key])

                    filename = str(i).zfill(4)
                    args['outpath'] = 'fits/' + filename
                    args['model'] = model
                    args['parameters'] = json.dumps(parameters)
                    print "Run:", i
                    modelrun = modelling.ModelWrapper(args)
                    modelrun.execute()
                    modelrun.write()
                    i+=1
                    
                except BufferError:
                    print 'failed fit'
		    print e
                    i+=1
                    pass
                
            
    
    
