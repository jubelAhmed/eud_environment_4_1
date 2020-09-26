import random
from app_dir.main.generated_functions import *
import app_dir.main.application_manager as am
import re
import ast
import copy
import time
import json
import requests
from math import isclose
import webbrowser


regex_mapper = re.compile(r"(if).*?:$", re.MULTILINE)
city_new_regex = "(.)(weather_info)*('.*?')"

variant = {}
global open_url
open_url = 1
context_values = []
global live_data
live_data = []

def OpenNewurl():
    url = 'http://127.0.0.1:8081/app/'
    webbrowser.register('chrome',
        None,
        webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
    webbrowser.get('chrome').open_new(url)

def get_context():
    cm = am.ContextManager()
    OpenNewurl()        
    #request_variant()
    while True:
        context_values[:] = []
        time.sleep(20)
        context_values.append(cm.watch_context())
        AdaptationEngine.get_selected_variant(AdaptationEngine)
        # print("IN AE As CM ::::: "+str(cm.watch_context()))
    return


def request_variant():
    vm = am.VariantManager()

    print(am.variants)
    print("----Acquired variants----")
    for key, value in variant.items():
        print(key, 'corresponds to', value)
    return


class AdaptationEngine:
    app_id = ""
    code = ""
    mapping_dict = {}
    # mapping_dict = {
        # Current_context: "Sunny/Rainy" ,
        # Required_value : "Rainy for Robindro Song"
        # 
        # }

    def __init__(self) -> None:
        super.__init__()

    def set_variants(self, variants):
        variant = variants
        print("test ===== "+str(variant))

    def set_details(self, app_id, code):
        self.app_id = app_id
        self.code = code
        print("\n-----------------Start Adaptation Engine-------------\n")
        # self.mapper(self)
        get_context()
        # self.get_selected_variant(self) # test
        # RuntimeEngine.get_and_set_code(RuntimeEngine, self.get_selected_variant(self))
        print("\n-----------------End Adaptation Engine-------------\n")
        return
    
    
    def getConditionSelect(self,prev_cond):
        cond_part = prev_cond.split("previous")
        cond_part = [x.strip() for x in cond_part ]
        if(len(cond_part)==2):
            time_with_type = cond_part[0].strip().split(" ")
            time_with_type = list(filter(None, time_with_type))
            time_with_type.append(cond_part[len(cond_part)-1])
            return time_with_type;

    def getSeconds(self,time_list):
        total_seconds = 0
        # print(time_list)
        if(time_list[1].lower() == "day" or time_list[1].lower() == "days"):
            total_seconds = int(time_list[0])*24*3600
        elif(time_list[1].lower() == "hour" or time_list[1].lower() == "hours"):
            total_seconds = int(time_list[0])*3600
        elif(time_list[1].lower() == "min" or time_list[1].lower() == "minute"  or time_list[1].lower() == "minutes"):
            total_seconds = int(time_list[0])*60
        elif(time_list[1].lower() == "second" or time_list[1].lower() == "seconds"  or time_list[1].lower() == "sec"):
            total_seconds = int(time_list[0])
        
        return total_seconds;
    
    def getDifferentTime(self,present,old):
        sec_diff = (present-old).total_seconds();
        return sec_diff

    def calculateTime(self,time_with_type,present_time,old_time_list):
        # print("calculateTime")
        isPresent = False
        result_w = ""
        # print(present_time)
        total_seconds = self.getSeconds(self,time_with_type)
        # print(total_seconds)
        for i, e in reversed(list(enumerate(old_time_list))):
            # print(i, e)
            old_t = dict(old_time_list[i])
             
            if old_t.get("time")!=None:
                old_time = old_t["time"]
                # print(old_time) 
                calc_data = self.getDifferentTime(self,present_time,old_time)
                # print("calc ",calc_data)
                if isclose(total_seconds, calc_data, abs_tol=1e-8):
                    isPresent = True;
                    result_w = old_t["weather"]
                    break
                elif calc_data >= total_seconds:
                    isPresent = True;
                    # print("yes ")
                    result_w = old_t["weather"]
                    break
                    
                       
        return result_w            
       
            
            
    def checkContextMatch(self,context):
        divide_weather = context.split("=")
        divide_weather = list(filter(None, divide_weather))
        # print(divide_weather)
        divide_weather = divide_weather[1].split(")")
        divide_weather = list(filter(None, divide_weather)) # this is for deleted empty string in Array list
        divide_weather = [x.strip() for x in divide_weather ]  
        required_weather = divide_weather[0][1:-1]
        # print(required_weather)
        
        return required_weather
        

    def get_selected_variant(self):
        
        key = ""
        true_count = 0;
        rm = RuntimeEngine()
        for index in range(len(am.ContextManager.context_list)):
            context = am.ContextManager.context_list[index];
            city_type = context.find("previous");
            if(city_type <=-1 ):
                divide_weather = context.split("=")
                divide_weather = list(filter(None, divide_weather))
               
                divide_weather = divide_weather[1].split(")")
                divide_weather = list(filter(None, divide_weather)) # this is for deleted empty string in Array list
                divide_weather = [x.strip() for x in divide_weather ]  
                required_weather = divide_weather[0][1:-1]
                
                cv = context_values[0] # this is latest found context
                cv = dict(cv)  
                r_w = cv["weather"]
                if r_w in required_weather:
                    key= key+str(index)
                    true_count += 1
    
            elif city_type > -1:
                rg = re.compile(city_new_regex, re.IGNORECASE | re.DOTALL)
                m = rg.search(context)
                city_part = ""
                if m:
                    city_part = m.group(3)[1:-1]
                
                time_with_type = self.getConditionSelect(self,city_part)
                # print(time_with_type)
                t_cv = context_values[0] # this is latest found context
                t_cv = dict(t_cv)
                r_time = cv["time"]
                result_weather = self.calculateTime(self,time_with_type,r_time, am.ContextHistoryManager.previous_weather_and_time)
                # print("result w ",result_weather)
                context_weather = self.checkContextMatch(self,context)
                if len(result_weather) >0 and result_weather in context_weather:
                    key= key+str(index)
                    true_count += 1
                 
                
        if(true_count == 0):         
            selected_variant = dict(am.VariantManager.variant_list[0])["No"]
            rm.get_and_set_code(selected_variant)
            print("\nSelected Variant")
            print(selected_variant)
                    
        if(true_count == len(am.ContextManager.context_list)):
            selected_variant = dict(am.VariantManager.variant_list[1])["All"]
            rm.get_and_set_code(selected_variant)
            print("\nSelected Variant")
            print(selected_variant)

        for i in range(2,len(am.VariantManager.variant_list)):  
            vm_d = dict(am.VariantManager.variant_list[i])
            if len(key) >0:
                # print(key)
                if vm_d.get(key)!=None:
                    selected_variant = vm_d[key] 
                    rm.get_and_set_code(selected_variant)
                    print("\nSelected Variant")
                    print(selected_variant)
                     
                
    
class RuntimeEngine:
    live_data_list = []
    
    def __init__(self):
        # print("in init runtime engine")
        pass
    
    def get_live_data(self):
        return self.live_data_list

    def get_and_set_code(self, variantList):
        self.exec_print_result(variantList)
        return

    def exec_print_result(self,variantList):
        new_loc = {}
        result_list = []
        for variant in variantList: 
             exec("l_result = "+str(variant), globals(), new_loc)
             data = new_loc["l_result"]
             result_list.append(data)
        # print("Start From Runtime Engine ")
        
        self.live_data_list = copy.deepcopy(result_list)
        live_data = copy.deepcopy(result_list)
        am.ApplicationManager.live_json_data = copy.deepcopy(result_list)
        # print(am.ApplicationManager.live_json_data)
        # print("End From Runtime Engine ")
        
       
           
           
        
    def exec_default_result(self):
        vm = am.VariantManager()
        # print(vm.services)
        final_result = ""
        loc = {}
        exec("final_result = "+vm.services[0], globals(), loc)  
        final_result = loc["final_result"]        
        return final_result;
    
    
    
    # def old_mapper(self):
    #     new_lines = len(self.code.split('\n'))
    #     print("New lines ===>> " + str(new_lines))

    #     # Split string into segments based on new line
    #     code_list = self.code.splitlines()
    #     for item in code_list:
    #         print("Item :> " + item + " Space count ==>> " + str(item.count(' ')))
    #     if len(code_list) > 1:
    #         for i in range(len(code_list)):
    #             item_code = code_list[i].strip()
    #             if item_code.startswith('if'):
    #                 if regex_mapper.match(item_code):
    #                     print("Matched code  :::>>>:::: "+item_code)
    #                     context_with_required_value_cs = item_code.split("==")
    #                     print("Context :::: "+str(context_with_required_value_cs))
    #                     cs_ = code_list[i+1].strip()
    #                     print("Conditional service _cs :::: "+cs_)
    #                      .insert(len(context_with_required_value_cs), cs_)
    #                     print("context_with_required_value_cs :: "+str(context_with_required_value_cs))
    #                     self.mapping_dict["mapped_value"+str(i)] = context_with_required_value_cs
    #     for k, v in self.mapping_dict.items():
    #         print(k, ':::::corresponds to::::', v)
    #     return
    
            
    # def old_get_selected_variant(self):
    #     #while True:
    #         #time.sleep(1)
    #         #print("time:::::"+get_am_pm())
    #     selected_variant = ""
    
    #     for k, value in self.mapping_dict.items():
    #         rm = RuntimeEngine()
    #         # required_val = value[1]
    #         required_val = value[1].split(")")[0]
    #         print("required_val:::"+str(required_val))
    #         print("Context Values :: : : : :: : "+str(context_values))
    #         for cv in context_values:
    #             print("current context value + + required_val ")
    #             print(cv)
    #             print(required_val)
    #             if cv in required_val:
    #                 print("Selected Variant : " + str(value[len(value)-1]))
    #                 selected_variant = value[len(value)-1]
    #                 print(str(selected_variant))
    #                 rm.get_and_set_code(selected_variant)
    #             else:
    #                 vm = am.VariantManager()
    #                 services = vm.services
    #                 selected_variant = services[random.randint(0, 1)]
    #                 print(str(selected_variant))
    #                 rm.get_and_set_code(selected_variant)
    #                 #exec(selected_variant)
    #                 #print(str((newspaper_headlines('bitcoin', '2019-11-12', 'publishedAt'))))
    #         #if value[1][:-1] in context_values:
    #         #if any(substring in string for substring in context_values):

    #     return selected_variant








