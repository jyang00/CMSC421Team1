# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 19:25:56 2021

@author: acneu
runExperiment runner
"""

import subprocess
import sys

## Give me a 1, 2, or 3 to do the set of experiments of that number.


if len(sys.argv) > 1:
  if sys.argv[1] == '1':
    ## Experiment 1 ##
    subprocess.check_call(['python', 'runExperiment', '1', '50', '4', 'exp1_d4_data', '1'], stdout=sys.stdout)
    subprocess.check_call(['python', 'runExperiment', '1', '50', '5', 'exp1_d5_data', '1'], stdout=sys.stdout)
  elif sys.argv[1] == '2':
    ## Experiment 2 ##
    subprocess.check_call(['python', 'runExperiment', '2', '50', '4', 'exp2_d4_data', '1'], stdout=sys.stdout)
    subprocess.check_call(['python', 'runExperiment', '2', '50', '5', 'exp2_d5_data', '1'], stdout=sys.stdout)
  else:
    ## Experiment 3 ##
    subprocess.check_call(['python', 'runExperiment', '3', '30', '3', 'exp3_d3_data', '1'], stdout=sys.stdout)
    subprocess.check_call(['python', 'runExperiment', '3', '30', '4', 'exp4_d4_data', '1'], stdout=sys.stdout)
    subprocess.check_call(['python', 'runExperiment', '3', '30', '5', 'exp5_d5_data', '1'], stdout=sys.stdout)