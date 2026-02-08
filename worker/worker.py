import redis
import json
from pathlib import Path
import time
from tasks.transform import process_image

def redissetup():
   r = redis.Redis(host='localhost', port=6379, decode_responses = True)
   try:
       r.ping()
       print ("connected to redis")
       return r
       
   except Exception as e:
       print (f"can't connect to redis. Is it running? error: {e}")

r = redissetup()

def getajob() -> dict:
   result = r.brpop("jobs", timeout=5)

   if result:
            job = json.loads(result[1])
            print(f"worker found a job!{job}")
            return job
   else:
      print ("waiting.. no jobs available..")
      
   
redissetup()
   
while True:
   job = getajob()
   if job:
      try:
         process_image(job)
         print(f"Processed {Path(job["input_path"]).name}")
      except Exception as e:
         print(f"Failed to process {job.get("input_path")}: {e}")
         
   else:
       time.sleep(1)


