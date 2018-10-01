#!/usr/bin/env python

import sys
from launch_utils import launch_util

# [Local]
# python logistic_regression.py local
#
# [Cluster]
# python logistic_regression.py

local_debug = True if len(sys.argv) >= 2 and sys.argv[1] == "local" else False

hostfile = "machinefiles/local" if local_debug else "machinefiles/clusternodes"
progfile = ("cmake-build-debug" if local_debug else "debug") + "/LRExample"

params = {
    "hdfs_namenode": "localhost" if local_debug else "proj10",
    "hdfs_namenode_port": 9000,
    "input": "hdfs:///datasets/classification/a1a" if local_debug else "hdfs:///jasper/kdd12",
    "kStaleness": 0,
    "kSpeculation": 5,
    "kModelType": "SSP",  # {ASP/SSP/BSP/SparseSSP}
    "kSparseSSPRecorderType": "Vector",  # {Vector/Map}
    "num_dims": 54686452,
    "batch_size": 1,
    "num_workers_per_node": 2,
    "num_servers_per_node": 1,
    "num_iters": 1000,
    "alpha": 0.1,  # learning rate
    "with_injected_straggler": 1,  # {0/1}
    "kStorageType": "Vector",  # {Vector/Map}
}

env_params = (
    "GLOG_logtostderr=true "
    "GLOG_v=-1 "
    "GLOG_minloglevel=0 "
    # this is to enable hdfs short-circuit read (disable the warning info)
    # change this path accordingly when we use other cluster
    # the current setting is for proj5-10
    "" if local_debug else "LIBHDFS3_CONF=/data/opt/course/hadoop/etc/hadoop/hdfs-site.xml"
)

launch_util(progfile, hostfile, env_params, params, sys.argv)
