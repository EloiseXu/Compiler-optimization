from smac.configspace import ConfigurationSpace
from ConfigSpace.hyperparameters import CategoricalHyperparameter
from ConfigSpace.conditions import InCondition

from smac.tae.execute_func import ExecuteTAFuncDict
from smac.scenario.scenario import Scenario
from smac.facade.smac_hpo_facade import SMAC4HPO
import numpy as np
import time
import os
import sys
here = os.path.abspath(os.path.dirname(__file__))

dir = ''

options = [    
'-funsafe-math-optimizations',
'-fno-guess-branch-probability',
'-fno-ivopts',
'-fno-tree-loop-optimize',
'-fno-inline-functions',
'-funroll-all-loops',
'-O2'
]

cs = ConfigurationSpace()
for option in options:
	cs.add_hyperparameter(CategoricalHyperparameter(option, ['true', 'false'], default_value='true'))

def run_gcc_time(argsDict):
	opt = ''
	for option in options:
		if argsDict[option] == 'true':
			opt = opt + ' ' + option 

	cmd = 'sh ' + '__compile gcc ' + opt 
	os.system(cmd)
	cmd = 'sh ' + '__run 1'
	os.system(cmd)
	cmd = 'echo "time ./a.out $cmd" > tmp_bat'
	os.system(cmd)
	begin = time.time()
	for i in range(100):
		os.system('source tmp_bat')
	end = time.time()

	return end-begin

scenario = Scenario({"run_obj": "quality",   # we optimize quality (alternatively runtime)
                     "runcount-limit": 10,   # max. number of function evaluations; for this example set to a low number
                     "cs": cs,               # configuration space
                     "deterministic": "true"
                     })

smac = SMAC4HPO(scenario=scenario, rng=np.random.RandomState(42),
        tae_runner=run_gcc_time)

incumbent = smac.optimize()
inc_value = run_gcc_time(incumbent)

print ('the best time!')
print (inc_value)
print ('-----------------------------')
print ('-----------------------------')
with open('best_time.txt', 'w') as f:
    f.write(str(inc_value))
