import time
from training.queries import get_hiscore_rows
from training.processing.conversion import convert_rows_to_daily
from entities.data_process import flatten
def get_hiscore(activity, limit=500, offset=0, activity_type='skills'):
    rows = get_hiscore_rows(activity, limit=limit, offset=offset, activity_type=activity_type)
    rows, elapsed_time = time_convert_rows_to_daily(rows)
    rows = [flatten(row) for row in rows]
    print(f'Processing time: {elapsed_time} seconds for {limit} rows.')
    return rows

def time_convert_rows_to_daily(rows):
    start_time = time.time()
    processed_rows = convert_rows_to_daily(rows)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return processed_rows, elapsed_time

