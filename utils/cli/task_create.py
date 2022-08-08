import os
import time
import json

path=r"/home/apexon/Videos/AnyDesk"
project_id=88
#def create_task(path, project_id):
path_to_h5files=os.path.join(path, "h5_files")
h5_files_list = os.listdir(path_to_h5files)
h5_files_list=[os.path.join(path_to_h5files,item) for item in h5_files_list]

time_dict={}
for h5_file in h5_files_list:
    start_time=time.time()
    task_name=h5_file.split("/")[-1]
    task_name=task_name.rsplit('.', 1)[0]

    cmd = 'python3 cli.py --auth sai:sai --server-host 10.40.41.58 --server-port 8080  create {0} --project_id {1} local {2}'.format(task_name, project_id, h5_file)

    os.system(cmd) 
    end_time=time.time()
    time_taken=end_time-start_time
    time_dict["H5_file_name"]=task_name
    time_dict["Time_Taken"]=time_taken
    print("time_taken-------------------------------------->", time_taken)
#with open('time.txt', 'w') as file:
     #file.write(json.dumps(time_dict))   
