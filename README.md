# daos-benchmarking
Notes doc: https://docs.google.com/document/d/1mf2JfuIG7SXV3KOU3kDi35w4nssFurwodq81qu-ZrRA/edit?usp=sharing 

# Graphs
All pictures are inside /graphs

Missing cases are due to failed container creation here. I don't like results presented for NJ, although all test cases are present, I had removed time based to see if some cases were getting cut off (before I realized my containers issue). 

I created a version I thought would be good but it has not been running even when I have just one fio command it should be doing - on tiny it will run for a while and give nothing and on debug it exits immediately. Right now `daos pool list` has been giving :

```
rgeorge@aurora-uan-0009:~/daos-benchmarking> module use /soft/modulefiles/
rgeorge@aurora-uan-0009:~/daos-benchmarking> module load daos
rgeorge@aurora-uan-0009:~/daos-benchmarking> daos pool list
mgmt ERR  src/mgmt/cli_mgmt.c:1408 dc_mgmt_pool_list() rpc send failed: DER_TIMEDOUT(-1011): 'Time out'
^C
```

![Mean Read BW vs BS](graphs/read_bw_mean_gb-bs.svg)
![Mean Write BW vs BS](graphs/write_bw_mean_gb-bs.svg)
![Read IOPS vs BS](graphs/read_iops-bs.svg)
![Write IOPS vs BS](graphs/write_iops-bs.svg)
![Mean Read Latencyvs BS](graphs/read_lat_mean_us-bs.svg)
![Mean Write Latency vs BS](graphs/write_lat_mean_us-bs.svg)

![Mean Read BW vs NJ](graphs/read_bw_mean_gb-nj.svg)
![Mean Write BW vs NJ](graphs/write_bw_mean_gb-nj.svg)
![Read IOPS vs NJ](graphs/read_iops-nj.svg)
![Write IOPS vs NJ](graphs/write_iops-nj.svg)
![Mean Read Latency vs NJ](graphs/read_lat_mean_us-nj.svg)
![Mean Write Latency vs NJ](graphs/write_lat_mean_us-nj.svg)
