import redis
import json
import os
from pathlib import Path
import time

redis_host = os.getenv('REDIS_HOST', 'localhost')  
r = redis.Redis(host=redis_host, port=6379, decode_responses=True) # set up redis connection

config_path = Path(__file__).parent / "interface" / "config" # navigate to the relative path of config



def pull_config(config_path) -> dict:  #scan config directory for valid config files
   tasks = {}
   try:
       if not config_path.exists():
           print ("config path does not exist")
           return tasks
       for f in config_path.iterdir():
           if f.is_file() and f.suffix == '.json':
               with open(f, 'r') as file:
                  tasks[f.stem] = json.load(file)
       return tasks
       
   except Exception as e:
       print(f"error loading configs {e}")
   
   

def generate_jobs(tasks: dict, redis_client)-> int:
   # Generate jobs from task configs and enqueue them to Redis. Returns number of jobs successfully enqueued. 
   jobs_enqueued = 0
   if not tasks:
      print ("no tasks configured")
      return 0
   
   processed_dir = Path(__file__).parent / "interface" / "input" / "processed"
   processed_dir.mkdir(parents=True, exist_ok=True)
       

   for task_name, task_config in tasks.items():
      input_dir = Path(task_config["input_path"])

      if not input_dir.exists():
          print(f"the input directory: {input_dir}, does not exist for task: {task_name}")
          continue

      if not input_dir.is_dir():
         print(f"Input path {input_dir} is not a directory")
         continue

      for file in input_dir.iterdir():
         if not file.is_file():
             continue
         
         job = task_config.copy()
         job["input_path"] = str(file)
         job["output_path"] = str(Path(job["output_path"]) / file.name)
         job["time_enqueued"] = time.time()

         try:
            redis_client.lpush("jobs", json.dumps(job))
            print(f"enqueued {file.name}")
            file.rename (processed_dir / file.name)
            jobs_enqueued += 1

         except Exception as e:
            print(f"unable to enqueue {file.name}. Is the Redis Queue running?{e}")
   return jobs_enqueued


while True:
    
    task_configs = pull_config(config_path)

    if task_configs:
        generate_jobs(task_configs, r)

    time.sleep(5)

   
         
   


