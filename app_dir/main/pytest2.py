import time
import random
import re

# cd = ["if  weather_info(('Dhaka' == 'Rainy')):\n  print_content((newspaper_headlines('Footbal','2020-9-19','PublishedAt')))", "if  weather_info(('1 hour previous Dhaka' == 'Rainy')):\n  print_content((newspaper_headlines('Entertainment','2020-9-19','PublishedAt')))", "if  weather_info(('1 hour previous Dhaka' == 'Rainy')):\n  print_content((newspaper_headlines('Entertainment','2020-9-19','PublishedAt')))"]

# common_service = ["print_content((source_news('bbc-news')))"]

# all_context = ["  weather_info(('Dhaka' == 'Rainy'))", "  weather_info(('1 hour previous Dhaka' == 'Rainy'))","  weather_info(('2 hour previous Dhaka' == 'Rainy'))"]

# bit_count = len(cd)
# combination_list = []
# for i in range(2**len(cd)):
#     position = i
#     b = f'{position:0{bit_count}b}'
#     combination_list.append(b)

# print(combination_list)

# variant_list = []

# import copy

# cs  = ["print_content((newspaper_headlines('Footbal','2020-9-19','PublishedAt')))", "print_content((newspaper_headlines('Entertainment','2020-9-19','PublishedAt')))","print_content((newspaper_headlines('Footbal','2020-9-19','PublishedAt')))"]

# print(combination_list[len(combination_list)-1][1:])


# if all(c == '0' for c in combination_list[0][1:]):
#     if len(common_service) > 0:
#        variant_list.append({"No":common_service})

# print(variant_list)
# if all(c == '1' for c in combination_list[len(combination_list)-1][1:]):
#        list_of_cs_and_s = copy.deepcopy(common_service)
#        list_of_cs_and_s.append(cs)
#        variant_list.append({"All":list_of_cs_and_s})
     

# for i in range(1,len(combination_list)-1):
#   print(cs,len(cs))
#   list_of_cs_and_s = []
#   variant_key = ''
#   check_1 = False
#   for j in range(len(cs)):
#       print(i,j,combination_list[i])
     
#       if combination_list[i][j] == '1':
#           check_1 = True
#           list_of_cs_and_s.append(cs[j])
#           variant_key += str(j)
          
#   # variant_12 -> means condions 1 and 2 index 
#   if(check_1):
#     cs1 = copy.deepcopy(common_service)
#     cs1.extend(list_of_cs_and_s)# list_of_cs_and_s.insert(0,copy.deepcopy(common_service)) 
#     variant_list.append({variant_key:cs1})
          

# print(variant_list)
# print(len(variant_list))

#  #######   minute diff

import time
from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print(current_time)
# time.sleep(20)
now2 = datetime.now()
current_time2 = now2.strftime("%H:%M:%S")
print(current_time2)

minutes_diff = (now2 - now).total_seconds();

from math import isclose
a = 1.0
b = 1.00000001
k= isclose(a, b, abs_tol=1e-8)

print(k)


print(minutes_diff)

city_prev = "  1   hour   previous          dhaka"

# previous_regex = "(previous)(*)"

# rg = re.compile(previous_regex, re.IGNORECASE | re.DOTALL)

# m = rg.search(city_prev)

# print(m.group(1))
# Default_Time = ["hour","minute","day"]
# print(city_prev.find("previous"))
# c = city_prev.split("previous")
# c = [x.strip() for x in c ]
# if(len(c)==2):
#     nt = c[0].strip().split(" ")
#     nt = list(filter(None, nt))
#     print(nt)

# print(c)

c = ["  weather_info(('Dhaka' == 'Rainy'))", "  weather_info(('1 hour previous Dhaka' == 'Rainy'))"]

# def getConditionSelect(condition):
#     cond_part = city_prev.split("previous")
#     cond_part = [x.strip() for x in cond_part ]
#     if(len(cond_part)==2):
#         time_with_type = cond_part[0].strip().split(" ")
#         time_with_type = list(filter(None, time_with_type))
#         time_with_type.append(cond_part[len(cond_part)-1])
#         return time_with_type;


# def calculateTime(present_time,old_time_list):
#     pass
    
# li = []
# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# li.append({"weather":"rainy", "time":now})
# print(li)
# for context in c :
#     city_type = context.find("previous");
#     if(city_type>-1):
#         divide_weather = context.split("=")
#         divide_weather = list(filter(None, divide_weather))
#         print(divide_weather)
#         divide_weather = divide_weather[1].split(")")
#         divide_weather = list(filter(None, divide_weather)) # this is for deleted empty string in Array list
#         divide_weather = [x.strip() for x in divide_weather ]  
#         weather = divide_weather[0][1:-1]
     
#         print(weather)
        
#     elif city_type == -1:
#         getConditionSelect(city_prev)
#         # calculateTime(li[0])

# cu = datetime.now()
# d ={'weather': 'Rain', 'time':cu}

# print(d["weather"])

arr = []

for j in range(5):
   
    a = []
    for i in range(10):
        a.append(i*i)

    arr = a
    print(arr)




    
       

      


