echo 'get first child'
python get_first_child.py
echo 'find non payment to depth 2'
python get_SUB_NON_PAYMENT.py
echo 'merge non payment from main, hideen, and hand'
python get_MERGED_NON_PAYMENT.py
echo 'will find option and page'
python get_MERGED_depth_2.py
echo 'get non payment page until it ends'
python get_MERGED_depth_100.py
echo 'get final csv! '
python get_final_csv.py
echo "finished!"