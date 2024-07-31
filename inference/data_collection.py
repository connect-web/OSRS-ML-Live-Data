import time
import numpy as np
from .processing.formatting import format_row

from .queries import get_hiscore_rows

def get_hiscore(activity, limit=1000, offset=0, activity_type='skills'):
    rows = get_hiscore_rows(activity, limit=limit, offset=offset, activity_type=activity_type)
    rows, elapsed_time = filter_rows(rows)
    print(f'Processing time: {elapsed_time:.2f} seconds for {limit} rows.')
    return rows

def filter_rows(rows):
    start = time.time()
    np_array = np.array(rows)
    filtered_rows = [format_row(row) for row in np_array]
    elapsed_seconds = time.time() - start
    return filtered_rows, elapsed_seconds