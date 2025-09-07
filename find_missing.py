import os
import pandas as pd

BLOCK_SIZES=["4K", "16K", "1M", "2M", "4M"]
RW_CATEGORIES=["SeqR", "SeqRH", "SeqBal", "SeqWH", "SeqW", "RandR", "RandRH", "RandBal", "RandWH", "RandW"]
NUM_JOBS_SIZES=["16", "32", "64", "128"]
IO_DEPTHS=["1", "4", "8", "16", "32", "64", "128"]


full_list = []
for bs in BLOCK_SIZES:
    for rw_cat in RW_CATEGORIES:
        for nj in NUM_JOBS_SIZES:
            for iod in IO_DEPTHS:

                CASE_ID=f"{rw_cat}-{bs}-{nj}-{iod}"
                fname = f"fio_{CASE_ID}.json"
                full_list.append(fname)

json_dir = "fio_results"
actual = []
for file_name in os.listdir(json_dir):
    actual.append(file_name)

missing = list(set(full_list) - set(actual))
missing = pd.Series(missing)
with open('missing.txt', 'a') as f:
    f.write(missing.to_string())



ser = pd.Series(actual)
freq_tab = ser.value_counts()
print(max(freq_tab))

with open('freq.txt', 'a') as f:
    f.write(freq_tab.to_string())
