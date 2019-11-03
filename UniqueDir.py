#!/usr/bin/python

import os
from RunCmdPy import RunCmd
# from Cython.Utility.CConvert import length

class UniqueDir:

	
	def __init__(self):
		"""
		Only constructor for this class.  No parameters

		"""
		
		self.pattern = ""
		return
	
	def __verify_dir(self, dir_path):
		"""
		Verifies input directory exists AND is writeable.
		
		:param dir_path: Full path to a directory
		:return: (return code, return message)
		:rtype: (int, string)
		"""
		
		rval = 0
		msg = "*unknown error"
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
		"""
		Determines first and last full sub-directory path with given pattern.
		
		:param dir_path: Full path to a directory
		:param pattern: Prefix pattern for new sub-directory
		:return: (count, first subdirectory, last subdirectory)
		:rtype: (int, string, string)
		"""
		
		cmd_runner = RunCmd()
		
		cnt = 0
		first_dir = last_dir = ""
		
		# Determine number of potential EXISTING directories
		cmd = 'find {} -maxdepth 1 -type d -name  "{}*" 2>/dev/null|wc -l'.format(dir_path, pattern)
		cmd_runner.run(cmd)
		
		if cmd_runner.rc == 0:
			cnt = int(cmd_runner.get_stdout[0])
			print('>>> INFO: There are {} directories with same pattern'.format(cnt))
		else:
			cnt = 0
		
		if cnt >0:
			
			# There are EXISTING directories.  Determine first and last.
			cmd = 'find {} -maxdepth 1 -type d -name  "{}*" 2>/dev/null|sort|head -n 1'.format(dir_path, pattern)
			cmd_runner.run(cmd)
			if cmd_runner.get_rc == 0:
				first_dir = cmd_runner.get_stdout[0]
				print('>>> INFO: <first_dir={}>'.format(first_dir))
			else:
				print('>>> ERROR: Cannot determine first directory.  stderr follows:\n')
				cmd_runner.dump_stderr()
				cnt = -1
				first_dir = last_dir = ""
				return cnt, first_dir, last_dir
		
			# Found first directory, find the last directory
			cmd = 'find {} -maxdepth 1 -type d -name  "{}*" 2>/dev/null|sort|tail -n 1'.format(dir_path, pattern)
			cmd_runner.run(cmd)
			if (cmd_runner.get_rc == 0):
				last_dir = cmd_runner.get_stdout[0]
				print('>>> INFO: <last_dir={}>'.format(last_dir))		
			else:
				print('>>> ERROR: Cannot determine last directory.  stderr follows:\n')
				cmd_runner.dump_stderr()
				cnt = -1
				last_dir = ""
				return cnt, first_dir, last_dir
			
		return cnt, first_dir, last_dir
		
	def mkdir(self, dir_path = "/tmp", pattern = 'dir-', max_dirs = 5):
		"""
		Creates a new sub-directory and removes extra sub-directories.
		
		:param dir_path: Full path to a directory (default is /tmp)
		:param pattern: Prefix pattern for new sub-directory (default is 'dir-')
		:param max_dirs: Maximum sub-directories to leave in dir_path
		:return: (return code, new sub-directory path)
		:rtype: (int, string)
		"""	
		cmd_runner = RunCmd()
		
		self.dir_path = dir_path
		self.pattern = pattern
		self.made_dir = False
		self.new_dir = ''
		self.max_dirs = max_dirs
		
		rc,msg = self.__verify_dir(dir_path)
		if rc == 0:
			print('>>> INFO: Found directory {} and it is writeable.'.format(dir_path))
		else:
			print('>>> ERROR: {}'.format(msg))
			return 1,""
		
		# Determine number of directories with pattern, first and last directories
		dir_cnt, first_dir, last_dir = self.__find_first_last_dir(dir_path, pattern)
		n = 0
		if dir_cnt == 0:
			
			# There are no existing directories. 
			n = 1
		elif dir_cnt == -1:
			return 1, ""
		else:
			
			# Got first at least 1 existing directory.
			plen = len(dir_path + pattern + '-')
			n = int(last_dir[plen:]) + 1

		new_dir = '{}/{}{num:03d}'.format(dir_path, pattern, num=n)
		cmd = 'mkdir {}'.format(new_dir)
		cmd_runner.run(cmd)
		if (cmd_runner.get_rc != 0):
			print('>>> ERROR: Creation of directory <new_dir={}> failed. stderr follows:'.format(new_dir))
			cmd_runner.dump_stderr()
			return 2, ''
		else:
			print('>>> INFO: Created new directory <new_dir={}>'.format(new_dir))
			
		# New directory created.
		self.new_dir = new_dir
		self.made_dir = True
	
		# Delete multiple directories if more than max.  New feature. 
		if dir_cnt >= max_dirs:
								
				remove_dir_1 = int(first_dir[plen:])
				remove_dir_last = dir_cnt - self.max_dirs + remove_dir_1 + 1
                                print('>>> DBUG: <remove_dir_1={}> <remove_dir_last={}>'.format(remove_dir_1, remove_dir_last))
				for j in range(remove_dir_1, remove_dir_last):
					remove_dir = '{}/{}{num:03d}'.format(dir_path, pattern, num=j)
					cmd = "rm -rf {}".format(remove_dir)
					cmd_runner.run(cmd)
					if cmd_runner.get_rc != 0:
						print('>>> ERROR: Could not remove directory {}. stderr follows:'.format(remove_dir))
						cmd_runner.dump_stderr()
						return 3,''
			
		return 0, new_dir		
	
	@property
	def get_dir(self):
		"""
		Accessor to new sub-directory path.  Might be null string.
		
		:param none
		:return: new sub-directory path
		:rtype: string
		"""	
		return self.new_dir
			
def test1():
	"""
	Standalone test 1
	
	:param none
	:return: return code
	:rtype: int
	"""	
	print("Running test1()")
	t = UniqueDir()
	rc, new_dir = t.mkdir('/tmp', "kwr540-")
	if rc == 0:
		print('>>> INFO: Created new dir <new_dir={}> <get_dir()={}>'.format(new_dir, t.get_dir))
		return 0
	else:
		print(">>> ERROR: Failed making new directory.")
		return 1
		
def test2():
	"""
	Standalone test 2
	
	:param none
	:return: return code
	:rtype: int
	"""	
	print("Running test2()")
	return 0

def main():
	"""
	Main control function for testing
	
	:param none
	:return: return code
	:rtype: int
	"""	
	print("running main()")
	test1()
	test2()
	return 0
	
if __name__ == "__main__":
	# execute only if run as a script
	rc = main()
	exit(rc)

