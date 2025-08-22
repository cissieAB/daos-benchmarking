# daos-benchmarking
Notes doc: https://docs.google.com/document/d/1mf2JfuIG7SXV3KOU3kDi35w4nssFurwodq81qu-ZrRA/edit?usp=sharing 

# Graphs
All pictures are inside /graphs

When --runtime is not set, so there is not a limit, and --time_based is not set, so it does not force it to loop over the workload for the given time, these graphs look much more erratic. Unsetting this runtime did not fix the issue of some read-write/block-size/num-jobs combinations not running..

Graphs shown are from when these parameters are set.

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
