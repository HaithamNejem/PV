# PV    
PV System project   

@ The main file to run is called "figure.py":   
    - it includes all of the animated graphs to present the results of the simulation   
    
@ "system.py":  
    - includes the data structure of the PV system, and classes for each component with its' parameters and functions   
    
@ "simulation": 
    includes:   
    - Gui interface defenition  
    - functions which analyze the input files and save it in the system data structure  
    - the step function of the simulator which do the smart partition, called simulate  

@ the input files must have the same path names in order to run without errors  
@ there are provided data files regarded to 2019 data in order to try to simulate   
@ make sure the below libraries are installed before running:   
    import pandas   
    import pandas_datareader    
    import glob 
    import matplotlib   
    import PySimpleGUI  
    import datetime 
    import sys  

