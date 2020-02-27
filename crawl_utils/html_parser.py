
def select_sub_page_by_query(df, query):
    '''
    input : df(DataFrame), query(str)
    output : DataFrame

    given query, get DataFrame whose text has query 
    '''
    return df[df['text'].apply(lambda e: query in e)]