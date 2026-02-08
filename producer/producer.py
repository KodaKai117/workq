import redis
import json
from pathlib import Path
import time


r = redis.Redis(host="localhost", port=6379, decode_responses=True) # set up redis connection

config_path = Path(__file__).parent.parent.resolve() / "interface" / "config" / "transform.json" # navigate to the relative path of config.json but save it as an absolute path


with open(config_path, 'r') as file:                 
    task = json.load(file)                           #open and load config.json
input_dir = config_path.parent.parent / "input"             #define the input directory
for file in input_dir.iterdir():      
        job = task.copy()                    
        job["input_path"] = str(file)
        job["output_path"] = str(Path(job["output_path"]) / file.name)
        job["time_enqueued"] = str(time.time())
        r.lpush("jobs", json.dumps(job))
        print(f"pushed {file} to the queue")
        """try:
           r.lpush(json.dumps(job))
           print(f"pushed {Path(file)} to the queue")
        except:
           print(f"unable to push {Path(file)} to the queue. Is the Redis Queue running?")"""



