from crawl_utils.html_request import * 
import copy

def strip_all(text):
    '''
    input : text(str)
    output : text(str)

    strip all blank in the text
    '''
    return text.strip().replace(" ", "").replace("\n", "").replace("\t", "").replace('\r',"")
def get_table_element(dom):
    '''
    input : dom
    output : list
    get element whose tag name is 'td' or 'th' or 'dd'
    '''
    return dom.find_all(['td', 'th', 'dd'])
def get_template(row):
    '''
    input : row(bs4.element.ResultSet)
    output : template(list)
    get text whose tag has attribute rowspan, otherwise None
    '''
    template = []
    for r in row:
        if r.has_attr('rowspan'):
            if r.has_attr('colspan'):
                template += [r.text for _ in range(int(r["colspan"]))]
            else:
                template += [r.text]
        elif r.has_attr('colspan'):
            template += [None for _ in range(int(r["colspan"]))]
        else:
            template += [None]
    return template

def put_in_list(text, idx, standard_len, len_list):
    template = [None for _ in range(standard_len)]
    template[standard_len - len_list + idx] = text
    return template


def get_rowspan(element):
    return [(int(e["rowspan"]), put_in_list(e.text, idx, standard_len, len(get_row(element)))) 
            for idx, e in enumerate(element) if e.has_attr('rowspan')]


def merge_templates(templates):
    result = []
    for _ in zip(*templates):
        temp = [__ for __ in _ if __ is not None]
        if len(temp) == 1:
            result += temp
        if len(temp) == 0:
            result += [None]
        if len(temp) == 2:
            print(temp)
            print("음?")
    return result


def merge_template(template, row):
    '''
    input : template(list), row(list)
    output : merged(list)

    given template(mostly row having rowspan element),
    merge it with row
    '''
    merged = []
    for temp in template:
        if temp is not None:
            merged += [temp]
        else:
            merged += [row.pop(0)]
    return merged


def merge(template, row):
    for temp in template:
        if temp is None:
            template[template.index(temp)] = row[template.index(temp) + len(row) - len(template)]
    return template

def get_row(row):
    '''
    input : row(bs4.element.ResultSet)
    output : element(list)

    get list of text from row
    '''
    element = []
    for r in row:
        if r.has_attr('colspan'):
            element += [strip_all(r.text) for _ in range(int(r['colspan']))]
        else:
            element += [strip_all(r.text)]
    return element

def get_table_column(table):
    '''
    input : table(dom obejct)
    output : column(list)
    
    given table dom, get column list 
    if having double column, merge first and second
    '''
    columns = []
    columns_final = []
    trs = table.find_all('tr')
    if len(trs) > 1:
        for tr in trs:
            columns.append(get_table_element(tr))
        first_row = get_template(columns[0])
        if any(first_row):
            second_row = [strip_all(c.text) for c in columns[1]]
            return (merge_template(first_row, second_row), 2)      
        else:
            return (get_row(columns[0]), 1)
    else:
        return (get_row(get_table_element(trs[0])), 1)
    
def merge(template, row):
    for temp in template:
        if temp is None:
            template[template.index(temp)] = row[template.index(temp) + len(row) - len(template)]
    return template

def put_in_list(text, idx, standard_len, len_list):
    template = [None for _ in range(standard_len)]
    template[standard_len - len_list + idx] = text
    return template

def get_rowspan(element, standard_len):
    return [(int(e["rowspan"]), put_in_list(e.text, idx, standard_len, len(get_row(element)))) 
            for idx, e in enumerate(element) if e.has_attr('rowspan')]

def tbody_parsing(rows):
    '''
    input : rows(list of bs4.element.ResultSet)
    output : element_list(list)

    parse 
    '''
    standard_len = max(len(get_table_element(r)) for r in rows)
    rowspan_list = []
    element_list = []
    template = []
    for row in rows:
        element = get_table_element(row)
        rspn = get_rowspan(element, standard_len)
        if rspn:
            rowspan_list.extend(rspn)
        if rowspan_list:
            template = merge_templates(list(zip(*rowspan_list))[1])
            rowspan_list = [(i-1, j) for i, j in rowspan_list if i > 1]
        if len(template) != standard_len:
            template = [None for _ in range(standard_len)]
        emnt = get_row(element)
        element_list.append(merge(template, emnt))
    return element_list


def table_parsing(url):
    '''
    input : url(str)
    output : list of table(DataFrame)
    get list of table given url
    '''
    table_df_list = []
    columns = []
    columns_list = []
    soup = parsing(url)
    if soup:
        tables = soup.find_all('table')
        for table in tables:
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
            i = 1
            table_df = pd.DataFrame()
            for key, value in zip(columns, zip(*element_list)):
                if key not in table_df:
                    table_df[key] = [v for v in list(value)]         
                else:
                    table_df["{}_{}".format(key, i)] = [v for v in list(value)] 
                    i += 1
            table_df_list.append(table_df)
    table_df_list = [table for table in table_df_list if any(table)]
    return table_df_list