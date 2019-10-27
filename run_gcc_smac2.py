from hyperopt import fmin, tpe, hp, space_eval, rand, Trials, partial, STATUS_OK
import time
import os
import sys
here = os.path.abspath(os.path.dirname(__file__))
print(here)
level = os.environ.get('LEVEL', 'bn')
dir = ''

if level == 'bn':
	options = [
'-funsafe-math-optimizations',
'-fno-guess-branch-probability',
'-fno-ivopts',
'-fno-tree-loop-optimize',
'-fno-inline-functions',
'-funroll-all-loops',
'-O2'
]
	fixed = ''
elif level == 'o1':
	options = ['-fdefer-pop',
 '-fdelayed-branch',
 '-fguess-branch-probability',
 '-fcprop-registers',
 '-floop-optimize',
 '-fif-conversion',
 '-fif-conversion2',
 '-ftree-ccp',
 '-ftree-dce',
 '-ftree-dominator-opts',
 '-ftree-dse',
 '-ftree-ter',
 '-ftree-lrs',
 '-ftree-sra',
 '-ftree-copyrename',
 '-ftree-fre',
 '-ftree-ch',
 '-funit-at-a-time',
 '-fmerge-constants'
]
	fixed = ''
elif level == 'o2':
	options = [
  '-fthread-jumps-fcrossjumping',
  '-foptimize-sibling-calls',
  '-fcse-follow-jumps',
  '-fcse-skip-blocks',
  '-fgcse -fgcse-lm',
  '-fexpensive-optimizations',
  '-fstrength-reduce',
  '-frerun-cse-after-loop',
  '-frerun-loop-opt',
  '-fcaller-saves',
  '-fpeephole2',
  '-fschedule-insns',
  '-fschedule-insns2',
  '-fsched-interblock',
  '-fsched-spec',
  '-fregmove',
  '-fstrict-aliasing',
  '-fdelete-null-pointer-checks',
  '-freorder-blocks',
  '-freorder-functions',
  '-falign-functions',
  '-falign-jumps',
  '-falign-loops',
  '-falign-labels',
  '-ftree-vrp',
  '-ftree-pre']
	fixed = '-fdefer-pop -fdelayed-branch -fguess-branch-probability -fcprop-registers -floop-optimize -fif-conversion -fif-conversion2 -ftree-ccp -ftree-dce -ftree-dominator-opts -ftree-dse -ftree-ter -ftree-lrs -ftree-sra -ftree-copyrename -ftree-fre -ftree-ch -funit-at-a-time -fmerge-constants'
elif level == 'o3':
	options = [
'-finline-functions',
   '-funswitch-loops',
   '-fgcse-after-reload']
	fixed = '-fdefer-pop -fdelayed-branch -fguess-branch-probability -fcprop-registers -floop-optimize -fif-conversion -fif-conversion2 -ftree-ccp -ftree-dce -ftree-dominator-opts -ftree-dse -ftree-ter -ftree-lrs -ftree-sra -ftree-copyrename -ftree-fre -ftree-ch -funit-at-a-time -fmerge-constants -fthread-jumps -fcrossjumping -foptimize-sibling-calls -fcse-follow-jumps -fcse-skip-blocks -fgcse -fgcse-lm -fexpensive-optimizations -fstrength-reduce -frerun-cse-after-loop -frerun-loop-opt -fcaller-saves -fpeephole2 -fschedule-insns -fschedule-insns2 -fsched-interblock -fsched-spec -fregmove -fstrict-aliasing -fdelete-null-pointer-checks -freorder-blocks -freorder-functions -falign-functions -falign-jumps -falign-loops -falign-labels -ftree-vrp -ftree-pre'

def run_gcc_time(argsDict):
	opt = ''
	for option in options:
		if argsDict[option] == 1:
			opt = opt + ' ' + option 

	cmd = 'rm -f a.out *.o *.a *.s *.i *.I'
	os.system(cmd)
	cmd = 'gcc ' + opt + ' ' + fixed + ' -c *.c'
	#print(cmd)
	os.system(cmd)
	cmd = 'gcc ' + opt + ' ' + fixed + ' -o a.out -lm *.o'
	#print(cmd)
	os.system(cmd)
	cmd = 'sh __run 1'
	os.system(cmd)
	begin = time.time()
	for i in range(10):
		os.system('source ./tmp_bat')
	end = time.time()

	return end-begin

space = {}
for option in options:
    space[option] = hp.choice(option, [0, 1])

algo = partial(tpe.suggest, n_startup_jobs=1)
best = fmin(run_gcc_time, space, algo=algo, max_evals=10)
best_time = str(run_gcc_time(best))
print ('the best time!')
print (best_time)
with open('bn_tpe_best_time.txt', 'w') as f:
    f.write(best_time)

