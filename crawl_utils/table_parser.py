from crawl_utils.html_request import * 
from crawl_utils.url_extractor import *

def strip_all(text):
    '''
    input : text(str)
    output : text(str)

    strip all blank in the text
    '''
    return text.strip().replace(" ", "").replace("\n", "").replace("\t", "").replace('\r',"")


def get_row(row):
    element = []
    for r in row:
        if r.has_attr('colspan'):
            element += [strip_all(r.text) for _ in range(int(r['colspan']))]
        else:
            element += [strip_all(r.text)]
    return element

def get_table_element(dom):
    '''
    input : dom
    output : list
    get element whose tag name is 'td' or 'th'
    '''
    return dom.find_all(['td', 'th'])


def get_template(row):
    '''
    input : row(bs4.element.ResultSet)
    output : list 

    '''
    template = []
    for r in row:
        if r.has_attr('rowspan'):
            template += [strip_all(r.text)]
        elif r.has_attr('colspan'):
            template += [None for _ in range(int(r["colspan"]))]
        else:
            template += [None]
    return template

def merge_template(template, row):
    '''
    input : template(list), row(list)
    output : merged(list)

    '''
    merged = []

    for temp in template:
        if temp:
            merged += [temp]
        else:
            try:
                merged += [row.pop(0)]
            except:
                pass
    return merged
    

def tbody_parsing(rows):
    '''
    input : nested list(# of columns, # of rows)
    output : 
    '''
    element = []
    element_list = []
    if rows:
        standard_len = max(len(get_table_element(r)) for r in rows)
        template = get_template(get_table_element(rows[0]))
        for row in rows:
            emnt = get_table_element(row)
            if emnt:
                if len(emnt) == standard_len:
                    template = get_template(emnt)
                    element = get_row(emnt)
                else:
                    element = merge_template(template, get_row(emnt))
            element_list.append(element)
        return element_list


def get_table_column(table):
    '''
    input : table(dom obejct)
    output : column(list)
    
    given table dom, get column list 
    if having double column, ignore first
    '''
    columns = []
    columns_final = []
    trs = table.find_all('tr')
    if len(table.find_all('tr')) > 1:
        for tr in trs:
            columns.append(tr.find_all(['th', 'td']))
        first_row = get_template(columns[0])
        if any(first_row):
            second_row = [strip_all(c.text) for c in columns[1]]
            return (merge_template(first_row, second_row), 2)
            
        else:
            return (get_row(columns[0]), 1)
    else:
        return (get_row(trs[0].find_all(['th', 'td'])), 1)

def table_parsing(url):
    '''
    input : url(str)
    output : list of table(DataFrame)

    get list of table given url
    '''
    table_df_list = []
    columns = []
    columns_head = []
    columns_body = []
    soup = parsing(url)
    if soup:
        tables = soup.find_all('table')
        for table in tables:
            table_df = pd.DataFrame()
            columns_body, n = get_table_column(table)
            rows = table.find_all('tr')
        
            element_list = tbody_parsing(rows)
            columns, n = get_table_column(table)
            len_element = max(len(e) for e in element_list)
            for _ in range(n):
                element_list.pop(0)
            if not columns:
                columns = [str(_) for _ in range(len_element)]
            columns = list(map(strip_all, columns))
            for key, value in zip(columns, zip(*element_list)):
                table_df[key] = [v for v in list(value)]         
            table_df_list.append(table_df)
    table_df_list = [table for table in table_df_list if any(table)]
    return table_df_list
