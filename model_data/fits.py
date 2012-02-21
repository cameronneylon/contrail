from pybiosas import modelling
import json

sldSolv=6.3e-6
sldMod=3.14e-6
background=0

scales = [(float(i)/1e9) for i in range(2,20,2)]

args = {'xml' : True,
        'dataset' : 'pin_a.xml',
        'command' : 'fit'}
i=1
for model in ['cylinder', 'ellipse']:
    for start_r in range(10,100,10):
        for length in range(40,400,40):
            for scale in scales:
                try:
                    dict = {'cylinder' : { 'radius' : {'value' : start_r,
                                   'paramname' : 'radius'},
                       'length' : {'value' : length,
                                   'paramname' : 'length'},
                       'sldCyl' : {'value' : sldMod,
                                   'paramname' : 'sldCyl',
                                   'fixed' : True},
                       'scale'  : {'value' : scale,
                                   'paramname' : 'scale'},
                       'sldSov' : {'value' : sldSolv,
                                   'paramname': 'sldSolv',
                                   'fixed' : True},
                       'background' : {'value' : background,
                                       'paramname' : 'background'}},
        'ellipse' : {  'radius_a': {'value' : start_r,
                                   'paramname' : 'radius_a'},
                       'radius_b': {'value' : length/2,
                                   'paramname' : 'radius_b'},
                       'sldEll'  : {'value' : sldMod,
                                   'paramname' : 'sldEll',
                                   'fixed' : True},
                       'sldSolv' : {'value' : sldSolv,
                                   'paramname': 'sldSolv',
                                   'fixed' : True},
                       'background': {'value' : background,
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
                    
                except:
                    print 'failed fit'
                    i+=1
                    pass
                
            
    
    
