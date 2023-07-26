import customtkinter

#### MAIN 
__author__='H4NM'
app_title: str='Groppy'
app_version: str='1.2.5'
window_width: int=1500
window_height: int=880
regex_window_width: int=1100
regex_window_height: int=500
app_icon: str='./img/groppy.ico'
default_mode: str = 'dark'
default_theme: str = 'DaynNight'
available_themes_dict: dict = {'Blue': './themes/Blue.json', 
                          'Dark-Blue': './themes/Dark-Blue.json',
                          'DaynNight': './themes/DaynNight.json',
                          'FlipperZero': './themes/FlipperZero.json',
                          'GhostTrain': './themes/GhostTrain.json',
                          'Green': './themes/Green.json',
                          'Greengage': './themes/Greengage.json',
                          'GreyGhost': './themes/GreyGhost.json',
                          'Hades': './themes/Hades.json',
                          'Harlequin': './themes/Harlequin.json',
                          'NightTrain': './themes/NightTrain.json',
                          'Oceanix': './themes/Oceanix.json',
                          'TestCard': './themes/TestCard.json',
                          'TrojanBlue': './themes/TrojanBlue.json',
                          'Yellow': './themes/Yellow.json'}

#### REGEX HIGHLIGHT 
highlight_bg_color: str='#e7e707'    
highlight_fg_color: str='#078dd5'
#BLUE - #078dd5
#GREEN - #07d56b
#YELLOW - #e7e707

### REGEX COMBOBOX MATCHES
maximum_matched_fields: int=14

### FONTS 
main_font: str='Arial'
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
regex_help_button_name: str='Help'
regex_help_window_title: str='Regex Help'
regex_help_headers: list=['Type','Syntax','Description']
regex_help_data: list=[
['Special Character', '^', 'Matches the expression to its right at the start of a string. It matches every such instance before each \n in the string.'],
['Special Character', '$', 'Matches the expression to its left at the end of a string. It matches every such instance before each \n in the string.'],
['Special Character', '.', 'Matches any character except line terminators like \n.'],
['Special Character', '\\', 'Escapes special characters or denotes character classes.'],
['Special Character', 'A|B', 'Matches expression A or B. If A is matched first, B is left untried.'],
['Special Character', '+', 'Greedily matches the expression to its left 1 or more times.'],
['Special Character', '*', 'Greedily matches the expression to its left 0 or more times.'],
['Special Character', '?', 'Greedily matches the expression to its left 0 or 1 times. But if ? is added to qualifiers (+, *, and ? itself) it will perform matches in a non-greedy manner.'],
['Special Character', '{m}', 'Matches the expression to its left m times, and not less.'],
['Special Character', '{m,n}', 'Matches the expression to its left m to n times, and not less.'],
['Special Character', '{m,n}?', 'Matches the expression to its left m times, and ignores n. See ? above.'],
['Character Classes', '\w', 'Matches alphanumeric characters, which means a-z, A-Z, and 0-9. It also matches the underscore, _.'],
['Character Classes', '\d', 'Matches digits, which means 0-9.'],
['Character Classes', '\D', 'Matches any non-digits.'],
['Character Classes', '\s', 'Matches whitespace characters, which include the \t, \n, \r, and space characters.'],
['Character Classes', '\S', 'Matches non-whitespace characters.'],
['Character Classes', '\b', 'Matches the boundary (or empty string) at the start and end of a word, that is, between \w and \W.'],
['Character Classes', '\B', 'Matches where \b does not, that is, the boundary of \w characters.'],
['Character Classes', '\A', 'Matches the expression to its right at the absolute start of a string whether in single or multi-line mode.'],
['Character Classes', '\Z', 'Matches the expression to its left at the absolute end of a string whether in single or multi-line mode.'],
['Sets', '[ ]', 'Contains a set of characters to match.'],
['Sets', '[amk]', 'Matches either a, m, or k. It does not match amk.'],
['Sets', '[a-z]', 'Matches any alphabet from a to z.'],
['Sets', '[a\-z]', 'Matches a, -, or z. It matches - because \ escapes it.'],
['Sets', '[a-]', 'Matches a or -, because - is not being used to indicate a series of characters.'],
['Sets', '[-a]', 'As above, matches a or -.'],
['Sets', '[a-z0-9]', 'Matches characters from a to z and also from 0 to 9.'],
['Sets', '[(+*)]', 'Special characters become literal inside a set, so this matches (, +, *, and ).'],
['Sets', '[^ab5]', 'Adding ^ excludes any character in the set. Here, it matches characters that are not a, b, or 5.'],
['Groups', '( )', 'Matches the expression inside the parentheses and groups it.'],
['Groups', '(? )', 'Inside parentheses like this, ? acts as an extension notation. Its meaning depends on the character immediately to its right.'],
['Groups', '(?PAB)', 'Matches the expression AB, and it can be accessed with the group name.'],
['Groups', '(?:A)', 'Matches the expression as represented by A, but unlike (?PAB), it cannot be retrieved afterwards.'],
['Groups', '(?#...)', 'A comment. Contents are for us to read, not for matching.'],
['Groups', 'A(?=B)', 'Lookahead assertion. This matches the expression A only if it is followed by B.'],
['Groups', 'A(?!B)', 'Negative lookahead assertion. This matches the expression A only if it is not followed by B.'],
['Groups', '(?<=B)A', 'Positive lookbehind assertion. This matches the expression A only if B is immediately to its left. This can only matched fixed length expressions.'],
['Groups', '(?<!B)A', 'Negative lookbehind assertion. This matches the expression A only if B is not immediately to its left. This can only matched fixed length expressions.'],
['Groups', '(?P=name)', 'Matches the expression matched by an earlier group named “name”.'],
['Groups', '(...)\1', 'The number 1 corresponds to the first group to be matched. If we want to match more instances of the same expresion, simply use its number instead of writing out the whole expression again.'],
['Groups - Flags', '(?aiLmsux)', 'Here, a, i, L, m, s, u, and x are flags:'],
['Groups - Flags', 'a', 'Matches ASCII only'],
['Groups - Flags', 'i', 'Ignore case'],
['Groups - Flags', 'L', 'Locale dependent'],
['Groups - Flags', 'm', 'Multi-line'],
['Groups - Flags', 's', 'Matches all'],
['Groups - Flags', 'u', 'Matches unicode'],
['Groups - Flags', 'x', 'Verbose']
]

export_patterns_button_name: str='Save'
clear_patterns_button_name: str='Clear'
getmatches_button_name: str='Test patterns'
automatch_label: str='Auto match'
bg_highlight_label: str='Background'
filter_label: str='Filter'
stats_appear_switch_label: str='View Pattern Stats'
patterns_appear_switch_label: str='View Patterns'


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
bogus_b64_api_key: str='UmVnZXhpbmcgaXMgZnVuIQ=='

#### SETTINGS
settings_file: str="./settings.json"
default_settings: dict={
            "mode": default_mode,
            "theme": default_theme,
            "elastic_host": es_bogus_hostname,
            "elastic_port": es_bogus_port,
            "elastic_auth": False,
            "elastic_user": '',
            "elastic_api_key_is_used": True,
            "elastic_api_key_value": bogus_b64_api_key,
            'elastic_cert_is_used': False,
            'elastic_cert_path': ''
}
available_themes = ", ".join(list(available_themes_dict.keys()))

#### ERROR MESSAGES
RETURN_MESSAGES: dict = {
                    'welcome_msg': f'Welcome to {app_title} version {app_version}!', 
'welcome_info': f'''
Groppy is meant to facilitate creating regex and grok patterns.
In the left frame you may load local files such as log files, grok patterns and json files.
There's also the possibility of retrieving field data from an elasticsearch cluster directly.

Loaded grok patterns can be tested to measure their efficiency to effectivize regex creation productivity.
Since the goal is to make the application easy and nice to use, there's also the option of configuring {app_title} in the file {settings_file}.

Themes that may be used are {available_themes}.
''',
                    'successful_connection': 'Managed to communicate with elasticsearch node',
                    'unsuccessful_connection': 'Unable to communicate with elasticsearch node',
                    'unsuccessful_retrieval_of_index': 'Unable to fetch index',
                    'unsuccessful_retrieval_of_field': 'Unable to fetch field for index',
                    'unsuccessful_retrieval_of_es_data': 'Unable to retrieve field from elasticsearch',
                    'unsuccessful_retrieval_of_jsonfile_data': 'Unable to read data from json file',
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