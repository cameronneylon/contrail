import xml.etree.ElementTree as ET
import os
import os.path

directory = raw_input("Path to data?")

fit_list = []

params = ['chi2', 'length', 'radius', 'sldCyl', 'sldSolv', 'background']

for file in os.listdir(directory):
    fit = []
    parsed = ET.parse(os.path.join(directory, file))
    modules = parsed.getroot().find('module').find('module').findall('module')
    properties = modules[1].find('propertyList').findall('property')
    # properties = parsed.getroot().iterfind('property')

    prop_indices = []
    for property in properties:
        prop_indices.append(property.get('dictRef'))

    for param in params:
        i = prop_indices.index(param)
        prop = properties[i]
        
        param_value = prop[0].text
        param_value = float(param_value)
        fit.append(param_value)

    fit_list.append(fit)

def compare_chi2(first_fit, second_fit):
    diff = first_fit[0]*1e10 - second_fit[0]*1e10
    if diff < 0: # Put chi2 as first parameter
        return -1
    elif diff == 0:
        return 0

    else:
        return 1
    
        
        
fit_list.sort(compare_chi2)
print params
for fit in fit_list:
    print fit
