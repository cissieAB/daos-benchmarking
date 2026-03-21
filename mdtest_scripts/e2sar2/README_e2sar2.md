# Description of files

## Script
### `qsub_mdt_largerfile.qsub`
- this is the same mdtest benchmark I've been attempting to run in the past, but with a larger file size than what I thought was the default data_thresh value (4 KiB)

this fails on mdtest command:
```
/home/rgeorge/ior/install/bin/mdtest '-a' 'DFS' '-d' '/mdtest' '-i' '2' '-n' '100000' '-u' '-F' '-w' '6144' '-e' '6144' '--dfs.pool' 'e2sar2' '--dfs.cont' 'rgeorge-mdtest'
```

I thought 1 client node, with 48 cores, creating 100000 files per process, where files are 6 KiB big would mean:

`4,800,000 files x 6 KiB = 28,800,000 KiB = ~27.5 GiB of files`

I am not sure how to calculate amount of space needed for the metadata itself, but it cannot be as much as 27.5 GiB (even so there is space). I think if they are written inline somehow... the pool should still be able to fit the files and quite a bit of other metadata in 2.6 TB? Maybe something is very unbalanced somehow but I am not sure why.

I am not sure how this fails when this one form io500 worked:
```
[mdtest-hard-write]
t_start         = 2026-02-15 06:26:58
exe             = ./mdtest --dataPacketType=timestamp -n 1000000 -t -w 3901 -e 3901 -P -G=-1622856514 -N 1 -F -d /tmp/e2sar/rgeorge-io500/io500_data/mdtest-hard -x /home/rgeorge/io500_8326336_1-n/mdtest-hard.stonewall -C -Y -W 300 --saveRankPerformanceDetails=/home/rgeorge/io500_8326336_1-n/mdtest-hard-write.csv -a DFS --dfs.pool=e2sar --dfs.cont=rgeorge-io500 --dfs.dir_oclass=RP_2GX --dfs.oclass=RP_2G1
rate-stonewall  = 28.468252
score           = 28.432556
t_delta         = 302.9975
t_end           = 2026-02-15 06:32:01
```


## Outputs
- I've kept every job I submitted on e2sar2 in order here just in case, but really half of these were accidental and do not provide information to the issue

### 1. `qsub_mdt_file.qsub.o8394431`
- Accidentally did nothing due to reorganizing my home directory and moving the ior install

### 2. `qsub_mdt_file.qsub.o8394453`
- This is where I somehow accidentally filled up the storage again, although it ends due to insufficient walltime, with no errors so I did not notice initially

### 3. `qsub_mdt_file.qsub.o8394552`
- Forgot to remove container from previous job. Nothing happened.

### 4. `qsub_mdt_file.qsub.o8394697`
- I realized the storage was full from `o8394453` after this attempted to make a container, but failed due to no space

