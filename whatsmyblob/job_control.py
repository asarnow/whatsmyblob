import os
import shutil

# given a (string)unique ID
# validate that it is a string
def validate_unique_id(unique_id):
	result = isinstance(unique_id, str)
	return result

# setup job
# 1 - create root app directory in /tmp if does not exist
# 2 - create tmp directory for given job with unique ID attached to name
def create_tmp_dir(root_tmp_dir_path, unique_id):
	# is main tmp directory accessible/exists?
	if not os.path.exists(root_tmp_dir_path):
		print("Root temporary directory, " + root_tmp_dir_path + " not found!")
		return False
	elif not os.access(root_tmp_dir_path, os.W_OK):
		print("Cannot write to root temporary directory, " + root_tmp_dir_path)
		return False

	app_tmp_path = root_tmp_dir_path + "/whatsmyblob"

	# try creating root app tmp directory
	if not os.path.exists(app_tmp_path):
		try:
			os.mkdir(app_tmp_path)
		except OSError:
			print("Creation of tmp root app directory %s failed" % app_tmp_path)
		else:
			print("Successfully created the directory %s \'" % app_tmp_path + "\'")
	
	try:
		unique_path = app_tmp_path + "/job_" + unique_id
		os.mkdir(unique_path)
	except OSError:
		print("Creation of tmp unique job directory %s failed" % app_tmp_path)
	else:
		print("Successfully created the directory %s " % unique_path)

	return unique_path

# if you want to get tmp directory path of given job
# to delete directory, or write extra things etc.
# this'll do it.
def get_tmp_dir_path_to_given_job(root_tmp_dir_path, unique_id):
	job_dir = root_tmp_dir_path + "/whatsmyblob/job_" + unique_id
	return job_dir

# teardown - delete directory
def rm_directory_recursive(path_to_directory):
	# check if directory to be deleted is actually there
	if os.path.exists(path_to_directory):
		try:
			shutil.rmtree(path_to_directory)
		except:
			print("Could not delete directory " + path_to_directory)
	else:
		print("Directory to delete not found!")
		return False

	return True

# may be redundant
def create_job_entry(unique_id):
	print('Create and populate entry')

# doing the actual leg work processing the data here
def process_data(unique_id):
	print('running algorithms here')
	# once job completion indicated somehow, finish
	return True

# update SQL db for given job with given status
def update_job_status(status_int, unique_id):
	# machine to human readable status key
	status_dict = {0:"Queued",
				   1:"Running",
				   2:"Complete",
				   3:"Error"}
	print("Update job status call here")

	return True


# run job function
def run_job(root_tmp_dir_path, unique_id):
	# validate the ID first
	validated_id = validate_unique_id(unique_id)
	if not validated_id:
		print("Invalid unique ID provided")
		return False

	try:
		# create temporary directory for unique job, and return path to it
		unique_tmp_dir = create_tmp_dir(root_tmp_dir_path, unique_id)
		if unique_tmp_dir:
			print("Temporary job directory created!")
			# processing dataset
			processed_data_bool = process_data(unique_id)
			if processed_data_bool:
				print("Processing complete!")
		else:
			print("Failed to start job, no temporary job directory created.")
			return False
	except:
		print("Job failed.")