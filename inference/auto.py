import os
import sys
from .save import run_inference
from time import sleep

sys.setrecursionlimit(999_999_999)


inference_runs = 0

while 1:
    inference_runs+=1
    run_inference()
    print(f'Inference has been run {inference_runs} times.')
    sleep(3600)
