# daos-benchmarking
Notes doc: https://docs.google.com/document/d/1mf2JfuIG7SXV3KOU3kDi35w4nssFurwodq81qu-ZrRA/edit?usp=sharing 

# Graphs
All pictures are inside /graphs

From new json runs
![bar block size](graphs/bs-bars.svg)
![bar block size](graphs/bw_mean_gb-nj.svg)
![bar block size](graphs/iops-nj.svg)
![bar block size](graphs/iops-bs-bars.svg)
![bar block size](graphs/mean-lat-nj.svg)
![bar block size](graphs/mean-lat-bs-bars.svg)
![bar block size](graphs/mean-lat-nj-99.svg)
![bar block size](graphs/mean-lat-bs-bars-99.svg)


For the following graphs,  `--numjobs=16 --iodepth=32`

![Mean Read BW vs BS](graphs/read_bw_mean_gb-bs.svg)
![Mean Write BW vs BS](graphs/write_bw_mean_gb-bs.svg)
![Read IOPS vs BS](graphs/read_iops-bs.svg)
![Write IOPS vs BS](graphs/write_iops-bs.svg)
![Mean Read Latencyvs BS](graphs/read_lat_mean_us-bs.svg)
![Mean Write Latency vs BS](graphs/write_lat_mean_us-bs.svg)


For the following graphs, `--rw=randread --bs=2M`

![Mean Read BW vs NJ](graphs/read_bw_mean_gb-nj.svg)
![Mean Write BW vs NJ](graphs/write_bw_mean_gb-nj.svg)
![Read IOPS vs NJ](graphs/read_iops-nj.svg)
![Write IOPS vs NJ](graphs/write_iops-nj.svg)
![Mean Read Latency vs NJ](graphs/read_lat_mean_us-nj.svg)
![Mean Write Latency vs NJ](graphs/write_lat_mean_us-nj.svg)
