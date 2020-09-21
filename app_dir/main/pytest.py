import time
import random
import re

regex_if_true = re.compile(r"^if\strue:|^if\sTrue:$", re.MULTILINE)
regex_if_false = re.compile(r"^if\sfalse|^if\sFalse:$", re.MULTILINE)
regex_service = re.compile(r"(if).*?:$", re.MULTILINE)
regex_step_only = re.compile(r".*?", re.MULTILINE)
city_regex = "(.)(weather_info)(.)(\\'.*?\\').*?(=)(=).*?(\\'.*?\\')"
city_new_regex = "(.)(weather_info)*('.*?')"


code = """if weather_info(('Dhaka' == 'Rainy')):
  print_content((newspaper_headlines('Cricket','2020-18-9','PublishedAt')))if weather_info(('1 hour Previous Dhaka' == 'Rainy')):
  print_content((newspaper_headlines('Entertainment','2020-18-9','PublishedAt')))""" 
# if(len(code.splitlines()) == 1):
#    print("Only One Statement")
# print(len(code)) 
# # if len(code.splitlines() == 1):
# #    print("Only One Statement")
    
conditions = code.split("if")
conditions.pop(0)

for i in range(len(conditions)):
    conditions[i] = "if "+conditions[i]
  
print(conditions)
    

# index = 0;
# test_index = 0;
# total_condition = []
# while(test_index > -1): 
#   find_if = code.find("if",index,-1)
#   if(find_if > -1):
#     total_condition.append(find_if)
#   index = find_if+1
#   test_index = find_if;
  

# condition_list = []
# if(len(total_condition)>0):
#   for cd in total_condition:
#     condition_list

# for cd in conditions:
#   item_codes = cd.splitlines()
#   print(item_codes)
#   match_str = regex_service.match(item_codes[0].strip())
#   print(match_str.group())

cs = ["print_content((newspaper_headlines('Cricket','2020-18-9','PublishedAt')))"]

comb = []
for i in range(len(cs)):
    for j in range(2*len(cs)):
         comb.append(str(i)+str(j))
print(comb)




  

