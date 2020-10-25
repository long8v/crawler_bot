[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Flong8v%2Fcrawler_bot&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
# crawler_bot
해당 프로젝트는 다양한 html 양식의 사이트에서 원하는 메뉴의 내용을 가져오기 위해 개발되었습니다.
html_request, main_site_extractor, url_extractor, 
table_parser, create_table, bot_utils의 모듈이 있습니다
주요 아이디어는 검색엔진들의 방식을 활용하여 페이지에 달려 있는 모든 서브페이지를 텍스트와 가져와 직접 해당 페이지에 들어가지 않고도 원하는 메뉴를 가져오는 방식입니다.

## prerequisite 
- bs4
- lxml 
- selenium
- pydash
- Pillow
- PyVirtualDisplay


## html_request
requests를 활용하여 페이지에게 request를 보내고 html를 가져오는 모듈입니다
이후 BeautifulSoup 패키지를 활용하여 lxml 방식으로 parsing하여 dom 객체를 만듭니다
500대 에러인 경우 세 번까지 시도해보고 실패하면 출력을 합니다
이 때 bot detection을 줄이기 위하여 user_agent를 parameter로 넣었습니다

## main_site_extractor
기관명만 주어지고 사이트가 주어지지 않았을 때, 네이버에 해당 기관명을 검색하여 공식 홈페이지를 가져오는 가져오는 모듈입니다
이 때, 네이버에서 가져온 페이지에서 redirect 되는 페이지들이 많아 Selenium을 사용하여 가상페이지를 띄우고 페이지에 접속한 뒤 redirect된 페이지를 가져오는 방식을 진행하였습니다
다만 이때, Selenium을 사용함에 따라 봇으로 판단이 되어 사이트에서 차단을 할 수도 있습니다. 아직 이에 대해서는 해결을 하지 못했습니다

## url_extractor 
페이지가 주어졌을 때, 모든 href를 긁어오는 모듈입니다
특히 href를 긁어올 때 옆에 있는 text를 긁어서 테이블을 만듭니다
태그가 image인 경우, 옆에 text가 있을 때만 긁어옵니다
href가 javascipt::함수명이 있을 경우 Selenium의 execute_script를 활용하여 해당 함수를 호출하도록 했습니다

## table_parser
html의 table 태그를 활용하여 parsing을 하는 모듈입니다
병합 셀을 처리하기 위하여 rowspan, colspan attribute를 활용하였습니다
이중 컬럼의 경우, 첫번째 컬럼이 rowspan이 있을 경우에만 컬럼 제목이 잘 들어갑니다
그렇지 못한 컬럼의 경우 0, 1, 2, ..등으로 넘버링해서 들어가게 됩니다
...pd.read_html이 있다는 것을 뒤늦게 앎

## create_table
csv 파일로 만들어야 하기 때문에 DataFrame 형태로 만드는 모듈입니다

## bot_utils
각종 자주 쓰이는 함수를 모아둔 모듈입니다
