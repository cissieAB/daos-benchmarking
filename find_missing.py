import os
import pandas as pd

json_dir = "fio_results"
actual = []
for file_name in os.listdir(json_dir):
    actual.append(file_name)

BLOCK_SIZES=["4K", "16K", "1M", "2M", "4M"]
RW_CATEGORIES=["SeqR", "SeqRH", "SeqBal", "SeqWH", "SeqW", "RandR", "RandRH", "RandBal", "RandWH", "RandW"]
NUM_JOBS_SIZES=["16", "32", "64", "128"]
IO_DEPTHS=["1", "4", "8", "16", "32", "64", "128"]

rw_map = {
        "SeqR":"--rw=read                     --unified_rw_reporting=0",
        "SeqRH":"--rw=rw       --rwmixread=80  --unified_rw_reporting=1",
        "SeqBal":"--rw=rw                       --unified_rw_reporting=1",
        "SeqWH":"--rw=rw       --rwmixread=20  --unified_rw_reporting=1",
        "SeqW":"--rw=write                    --unified_rw_reporting=0",
        "RandR":"--rw=randread                 --unified_rw_reporting=0",
        "RandRH":"--rw=randrw   --rwmixread=80  --unified_rw_reporting=1",
        "RandBal":"--rw=randrw                   --unified_rw_reporting=1",
        "RandWH":"--rw=randrw   --rwmixread=20  --unified_rw_reporting=1",
        "RandW":"--rw=randwrite                --unified_rw_reporting=0"
}
ids=[]
params = []
# full_list = []
for bs in BLOCK_SIZES:
    for rw_cat in RW_CATEGORIES:
        for nj in NUM_JOBS_SIZES:
            for iod in IO_DEPTHS:
                CASE_ID=f"{rw_cat}-{bs}-{nj}-{iod}"
                fname = f"fio_{CASE_ID}.json"
                if fname not in actual:
                    rw_full = rw_map[rw_cat]
                    p = f'{rw_cat} --bs={bs} --numjobs={nj} --iodepth={iod}'
                    ids.append(CASE_ID)
                    params.append(p)
                # full_list.append(fname)

bash_param_str = "("
for p in params:
    bash_param_str += f"\'{p}\' "
bash_param_str += ")"
print(bash_param_str)


# params = pd.Series(params)
# missing = list(set(full_list) - set(actual))
# missing = pd.Series(missing)

# with open('missing-params.txt', 'a') as f:
#     f.write(params.to_string())

# with open('missing.txt', 'a') as f:
#     f.write(missing.to_string())

# ser = pd.Series(actual)
# freq_tab = ser.value_counts()
# # print(max(freq_tab))

# with open('freq.txt', 'a') as f:
#     f.write(freq_tab.to_string())
