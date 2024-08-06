import numpy as np
from multiprocessing import Pool, cpu_count
from .calculations import remove_overall, daily_rate
from .formatting import format_row

def convert_rows_to_daily(rows):
    # convert list[tuple] to list[list]
    np_array = np.array(rows)
    batch_size = 50
    # Split the rows into batches of size 50
    batches = [np_array[i:i + batch_size] for i in range(0, len(np_array), batch_size)]
    with Pool(cpu_count()) as pool:
        processed_batches = pool.map(process_batch, batches)
    # Flatten the list of lists
    processed_rows = [row for batch in processed_batches for row in batch]
    return processed_rows

def process_batch(batch):
    return [process_row(row) for row in batch]

def process_row(row):
    """
    Removes 'Overall' Key from skills dicts
    Calculates daily rate for experience and minigames
    Converts the variable size dicts into fixed size arrays
    """
    skill_indexes = [3, 6]
    # Remove overall key
    for i in skill_indexes:
        row[i] = remove_overall(row[i])
    # Daily rate calculations
    row = daily_rate(row)
    # Convert Dict to Array
    row = format_row(row)
    return row
