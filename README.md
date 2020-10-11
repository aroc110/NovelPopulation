# NovelPopulation

Supplementary Files for "Novel Population Genetics in Ciliates due to Nuclear Dimorphism and Life Cycle"

File list:
Simulation_Results_Fixation_Probability :: Excel file containing fixation probabilities from simulations
Simulation_Results_Segregation_Time     :: Excel file containing segregation times from simulations
finPop.py                               :: Python file containing code for Selection-drift simulations
balFinPop.py                            :: Python file containing code for Selection-Mutation-Drift simulations used in study
SupplementaryFiguresAndTables           :: PDF containing supplementary figures and tables

Instructions for finPop.py and balFinPop.py:
Requires Python 2.7 or greater to run. May be incompatible with Python 3.  

Required packages: random, pp

Using parrellel python (pp), programs run on multiple cores, making use of all available computational power.  Due to this intensity, it is not recommended to try and run other programs on the same computer.

To run with IDLE or other IDEs, open the file and hit run.

To run via the command line, move to the containing directory, and type the command: python finPop.py or python balFinPop.py.

Data is output as comma-seperated values (csv) and can be opened in excel.

See code for instructions on changing parameter values.

 
