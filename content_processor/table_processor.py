def filter_tables(list_of_df):
    # add logic for filtering which tables to keep and which to discard
    filtered_tables = []
    for df in list_of_df:
        if len(df) > 1:
            filtered_tables.append(df)
    return filtered_tables