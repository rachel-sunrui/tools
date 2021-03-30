# Ref: https://gist.github.com/jimgoo/76ce3caaa25ed02084f7
# Monotoring the GPU Utilization for one GPU on the node for every 2 second
# Usage: 
# ----------------------------------------------
# ssh (node_id you were assigned to, such as v001)
# module load anaconda3
# source activate (your python enviroment)
# nvidia-smi (to get the GPU_id where your job is running)
# python GPU_Utils.py --GPU_id (your GPU_id, such as 0)
# ------------------------------------------------
# Default saving directory: temp_data, please make sure the saving directory exist.
# July, 2020 @ rachel_sunrui

from pynvml import (nvmlInit,
                     nvmlDeviceGetCount, 
                     nvmlDeviceGetHandleByIndex, 
                     nvmlDeviceGetUtilizationRates,
                     nvmlDeviceGetName)
import time
import argparse
import datetime
import numpy as np
from scipy.io import savemat

def gpu_info():
    "Returns a tuple of (GPU ID, GPU Description, GPU % Utilization)"
    nvmlInit()
    deviceCount = nvmlDeviceGetCount()
    info = []
    for i in range(0, deviceCount): 
        handle = nvmlDeviceGetHandleByIndex(i) 
        util = nvmlDeviceGetUtilizationRates(handle)
        desc = nvmlDeviceGetName(handle) 
        info.append((i, desc, util.gpu)) #['GPU %i - %s' % (i, desc)] = util.gpu
    return info

if __name__ == '__main__':
    utils = []
    parser = argparse.ArgumentParser(description='Rachel DLSL Model')
    parser.add_argument('--GPU_id', type=int, default=0, metavar='t/f',
                        help='which GPU we are using')
    parser.add_argument('--fn', type=str, default='GPU_usage', metavar='t/f',
                        help='the file name')
    args = parser.parse_args()
    print('Start')

    while True:
        try:
            dt = datetime.datetime.now()
            util = gpu_info()
            print(util[args.GPU_id])
            utils.append(util[args.GPU_id][2])
            time.sleep(2)   # wait time can be changed or set as an input
            savemat('temp_data/{}.mat'.format(args.fn),{'utils':utils})
        except KeyboardInterrupt:
            print(utils)
            break
