
def select_sub_page_by_hspt_name(df, query):
    '''
    input : df(DataFrame), query(str)
    output : DataFrame

    given query, get DataFrame whose hspt_name has query 
    '''
    return df[df['hspt_name'].apply(lambda e: query in e)]


def select_sub_page_by_query(df, query):
    '''
    input : df(DataFrame), query(str)
    output : DataFrame

    given query, get DataFrame whose text has query 
    '''
    return df[df['text'].apply(lambda e: query in e)]