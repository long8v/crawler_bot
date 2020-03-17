import pickle_io 
from collections import Counter

column = ['분류', '구분', '명칭', '코드', '비용', '특이사항', '최저비용', '약제비포함여부', '치료재료대포함여부', '최고비용',
         '중분류', '소분류']
change_column = {c:c for c in column}

column = {'최대':'최고비용','최저': '최저비용', '최고':'최고비용', '최소':'최저비용', 
          '비고':'특이사항',  '기타':'특이사항', '단위' : '특이사항',
          '단가': '비용', '금액':'비용', '가격':'비용', '(원)':'비용',
          '수가명칭':'명칭', '내용':'명칭', '비급여명':'명칭', '처방명':'명칭', 
          '항목':'명칭', '품목':'명칭', '수가명':'명칭', '명':'명칭', '품명':'명칭', '기본항목':'명칭',
          '수가':'비용', '일반수가':'비용',
          '약제':'약제비포함여부', '약재':'약제비포함여부', 
          '치료재료':'치료재료대포함여부', '치료대':'치료재료대포함여부', }
change_column.update(column)

counter = Counter([c for table in table_list.values() for t in table for c in t.columns]).most_common()
for c, v in counter:
    c = str(c)
    for col in column:
        if len(c) == 1 or len(col) == 1:
            continue
        if c in col:
            if c =="":
                continue
            change_column[c] = column[col]
        if col in c:
            change_column[c] = column[col]

change_column = dict(filter(lambda e: len(e[0]) < 10 and len(e[0]) > 1, change_column.items()))

change_column['제증명 내역'] = '명칭'
change_column['기본항목'] = '명칭'
change_column['분류/명칭'] = '명칭'
change_column['수가명'] = '명칭'
change_column['상세 분류'] = '명칭'
change_column['세부항목'] = '명칭'
change_column['수가코드'] = '특이사항'
change_column['수가명칭(한글)'] = '명칭'
change_column['최저부가비율'] = '특이사항'
change_column['최고가비율'] = '특이사항'
change_column['비급여가(원)'] = '비용'
change_column['단위'] = '특이사항'

gubun = ['제증명료 구분','상급병실료 구분','식대료 구분','이송료 구분','주사료 구분','처치수술료 구분', '처치수술료 구분', '약제료 구분']
for gub in gubun:
    change_column[gub] = '명칭'

pickle_io.pickle_save('change_column.p', change_column)