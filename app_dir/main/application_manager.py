import time
from app_dir.main.adaptation_engine import *
import random
import re
import app_dir.main.generated_functions as gf
import copy
from datetime import datetime

app_name = "eud_environment_"
variants = {}
# if(variable = true)
# if(Dhaka = Rainy)
regex_if_true = re.compile(r"^if\strue:|^if\sTrue:$", re.MULTILINE)
regex_if_false = re.compile(r"^if\sfalse|^if\sFalse:$", re.MULTILINE)
regex_service = re.compile(r"(if).*?:$", re.MULTILINE)
regex_step_only = re.compile(r".*?", re.MULTILINE)
city_regex = "(.)(weather_info)(.)(\\'.*?\\').*?(=)(=).*?(\\'.*?\\')"
city_new_regex = "(.)(weather_info)*('.*?')"


# if weather_info(('Dhaka' == 'Clear')):
#   print_content((newspaper_headlines('bitcoin','2020-6-6','PublishedAt')))

# # Clouds --6:08 -- "Clouds"
#           6:28 -- "Clouds"
#  "if weather_info(('Dhaka' == 'Rainy')):                               
#   print_content((newspaper_headlines('Cricket','2020-18-9','PublishedAt')))"
# "if weather_info(('1 hour Previous Dhaka' == 'Rainy')):
#   print_content((newspaper_headlines('Entertainment','2020-18-9','PublishedAt')))

# context
# "weather_info(('Dhaka' == 'Rainy'))"
# "weather_info(('1 hour Previous Dhaka' == 'Rainy'))"

# 
# print_content((newspaper_headlines('Cricket','2020-18-9','PublishedAt')))
# print_content((newspaper_headlines('Entertainment','2020-18-9','PublishedAt')))




class ApplicationManager:
    code = ""
    app_id = ""
    Live_Josn_Data = []
    
    def __init__(self):
        print("in init")

    def get_app(self, code):
        if(len(code)<=0):
            return;
        code = code
        app_id = generate_id()
        ContextManager.register(ContextManager, app_id, code)
        VariantManager.register(VariantManager, app_id, code)
        ContextHistoryManager.register(ContextHistoryManager, app_id, code)
        AdaptationEngine.set_details(AdaptationEngine, app_id, code)
    
    def get_live_data(self):
        return self.Live_Josn_Data
        
        
class ContextManager:
    code = ""
    app_id = ""
    conditions = []
    context_list = []

    def __init__(self):
        print("in init context manager")

    def register(self, app_id, code):
        self.code = code
        self.app_id = app_id
        print("-------------------Context Manager------------------")
        print("Context registered with ContextHistoryManager id :> " + app_id)
        self.find_context(self)
        print("-------------------Context Manager------------------")
        return

    def unregister(self):
        self.code = ""
        self.app_id = ""
        self.context_list = []
        print("Unregistered >> Context Manager")

    def find_context(self):
        
        divide_condition = self.code.split("if")
        divide_condition.pop(0)
        
        if len(divide_condition) > 0:
            for i in range(len(divide_condition)):
                self.conditions.append("if "+divide_condition[i]) 
        elif(len(self.code.splitlines()) == 1):
            item_code = self.code.splitlines()[0]
            if regex_step_only.match(item_code):
                match_str = regex_step_only.match(item_code.strip())
                print('matched_str[step_only]::' + match_str.group())
                context = match_str.group()
                self.context_list.append(context)
            return ;
           
        
        print(self.conditions)   
        # new_lines = len(self.code.split('\n'))
        # print("New lines ===>> " + str(new_lines))
        
        # Split string into segments based on new line
        
        # ["if weather_info(('Dhaka' == 'Clear')):", "  print_content((newspaper_headlines('bitcoin','2020-6-6','PublishedAt')))"]
      
        # for item in code_list:
        #     print("Item :> " + item + " Space count ==>> " + str(item.count(' ')))
        for condition in self.conditions:  
            code_list = condition.splitlines()
            print(code_list)
            if len(code_list) > 1:
                for i in range(len(code_list)):
                    item_code = code_list[i].strip()
                    print(item_code)
                    if item_code.startswith('if'):
                        if regex_if_true.match(item_code):
                            match_str = regex_if_true.match(item_code.strip())
                            print('matched_str[if_true]::' + match_str.group()[2:-1])
                            context = match_str.group()[2:-1]
                            self.context_list.append(context)
                            print('separated_service=>>>' + context)
                        elif regex_if_false.match(item_code):
                            match_str = regex_if_false.match(item_code.strip())
                            print('matched_str[if_false]::' + match_str.group()[2:-1])
                            context = match_str.group()[2:-1]
                            self.context_list.append(context)
                            print('separated_service=>>>' + context)
                        elif regex_service.match(item_code):
                            match_str = regex_service.match(item_code.strip())
                            print('matched_str[service]::' + match_str.group()[2:-1])
                            context = match_str.group()[2:-1]
                            self.context_list.append(context)
                            print('separated_service=>>>' + context)
                        # elif regex_step_only.match(item_code):
                        #     match_str = regex_step_only.match(item_code.strip())
                        #     print('matched_str[step_only]::' + match_str.group())
                        #     context = match_str.group()[2:-1]
                        #     self.context_list.append(context)
                        #     print('separated_service=>>>' + context)
                        else:
                            print("Does not match")
                    else:
                        print("No match found.")
            elif len(code_list) == 1:
                print("Only One Statement")
        
        print("::: Context List :::")       
        print(self.context_list)
        return

    def watch_context(self):
        latest_result = []
        for context in self.context_list:
            print("Watching ::::: "+context)
            city = ""
            if 'weather' in context:
                # rg = re.compile(city_regex, re.IGNORECASE | re.DOTALL)
                # Dhaka
                rg = re.compile(city_new_regex, re.IGNORECASE | re.DOTALL)
                m = rg.search(context)
                if m:
                    # city = m.group(4)[1:-1]
                    city = m.group(3)[1:-1]
                
                if(city.find("previous")>-1):
                    pass
                else:             
                    print("City : "+city)
                    result = gf.weather_info(city)  
                    current_time = datetime.now()
                    ContextHistoryManager.setHistory(ContextHistoryManager,result,current_time)
                    latest_result.append({"weather":result, "time":current_time})
                    context_values.insert(0,{"weather":result, "time":current_time})
            elif 'get_am_pm':
                result = get_am_pm()
            
        print("Current Context :: ")
        print(latest_result)
        ContextHistoryManager.getHistory(ContextHistoryManager)
        return latest_result


class VariantManager:
    code = ""
    app_id = ""
    conditional_services = []
    # services = ["print_content((source_news('bbc-news')))"]
    # general_services = ["print_content((source_news('bbc-news')))"]
    general_services = ["weather_info(city)"]
    variant_list = []
    
    def __init__(self):
        print("in init variant manager")

    def register(self, app_id, code):
        self.code = code
        self.app_id = app_id
        print("-------------------Variant Manager------------------")
        print("Variant Registered with ContextHistoryManager id :> "+app_id)
        self.extract_variant(self)
        self.make_variant(self)
        print("-------------------Variant Manager------------------")
        return

    def unregister(self):
        self.app_id = ""
        self.code = ""
        self.services = []
        self.conditional_services = []
        self.variants = {}
        print("Unregistered >> Variant Manager")

    def extract_variant(self):
        # Split string into segments based on new line
        print(ContextManager.conditions)
        for cd in ContextManager.conditions:
            print(cd)   
            code_list = cd.splitlines()
            # for item in code_list:
            #     print("Item :> " + item + " Space count ==>> " + str(item.count(' ')))
            if len(code_list) > 1:
                for i in range(len(code_list)):
                    if code_list[i].strip().startswith('if'):
                        item_code = code_list[i+1].strip()
                        print('matched_str[step_only]::' + item_code)
                        conditional = item_code
                        self.conditional_services.append(conditional)
                        print('separated_service=>>>' + conditional)
                    else:
                        print("No match found.")
            elif len(code_list) == 1:
                print("Only One Statement")
        print("CS ")
        print(self.conditional_services)
        return
    
    def make_variant(self):
        condition_length = len(ContextManager.conditions)
        
        # this is for binary combaination ['00','01','10','11']
        bit_count = condition_length
        combination_list = []
        for i in range(2**condition_length):
            position = i
            b = f'{position:0{bit_count}b}'
            combination_list.append(b)

       
        if all(c == '0' for c in combination_list[0][1:]):
            if len(self.general_services) > 0:
                self.variant_list.append({'No':self.general_services})

        if all(c == '1' for c in combination_list[len(combination_list)-1][1:]):
            list_of_cs_and_s = copy.deepcopy(self.general_services)
            list_of_cs_and_s.extend(self.conditional_services)
            self.variant_list.append({'All':list_of_cs_and_s})
            
        for i in range(1,len(combination_list)-1):
            list_of_cs_and_s = []
            variant_key = ''
            check_1 = False
            for j in range(len(self.conditional_services)):

                if combination_list[i][j] == '1':
                    check_1 = True
                    list_of_cs_and_s.append(self.conditional_services[j])
                    variant_key += str(j) # this is for condition_key as an index

                # variant_12 -> means condions 1 and 2 index 
            if(check_1):
                cs1 = copy.deepcopy(self.general_services)
                cs1.extend(list_of_cs_and_s)# list_of_cs_and_s.insert(0,copy.deepcopy(common_service)) 
                self.variant_list.append({variant_key:cs1})
        
        self.get_variant(self)
        
    # def make_variant(self):
    #     length_cs = len(self.conditional_services)
    #     print("Length of CS :::: "+str(length_cs))

    #     for index in range(length_cs - 1, -1, -1):
    #         print(""+self.conditional_services[index])
    #         if length_cs==1:
    #             list_of_1_0 = list(map(int, str(format(1, '01b'))))
    #             # [1] 
    #         else:
    #             list_of_1_0 = list(map(int, str(format(index, '02b'))))
    #         print(str(list_of_1_0))
    #         if all(value == 0 for value in list_of_1_0):
    #             print("All Values Are Zero,,So No CS")
    #             list_of_cs_and_s = self.services.copy()
    #             variants['variant' + str(index)] = list_of_cs_and_s
    #         elif all(value == 1 for value in list_of_1_0):
    #             print("ALl Values are One,, So ALl CS")
    #             list_of_cs_and_s = self.services.copy()
    #             j = len(list_of_cs_and_s)
    #             for item in self.conditional_services:
    #                 list_of_cs_and_s.insert(j, item)
    #                 j += 1;
                
    #             variants['variant' + str(index)] = list_of_cs_and_s
    #         else:
    #             list_of_cs_and_s = self.services.copy()
    #             for value in list_of_1_0:
    #                 if value == 1:
    #                     index_ = list_of_1_0.index(value)
    #                     cs_ = self.conditional_services[index_]
    #                     list_of_cs_and_s.insert(len(list_of_cs_and_s), cs_)
    #                     variants['variant' + str(index)] = list_of_cs_and_s

    #     self.get_variant(self)
    #     return

    def get_variant(self):
        print("::: Variant Maping List :::")
        for variant in self.variant_list:
            print(variant)
        # AdaptationEngine.set_variants(self, variants)
        return variants

class ContextHistoryManager:
    code = ""
    app_id = ""
    previous_weather_and_time = []    
     
    def __init__(self):
        print("History ContextHistoryManager")

    def register(self, app_id, code):
        self.code = code
        self.app_id = app_id
        print("-------------------History ContextHistoryManager------------------")
        print("History ContextHistoryManager registered with ContextHistoryManager id :> " + app_id)
        
        print("-------------------History ContextHistoryManager------------------")
        return

    def unregister(self):
        self.code = ""
        self.app_id = ""
        
        print("Unregistered >> History ContextHistoryManager")
        
    def setHistory(self,weather,p_date_time):
        self.previous_weather_and_time.append({"weather":weather,"time":p_date_time})
    
    def getHistory(self):
        print("::: ContextHistoryManager History :::")
        for data in self.previous_weather_and_time:
            print(data)
        return self.previous_weather_and_time


def generate_id():
    app_id = app_name + "" + str(random.randint(1, 100))
    print('application_id::'+app_id)
    return app_id


def decimal_to_binary(num):
    if num > 1:
        decimal_to_binary(num // 2)
    return num % 2