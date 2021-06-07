import subprocess
import time
import os
import ntpath
from shutil import copyfile
import psutil

class LoadRunner:
	def __init__(self):
		print("Please Provide Following Information")
		self.sub_name = input("Submission Name:")
		self.script_name = input("Please Provide Path of scrit:")
		self.run_count = int(input("run count:"))
		self.env = None
		self.stored_script_path="/var/spool/LoadRunner/" + self.sub_name


	def get_file_extension(self):
		split_tup = os.path.splitext(self.script_name)
		file_extension = split_tup[1]
		return file_extension

	@staticmethod
	def __get_env():
		return os.environ

	def get_script_executor(self):
		executor = {'.py': 'python', '.sh': '/bin/bash'}
		file_exetension = self.get_file_extension()
		return executor[file_exetension]

	def get_system_data():
		sys_data = {}
		sys_data['cpu'] = psutil.cpu_count(logical=True)
		svmem = psutil.virtual_memory()
		sys_data['memory'] = str(svmem.available/(1024*1024)) + 'mb' 
		return sys_data		

	def run_load_runner(self):
		sys_data = LoadRunner.get_system_data()
		s_executor = self.get_script_executor()
		print("Gathering Environment during run")
		self.env = LoadRunner.__get_env()
		run_cmd = [s_executor, self.script_name]
		if self.run_count > 0:
			initial_time = time.time()
			for i in range(1, self.run_count+1):
				print("+" * 40)
				print("Started run count: ", i)
				loop_time = time.time()
				test_ext = open('test.txt', 'w')
				subprocess.call(run_cmd, stdout=test_ext)
				test_ext.close()
				final_loop_time = time.time()
				print("Time taken to complete cycle no. %s: %s" %(i, final_loop_time - loop_time))
			final_time = time.time()
		time_diff = final_time - initial_time
		self.show_result(time_diff, sys_data)
			
	def show_result(self, time_diff, sys_data):
		print("=" * 80)
		print("|", " " * 29, "Load Runner Data", " " * 29, "|")
		print("=" * 80)
		c_str = "Available CPU before start load runner:" + str(sys_data['cpu'])
		print(c_str)
		print("-" * 80)
		c_str = "Available Memory before start load runner:"
		print(c_str, sys_data['memory'])
		print("-" * 80)
		c_str = "Average time taken to complete load run:" + str((time_diff/self.run_count))
		print(c_str)
		print("-" * 80)
		file_name = ntpath.basename(self.script_name)
		copyfile(self.script_name, self.stored_script_path + '_' + file_name)
		print("Scipt stored at location:", self.stored_script_path + '_' + file_name)
		print("=" * 80)
