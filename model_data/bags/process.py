import xml.etree.ElementTree as ET
import os
import os.path

def compare_chi2(first_fit, second_fit):
    diff = first_fit[0]*1e10 - second_fit[0]*1e10
    if diff < 0: # Put chi2 as first parameter
        return -1
    elif diff == 0:
        return 0

    else:
        return 1

def approx_equal(x, y, tol=1e-18, rel=1e-7):
    if tol is rel is None:
        raise TypeError('cannot specify both absolute and relative errors are None')
    tests = []
    if tol is not None: tests.append(tol)
    if rel is not None: tests.append(rel*abs(x))
    assert tests
    return abs(x - y) <= max(tests)

directory = raw_input("Path to data?")

fit_list = []

params = ['chi2', 'length', 'radius', 'sldCyl', 'sldSolv', 'background', 'scale']

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

fit_list.sort(compare_chi2)
print params
for fit in fit_list:
    print fit

concatenated = []
count = 1
i=0
while i < len(fit_list)-1:
    if approx_equal(fit_list[i][0], fit_list[i+1][0], rel=1e-6):
        count+=1
    else:
        fit_list[i].append(count)
        concatenated.append(fit_list[i])
        count = 1
    i+=1

print params
for fit in concatenated:
    print fit
    



        
        
