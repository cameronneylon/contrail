# Text for the CLI App
#

app_header = """

CLI GUI App for PyBioSAS

"""

main_params = """Fit models or write out a bag of tasks (Fit/Write) [${command}]?... 
Model to fit [${model}]?... 
Location and filename of dataset [${dataset}]?    
Location to write output files [${outpath}]?
Location to write bag of tasks to [${bagpath}]?
Path to the modelling script [${progpath}]?   
Write out to XML [${xml}]?    """

param_entry = """${paramname}: Value for parameters, integer, float or list[${value}]... 
${paramname}: Fix the parameter within the fit (True/False) [${fixed}]... """
