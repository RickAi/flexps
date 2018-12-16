#!/usr/bin/env python

import sys
from launch_utils import launch_util

# [Local]
# python logistic_regression.py local
#
# [Cluster]
# python logistic_regression.py

local_debug = True if len(sys.argv) >= 2 and sys.argv[1] == "local" else False

hostfile = "machinefiles/localnodes" if local_debug else "machinefiles/5node"
progfile = ("cmake-build-debug" if local_debug else "debug") + "/LRExample"

params = {
    "hdfs_namenode": "localhost" if local_debug else "proj10",
    "hdfs_namenode_port": 9000,
    "input": "hdfs:///a2a" if local_debug else "hdfs:///datasets/classification/webspam",
    "kStaleness": 0,
    "kSpeculation": 5,
    "kModelType": "SSP",  # {ASP/SSP/BSP/SparseSSP}
    "kSparseSSPRecorderType": "Vector",  # {Vector/Map}
    "num_dims": 123 if local_debug else 16609143,
    "batch_size": 1,
    "num_workers_per_node": 2,
    "num_servers_per_node": 1,
    "num_iters": 1000,
    "alpha": 0.1,  # learning rate
    "with_injected_straggler": 1,  # {0/1}
    "kStorageType": "Vector",  # {Vector/Map}
    "num_loader_per_node": 2 if local_debug else 100,
}

env_params = (
    "GLOG_logtostderr=true "
    "GLOG_v=-1 "
    "GLOG_minloglevel=0 "
)

# this is to enable hdfs short-circuit read (disable the warning info)
# change this path accordingly when we use other cluster
# the current setting is for proj5-10
if (local_debug is False):
    env_params += "LIBHDFS3_CONF=/data/opt/course/hadoop/etc/hadoop/hdfs-site.xml"

launch_util(progfile, hostfile, env_params, params, sys.argv)
