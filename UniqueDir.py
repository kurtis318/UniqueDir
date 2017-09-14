#!/usr/bin/python

import os
from RunCmdPy import RunCmd

class UniqueDir:
	
	def __init__(self):
		"""
		Constructor for UniqueDir object. KWR
		"""
		self.pattern = ""
   
	def __verify_dir(dir_path):
		"""
		Verify the directory exists AND user has r/w access.
		"""
		rval = 0
		if os.path.exists(dir_path):
			if os.access(dir_path, os.W_OK):
				rval = 0
			else:
				rval = 2
				msg = 'Directory {} is not writable.'.format(dir_path)
		else:
			rval=1
			msg = 'Cannot find directory {}.'.format(dir_path)			
		
		return (rval, msg)
		
	def __find_first_last_dir(dir_path, pattern):
		
		cmd_runner = RunCmd()
		
		cnt = 0
		first_dir = last_dir = ""
		# Determine number of potential EXISTING directories
		cmd = 'ls -1 {}/{}-*|wc -l'.format(dir_path, pattern)
		cmd_runner.run(cmd)
		if cmd_runner.rc == 0:
			cnt = int(cmd_runner.get_stdout[0])
			print('>>> INFO: There are {} directories wiht same pattern'.format(cnt))
		else:
			cnt = 0
		
		if cnt > 0:
			# No existing directorys with pattern.
			new_dir = '{}/{}-01'.format(dir_path, pattern)
		else:
			# There are EXISTING directories.  Determine first and last.
			cmd = 'ls -1 {}/{}-*|sort|head -n 1'
			cmd_runner(cmd)
			if (cmd_runner.get_rc == 0)
				first_dir = cmd_runner.get_stdout[0]
				print('>>> INFO: <first_dir={}>'.format(first_dir))
			else:
				print('>>> ERROR: Cannot determine first directory.  stderr follows:\n')
				cmd_runner.dump_stderr()
				cnt = -1
				first_dir = last_dir = ""
				return cnt, first_dir, last_dir
		
		# Found first directory, find the last directory
		
			
		
	def mkdir(self, dir_path = "/tmp", pattern = '__udo', max_dirs = 5):
		
		self.dir_path = path
		self.pattern = pattern
		self.made_dir = False
		
		rc,msg = __verify_dir(dir_path)
		if rc == 0:
			print('>>> INFO: Found directory {} and it is writeable.'.format(dir_path))
		else:
			print('>>> ERROR: {}'.format(msg))
			return 1 
		
			
			
				
		
			
    
   
def test1():
	print("Running test1()")
	return 0
		
def test2():
	print("Running test2()")
	return 0

def main():
	print("running main()")
	test1()
	test2()
	return 0
	
if __name__ == "__main__":
    # execute only if run as a script
    main()
    exit(0)

