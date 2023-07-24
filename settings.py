import customtkinter

#### MAIN 
__author__='H4NM'
app_title: str='Groppy'
app_version: str='1.1.0'
window_width: int=1500
window_height: int=880

default_main_color: str = 'dark'
#default_sub_color: str = 'green'
default_sub_color: str = './themes/yellow.json'

#### REGEX HIGHLIGHT 
highlight_bg_color: str='#e7e707'    
highlight_fg_color: str='#078dd5'
#BLUE - #078dd5
#GREEN - #07d56b
#YELLOW - #e7e707

### REGEX COMBOBOX MATCHES
maximum_matched_fields: int=14

### FONTS 
custom_font='./fonts/DM Mono.ttf'
main_font: str='DM Mono'
log_box_font: tuple=('Arial',15,'bold')
loading_label_size: int=32
sheet_header_font:tuple=(main_font, 10, 'normal')
sheet_font: tuple=(main_font, 9, 'normal')
small_font: tuple=(main_font, 12, 'normal')
medium_font: tuple=(main_font, 14, 'normal')
large_font: tuple=(main_font, 20, 'normal')
extra_large_font: tuple=(main_font, 32, 'normal')


#### SIZES
left_sidebar_size: int=150
checkbox_size: int=18
left_es_entry_width: int=130
left_es_entry_height: int=25
loading_label_text: str='Loading...'


#### TEXT LABELS
lfi_frame_label: str='Grok patterns'
load_field_label: str='Load data'
load_data_tabview_es: str='Elasticsearch'
load_data_tabview_local_file: str='Local Files'
es_basic_auth_label: str='Basic Auth'
es_api_key_label: str='API Key'
es_cert_label: str='SSL Cert'
es_unique_lines_label: str='Unique Lines'
es_hostname_label_text: str='Host:'
es_port_label_text: str='Port:'
es_username_label_text: str='User:'
es_password_label_text: str='Pass:'
es_api_key_label_text: str='Key:'
es_cert_label_text: str='Cert:'
es_index_label_text: str='Index:'
es_field_label_text: str='Field:'
es_query_label_text: str='Query:'
appearance_frame_label: str='Appearance'
lfi_log_button_name: str='Log File'
lfi_unique_fields_label: str='Unique\nlines'
lfi_pattern_button_name: str='Grok Patterns'
lfi_json_file_button_name: str='JSON File'
conn_test_button_name: str='Check connection'
getesfield_button_name: str='Get field value'
getjsonfield_button_name: str='Get json key value'
match_button_name: str='Match'
add_pattern_button_name: str='Add pattern'
export_patterns_button_name: str='Save'
clear_patterns_button_name: str='Clear'
getmatches_button_name: str='Test patterns'
automatch_label: str='Auto match'
bg_highlight_label: str='Background'
filter_label: str='Filter'
stats_appear_switch_label: str='View Pattern Stats'
patterns_appear_switch_label: str='View Patterns'

#### ERROR MESSAGES
RETURN_MESSAGES: dict = { 
                    'successful_connection': 'Managed to communicate with elasticsearch node',
                    'unsuccessful_connection': 'Unable to communicate with elasticsearch node',
                    'unsuccessful_retrieval_of_index': 'Unable to fetch index',
                    'unsuccessful_retrieval_of_field': 'Unable to fetch field for index',
                    'unsuccessful_retrieval_of_es_data': 'Unable to retrieve field from elasticsearch',
                    'unsuccessful_retrieval_of_jsonfile_data': 'Unable to retrieve field from json file',
                    'no_patterns_for_export': 'There are no patterns to export',
                    'invalid_export_dest':'Unable to export patterns to provided destination',
                    'successful_pattern_export':'Successfully saved the patterns',
                    'no_log_to_match':'There is no log to match patterns against',
                    'no_patterns_to_match':'There are no patterns to match against the log',
                    'unsuccessful_log_file_load':'Unable to load the specified log file',
                    'unsuccessful_grok_file_load':'Unable to load the specified grok patterns file',
                    'unsuccessful_json_file_load':'Unable to load the specified json file',
                    'unsuccessful_pattern_matches':'Unable to test the provided patterns to the given log'
                    }


#### ELASTIC
requests_timeout: int=5
es_bogus_hostname: str='localhost'
es_bogus_port: str='9200'
es_default_auth: str=None
es_default_api_key: str=None
es_default_cert: str=None
es_bogus_username: str='elastic'
es_bogus_password: str='secret'
es_bogus_api_key: str='B64 encoded key'
es_bogus_cert: str='/path/to/cert'
es_bogus_field: str='message'
es_bogus_index: str='*'
es_bogus_query: str='*'
json_bogus_field: str=''
es_max_docs: int=1500
bogus_textbox_text: str='Regex me please..'

#### RESOURCES
app_icon: str=r'.\img\groppy.ico'
clear_button_path: str=r'.\img\clear.png'
getmatches_button_path: str=r'.\img\getmatches.png'
getesfields_button_path: str=r'.\img\getesfields.png'
match_button_path: str=r'.\img\match.png'
save_button_path: str=r'.\img\save.png'
add_button_path: str=r'.\img\add.png'

