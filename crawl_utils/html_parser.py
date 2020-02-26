
def select_sub_page_by_query(df, query):
    return df[df['text'].apply(lambda e: query in e)]