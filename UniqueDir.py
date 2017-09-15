#!/usr/bin/python

import os
from RunCmdPy import RunCmd
from Cython.Utility.CConvert import length

class UniqueDir:

	
	def __init__(self):
		"""
		Constructor for UniqueDir object. KWR
		"""
		self.pattern = ""
		return
	
	def __verify_dir(self, dir_path):
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
		
	def __find_first_last_dir(self, dir_path, pattern):
		
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
		
		if cnt >0:
			
			# There are EXISTING directories.  Determine first and last.
			cmd = 'ls -1 {}/{}-*|sort|head -n 1'
			cmd_runner(cmd)
			if (cmd_runner.get_rc == 0):
				first_dir = cmd_runner.get_stdout[0]
				print('>>> INFO: <first_dir={}>'.format(first_dir))
			else:
				print('>>> ERROR: Cannot determine first directory.  stderr follows:\n')
				cmd_runner.dump_stderr()
				cnt = -1
				first_dir = last_dir = ""
				return cnt, first_dir, last_dir
		
			# Found first directory, find the last directory
			cmd = 'ls -1 {}/{}-*|sort|tail -n 1'
			cmd_runner(cmd)
			if (cmd_runner.get_rc == 0):
				last_dir = cmd_runner.get_stdout[0]
				print('>>> INFO: <first_dir={}>'.format(first_dir))		
			else:
				print('>>> ERROR: Cannot determine last directory.  stderr follows:\n')
				cmd_runner.dump_stderr()
				cnt = -1
				last_dir = ""
				return cnt, first_dir, last_dir
			
		return cnt, first_dir, last_dir
		
	def mkdir(self, dir_path = "/tmp", pattern = '__udo', max_dirs = 5):
		
		cmd_runner = RunCmd()
		
		self.dir_path = dir_path
		self.pattern = pattern
		self.made_dir = False
		self.new_dir = ''
		
		rc,msg = self.__verify_dir(dir_path)
		if rc == 0:
			print('>>> INFO: Found directory {} and it is writeable.'.format(dir_path))
		else:
			print('>>> ERROR: {}'.format(msg))
			return 1,""
		
		# Determine number of directories with patthen, first and last directories
		dir_cnt, first_dir, last_dir = self.__find_first_last_dir(dir_path, pattern)
		if dir_cnt == 0:
			
			# There are no existing directories.
			new_dir = '{}/{}.001'.format(dir_path, pattern)
		elif dir_cnt == -1:
			return 1, ""
		else:
			
			# Got first at least 1 existing directory.
			plen = length(dir_path + pattern + '-')
			n = int(last_dir[plen:]) + 1
			new_dir = '{}/{}.{num:02d}'.format(dir_path, pattern, num=n)
		
		cmd = 'mkdir {}'.format(new_dir)
		cmd_runner.run(cmd)
		if (cmd_runner.get_rc != 0):
				print('>>> ERROR: Creation ofr directory <new_dir={}> failed. stderr follows:'.format(new_dir))
				cmd_runner.dump_stderr()
				return 2, ''
			
		# New directory created.
		self.new_dir = new_dir
		self.made_dir = True
		
		# Delete first directory in pattern IF total directories more than max
		if dir_cnt >= max_dirs:
				
				# Need to delete the first directory
				cmd = 'rm -f {}'.format(*last_dir)
				cmd_runner.run(cmd)
				if cmd_runner.get_rc != 0:
					
					# Could not delete first dir.
					print('>>> ERROR: Could not delete directory <first_dir={}>'.format(first_dir))
					return 4, ""
			
		return 0, new_dir		
			
		
		
def test1():
	print("Running test1()")
	t = UniqueDir()
	rc, new_dir = t.made_dir()
	if rc == 0:
		print('>>> INFO: Created new dir <new_dir={}>'.format(new_dir))
		return 0
	else
		print(">>> ERROR: Failed making new directory.")
		retun 1
		
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

