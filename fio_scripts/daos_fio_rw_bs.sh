#!/bin/bash

# Usage: ./daos_fio_rw_bs.sh <username> <pool_name> [container_base_name]

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
USER="${1}"
POOL_NAME="${2}"
CONTAINER_BASE_NAME="${3:-fio_test}"
MOUNT_BASE="/tmp/$USER/$POOL_NAME"
RESULTS_DIR="./fio_results_$(date +%Y-%m-%d_%H-%M-%S)"
NUM_JOBS=8
IO_DEPTH=16
DIRECT=1
BUFFERED=0

# Values for --bs
# BLOCK_SIZES=("4K") # mini for testing
BLOCK_SIZES=("4K" "16K" "1M" "2M" "4M")
# Keys for setting --rw and --rwmixread
# RW_CATEGORIES=("SeqR") # mini for testing
RW_CATEGORIES=("SeqR" "SeqRH" "SeqBal" "SeqWH" "SeqW" "RandR" "RandRH" "RandBal" "RandWH" "RandW")
get_fio_rw_params() {
    local category="$1"
    case "$category" in
        "SeqR") echo "--rw=read" ;;
        "SeqRH") echo "--rw=rw --rwmixread=80" ;;
        "SeqBal") echo "--rw=rw" ;;
        "SeqWH") echo "--rw=rw --rwmixread=20" ;;
        "SeqW") echo "--rw=write" ;;
        "RandR") echo "--rw=randread" ;;
        "RandRH") echo "--rw=randrw --rwmixread=80" ;;
        "RandBal") echo "--rw=randrw" ;;
        "RandWH") echo "--rw=randrw --rwmixread=20" ;;
        "RandW") echo "--rw=randwrite" ;;
        *) echo "ERROR: Unknown category $category"; return 1 ;;
    esac
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Cleanup function
cleanup() {
    local pool_name="$1"
    local container_name="$2"
    local mount_point="$3"
    
    echo "Cleaning up container: $container_name"
    
    # Unmount if mounted
    if mount | grep -q "$mount_point"; then
        echo "Unmounting $mount_point"
        fusermount3 -u "$mount_point" || warning "Failed to unmount $mount_point"
        sleep 2
    fi
    
    # Remove mount point
    if [ -d "$mount_point" ]; then
        rmdir "$mount_point" || warning "Failed to remove directory $mount_point"
    fi
    
    # Destroy container
    echo "Destroying container $container_name"
    daos container destroy "$pool_name" "$container_name" || warning "Failed to destroy container $container_name"
}

# Check if pool name is provided
if [ -z "$POOL_NAME" ]; then
    error "Usage: $0 <pool_name> [container_base_name]"
    error "Example: $0 my_pool fio_test"
    exit 1
fi

# Create results directory
mkdir -p $RESULTS_DIR

# Load DAOS module
echo "Loading DAOS module"
module use /soft/modulefiles/ || { error "Failed to use modulefiles"; exit 1; }
module load daos || { error "Failed to load DAOS module"; exit 1; }

# Verify pool exists
echo "Verifying pool '$POOL_NAME' is Ready"
if ! daos pool query "$POOL_NAME" | grep -q "Ready" ; then
    error "Pool '$POOL_NAME' not Ready"
    exit 1
fi
success "Pool '$POOL_NAME' found and accessible"

# read-write category loop
for rw_cat in "${RW_CATEGORIES[@]}"; do
    RW_PARAMS=$(get_fio_rw_params "$rw_cat")
    # block size loop
    for bs in "${BLOCK_SIZES[@]}"; do

        CONTAINER_NAME="${CONTAINER_BASE_NAME}_${rw_cat}_${bs}"
        MOUNT_POINT="$MOUNT_BASE/$CONTAINER_NAME"
        echo "----------------------------------------"
        echo "Read-write category: $rw_cat"
        echo "Block Size: $bs"
        
        # Create container
        echo "Creating container: $CONTAINER_NAME"
        if ! daos container create --type=POSIX "$POOL_NAME" "$CONTAINER_NAME"; then
            error "Failed to create container $CONTAINER_NAME"
            continue
        fi
        
        # Create mount directory
        echo "Creating mount directory: $MOUNT_POINT"
        mkdir -p "$MOUNT_POINT"
        
        # Mount filesystem
        echo "Doing start-dfuse.sh"
        if ! start-dfuse.sh -m "$MOUNT_POINT" --pool "$POOL_NAME" --container "$CONTAINER_NAME"; then
            error "Failed to mount filesystem for container $CONTAINER_NAME"
            cleanup "$POOL_NAME" "$CONTAINER_NAME" "$MOUNT_POINT"
            continue
        fi


        # Build FIO command
        fio_cmd="fio"
        fio_cmd+=" --name=${rw_cat}-${bs}"
        fio_cmd+=" --ioengine=pvsync"
        fio_cmd+=" ${RW_PARAMS} --bs=${bs}"
        fio_cmd+=" --size=128M --nrfiles=4"
        fio_cmd+=" --directory=${MOUNT_POINT}"
        fio_cmd+=" --numjobs=${NUM_JOBS} --iodepth=${IO_DEPTH}"
        fio_cmd+=" --runtime=60 --time_based"
        fio_cmd+=" --direct=${DIRECT} --buffered=${BUFFERED}"
        fio_cmd+=" --randrepeat=0 --norandommap --refill_buffers --group_reporting"
        fio_cmd+=" --output-format=terse"
        fio_cmd+=" --output=${RESULTS_DIR}/fio_result_${rw_cat}_${bs}.csv"
        fio_cmd+=" --description=${rw_cat}-${bs}"

        echo "Doing $fio_cmd"
        ${fio_cmd} 
        success "FIO benchmark completed for block size $bs and read-write setting $rw_cat"
        
        # Cleanup
        cleanup "$POOL_NAME" "$CONTAINER_NAME" "$MOUNT_POINT"
        
        sleep 3
        echo "----------------------------------------"
    done

done
