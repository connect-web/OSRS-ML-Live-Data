

def flatten(row):
    flat_row = []
    for i, elements in enumerate(row):
        if isinstance(elements, list):
            for element in elements:
                flat_row.append(element)
        else:
            flat_row.append(elements)
    return flat_row