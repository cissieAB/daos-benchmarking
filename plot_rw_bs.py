import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
import io
import os 

png_dir = "graphs"

'''
Terse output headers:
terse_version_3;fio_version;jobname;groupid;error;read_kb;read_bandwidth_kb;read_iops;read_runtime_ms;read_slat_min_us;read_slat_max_us;read_slat_mean_us;read_slat_dev_us;read_clat_min_us;read_clat_max_us;read_clat_mean_us;read_clat_dev_us;read_clat_pct01;read_clat_pct02;read_clat_pct03;read_clat_pct04;read_clat_pct05;read_clat_pct06;read_clat_pct07;read_clat_pct08;read_clat_pct09;read_clat_pct10;read_clat_pct11;read_clat_pct12;read_clat_pct13;read_clat_pct14;read_clat_pct15;read_clat_pct16;read_clat_pct17;read_clat_pct18;read_clat_pct19;read_clat_pct20;read_tlat_min_us;read_lat_max_us;read_lat_mean_us;read_lat_dev_us;read_bw_min_kb;read_bw_max_kb;read_bw_agg_pct;read_bw_mean_kb;read_bw_dev_kb;write_kb;write_bandwidth_kb;write_iops;write_runtime_ms;write_slat_min_us;write_slat_max_us;write_slat_mean_us;write_slat_dev_us;write_clat_min_us;write_clat_max_us;write_clat_mean_us;write_clat_dev_us;write_clat_pct01;write_clat_pct02;write_clat_pct03;write_clat_pct04;write_clat_pct05;write_clat_pct06;write_clat_pct07;write_clat_pct08;write_clat_pct09;write_clat_pct10;write_clat_pct11;write_clat_pct12;write_clat_pct13;write_clat_pct14;write_clat_pct15;write_clat_pct16;write_clat_pct17;write_clat_pct18;write_clat_pct19;write_clat_pct20;write_tlat_min_us;write_lat_max_us;write_lat_mean_us;write_lat_dev_us;write_bw_min_kb;write_bw_max_kb;write_bw_agg_pct;write_bw_mean_kb;write_bw_dev_kb;cpu_user;cpu_sys;cpu_csw;cpu_mjf;cpu_minf;iodepth_1;iodepth_2;iodepth_4;iodepth_8;iodepth_16;iodepth_32;iodepth_64;lat_2us;lat_4us;lat_10us;lat_20us;lat_50us;lat_100us;lat_250us;lat_500us;lat_750us;lat_1000us;lat_2ms;lat_4ms;lat_10ms;lat_20ms;lat_50ms;lat_100ms;lat_250ms;lat_500ms;lat_750ms;lat_1000ms;lat_2000ms;lat_over_2000ms;disk_name;disk_read_iops;disk_write_iops;disk_read_merges;disk_write_merges;disk_read_ticks;write_ticks;disk_queue_time;disk_util
'''
terse_shortnames = io.StringIO("terse_version_3;fio_version;jobname;groupid;error;read_kb;read_bandwidth_kb;read_iops;read_runtime_ms;read_slat_min_us;read_slat_max_us;read_slat_mean_us;read_slat_dev_us;read_clat_min_us;read_clat_max_us;read_clat_mean_us;read_clat_dev_us;read_clat_pct01;read_clat_pct02;read_clat_pct03;read_clat_pct04;read_clat_pct05;read_clat_pct06;read_clat_pct07;read_clat_pct08;read_clat_pct09;read_clat_pct10;read_clat_pct11;read_clat_pct12;read_clat_pct13;read_clat_pct14;read_clat_pct15;read_clat_pct16;read_clat_pct17;read_clat_pct18;read_clat_pct19;read_clat_pct20;read_tlat_min_us;read_lat_max_us;read_lat_mean_us;read_lat_dev_us;read_bw_min_kb;read_bw_max_kb;read_bw_agg_pct;read_bw_mean_kb;read_bw_dev_kb;write_kb;write_bandwidth_kb;write_iops;write_runtime_ms;write_slat_min_us;write_slat_max_us;write_slat_mean_us;write_slat_dev_us;write_clat_min_us;write_clat_max_us;write_clat_mean_us;write_clat_dev_us;write_clat_pct01;write_clat_pct02;write_clat_pct03;write_clat_pct04;write_clat_pct05;write_clat_pct06;write_clat_pct07;write_clat_pct08;write_clat_pct09;write_clat_pct10;write_clat_pct11;write_clat_pct12;write_clat_pct13;write_clat_pct14;write_clat_pct15;write_clat_pct16;write_clat_pct17;write_clat_pct18;write_clat_pct19;write_clat_pct20;write_tlat_min_us;write_lat_max_us;write_lat_mean_us;write_lat_dev_us;write_bw_min_kb;write_bw_max_kb;write_bw_agg_pct;write_bw_mean_kb;write_bw_dev_kb;cpu_user;cpu_sys;cpu_csw;cpu_mjf;cpu_minf;iodepth_1;iodepth_2;iodepth_4;iodepth_8;iodepth_16;iodepth_32;iodepth_64;lat_2us;lat_4us;lat_10us;lat_20us;lat_50us;lat_100us;lat_250us;lat_500us;lat_750us;lat_1000us;lat_2ms;lat_4ms;lat_10ms;lat_20ms;lat_50ms;lat_100ms;lat_250ms;lat_500ms;lat_750ms;lat_1000ms;lat_2000ms;lat_over_2000ms;disk_name;disk_read_iops;disk_write_iops;disk_read_merges;disk_write_merges;disk_read_ticks;write_ticks;disk_queue_time;disk_util")
col_df = pd.read_csv(terse_shortnames, sep=';')
cols = col_df.columns.tolist()
cols = cols[:-9] # it seems the last 9 short names provided are unused by my outputs
cols.append("description")

bs_map = {
    '4K':4096,
    '16K':16384,
    '1M':1048576,
    '2M':2097152,
    '4M':4194304 
}
rw_map = {
    'SeqR':'Sequential Read-only',
    'SeqRH':'Sequential Read-heavy 4:1',
    'SeqBal':'Sequential Balanced 1:1',
    'SeqWH':'Sequential Write-heavy 1:4',
    'SeqW':'Sequential Write-only',
    'RandR':'Random Read-only',
    'RandRH':'Random Read-heavy 4:1',
    'RandBal':'Random Balanced 1:1',
    'RandWH':'Random Write-heavy 1:4',
    'RandW':'Random Write-only'
}
hue_order = ['Sequential Read-only','Sequential Read-heavy 4:1','Sequential Balanced 1:1','Sequential Write-heavy 1:4','Sequential Write-only','Random Read-only','Random Read-heavy 4:1','Random Balanced 1:1','Random Write-heavy 1:4','Random Write-only']
sns.set_style("whitegrid")
palette = sns.color_palette("flare", 5) + sns.color_palette("crest", 5)


csv_dir = "fio_results_2025-08-18_11-13-20"
first = True
for file_name in os.listdir(csv_dir):
    full_path = os.path.join(csv_dir, file_name)
    if os.path.isfile(full_path):
        # print(f"File: {file_name}")
        if first:
            df = pd.read_csv(full_path, sep=';', header=None, names=cols)
            first = False
        else:
            tmp = pd.read_csv(full_path, sep=';', header=None, names=cols)
            df = pd.concat([df, tmp])

df["rw-cat"] = df["description"].str.extract(r'(.*)-')
df["rw_full"] = df["rw-cat"].map(rw_map)
df["bs"] = df["description"].str.extract(r'-(.*)')
df["bs_num"] = df["bs"].map(bs_map)
# df["nj"] = df["description"].str.extract(r'-.*-(.*)')

df.to_csv("fio_results_2025-08-18_11-13-20.csv")

################### BANDWIDTH PLOTS ###################

ax = sns.lineplot(
    data=df,
    x="bs_num",
    y="read_bw_mean_kb",
    hue="rw_full", 
    marker="o",
    hue_order=hue_order,
    palette=palette
)
# ax.set_aspect('equal')
ax.set_xlabel("Block Size (bytes)")
ax.set_ylabel("Mean Read Bandwidth (KiB/s)")
ax.set_title("Mean Read Bandwidth vs Block Size")
ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/read_bw_mean_kb-bs.svg"), bbox_inches="tight")
plt.clf()

ax = sns.lineplot(
    data=df,
    x="nj",
    y="read_bw_mean_kb",
    hue="rw_full", 
    marker="o",
    hue_order=hue_order,
    palette=palette
)
# ax.set_aspect('equal')
ax.set_xlabel("Number of Jobs")
ax.set_ylabel("Mean Read Bandwidth (KiB/s)")
ax.set_title("Mean Read Bandwidth vs Number of Jobs")
ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/read_bw_mean_kb-nj.svg"), bbox_inches="tight")
plt.clf()

ax = sns.lineplot(
    data=df,
    x="bs_num",
    y="read_bandwidth_kb",
    hue="rw_full", 
    marker="o",
    hue_order=hue_order,
    palette=palette
)
ax.set_aspect('equal')
ax.set_xlabel("Block Size (bytes)")
ax.set_ylabel("Read Bandwidth (KiB/s)")
ax.set_title("Read Bandwidth vs Block Size")
ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/read_bandwidth_kb.svg"), bbox_inches="tight")
plt.clf()

ax = sns.lineplot(
    data=df,
    x="bs_num",
    y="write_bw_mean_kb",
    hue="rw_full", 
    marker="o",
    hue_order=hue_order,
    palette=palette
)
ax.set_aspect('equal')
ax.set_xlabel("Block Size (bytes)")
ax.set_ylabel("Mean Write Bandwidth (KiB/s)")
ax.set_title("Mean Write Bandwidth vs Block Size")
ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/write_bw_mean_kb-bs.svg"), bbox_inches="tight")
plt.clf()

ax = sns.lineplot(
    data=df,
    x="nj",
    y="write_bw_mean_kb",
    hue="rw_full", 
    marker="o",
    hue_order=hue_order,
    palette=palette
)
ax.set_aspect('equal')
ax.set_xlabel("Number of Jobs")
ax.set_ylabel("Mean Write Bandwidth (KiB/s)")
ax.set_title("Mean Write Bandwidth vs Number of Jobs")
ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/write_bw_mean_kb-nj.svg"), bbox_inches="tight")
plt.clf()

ax = sns.lineplot(
    data=df,
    x="bs_num",
    y="write_bandwidth_kb",
    hue="rw_full", 
    marker="o",
    hue_order=hue_order,
    palette=palette
)
ax.set_aspect('equal')
ax.set_xlabel("Block Size (bytes)")
ax.set_ylabel("Write Bandwidth (KiB/s)")
ax.set_title("Read Bandwidth vs Block Size")
ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/write_bandwidth_kb.svg"), bbox_inches="tight")
plt.clf()

################### IOPS PLOTS ###################

ax = sns.lineplot(
    data=df,
    x="bs_num",
    y="write_iops",
    hue="rw_full", 
    marker="o",
    hue_order=hue_order,
    palette=palette
)
# ax.set_aspect('equal')
ax.set_xlabel("Block Size (bytes)")
ax.set_ylabel("Write IOPS")
ax.set_title("Write IOPS vs Block Size")
ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/write_iops.svg"), bbox_inches="tight")
plt.clf()

ax = sns.lineplot(
    data=df,
    x="bs_num",
    y="read_iops",
    hue="rw_full", 
    marker="o",
    hue_order=hue_order,
    palette=palette
)
# ax.set_aspect('equal')
ax.set_xlabel("Block Size (bytes)")
ax.set_ylabel("Read IOPS")
ax.set_title("Read IOPS vs Block Size")
ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/read_iops.svg"), bbox_inches="tight")
plt.clf()

################### LATENCY PLOTS ###################

ax = sns.lineplot(
    data=df,
    x="bs_num",
    y="write_lat_mean_us",
    hue="rw_full", 
    marker="o",
    hue_order=hue_order,
    palette=palette
)
# ax.set_aspect('equal')
ax.set_xlabel("Block Size (bytes)")
ax.set_ylabel("Mean Write Latency (us)")
ax.set_title("Mean Write Latency vs Block Size")
ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/write_lat_mean_us.svg"), bbox_inches="tight")
plt.clf()

ax = sns.lineplot(
    data=df,
    x="bs_num",
    y="read_lat_mean_us",
    hue="rw_full", 
    marker="o",
    hue_order=hue_order,
    palette=palette
)
# ax.set_aspect('equal')

'''
# potentially useful, needs overlap fix:
# ref: https://stackoverflow.com/questions/73069802/how-to-label-end-of-lines-of-plot-area-seaborn-or-matplotlib
last_values = df[["rw_full", "read_lat_mean_us"]][df["bs_num"] == df["bs_num"].max()]
for cat, value in last_values.itertuples(index=False):
    ax.text(x=df["bs_num"].max() + 0.2, y=value, s=cat, va="center")
'''

ax.set_xlabel("Block Size (bytes)")
ax.set_ylabel("Mean Read Latency (us)")
ax.set_title("Mean Read Latency vs Block Size")
ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/read_lat_mean_us.svg"), bbox_inches="tight")
plt.clf()
