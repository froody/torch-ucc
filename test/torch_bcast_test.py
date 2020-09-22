#
# Copyright (C) Mellanox Technologies Ltd. 2001-2020.  ALL RIGHTS RESERVED.
#

import numpy as np
from torch_ucc_test_setup import *

args = parse_test_args()
pg = init_process_groups(args.backend)

comm_size = dist.get_world_size()
comm_rank = dist.get_rank()

counts = 2 ** np.arange(24)
print_test_head("Broadcast", comm_rank)
for count in counts:
    tensor_ucc = get_tensor(count, args.use_cuda)
    tensor_test = tensor_ucc.clone()
    dist.broadcast(tensor_ucc, 0)
    dist.broadcast(tensor_test, 0, group=pg)
    status = check_tensor_equal(tensor_ucc, tensor_test)
    dist.all_reduce(status, group=pg)
    print_test_result(status, count, comm_rank, comm_size)

if comm_rank == 0:
    print("Test Broadcast: succeeded")