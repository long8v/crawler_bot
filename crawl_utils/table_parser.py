from crawl_utils.html_request import * 
import copy

def strip_all(text):
    '''
    input : text(str)
    output : text(str)

    strip all blank in the text
    '''
    return text.strip().replace(" ", "").replace("\n", "").replace("\t", "").replace('\r',"")


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
    
    
def tbody_parsing(rows):
    '''
    input : rows(list of bs4.element.ResultSet)
    output : element_list(list)

    parse 
    '''
    element = []
    element_list = []
    if rows:
        standard_len = max(len(get_table_element(r)) for r in rows)
        template = get_template(get_table_element(rows[0]))
        for row in rows:
            emnt = get_table_element(row)
            if emnt:
                if any(e for e in emnt if e.has_attr('rowspan')):
                    template_sub = get_template(emnt)
                if len(emnt) == standard_len: 
                    template = get_template(emnt)
                    element = get_row(emnt)
                else:
                    try:
                        element = merge_template(template, get_row(emnt))
                    except:
                        try:
                            template_ = merge_template(template, template_sub)
                            element = merge_template(template_, get_row(emnt))
                        except:
                            element = []
            element_list.append(element)
        return element_list



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
    table_df_list = []
    columns_list = []
    soup = parsing(url)
    tables = soup.find_all('table')
    for n in range(0, len(tables)):
        n_cols = 0
        n_rows = 0
        for row in tables[n].find_all("tr"):
            col_tags = row.find_all(["td", "th"])

            if len(col_tags) > 0:
                n_rows += 1
                if len(col_tags) > n_cols:
                    n_cols = len(col_tags)    
        df = pd.DataFrame(index = range(0, n_rows), columns = range(0, n_cols))
        # Create list to store rowspan values 
        skip_index = [0 for i in range(0, n_cols)]
        # Start by iterating over each row in this table...
        row_counter = 0
        for row in tables[n].find_all("tr"):
            # Skip row if it's blank
            if len(row.find_all(["td", "th"])) == 0:
                next
            else:
                # Get all cells containing data in this row
                columns = row.find_all(["td", "th"])
                col_dim = []
                row_dim = []
                col_dim_counter = -1
                row_dim_counter = -1
                col_counter = -1
                this_skip_index = copy.deepcopy(skip_index)
                for col in columns:
                    # Determine cell dimensions
                    colspan = col.get("colspan")
                    if colspan is None:
                        col_dim.append(1)
                    else:
                        col_dim.append(int(colspan))
                    col_dim_counter += 1

                    rowspan = col.get("rowspan")
                    if rowspan is None:
                        row_dim.append(1)
                    else:
                        row_dim.append(int(rowspan))
                    row_dim_counter += 1

                    # Adjust column counter
                    if col_counter == -1:
                        col_counter = 0  
                    else:
                        col_counter = col_counter + col_dim[col_dim_counter - 1]

                    while skip_index[col_counter] > 0:
                        col_counter += 1

                    # Get cell contents  
                    cell_data = col.get_text()

                    # Insert data into cell
                    df.iat[row_counter, col_counter] = cell_data

                    # Record column skipping index
                    if row_dim[row_dim_counter] > 1:
                        this_skip_index[col_counter] = row_dim[row_dim_counter]

            # Adjust row counter 
            row_counter += 1

            # Adjust column skipping index
            skip_index = [i - 1 if i > 0 else i for i in this_skip_index]
        columns_list.append(get_table_column(tables[n]))
        # Append dataframe to list of tables
        table_df_list.append(df)
    table_list = []
    for table, column in zip(table_df_list, columns_list):
        if table.shape[1] == len(column[0]):
            table.columns = column[0]
        table_list.append(table.loc[column[1]:].fillna(method ='ffill'))
    return table_list