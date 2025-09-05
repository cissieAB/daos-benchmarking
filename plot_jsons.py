import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
import numpy as np
import io
import os 
import json

png_dir = "graphs"
json_dir = "fio_results"

bs_map = {
    '4K':4096,
    '16K':16384,
    '1M':1048576,
    '2M':2097152,
    '4M':4194304 
}
bs_order = [
    '4K',
    '16K',
    '1M',
    '2M',
    '4M' 
]

rw_map = {
    'read-':'Sequential Read-only',
    'rw-80':'Sequential Read-heavy 4:1',
    'rw-':'Sequential Balanced 1:1',
    'rw-20':'Sequential Write-heavy 1:4',
    'write-':'Sequential Write-only',
    'randread-':'Random Read-only',
    'randrw-80':'Random Read-heavy 4:1',
    'randrw-':'Random Balanced 1:1',
    'randrw-20':'Random Write-heavy 1:4',
    'randwrite-':'Random Write-only'
}
# wanted to use this dict to label lines.. 
marker_dict = {
    'Sequential Read-only':'SR',
    'Sequential Read-heavy 4:1':'SRH',
    'Sequential Balanced 1:1':'SB',
    'Sequential Write-heavy 1:4':'SWH',
    'Sequential Write-only':'SW',
    'Random Read-only':'RR',
    'Random Read-heavy 4:1':'RRH',
    'Random Balanced 1:1':'RB',
    'Random Write-heavy 1:4':'RWH',
    'Random Write-only':'RW'
}
hue_order = ['Sequential Read-only','Sequential Read-heavy 4:1','Sequential Balanced 1:1','Sequential Write-heavy 1:4','Sequential Write-only','Random Read-only','Random Read-heavy 4:1','Random Balanced 1:1','Random Write-heavy 1:4','Random Write-only']
sns.set_style("whitegrid")
palette = sns.color_palette("magma", 5) 


# Assemble columns names
rwfile = 'rw_json_example.json'
mixfile = 'mix_json_example.json'
cols = pd.json_normalize(pd.read_json(rwfile)['jobs']).columns.tolist() + pd.json_normalize(pd.read_json(mixfile)['jobs']).columns.tolist() 
cols = list(set(cols))


# Read in json files
first = True
df = pd.DataFrame()
for file_name in os.listdir(json_dir):
    file = os.path.join(json_dir, file_name)

    tmp = pd.json_normalize(pd.read_json(file)['jobs'])
    # tmp = tmp.reindex(columns=cols)

    for col in tmp.select_dtypes(include=['int', 'int64', 'int32']).columns:
        tmp[col] = tmp[col].astype(float)

    if first:
        df = tmp
        first = False
    else:
        # df = pd.merge(tmp, df, how="outer", on=cols)
        df = pd.concat([tmp, df])
df = df.copy()

# with open("df.txt", 'a') as f:
#     f.write(df.to_string())


# Read-Write
df['job options.rwmixread']
df['rw_code'] = df['job options.rw'].str.cat(df['job options.rwmixread'], sep='-', na_rep='')
df["rw_full"] = df["rw_code"].map(rw_map)
unique_rw = df["rw_full"].unique()
print(unique_rw)

# Block Size 
df['bs_num'] = df['job options.bs'].map(bs_map)

# Helper function to combine mixes/read/write outputs into one column for plotting
def get_var(row, colname):
    var_cols = ['mixed.'+colname, 'read.'+colname, 'write.'+colname]
    for col in var_cols:
        if col in row.index:
            var = row[col]
            if pd.notna(var) and var != 0:
                return var, col
    return np.nan, None

# Bandwidth
df['bw_mean']  = df.apply(lambda row: get_var(row, 'bw_mean')[0], axis=1)
df['bw_mean'] = df['bw_mean']/(1024*1024)

# Iops
df['iops'] = df.apply(lambda row: get_var(row, 'iops')[0], axis=1)

# Latency
df['lat_ns.mean'] = df.apply(lambda row: get_var(row, 'lat_ns.mean')[0], axis=1)
df['lat_ns.percentile.99.000000'] = df.apply(lambda row: get_var(row, 'lat_ns.percentile.99.000000')[0], axis=1)


#### COLUMN NAMES ####
#####   Variables:  
# "job options.iodepth" : io depth
# "job options.numjobs" : number of jobs
# "job options.bs" : block size
# "rw_full" : read write type (human readable)
#
#####   Outputs:    
# "bw_mean" : mean bandwidth
# "iops" : iops
# "lat_ns.mean" : mean latency
# "lat_ns.percentile.99.000000" : 99% latency
######################


################### BANDWIDTH PLOTS ###################

# BANDWIDTH vs NUMJOBS
ax = sns.lineplot(
    data=df,
    x="job options.numjobs",
    y="bw_mean",
    hue="rw_full", 
    style="rw_full",
    # marker=False,
    # hue_order=hue_order,
    palette=palette
)
# ax.set_aspect('equal')
ax.set_xticks(df["job options.numjobs"].unique())
ax.set_xticklabels(df['job options.numjobs'].unique())
# ax.set_yticks(df['read_bw_mean_gb'])
# ax.set_yticklabels(df['read_bw_mean_gb'])
ax.set_xlabel("Number of Jobs")
ax.set_ylabel("Mean Bandwidth (GiB/s)")
ax.set_title("Mean Bandwidth vs Number of Jobs ")
# ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/bw_mean_gb-nj.svg"), bbox_inches="tight")
plt.clf()


# BANDWIDTH vs BLOCK SIZE
ax = sns.lineplot(
    data=df,
    x="bs_num",
    y="bw_mean",
    hue="rw_full", 
    style="rw_full",
    # marker=False,
    # hue_order=hue_order,
    palette=palette
)
# ax.set_aspect('equal')
ax.set_xticks(df["bs_num"].unique())
ax.set_xticklabels(df['bs_num'].unique())
# ax.set_yticks(df['read_bw_mean_gb'])
# ax.set_yticklabels(df['read_bw_mean_gb'])
ax.set_xlabel("Block Size")
ax.set_ylabel("Mean Bandwidth (GiB/s)")
ax.set_title("Mean Bandwidth vs Block Size")
ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/bw_mean_gb-bs.svg"), bbox_inches="tight")
plt.clf()

g = sns.catplot(data=df,
                kind="bar",
                x="job options.bs", 
                hue="rw_full", 
                y="bw_mean",
                row="job options.numjobs",
                # width=5,
                hue_order=hue_order,
                order=bs_order,
                height=5, aspect=1.5,
                sharex=False)

for ax in g.axes.flat:
    ax.set_ylabel("Bandwidth (GiB/s)")
    ax.tick_params(axis='x', labelbottom=True)  
    # ax.set_xticklabels(df['job options.bs'].unique())   
    ax.margins(x=0.1)
    # for container in ax.containers:
    #     ax.bar_label(container)

g.savefig((png_dir + "/bs-bars.svg"), bbox_inches="tight")
plt.clf()



'''

df["read_bw_mean_gb"] = df["read_bw_mean_kb"]/(1024*1024)
ax = sns.lineplot(
    data=df,
    x="nj",
    y="read_bw_mean_gb",
    hue="iod", 
    marker="o",
    # hue_order=hue_order,
    palette=palette
)
# ax.set_aspect('equal')
ax.set_xticks(df["nj"].unique())
ax.set_xticklabels(df['nj'].unique())
# ax.set_yticks(df['read_bw_mean_gb'])
# ax.set_yticklabels(df['read_bw_mean_gb'])
ax.set_xlabel("Number of Jobs")
ax.set_ylabel("Mean Read Bandwidth (GiB/s)")
ax.set_title("Mean Read Bandwidth vs Number of Jobs ")
# ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/read_bw_mean_gb-nj.svg"), bbox_inches="tight")
plt.clf()

df["write_bw_mean_gb"] = df["write_bw_mean_kb"]/(1024*1024)

ax = sns.lineplot(
    data=df,
    x="nj",
    y="write_bw_mean_gb",
    hue="iod", 
    marker="o",
    # hue_order=hue_order,
    palette=palette
)
ax.set_xticks(df['nj'].unique())
ax.set_xticklabels(df['nj'].unique())
# ax.set_yticks(df['write_bw_mean_gb'])
# ax.set_yticklabels(df['write_bw_mean_gb'])
ax.set_xlabel("Number of Jobs")
ax.set_ylabel("Mean Write Bandwidth (GiB/s)")
ax.set_title("Mean Write Bandwidth vs Number of Jobs")
# ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/write_bw_mean_gb-nj.svg"), bbox_inches="tight")
plt.clf()


################### IOPS PLOTS ###################

ax = sns.lineplot(
    data=df,
    x="nj",
    y="write_iops",
    hue="iod", 
    marker="o",
    # hue_order=hue_order,
    palette=palette
)
# ax.set_aspect('equal')
ax.set_xticks(df['nj'].unique())
ax.set_xticklabels(df['nj'].unique())
# ax.set_yticks(df['write_iops'])
# ax.set_yticklabels(df['write_iops'])
ax.set_xlabel("Number of Jobs")
ax.set_ylabel("Write IOPS")
ax.set_title("Write IOPS vs Number of Jobs")
# ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/write_iops-nj.svg"), bbox_inches="tight")
plt.clf()

ax = sns.lineplot(
    data=df,
    x="nj",
    y="read_iops",
    hue="iod", 
    marker="o",
    # hue_order=hue_order,
    palette=palette
)
# ax.set_aspect('equal')
ax.set_xticks(df['nj'].unique())
ax.set_xticklabels(df['nj'].unique())
# ax.set_yticks(df['read_iops'])
# ax.set_yticklabels(df['read_iops'])
ax.set_xlabel("Number of Jobs")
ax.set_ylabel("Read IOPS")
ax.set_title("Read IOPS vs Number of Jobs ")
# ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/read_iops-nj.svg"), bbox_inches="tight")
plt.clf()

################### LATENCY PLOTS ###################

ax = sns.lineplot(
    data=df,
    x="nj",
    y="write_lat_mean_us",
    hue="iod", 
    marker="o",
    # hue_order=hue_order,
    palette=palette
)
# ax.set_aspect('equal')
ax.set_xticks(df['nj'].unique())
ax.set_xticklabels(df['nj'].unique())
# ax.set_yticks(df['write_lat_mean_us'])
# ax.set_yticklabels(df['write_lat_mean_us'])
ax.set_xlabel("Number of Jobs")
ax.set_ylabel("Mean Write Latency (us)")
ax.set_title("Mean Write Latency vs Number of Jobs")
# ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/write_lat_mean_us-nj.svg"), bbox_inches="tight")
plt.clf()

ax = sns.lineplot(
    data=df,
    x="nj",
    y="read_lat_mean_us",
    hue="iod", 
    marker="o",
    # hue_order=hue_order,
    palette=palette
)
# ax.set_aspect('equal')
ax.set_xticks(df['nj'].unique())
ax.set_xticklabels(df['nj'].unique())
# ax.set_yticks(df['read_lat_mean_us'])
# ax.set_yticklabels(df['read_lat_mean_us'])
ax.set_xlabel("Number of Jobs")
ax.set_ylabel("Mean Read Latency (us)")
ax.set_title("Mean Read Latency vs Number of Jobs")
# ax.legend(bbox_to_anchor=(1, 1), title='Read-Write Type')
plt.savefig((png_dir + "/read_lat_mean_us-nj.svg"), bbox_inches="tight")
plt.clf()

df.to_csv("fio_results_nj_iops_2025-08-28_01-03-23.csv")
'''