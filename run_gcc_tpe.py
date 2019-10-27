from hyperopt import fmin, tpe, hp, space_eval, rand, Trials, partial, STATUS_OK
import time
import os
import sys
here = os.path.abspath(os.path.dirname(__file__))
print(here)
level = os.environ.get('TPE_LEVEL', 'bn')
dir = ''

o1_options = [
'-fcombine-stack-adjustments',
          '-fcompare-elim',
          '-fcprop-registers',
          '-fdce',
          '-fdefer-pop',
          '-fdse',
          '-fforward-propagate',
          '-fguess-branch-probability',
          '-fif-conversion2',
          '-fif-conversion',
          '-finline-functions-called-once',
          '-fipa-pure-const',
          '-fipa-profile',
          '-fipa-reference',
          '-fmerge-constants',
          '-fshrink-wrap',
          '-fsplit-wide-types',
          '-ftree-bit-ccp',
          '-ftree-ccp',
          '-ftree-ch',
          '-ftree-copy-prop',
          '-ftree-copyrename',
          '-ftree-dce',
          '-ftree-dominator-opts',
          '-ftree-dse',
          '-ftree-forwprop',
          '-ftree-fre',
          '-ftree-phiprop',
          '-ftree-sink',
          '-ftree-slsr',
          '-ftree-sra',
          '-ftree-pta',
          '-ftree-ter',
          '-funit-at-a-time']

o2_options = ['-fthread-jumps',
          '-falign-functions',
'-falign-jumps',
          '-falign-loops',
'-falign-labels',
          '-fcaller-saves',
          '-fcrossjumping',
          '-fcse-follow-jumps',  '-fcse-skip-blocks',
          '-fdelete-null-pointer-checks',
          '-fdevirtualize',
          '-fexpensive-optimizations',
          '-fgcse',  
          '-fhoist-adjacent-loads',
          '-finline-small-functions',
          '-findirect-inlining',
          '-fipa-sra',
          '-foptimize-register-move',
          '-foptimize-sibling-calls',
          '-foptimize-strlen',
          '-fpeephole2',
          '-fregmove',
          '-freorder-blocks',
'-freorder-functions',
          '-frerun-cse-after-loop',
          '-fsched-interblock',
'-fsched-spec',
'-fschedule-insns2',
          '-fstrict-aliasing',
          '-fthread-jumps',
          '-ftree-builtin-call-dce',
          '-ftree-pre',
          '-ftree-switch-conversion',
'-ftree-tail-merge',
          '-ftree-vrp']

o3_options = ['-finline-functions', '-funswitch-loops', '-fpredictive-commoning', '-fgcse-after-reload', '-ftree-vectorize', '-fvect-cost-model', '-ftree-partial-pre', '-fipa-cp-clone']

if level == 'bn':
	options = [
'-funsafe-math-optimizations',
'-fno-guess-branch-probability',
'-fno-ivopts',
'-fno-tree-loop-optimize',
'-fno-inline-functions',
'-funroll-all-loops'
]
	fixed = ' -O2 '
elif level == 'O1':
	options = o1_options
	fixed = ' -O '
elif level == 'O2':
	options = o2_options
	fixed = ' -O ' + ' '.join(o1_options) + ' '
elif level == 'O3':
	options = o3_options
	fixed = ' -O ' + ' '.join(o1_options) + ' ' + ' '.join(o2_options) + ' '

def run_gcc_time(argsDict):
	opt = ''
	for option in options:
		if argsDict[option] == 1:
			opt = opt + ' ' + option 

	cmd = 'rm -f a_' + str(level) + '.out *.o *.a *.s *.i *.I tmp_bat_' + str(level)
	print(cmd)
	os.system(cmd)
	cmd = 'gcc ' + fixed + ' ' + opt + ' -c *.c'
	print(cmd)
	os.system(cmd)
	cmd = 'gcc ' + fixed + ' ' + opt + ' -o a_' + str(level) + '.out -lm *.o'
	print(cmd)
	os.system(cmd)
	cmd = '''#! /bin/bash

if test -z "1"; then
 echo "Usage: __run <dataset number> <number of runs (optional)>"
 exit
fi

#Searching for dataset info (command line and loop wrapper)
found="0"
exec 5< _ccc_info_datasets
 read <&5 ds_max ;
 while read <&5 line;
 do
  if [ "$line" == "=====" ]; then
   read <&5 ds ;
   read <&5 cmd ;
   read <&5 loop_wrap ;
   if [ $ds -eq 1 ] ; then
    found="1"
    break;
   fi
  fi
 done
exec 5>&-

if [ $found != "1" ] ; then
 echo "Can't find dataset info in the _ccc_info_datasets file ..."
 exit
fi

if test -n "$2"; then
 loop_wrap=$2
fi

echo "Found dataset: " $ds
echo "Command line:  " $cmd
echo "Loop wrap:     " $loop_wrap

if test -n "$2"; then
 echo $2 > _finfo_dataset
else
 echo $loop_wrap > _finfo_dataset
fi
echo ""

if test -n "$CCC_RE"; then
        echo "time $CCC_RE ./a_''' + str(level) + '''.out $cmd" > tmp_bat_''' + str(level) + '''
else
        echo "time ./a_''' + str(level) + '''.out $cmd" > tmp_bat_''' + str(level) + '''
fi'''
	os.system(cmd)
	begin = time.time()
	for i in range(10):
		os.system('source ./tmp_bat_' + str(level))
	end = time.time()

	return end-begin

space = {}
for option in options:
    space[option] = hp.choice(option, [0, 1])

algo = partial(tpe.suggest, n_startup_jobs=1)
best = fmin(run_gcc_time, space, algo=algo, max_evals=35)
best_time = str(run_gcc_time(best))
print ('the best time!')
print (best_time)
with open(level + '_tpe_best_time.txt', 'w') as f:
    f.write(best_time)

