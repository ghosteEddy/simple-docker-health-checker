import os
import sys
import json
from typing import TypedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from app import ReportReq, JobReport

DEFAULT_TARGET_CONFIG_PATH = "/checker/config.json"
DEFAULT_WORKER = 4
DEFAULT_SHOW_LOG = True

class Config(TypedDict):
    endpoints: list[str]
    
class HealthCheckJob:
    endpoint: str
    success: bool
    def  __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.success = False
    

def get_config(fp: str) -> Config:
    with open(fp, "r") as f:
        config: Config = json.load(f)
        return config
    
def check_health(job: HealthCheckJob) -> bool:
    res = requests.get(job.endpoint)
    if (200 <= res.status_code and 300 > res.status_code):
        job.success = True
        return True
    else:
        job.success = False
        return False

def convert_report(job: HealthCheckJob)-> JobReport:
    return {"endpoint": job.endpoint, "success":job.success}

if __name__ == "__main__":
    # get app config
    TARGET_DIR = os.environ.get('TARGET_DIR') or DEFAULT_TARGET_CONFIG_PATH
    CONCURRENT = os.environ.get('WORKER') or DEFAULT_WORKER
    SHOW_LOG = os.environ.get('SHOW_LOG') or DEFAULT_SHOW_LOG
    
    # get endpoint
    config = get_config(TARGET_DIR)
    endpoints = config["endpoints"]
    jobs = list(map(HealthCheckJob, endpoints))
    
    # initiate
    with ThreadPoolExecutor(max_workers=CONCURRENT) as executor:
        future =  [executor.submit(check_health, job) for job in jobs]
        
    if(SHOW_LOG):
        jobs_data = list(map(convert_report,jobs))
        payload: ReportReq = {"jobs": jobs_data}
        requests.post("http://localhost:5000/report",json=payload)
    
    fails = list(filter(lambda j: j.success == False,jobs))
    if len(fails) == 0:
        sys.exit(0)
    else:
        sys.exit(1)
        