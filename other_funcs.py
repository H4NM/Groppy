import re
from typing import Union 

grok_re = re.compile(r"\%\{[A-Z0-9_\:\[\]\.\_\-]+\}", flags=re.I)
grok_re_name = re.compile(r"\%\{([A-Z0-9\_\-]+)([a-zA-Z0-9\[\]\.\:\_\-]+)?\}")

def valid_regex(pattern: str) -> bool:
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False
    
def has_grok_pattern(text: str) -> bool:
    if grok_re.search(text):
        return True
    else:
        return False

def get_pattern_ref(match_pat: str) -> list:
    if has_grok_pattern(match_pat):
        return grok_re.findall(match_pat)
    else:
        return []

def extract_pattern_ref_name(pattern_str: str) -> str:
    result = grok_re_name.search(pattern_str)
    if result:
        return result.group(1)
    else:
        raise Exception
    
def convert_patterns(patterns: dict) -> dict:
    conv_patterns = {}
    for value in patterns:
        if has_grok_pattern(patterns[value]):
            conv_patterns[value] = convert_pattern_str(patterns[value], patterns)
        else:
            conv_patterns[value] = patterns[value]
    return conv_patterns

def convert_pattern_str(pattern_value: str, patterns: dict) -> Union[callable,str]:
    for ref in get_pattern_ref(pattern_value):
        ref_name = extract_pattern_ref_name(ref)
        if not ref_name in patterns:
            raise ValueError("Found reference to pattern that does not exist. Pattern name: {}. Please check that it's included in the patterns that are being processed.".format(ref_name))
        pattern_value = pattern_value.replace(ref, patterns[ref_name])
    
    if has_grok_pattern(pattern_value):
        return convert_pattern_str(pattern_value, patterns)
    else:
        return pattern_value

def get_matches(log: list, patterns: dict, pattern_filter: list=[]) -> tuple[dict, dict]:
    regex_matches = {}
    metadata = {}
    check_counter = 0

    for message in log:
        for pattern in pattern_filter:
            check_counter += 1
            if valid_regex(patterns[pattern]) and regex_does_match(patterns[pattern], message):
                if pattern not in regex_matches:
                    regex_matches[pattern] = {}
                    regex_matches[pattern]['total_checks'] = 0
                    regex_matches[pattern]['checks'] = []
                
                pattern_inst = {}
                pattern_inst['log_message'] = message
                pattern_inst['regex'] = patterns[pattern]
                pattern_inst['match'] = regex_search(patterns[pattern], message)
                pattern_inst['match_percent'] = get_percent(pattern_inst['match'], message)

                regex_matches[pattern]['checks'].append(pattern_inst)
                regex_matches[pattern]['total_checks'] += 1

    metadata['log_amount'] = len(log)
    metadata['pattern_amount'] = len(patterns)
    metadata['check_amount'] = check_counter
    return regex_matches, get_pattern_stats(regex_matches, metadata)

def get_pattern_stats(regex_results: dict, metadata: dict) -> dict:
    metadata['pattern_stats'] = {}
    for pattern in regex_results:
        match_counter = 0
        hundred_perc_match_counter = 0
        for instance in regex_results[pattern]['checks']:
            match_counter += 1
            if instance['match_percent'] == "{:.1%}".format(1):
                hundred_perc_match_counter += 1

        metadata['pattern_stats'][pattern] = {}
        metadata['pattern_stats'][pattern]['total_matches'] = match_counter
        metadata['pattern_stats'][pattern]['total_match_perc'] = get_percent(match_counter, metadata['log_amount'])
        metadata['pattern_stats'][pattern]['total_full_matches'] = hundred_perc_match_counter

    return metadata

def get_percent(part: Union[str, int], whole:Union[str, int]) -> str:
    if type(part) is str and type(whole) is str:
        return "{:.1%}".format(len(part)/len(whole))
    else: 
        #port is int and whole is int
        return "{:.1%}".format(part/whole)

def regex_does_match(regex: str, message: str) -> bool:
    if re.search(regex, message, flags=re.S|re.M|re.A):
        return True
    else:
        return False
    
def regex_search(regex: str, message: str) -> str:
    return re.search(regex, message, flags=re.S|re.M|re.A).group()

def get_res_table_format(matches: dict) -> tuple[list,list]:
    column_headers = ["Pattern", "Match", "Match %", "Row", "Regex"]
    table = []
    for pattern in matches:
        for check in matches[pattern]['checks']:
            table.append([pattern,                     
                               repr(check['match']),       
                               check['match_percent'],      
                               check['log_message'],        
                               check['regex']])             
    return table, column_headers

def get_stats_table_format(stats: dict) -> tuple[list,list]:
    column_headers = ["Pattern", "Total matches", "Total match %", "Entire message matches"]
    table_list = []
    for stat in stats['pattern_stats']:
        table_list.append([stat, 
                           stats['pattern_stats'][stat]['total_matches'],
                           stats['pattern_stats'][stat]['total_match_perc'],
                           stats['pattern_stats'][stat]['total_full_matches']])
    return table_list, column_headers

def get_pattern_table_format(patterns: dict) -> list[list[str, str]]:
    return [[pattern, patterns[pattern]] for pattern in patterns]

def extract_patterns(lines: list) -> dict:
    patterns = {}
    for line in lines:
        line = line.strip()
        if line and not line[0] == "#":
            line_comp = line.split(" ")
            pat_name, match_pat = line_comp[0], " ".join(line_comp[1:])
            if match_pat and (valid_regex(match_pat) or has_grok_pattern(match_pat)):
                patterns[pat_name] = match_pat
    return patterns

def get_jsonfile_key_names(json_obj: dict, parent_key: str='', key_paths: list=[]) -> list:
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            get_jsonfile_key_names(value, new_key, key_paths)
    else:
        key_paths.append(parent_key)
    return key_paths

def extract_jsonfile_field_data(json_obj: dict, key_string: str, unique: bool=True) -> list:
    field_list = []
    keys = key_string.split(".")
    value = json_obj

    for key in keys:
        value = value[key]
        if isinstance(value, list):
            value = ' '.join(value)    
        if unique and value in field_list:
            continue
    field_list.append(value)
  
    return field_list
