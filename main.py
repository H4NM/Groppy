#Custom modules
import other_funcs, es_funcs
from settings import *
from custom_widgets import *

#External modules
import re, customtkinter, json, os
from threading import Thread
from typing import Union

class Groppy(customtkinter.CTk):
    def __init__(self, app_settings):
        super().__init__()
        self.initialize_main_window()
        self.load_color_schema(app_settings)

        self.declare_variables()
        self.initialize_left_sidebar()
        self.initialize_middle_components()
        self.initialize_right_sidebar()

        self.declare_default_states()
        self.light_text_color, self.dark_text_color = self.application_title.cget("text_color")
        self.fg_light_color, self.fg_dark_color = self.sidebar_frame_left.cget("fg_color")
        self.border_light_color, self.border_dark_color = self.sidebar_frame_left.cget("border_color")
        self.update_color_scheme()

        if not app_settings['successful_load']:
            CustomMessagebox(title='Load settings', label=RETURN_MESSAGES['unsuccessful_retrieval_of_jsonfile_data'], text=app_settings['failure_reason'], geometry=self.messagebox_geometry)
        
        if app_settings['initial_start']:
            CustomMessagebox(title='Welcome', label=RETURN_MESSAGES['welcome_msg'], text=RETURN_MESSAGES['welcome_info'], geometry=self.welcome_messagebox_geometry)
        
        self.enable_settings(app_settings)

    def load_color_schema(self, app_settings: dict):
        self.main_color = app_settings['mode']
        self.sub_color = app_settings['theme']

    def enable_settings(self, app_settings: dict):

        if app_settings['elastic_host']:
            self.es_host_entry.insert(0, app_settings['elastic_host'])
        
        if app_settings['elastic_port']:
            self.es_port_entry.insert(0, app_settings['elastic_port'])

        if app_settings['elastic_auth']:
            self.toggle_es_auth()

        if app_settings['elastic_user']:
            self.es_username_entry.insert(0, app_settings['elastic_user'])

        if app_settings['elastic_api_key_is_used']:
            self.toggle_es_api()
        
        if app_settings['elastic_api_key_value']:
            self.api_key_entry.insert(0, app_settings['elastic_api_key_value'])

        if app_settings['elastic_cert_is_used']:
            self.toggle_es_cert()

        if app_settings['elastic_cert_path']:
            self.es_cert_entry.insert(0, app_settings['elastic_cert_path'])

    def initialize_main_window(self):
        """
        Initializes the window with components such as icon, title, geometry
        """
        self.wm_iconbitmap(app_icon)
        self.title(app_title+"/"+app_version)
        self.geometry("%dx%d" % (window_width, window_height))

        self.grid_columnconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13,14), weight=1)
        self.grid_columnconfigure((0,15,16), weight=0)
        self.grid_rowconfigure((1), weight=3)
     
    def declare_variables(self):
        """
        Declares variables
        """
        self.log_box_font=log_box_font
        self.created_patterns = 1
        self.auto_match = True
        self.bg_highlight = False
        self.es_indicies = []
        self.es_fields = []
        self.json_fields = []
        self.include=[]
        self.exclude=[]
        self.include_sign="\U00002714"
        self.exclude_sign="\U0000274C"
        self.filter_list = [self.include, self.exclude]
        self.table_list = set()
    
    def initialize_left_sidebar(self):
        """
        Initializes the left sidebar of the window and all of the components inside
        """
        self.sidebar_frame_left = customtkinter.CTkFrame(self, corner_radius=0, width=left_sidebar_size)
        self.sidebar_frame_left.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame_left.grid_rowconfigure(6, weight=1)
    
        self.application_title = customtkinter.CTkLabel(self.sidebar_frame_left, 
                                                       text=app_title, 
                                                       font=large_font)
        self.application_title.grid(row=0, column=0, columnspan=5, padx=10, pady=(5, 0), sticky="n")
        
        ### LOAD FIELD TABVIEW 
        self.load_data_tabview =  CustomTabView(self.sidebar_frame_left, 
                                                width=220)
        self.load_data_tabview.add(load_data_tabview_local_file)
        self.load_data_tabview.add(load_data_tabview_es)

        self.load_data_tabview.grid(row=1, column=0, columnspan=2,  padx=(30,30), sticky="new")
        self.load_data_tabview.tab(load_data_tabview_es).grid_columnconfigure((0,1), weight=0) 
        self.load_data_tabview.tab(load_data_tabview_local_file).grid_columnconfigure((0,1), weight=1) 

        #### Logg File Tabview
        self.initialize_local_file_tabview()

        #### Elasticsearch Tabview
        self.initialize_es_tabview()

        ### APPEARANCE FRAME
        self.sidebar_appearance_frame_left = customtkinter.CTkFrame(self.sidebar_frame_left, corner_radius=5)
        self.sidebar_appearance_frame_left.grid(row=9, column=0,columnspan=2, padx=(30,30),pady=(10,10), sticky="new")
        self.sidebar_appearance_frame_left.grid_columnconfigure((1,2,3), weight=1)
        self.sidebar_appearance_frame_left.grid_rowconfigure((0,1,2,3), weight=1)

        ### APPEARANCE LABEL
        self.appearance_label = customtkinter.CTkLabel(self.sidebar_appearance_frame_left, 
                                                       text=appearance_frame_label, 
                                                       font=medium_font)
        self.appearance_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(5, 0), sticky="n")
        
        ### PATTERNS SWITCH
        self.patterns_frame_switch = customtkinter.CTkCheckBox(master=self.sidebar_appearance_frame_left, 
                                                               command=self.toggle_patterns_frame, 
                                                               text=patterns_appear_switch_label,
                                                               checkbox_width=checkbox_size,
                                                               checkbox_height=checkbox_size,
                                                               font=small_font)
        self.patterns_frame_switch.grid(row=1, column=0,columnspan=2,padx=20, pady=(5, 0), sticky="w")
        
        ### STATS SWITCH
        self.patterns_stats_frame_switch = customtkinter.CTkCheckBox(master=self.sidebar_appearance_frame_left, 
                                                                     command=self.toggle_stats_frame, 
                                                                     text=stats_appear_switch_label,
                                                                     checkbox_width=checkbox_size,
                                                                     checkbox_height=checkbox_size,
                                                                     font=small_font)
        self.patterns_stats_frame_switch.grid(row=2, column=0,columnspan=2,padx=20, pady=(5, 5), sticky="w")


        ### APPEARANCE SWITCH
        self.switch_main_appearance = customtkinter.CTkSwitch(master=self.sidebar_appearance_frame_left, 
                                                              command=self.change_appearance_main_color, 
                                                              text=self.get_color_switch_label(),
                                                              font=medium_font)
        self.switch_main_appearance.grid(row=3, column=0, columnspan=2,padx=20, pady=(0, 5), sticky="w")

    def initialize_local_file_tabview(self):
        ### SIDEBAR BUTTON LOGFILE
        self.sidebar_button_logfile = customtkinter.CTkButton(self.load_data_tabview.tab(load_data_tabview_local_file), 
                                                              text=lfi_log_button_name, 
                                                              command=self.read_log,  
                                                              width=10,
                                                              font=small_font)
        self.sidebar_button_logfile.grid(row=0, column=0, columnspan=4, padx=(10,0), pady=10, sticky="we")
        
        ### SIDEBAR SWITCH UNIQUE LINES
        self.unique_logfile_lines_switch = customtkinter.CTkCheckBox(self.load_data_tabview.tab(load_data_tabview_local_file), 
                                                                     width=20,
                                                                     command=self.toggle_get_unique_logfile_lines, 
                                                                     text=lfi_unique_fields_label,
                                                                     checkbox_width=checkbox_size,
                                                                     checkbox_height=checkbox_size,
                                                                     font=small_font)
        self.unique_logfile_lines_switch.grid(row=0, column=5, padx=(5,10), pady=(5, 0))
        self.unique_logfile_lines_switch.select()
        
        ### SIDEBAR BUTTON GROK PATTERNS
        self.sidebar_button_patternlocation = customtkinter.CTkButton(self.load_data_tabview.tab(load_data_tabview_local_file), 
                                                                      text=lfi_pattern_button_name, 
                                                                      command=self.read_patterns, 
                                                                      width=10,
                                                                      font=small_font)
        self.sidebar_button_patternlocation.grid(row=1, column=0, columnspan=6, padx=10, pady=(5,10), sticky="we")

        ### SIDERBAR BUTTON JSON LOCATION        
        self.sidebar_button_jsonlocation = customtkinter.CTkButton(self.load_data_tabview.tab(load_data_tabview_local_file), 
                                                                   text=lfi_json_file_button_name, 
                                                                   command=self.read_json, 
                                                                   width=10,
                                                                   font=small_font)
        self.sidebar_button_jsonlocation.grid(row=2, column=0, columnspan=4, padx=(10,0), pady=10, sticky="we")

        ### SIDEBAR JSONFILE SWITCH UNIQUE LINES
        self.unique_jsonfile_lines_switch = customtkinter.CTkCheckBox(self.load_data_tabview.tab(load_data_tabview_local_file), 
                                                                      width=20,
                                                                      command=self.toggle_get_unique_jsonfile_results, 
                                                                      text=lfi_unique_fields_label,
                                                                      checkbox_width=checkbox_size,
                                                                      checkbox_height=checkbox_size,
                                                                      font=small_font)
        self.unique_jsonfile_lines_switch.grid(row=2, column=5, padx=(5,10), pady=(5, 0))
        self.unique_jsonfile_lines_switch.select()

        ### JSON FIELD LABEL
        self.json_field_label = customtkinter.CTkLabel(self.load_data_tabview.tab(load_data_tabview_local_file), 
                                                       text=es_field_label_text,
                                                       font=small_font)
        self.json_field_label.grid(row=3, column=0, padx=(5,0))
        
        ### JSON FIELD ENTRY
        self.json_field_entry_dv = customtkinter.StringVar()
        self.json_field_entry_dv.trace_add("write", self.json_field_autocomplete_callback)
        
        ### JSON FIELD COMBOBOX
        self.json_field_combobox = customtkinter.CTkComboBox(self.load_data_tabview.tab(load_data_tabview_local_file),
                                                            variable=self.json_field_entry_dv, 
                                                            values=self.json_fields, 
                                                            height=left_es_entry_height)
        
        self.json_field_combobox.grid(row=3, column=1, columnspan=5, padx=(5,10),pady=5)

        ### JSON BUTTON GET FIELDS
        self.sidebar_button_json_fields = customtkinter.CTkButton(self.load_data_tabview.tab(load_data_tabview_local_file), 
                                                                  text=getjsonfield_button_name,
                                                                  command=lambda: self.compute(self.get_json_field_data),
                                                                  font=small_font)
                                                                  
        self.sidebar_button_json_fields.grid(row=4, column=0, columnspan=6, padx=10, pady=(5,10), sticky="we")

    def initialize_es_tabview(self):
        ### ES HOST LABEL
        self.es_host_label = customtkinter.CTkLabel(self.load_data_tabview.tab(load_data_tabview_es), 
                                                    text=es_hostname_label_text,
                                                    font=small_font)
        self.es_host_label.grid(row=0, column=0, padx=(5,0), sticky="we")
       
        ### ES HOST ENTRY
        self.es_host_entry = customtkinter.CTkEntry(self.load_data_tabview.tab(load_data_tabview_es), 
                                                    placeholder_text=es_bogus_hostname, 
                                                    height=left_es_entry_height)
        self.es_host_entry.grid(row=0, column=1, columnspan=2, padx=(5,10), sticky="w")

        ### ES PORT LABEL
        self.es_port_label = customtkinter.CTkLabel(self.load_data_tabview.tab(load_data_tabview_es), 
                                                    text=es_port_label_text,
                                                    font=small_font)
        self.es_port_label.grid(row=1, column=0, padx=(5,0), sticky="we")
        
        ### ES PORT ENTRY
        self.es_port_entry = customtkinter.CTkEntry(self.load_data_tabview.tab(load_data_tabview_es), 
                                                    placeholder_text=es_bogus_port, 
                                                    height=left_es_entry_height)
        self.es_port_entry.grid(row=1, column=1, columnspan=2, padx=(5,10), sticky="w")
       
        ### ES AUTH SWITCH
        self.auth_switch = customtkinter.CTkCheckBox(self.load_data_tabview.tab(load_data_tabview_es), 
                                                     command=self.toggle_es_auth, 
                                                     text=es_basic_auth_label,
                                                     checkbox_width=checkbox_size,
                                                     checkbox_height=checkbox_size,
                                                     font=small_font)
        
        self.auth_switch.grid(row=2, column=0, columnspan=3, padx=20, pady=(5, 0), sticky="w")
        
        ### ES USERNAME LABEL
        self.es_username_label = customtkinter.CTkLabel(self.load_data_tabview.tab(load_data_tabview_es), 
                                                        text=es_username_label_text,
                                                        font=small_font)
        
        self.es_username_label.grid(row=3, column=0, padx=(5,0), sticky="w")

        ### ES USERNAME ENTRY
        self.es_username_entry = customtkinter.CTkEntry(self.load_data_tabview.tab(load_data_tabview_es), 
                                                        height=left_es_entry_height,
                                                        placeholder_text=es_bogus_username)
        
        self.es_username_entry.grid(row=3, column=1,columnspan=2, padx=(5,10), sticky="w")

        ### ES PASSWORD LABEL
        self.es_password_label = customtkinter.CTkLabel(self.load_data_tabview.tab(load_data_tabview_es), 
                                                        text=es_password_label_text,
                                                        font=small_font)
        self.es_password_label.grid(row=4, column=0, padx=(5,0), sticky="w")

        ### ES PASSWORD ENTRY
        self.es_password_entry = customtkinter.CTkEntry(self.load_data_tabview.tab(load_data_tabview_es),  
                                                        height=left_es_entry_height, 
                                                        placeholder_text=es_bogus_password)
        self.es_password_entry.grid(row=4, column=1,columnspan=2, padx=(5,10), sticky="w")

        ### ES API KEY SWITCH
        self.api_key_switch = customtkinter.CTkCheckBox(self.load_data_tabview.tab(load_data_tabview_es), 
                                                        command=self.toggle_es_api, 
                                                        text=es_api_key_label,
                                                        checkbox_width=checkbox_size,
                                                        checkbox_height=checkbox_size,
                                                        font=small_font)
        self.api_key_switch.grid(row=5, column=0, columnspan=3, padx=20, pady=(5, 0), sticky="w")

        ### API KEY LABEL
        self.api_key_label = customtkinter.CTkLabel(self.load_data_tabview.tab(load_data_tabview_es), 
                                                    text=es_api_key_label_text,
                                                    font=small_font)
        self.api_key_label.grid(row=6, column=0, padx=(5,0), sticky="w")

        ### API KEY ENTRY
        self.api_key_entry = customtkinter.CTkEntry(self.load_data_tabview.tab(load_data_tabview_es), 
                                                    height=left_es_entry_height,
                                                    placeholder_text=es_bogus_api_key)
        self.api_key_entry.grid(row=6, column=1,columnspan=2, padx=(5,10), sticky="we")

        ### ES CERT SWITCH
        self.es_cert_switch = customtkinter.CTkCheckBox(self.load_data_tabview.tab(load_data_tabview_es), 
                                                        command=self.toggle_es_cert, 
                                                        text=es_cert_label,
                                                        checkbox_width=checkbox_size,
                                                        checkbox_height=checkbox_size,
                                                        font=small_font)
        
        self.es_cert_switch.grid(row=7, column=0, columnspan=3, padx=20, pady=(5, 0), sticky="w")

        ### CERT LABEL
        self.es_cert_label = customtkinter.CTkLabel(self.load_data_tabview.tab(load_data_tabview_es), 
                                                    text=es_cert_label_text,
                                                    font=small_font)
        self.es_cert_label.grid(row=8, column=0, padx=(5,0), sticky="w")

        ### CERT ENTRY
        self.es_cert_entry = customtkinter.CTkEntry(self.load_data_tabview.tab(load_data_tabview_es), 
                                                    height=left_es_entry_height, 
                                                    placeholder_text=es_bogus_cert)
        self.es_cert_entry.grid(row=8, column=1,columnspan=2, padx=(5,10), sticky="we")

        ### ES TEST CONNECTION BUTTON
        self.sidebar_button_es_conn = customtkinter.CTkButton(self.load_data_tabview.tab(load_data_tabview_es), 
                                                              text=conn_test_button_name, 
                                                              command=lambda: self.compute(self.test_es_connection),
                                                              font=small_font)
        self.sidebar_button_es_conn.grid(row=9, column=0, columnspan=3,padx=5, pady=10)
        
        ### ES INDEX LABEL
        self.es_index_label = customtkinter.CTkLabel(self.load_data_tabview.tab(load_data_tabview_es), 
                                                     text=es_index_label_text,
                                                     font=small_font)
        self.es_index_label.grid(row=10, column=0, padx=(5,0), sticky="w")
        
        ### ES INDEX ENTRY
        self.es_index_entry_dv = customtkinter.StringVar()
        self.es_index_entry_dv.trace_add("write", self.index_autocomplete_callback)
        
        ### ES INDEX COMBOBOX
        self.es_index_combobox = customtkinter.CTkComboBox(self.load_data_tabview.tab(load_data_tabview_es), 
                                                           variable=self.es_index_entry_dv, 
                                                           values=self.es_indicies, 
                                                           height=left_es_entry_height)
        self.es_index_combobox.grid(row=10, column=1,columnspan=2, padx=(5,10),pady=5, sticky="we")
        
        ### ES FIELD LABEL
        self.es_field_label = customtkinter.CTkLabel(self.load_data_tabview.tab(load_data_tabview_es), 
                                                     text=es_field_label_text,
                                                     font=small_font)
        self.es_field_label.grid(row=11, column=0, padx=(5,0), sticky="w")
        
        ### ES FIELD ENTRY
        self.es_field_entry_dv = customtkinter.StringVar()
        self.es_field_entry_dv.trace_add("write", self.es_field_autocomplete_callback)
        
        ### ES FIELD COMBOBOX
        self.es_field_combobox = customtkinter.CTkComboBox(self.load_data_tabview.tab(load_data_tabview_es), 
                                                           variable=self.es_field_entry_dv, 
                                                           values=self.es_fields, 
                                                           height=left_es_entry_height)
        self.es_field_combobox.grid(row=11, column=1,columnspan=2, padx=(5,10),pady=5, sticky="we")
        
        ### ES QUERY LABEL
        self.es_query_label = customtkinter.CTkLabel(self.load_data_tabview.tab(load_data_tabview_es), 
                                                     text=es_query_label_text,
                                                     font=small_font)
        self.es_query_label.grid(row=12, column=0, padx=(5,0), sticky="w")
        
        ### ES QUERY ENTRY
        self.es_query_entry = customtkinter.CTkEntry(self.load_data_tabview.tab(load_data_tabview_es), 
                                                     placeholder_text=es_bogus_query, 
                                                     height=left_es_entry_height)
        self.es_query_entry.grid(row=12, column=1,columnspan=2, padx=(5,10),pady=5, sticky="we")
        
        ### GET UNIQUE ENTRIES
        self.es_unique_data_switch = customtkinter.CTkCheckBox(self.load_data_tabview.tab(load_data_tabview_es), 
                                                               command=self.toggle_get_unique_es_results, 
                                                               text=es_unique_lines_label,
                                                               checkbox_width=checkbox_size,
                                                               checkbox_height=checkbox_size,
                                                               font=small_font)
        self.es_unique_data_switch.grid(row=13, column=0, columnspan=3, padx=20, pady=(5, 0), sticky="w")
        self.es_unique_data_switch.select()

        ### ES BUTTON GET FIELDS
        self.sidebar_button_es_fields = customtkinter.CTkButton(self.load_data_tabview.tab(load_data_tabview_es), 
                                                                text=getesfield_button_name, 
                                                                command=lambda: self.compute(self.get_es_field_data),
                                                                font=small_font)
        self.sidebar_button_es_fields.grid(row=14, column=0, columnspan=3, padx=5, pady=10)

    def initialize_middle_components(self):
        """
        Initializes the components in the middle of the window
        """
        self.textbox_log = CustomTextBox(self, font=self.log_box_font)
        self.textbox_log.grid(row=1, column=1, columnspan=15, pady=(10,20), padx=20, sticky="nsew")
        self.update_textbox(self.textbox_log, bogus_textbox_text, editable=True)

        ### MIDDLE FRAME - LOADING BOX
        self.create_loading_frame()

        ### MIDDLE FRAME - REGEX ENTRY BOX
        self.regexp_entry_dv = customtkinter.StringVar()
        self.regexp_entry_dv.trace_add("write", self.highlight_callback)
        self.regexp_entry = customtkinter.CTkEntry(self,  textvariable=self.regexp_entry_dv, width=500)
        self.regexp_entry.grid(row=0,column=1, columnspan=13, padx=(20, 0),pady=(20, 20), sticky="we")

        ### MIDDLE FRAME - MATCH BUTTON
        self.match_entry_button = customtkinter.CTkButton(self, 
                                                          text=match_button_name,
                                                          command=self.highlight, 
                                                          width=20,
                                                          font=small_font)
        self.match_entry_button.grid(row=0, column=14, padx=(5,5), pady=(5,5), sticky="we")

        ### MIDDLE FRAME - ENTRY FRAME 
        self.entry_frame_middle = customtkinter.CTkFrame(self, corner_radius=5, height=20, width=20)
        self.entry_frame_middle.grid(row=0, column=15, padx=(0,20), pady=(10, 5), sticky="we")
        self.entry_frame_middle.grid_rowconfigure((0,1), weight=1)
        self.entry_frame_middle.grid_columnconfigure((0,1), weight=1)

        ### ENTRY FRAME - REGEX SWITCH
        self.switch_regexp_match = customtkinter.CTkSwitch(self.entry_frame_middle, 
                                                           command=self.toggle_auto_match, 
                                                           font=small_font,
                                                           text=automatch_label)
        self.switch_regexp_match.grid(row=0, column=0, pady=(5,0),padx=(10,10),sticky="we")
        self.switch_regexp_match.select()

        ### ENTRY FRAME - HIGHLIGHT SWITCH
        self.switch_bg_highlight = customtkinter.CTkSwitch(self.entry_frame_middle, 
                                                           command=self.toggle_bg_highlight, 
                                                           font=small_font,
                                                           text=bg_highlight_label)
        self.switch_bg_highlight.grid(row=1, column=0, pady=(0,5), padx=(10,10),sticky="we")

        ### ENTRY FRAME - EXPORT BUTTON
        self.save_entry_button = customtkinter.CTkButton(self.entry_frame_middle, 
                                                           text=add_pattern_button_name,
                                                           command=self.add_pattern_to_table,
                                                           font=small_font)
        self.save_entry_button.grid(row=0, rowspan=2, column=1, padx=(5,5), pady=(5,5), sticky="we")

        ### ENTRY FRAME - REGEX HELP BUTTON
        self.re_help_button = customtkinter.CTkButton(self.entry_frame_middle, 
                                                      width=20,
                                                      text=regex_help_button_name,
                                                      command=self.create_regex_help_msgbox,
                                                      font=small_font)
        

        self.re_help_button.grid(row=0, rowspan=2, column=2, padx=(5,5), pady=(5,5), sticky="we")

        ### MIDDLE FRAME - TABVIEW
        self.tabview = CustomTabView(self)
        self.tabview.grid(row=2, column=1, columnspan=15, rowspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.tabview.add("Stats")
        self.tabview.add("Results")
        self.tabview.tab("Stats").grid_columnconfigure((0,1), weight=1) 
        self.tabview.tab("Results").grid_columnconfigure(0, weight=1)

        ### MIDDLE FRAME - STATS TABLE
        self.stats_sheet = CustomSheet(self.tabview.tab("Stats"), 
                                theme=self.main_color+" "+self.sub_color,
                                show_x_scrollbar = True,
                                show_y_scrollbar = False,
                                empty_horizontal = False,
                                empty_vertical = False,
                                show_top_left = False,
                                show_row_index = True)

        self.stats_sheet.grid(row = 0, column = 0, columnspan=2, sticky = "nswe")
        self.table_list.add(self.stats_sheet)

        self.stats_sheet.enable_filter_in_menue("Include",lambda: self.pattern_filter(self.stats_sheet, self.include, "include"))
        self.stats_sheet.enable_filter_in_menue("Exclude",lambda: self.pattern_filter(self.stats_sheet, self.exclude, "exclude"))
 
        ### MIDDLE FRAME - RESULTS TABLE
        self.results_sheet = CustomSheet(self.tabview.tab("Results"), 
                            theme=self.main_color+" "+self.sub_color,
                            show_x_scrollbar = True,
                            show_y_scrollbar = False,
                            empty_horizontal = False,
                            empty_vertical = False,
                            show_top_left = False,
                            show_row_index = True)
        self.results_sheet.grid(row = 0, column = 0, sticky = "nswe")
        self.table_list.add(self.results_sheet)
        self.results_sheet.enable_filter_in_menue("Include",lambda: self.pattern_filter(self.results_sheet, self.include, "include"))
        self.results_sheet.enable_filter_in_menue("Exclude",lambda: self.pattern_filter(self.results_sheet, self.exclude, "exclude"))

    def initialize_right_sidebar(self):
        """
        Initializes the right frame and the components within
        """
        ### RIGHT FRAME
        self.sidebar_frame_right = customtkinter.CTkFrame(self, corner_radius=5, width=100)
        self.sidebar_frame_right.grid(row=0, column=16, rowspan=4, padx=(0,20), pady=(10, 20), sticky="nsew")
        self.sidebar_frame_right.grid_rowconfigure((0,1,2,4,5,6), weight=1)

        ### RIGHT FRAME - PATTERNS LABEL
        self.patterns_label = customtkinter.CTkLabel(self.sidebar_frame_right, 
                                                     text=lfi_pattern_button_name, 
                                                     font=large_font)
        self.patterns_label.grid(row=0, column=0, padx=40, pady=(0, 10), sticky="s")
        
        ### RIGHT FRAME - PATTERNS TABLE
        self.patterns_sheet = CustomSheet(self.sidebar_frame_right, width=100, 
                                theme=self.main_color+" "+self.sub_color,
                                show_x_scrollbar = False,
                                show_y_scrollbar = False,
                                empty_horizontal = False,
                                empty_vertical = False, 
                                show_top_left = False,
                                show_row_index = False,
                                show_header = False,
                                headers=["Pattern", "Regex"],
                                column_width=99)
        self.patterns_sheet.grid(row=1, rowspan=2, column=0, padx=20, sticky="nsew")
        self.table_list.add(self.patterns_sheet)

        ### RIGHT FRAME - PATTERNS TABLE FUNCTIONS
        self.patterns_sheet.enable_filter_in_menue("Include",
                                                   lambda: self.pattern_filter(self.patterns_sheet, self.include, "include"))
        self.patterns_sheet.enable_filter_in_menue("Exclude",
                                                   lambda: self.pattern_filter(self.patterns_sheet, self.exclude, "exclude"))
        self.patterns_sheet.popup_menu_add_command("Delete", 
                                                   lambda: self.delete_pattern_from_table(self.patterns_sheet), 
                                                   index_menu = False, 
                                                   header_menu = False)
        self.patterns_sheet.disable_bindings("double_click_column_resize")    

        ### RIGHT FRAME - EXPORT PATTERNS BUTTON
        self.sidebar_button_export_patterns = customtkinter.CTkButton(self.sidebar_frame_right, 
                                                                      text=export_patterns_button_name, 
                                                                      command=self.export_patterns, 
                                                                      width=10,
                                                                      font=small_font)
        self.sidebar_button_export_patterns.grid(row=3, column=0, padx=20, pady=(10,0), sticky="n")

        ### RIGHT FRAME - FILTER LABEL
        self.filter_label = customtkinter.CTkLabel(self.sidebar_frame_right, 
                                                   text=filter_label, 
                                                   font=large_font)
        self.filter_label.grid(row=4, column=0, padx=40, pady=(0, 10), sticky="s")
        
        ### RIGHT FRAME - FILTER BOX
        self.filter_box = customtkinter.CTkTextbox(self.sidebar_frame_right)
        self.filter_box.grid(row=5, column=0, rowspan=2, padx=20, sticky="nsew")
        self.filter_box.configure(state="disabled")       

        ### RIGHT FRAME - CLEAR FILTER BUTTON
        self.filter_button = customtkinter.CTkButton(self.sidebar_frame_right, 
                                                     command=self.clear_filters,
                                                     width=10,
                                                     text=clear_patterns_button_name,
                                                     font=small_font) 
        self.filter_button.grid(row=7, column=0, padx=50, pady=10, sticky="n")

        ### RIGHT FRAME - TEST PATTERNS BUTTON
        self.sidebar_button_get_matches = customtkinter.CTkButton(self.sidebar_frame_right, 
                                                                  height=20, 
                                                                  text=getmatches_button_name, 
                                                                  command=lambda: self.compute(self.get_pattern_matches), 
                                                                  font=large_font)
        self.sidebar_button_get_matches.grid(row=8, rowspan=2,column=0, padx=20, pady=20, sticky="nsew")

    def declare_default_states(self):
        self.showing_patterns_frame = False
        self.showing_patterns_stats_frame = False
        self.showing_es_auth = False
        self.showing_es_api = False
        self.showing_es_cert = False
        self.get_unique_es_results = True
        self.get_unique_jsonfile_results = True
        self.get_unique_logfile_lines = True

        self.es_username_label.grid_forget()
        self.es_username_entry.grid_forget()
        self.es_password_label.grid_forget()
        self.es_password_entry.grid_forget()
        self.api_key_label.grid_forget()
        self.api_key_entry.grid_forget()
        self.es_cert_label.grid_forget()
        self.es_cert_entry.grid_forget()
        self.match_entry_button.grid_forget()
        self.tabview.grid_forget()
        self.sidebar_frame_right.grid_forget()

        self.messagebox_geometry="%d+%d" % (self.winfo_x() + window_width/2, self.winfo_y() + window_height/2)
        self.welcome_messagebox_geometry="%d+%d" % (self.winfo_x() + window_width/2, self.winfo_y() + window_height/2)



    def toggle_get_unique_logfile_lines(self):
        if self.get_unique_logfile_lines:
            self.unique_logfile_lines_switch.deselect()
        else:
            self.unique_logfile_lines_switch.select()
        self.get_unique_logfile_lines = not self.get_unique_logfile_lines

    def toggle_get_unique_es_results(self):
        if self.get_unique_es_results:
            self.es_unique_data_switch.deselect()
        else:
            self.es_unique_data_switch.select()
        self.get_unique_es_results = not self.get_unique_es_results

    def toggle_get_unique_jsonfile_results(self):
        if self.get_unique_jsonfile_results:
            self.unique_jsonfile_lines_switch.deselect()
        else:
            self.unique_jsonfile_lines_switch.select()
        self.get_unique_jsonfile_results = not self.get_unique_jsonfile_results

    def toggle_es_cert(self):
        if self.showing_es_cert:
            self.es_cert_switch.deselect()
            self.es_cert_label.grid_forget()
            self.es_cert_entry.grid_forget()
        else:
            self.es_cert_label.grid(row=8, column=0, padx=(5,0), sticky="w")
            self.es_cert_entry.grid(row=8, column=1,columnspan=2, padx=(5,0), sticky="w")
            self.es_cert_switch.select()
        self.showing_es_cert = not self.showing_es_cert

    def toggle_es_api(self):
        if self.showing_es_api:
            self.api_key_switch.deselect()
            self.api_key_label.grid_forget()
            self.api_key_entry.grid_forget()
        else:
            self.api_key_entry.grid(row=6, column=1,columnspan=2, padx=(5,0), sticky="w")
            self.api_key_label.grid(row=6, column=0, padx=(5,0), sticky="w")
            self.api_key_switch.select()

        self.showing_es_api = not self.showing_es_api

    def toggle_es_auth(self):
        if self.showing_es_auth:
            self.es_username_label.grid_forget()
            self.es_username_entry.grid_forget()
            self.es_password_label.grid_forget()
            self.es_password_entry.grid_forget()
            self.auth_switch.deselect()
        else:
            self.es_password_entry.grid(row=4, column=1,columnspan=2, padx=(5,0), sticky="w")
            self.es_password_label.grid(row=4, column=0, padx=(5,0), sticky="w")
            self.es_username_entry.grid(row=3, column=1,columnspan=2, padx=(5,0), sticky="w")
            self.es_username_label.grid(row=3, column=0, padx=(5,0), sticky="w")
            self.auth_switch.select()
        self.showing_es_auth = not self.showing_es_auth

    def toggle_patterns_frame(self):
        self.showing_patterns_frame = not self.showing_patterns_frame 
        if self.showing_patterns_frame:
            self.sidebar_frame_right.grid(row=0, column=16, rowspan=4, padx=(0,20), pady=(10, 20), sticky="nsew")
            self.patterns_frame_switch.select()
        else:
            self.sidebar_frame_right.grid_forget()
            self.patterns_frame_switch.deselect()

    def toggle_stats_frame(self):
        self.showing_patterns_stats_frame = not self.showing_patterns_stats_frame 
        if self.showing_patterns_stats_frame:
            self.tabview.grid(row=2, column=1, columnspan=15, rowspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
            self.patterns_stats_frame_switch.select()
        else:
            self.tabview.grid_forget()
            self.patterns_stats_frame_switch.deselect()

    def get_es_server_details(function: callable) -> callable:
        def wrapper(*args: any) -> callable:
            self = args[0]
            self.es_hostname=es_bogus_hostname if self.es_host_entry.get().strip() == "" else self.es_host_entry.get().strip()
            self.es_port=es_bogus_port if self.es_port_entry.get().strip() == "" else self.es_port_entry.get().strip()

            if self.showing_es_auth:
                self.es_username = es_bogus_username if self.es_username_entry.get().strip() == "" else self.es_username_entry.get().strip()
                self.es_password = es_bogus_password if self.es_password_entry.get().strip() == "" else self.es_password_entry.get().strip()
                self.es_auth=(self.es_username, self.es_password)
            else:
                self.es_auth=es_default_auth

            if self.showing_es_api:
                self.es_api_key = es_default_api_key if self.api_key_entry.get().strip() == "" else self.api_key_entry.get().strip()
            else:
                self.es_api_key = es_default_api_key

            if self.showing_es_cert:
                self.es_cert = es_default_cert if self.es_cert_entry.get().strip() == "" else self.es_cert_entry.get().strip()
            else:
                self.es_cert = es_default_cert 

            self.es_index=es_bogus_index if self.es_index_combobox.get().strip() == "" else self.es_index_combobox.get().strip()
            self.es_field=es_bogus_field if self.es_field_combobox.get().strip() == "" else self.es_field_combobox.get().strip()
            self.es_query=es_bogus_query if self.es_query_entry.get().strip() == "" else self.es_query_entry.get().strip()
            function(*args)
        return wrapper

    def get_json_field_data(self):
        try:
            self.json_field = self.json_field_combobox.get().strip()
            json_data = other_funcs.extract_jsonfile_field_data(self.json_data, self.json_field, unique=self.get_unique_jsonfile_results)
            if json_data:
                self.update_textbox(self.textbox_log, "\n".join(json_data), editable=True)
        except Exception as error_msg:
            CustomMessagebox(title=error_msg.__class__.__name__, label=RETURN_MESSAGES['unsuccessful_retrieval_of_jsonfile_data'], text=str(error_msg), geometry=self.messagebox_geometry)
        finally:
            self.hide_loading()

    def compute(self, func: callable):
        self.show_loading()
        self.loading_thread = Thread(target=func)
        self.loading_thread.start()

    def show_loading(self):
        self.sidebar_button_es_fields.configure(state="disabled")
        self.sidebar_button_es_conn.configure(state="disabled")
        self.sidebar_button_get_matches.configure(state="disabled")
        self.sidebar_button_json_fields.configure(state="disabled")

        self.textbox_log.grid_forget()
        self.loading_frame.grid(row=1, column=1, columnspan=15, pady=(10,20), padx=20, sticky="nsew")

    def hide_loading(self):
        self.loading_frame.grid_forget()
        self.textbox_log.grid(row=1, column=1, columnspan=15,pady=(10,20), padx=20, sticky="nsew")
        self.sidebar_button_es_fields.configure(state="normal")
        self.sidebar_button_es_conn.configure(state="normal")
        self.sidebar_button_get_matches.configure(state="normal")
        self.sidebar_button_json_fields.configure(state="normal")

    def create_loading_frame(self):
        self.loading_frame = customtkinter.CTkFrame(self, corner_radius=5)
        self.loading_frame.grid_columnconfigure((0,1,2), weight=1)
        self.loading_frame.grid_rowconfigure((2,3), weight=2)
        loading_label = customtkinter.CTkLabel(self.loading_frame, text=loading_label_text, font=extra_large_font)
        loading_label.grid(row=2, column=0, columnspan=3, padx=10, pady=(0,15), sticky="ews")
        
        progressbar = customtkinter.CTkProgressBar(self.loading_frame, height=30,corner_radius=40,border_width=2)
        progressbar.grid(row=3, column=0, columnspan=3, pady=(0), padx=100, sticky="enw")
        progressbar.configure(mode="indeterminnate")
        progressbar.start()
        
    @get_es_server_details
    def test_es_connection(self):
        try:
            es_funcs.get_request_elastic(url='http://{}:{}'.format(self.es_hostname, self.es_port), 
                                         credentials=self.es_auth, 
                                         cert=self.es_cert, 
                                         api_key=self.es_api_key)
            CustomMessagebox(title="Connection", label=RETURN_MESSAGES['successful_connection'], geometry=self.messagebox_geometry)
        except Exception as error_msg:
            CustomMessagebox(title=error_msg.__class__.__name__, label=RETURN_MESSAGES['unsuccessful_connection'], text=str(error_msg), geometry=self.messagebox_geometry)
        finally:
            self.hide_loading()

        try:
            self.refresh_index_and_fields()
        except:
            pass
        
    @get_es_server_details
    def get_es_field_data(self):
        try:
            request_body = es_funcs.populate_json(self.es_field, self.es_query)
            response = es_funcs.get_request_elastic(url='http://{}:{}/{}/_search'.format(self.es_hostname, self.es_port, self.es_index), 
                                                    credentials=self.es_auth,
                                                    request_body=request_body,
                                                    cert=self.es_cert, 
                                                    api_key=self.es_api_key).json()
            es_data = es_funcs.extract_es_field_data(response, self.es_field,unique=self.get_unique_es_results)
            self.update_textbox(self.textbox_log, "\n".join(es_data), editable=True)
        except Exception as error_msg:
            CustomMessagebox(title=error_msg.__class__.__name__, label=RETURN_MESSAGES['unsuccessful_retrieval_of_es_data'], text=str(error_msg), geometry=self.messagebox_geometry)
        finally:
            self.hide_loading()

        try:
            self.refresh_index_and_fields()
        except:
            pass
    
    def refresh_index_and_fields(self):
        self.get_indicies()
        self.get_fields()
        self.index_autocomplete_callback()
        self.es_field_autocomplete_callback()

    def get_indicies(self):
        response = es_funcs.get_request_elastic(url='http://{}:{}/_cat/indices?format=json&pretty=true'.format(self.es_hostname,self.es_port), 
                                         credentials=self.es_auth,
                                         cert=self.es_cert, 
                                         api_key=self.es_api_key).json()
        self.es_indicies = self.retrieve_available_indicies(response)
        if not self.es_indicies:
            raise ValueError(RETURN_MESSAGES["unsuccessful_retrieval_of_index"])

    def get_fields(self):
        self.es_fields = []
        for index in self.es_indicies:
            response = es_funcs.get_request_elastic(url='http://{}:{}/{}/_mapping'.format(self.es_hostname, self.es_port, index), 
                                                    credentials=self.es_auth,
                                                    cert=self.es_cert, 
                                                    api_key=self.es_api_key)
            fields = response.json()[index]['mappings']['properties']
            field_list = es_funcs.get_field_names(fields)
            if field_list:
                for field in field_list:
                    if field not in self.es_fields:
                        self.es_fields.append(field)

        if not self.es_fields:
            raise ConnectionError(RETURN_MESSAGES["unsuccessful_retrieval_of_field"])

    def retrieve_available_indicies(self, response: dict):
        return set(index_nr['index'] for index_nr in response if index_nr['status'] == "open" and index_nr['health'] != "red")

    def export_patterns(self):
        if self.pattern_table_is_populated():
            patterns = self.get_patterns()
            filename = customtkinter.filedialog.asksaveasfilename()
            if filename:
                try:
                    with open(filename, "wt") as patfile:
                        for pattern in patterns:
                            patfile.write("{} {}\n".format(pattern, patterns[pattern]))
                        patfile.flush()
                        patfile.close()
                    CustomMessagebox(title="Export", label=RETURN_MESSAGES["successful_pattern_export"], geometry=self.messagebox_geometry)
                except Exception as error_msg:
                    CustomMessagebox(title=error_msg.__class__.__name__, label=RETURN_MESSAGES["invalid_export_dest"], text=str(error_msg), geometry=self.messagebox_geometry)
        else:
            CustomMessagebox(title="Export", label=RETURN_MESSAGES["no_patterns_for_export"], geometry=self.messagebox_geometry)

    def add_pattern_to_table(self):
        regex = self.regexp_entry.get().strip()
        if len(regex) > 0:
            if not self.showing_patterns_frame:
                self.toggle_patterns_frame()
            pattern_name = "{}-{}".format(app_title.upper(),self.created_patterns)
            self.patterns_sheet.insert_row(values = (pattern_name,regex), idx = 0,redraw = True)
            self.created_patterns += 1

    def delete_pattern_from_table(self, object: object):
        self.filter_list = object.delete_pattern(self.filter_list)

    def toggle_bg_highlight(self):
        self.bg_highlight = not self.bg_highlight
        if self.bg_highlight:
            self.textbox_log.tag_config("match", background=highlight_bg_color)
        else:
            self.textbox_log.tag_config("match", background="")

    def toggle_auto_match(self):
        self.auto_match = not self.auto_match
        if self.auto_match:
            self.match_entry_button.grid_forget()
        else:
            self.match_entry_button.grid(row=0, column=14, padx=(5,5), pady=(5,5), sticky="we")

    def get_filtered_patterns(self, converted_patterns: dict) -> list:
        all_patterns = [pattern for pattern in converted_patterns]

        if self.include:
            return self.include
        elif self.exclude:
            for excluded_pattern in self.exclude:
                all_patterns.remove(excluded_pattern)
        return all_patterns        

    def clear_filters(self):
        for list in self.filter_list:
            list.clear()
        self.update_textbox(self.filter_box, "", editable=False)

    def highlight_callback(self, *_args: any):
        if self.auto_match:
            self.textbox_log.highlight_pattern(pattern=self.regexp_entry.get())
        else:
            self.textbox_log.clean_highlights(tag="match")

    def index_autocomplete_callback(self, *_args: any):
        search_str=self.es_index_combobox.get()
        matching_index=[]
        for index in self.es_indicies:
            if(re.match(search_str,index,re.IGNORECASE)):
                matching_index.append(index)
                
        self.es_index_combobox.configure(values=matching_index[:maximum_matched_fields])
    
    def es_field_autocomplete_callback(self, *_args: any):
        search_str=self.es_field_combobox.get() 
        matching_fields=[]
        for field in self.es_fields:
            if(re.match(search_str,field,re.IGNORECASE)):
                matching_fields.append(field)
        self.es_field_combobox.configure(values=matching_fields[:maximum_matched_fields])

    def json_field_autocomplete_callback(self, *_args: any):
        search_str=self.json_field_combobox.get() 
        matching_fields=[]
        for field in self.json_fields:
            if(re.match(search_str,field,re.IGNORECASE)):
                matching_fields.append(field)
        self.json_field_combobox.configure(values=matching_fields[:maximum_matched_fields])

    def highlight(self):
        self.textbox_log.highlight_pattern(pattern=self.regexp_entry.get())

    def pattern_filter(self, object: object, pattern_filter_list: list, filter_type: str):
        pattern_filter_list = object.get_patterns(pattern_filter_list)
        if filter_type == "exclude": 
            box_icon=self.exclude_sign
            self.include.clear()
        elif filter_type == "include":
            box_icon=self.include_sign
            self.exclude.clear()
        self.update_textbox(self.filter_box, "", editable=False)
        message = "{} ".format(box_icon)+"\n{} ".format(box_icon).join(pattern_filter_list)
        self.update_textbox(self.filter_box, message, editable=False)

    def change_appearance_main_color(self):
        if self.main_color == "light":
            self.main_color = "dark"
        else:
            self.main_color = "light"
        self.switch_main_appearance.configure(text=self.get_color_switch_label())
        self.update_color_scheme()

    def update_color_scheme(self):
        customtkinter.set_appearance_mode(self.main_color)
        for object in self.table_list:
            if self.main_color == "dark":
                object.update_design(self.fg_dark_color,
                                 self.dark_text_color, 
                                 self.border_dark_color,
                                 self.dark_text_color)
            else:
                object.update_design(self.fg_light_color, 
                                 self.light_text_color,
                                 self.border_light_color,
                                 self.light_text_color)
                
    def create_regex_help_msgbox(self):
        if self.main_color == "dark":
            RegexHelpMessagebox(mode=self.main_color,
                                theme=self.sub_color,
                                first_color=self.fg_dark_color,
                                second_color=self.dark_text_color,
                                third_color=self.border_dark_color,
                                text_color=self.dark_text_color)
        else:
            RegexHelpMessagebox(mode=self.main_color,
                                theme=self.sub_color,
                                first_color=self.fg_light_color,
                                second_color=self.light_text_color,
                                third_color=self.border_light_color,
                                text_color=self.light_text_color)

    def get_color_switch_label(self) -> str:
        print("text: ", self.main_color.capitalize() + " Mode")
        return self.main_color.capitalize() + " Mode"
        
    def read_patterns(self):
        patternsfile = customtkinter.filedialog.askopenfilename(title="Please select a pattern file") 
        if patternsfile:                           
            try:                                
                self.pattern_file_raw = self.read_textfile(patternsfile)
                self.extracted_patterns = other_funcs.extract_patterns(self.pattern_file_raw)
            except Exception as error_msg:
                CustomMessagebox(title=error_msg.__class__.__name__, label=RETURN_MESSAGES["unsuccessful_grok_file_load"], text=str(error_msg), geometry=self.messagebox_geometry)
            table_format_patterns = other_funcs.get_pattern_table_format(self.extracted_patterns) 
            self.patterns_sheet.set_sheet_data(data=table_format_patterns)
            if not self.showing_patterns_frame:
                self.toggle_patterns_frame()

    def read_json(self):
        jsonfile = customtkinter.filedialog.askopenfilename(title="Please select a json file") 
        if jsonfile:                           
            try:                                
                self.json_data = self.read_jsonfile(jsonfile)
                self.populate_json_keyfield_list(self.json_data)
                if self.json_fields:
                    self.json_field_autocomplete_callback()
                else:
                    raise ValueError

            except Exception as error_msg:
                CustomMessagebox(title=error_msg.__class__.__name__, label=RETURN_MESSAGES["unsuccessful_json_file_load"], text=str(error_msg), geometry=self.messagebox_geometry)

    def populate_json_keyfield_list(self, json_data: dict):
        self.json_fields = []
                
        if isinstance(json_data, dict):
            key_list = other_funcs.get_jsonfile_key_names(json_data)
            if key_list:
                for key in key_list:
                    if key not in self.json_fields:
                        self.json_fields.append(key)
        else:
            for json_object in json_data:
                key_list = other_funcs.get_jsonfile_key_names(json_object)

                if key_list:
                    for key in key_list:
                        if key not in self.json_fields:
                            self.json_fields.append(key)

    def read_log(self):
        logfile = customtkinter.filedialog.askopenfilename(title="Please select a log file")
        if logfile:  
            try:                                         
                log = self.read_textfile(logfile, unique=self.get_unique_logfile_lines)
                if log:
                    self.update_textbox(self.textbox_log, "\n".join(log), editable=True)
                else:
                    raise ValueError
            except Exception as error_msg:
                CustomMessagebox(title=error_msg.__class__.__name__, label=RETURN_MESSAGES["unsuccessful_log_file_load"], text=str(error_msg), geometry=self.messagebox_geometry)

    def update_textbox(self, object: object, text: str, editable: bool = True):
        if not editable:
            object.configure(state="normal")
        object.delete("0.0", 'end')
        object.insert("0.0", text)
        object.focus_set()
        if not editable:
            object.configure(state="disabled")

    def get_textbox_text(self, object: object) -> str:
        return object.get('1.0', 'end')

    def pattern_table_is_populated(self) -> bool:
        patterns = self.get_patterns()
        if patterns:
            return True
        else:
            return False

    def logtextbox_is_populated(self) -> bool:
        if len([message.strip() for message in self.get_textbox_text(self.textbox_log).splitlines() if len(message.strip())>0]) > 0: 
            return True
        else:
            return False

    def get_textbox_log(self) -> list:
        return [message.strip() for message in self.get_textbox_text(self.textbox_log).splitlines() if len(message.strip())>0]

    def get_patterns(self) -> dict:
        table_data = self.patterns_sheet.get_sheet_data(return_copy = True, get_header = False, get_index = False)
        patterns={}
        for row in table_data:
            patterns[row[0]]=row[1]
        return patterns

    def get_pattern_matches(self):
        try:
            if self.pattern_table_is_populated():
                patterns = self.get_patterns()

                if self.logtextbox_is_populated():
                    log = self.get_textbox_log()

                    self.converted_patterns = other_funcs.convert_patterns(patterns)
                    filter_list = self.get_filtered_patterns(self.converted_patterns)
                    self.matches, self.metadata = other_funcs.get_matches(log, self.converted_patterns, pattern_filter=filter_list)

                    if not self.showing_patterns_stats_frame:
                        self.toggle_stats_frame()

                    #Stats table
                    self.stats_table_format, stats_column_headers =other_funcs.get_stats_table_format(self.metadata)
                    self.stats_sheet.headers(stats_column_headers)
                    
                    self.stats_sheet.set_sheet_data(data=self.stats_table_format)
                    self.stats_sheet.set_all_cell_sizes_to_text(redraw = True)
                    
                    #Results table
                    self.results_table_format, res_column_headers = other_funcs.get_res_table_format(self.matches)
                    self.results_sheet.headers(res_column_headers)
                    self.results_sheet.set_sheet_data(data=self.results_table_format)
                else:
                    CustomMessagebox(title="Pattern test", label=RETURN_MESSAGES["no_log_to_match"], geometry=self.messagebox_geometry)
            else:
                CustomMessagebox(title="Pattern test", label=RETURN_MESSAGES["no_patterns_to_match"], geometry=self.messagebox_geometry)
        except Exception as error_msg:
            CustomMessagebox(title=error_msg.__class__.__name__, label=RETURN_MESSAGES['unsuccessful_pattern_matches'], text=str(error_msg), geometry=self.messagebox_geometry)
        finally:
            self.hide_loading()

    def read_jsonfile(self, jsonfile: str) -> Union[dict, list[dict]]:

        try:
            with open(jsonfile, "rt") as jf:
                jd = {}
                jd = json.loads(jf.read())
        except:
            try:
                jd = []
                with open(jsonfile, "rt") as jf:
                    jd = [json.loads(line.strip()) for line in jf.readlines()]
            except:
                raise ValueError
        finally:
            if not jd:
                raise ValueError
            return jd

    def read_textfile(self, textfile: str, unique: bool = False) -> list:
        textfile_lines = []
        with open(textfile, "rt") as tf:
            for line in tf.readlines():
                line = line.strip()
                if unique and line in textfile_lines:
                    continue
                textfile_lines.append(line)
        return textfile_lines

def file_exists(file) -> bool:
    if  os.path.exists(file):
        return True
    else:
        return False

def create_settings_file(set_file: str):
    settings = json.dumps(default_settings, indent=4)
    with open(set_file, "wt") as settings_file: 
        settings_file.write(settings)

def read_settings_file(set_file: str):
    with open(set_file) as sf:
        return json.load(sf)

def load_design(app_settings: str) -> dict:
    try:
        app_settings['mode'] = app_settings['mode'].lower()
        customtkinter.set_appearance_mode(app_settings['mode'])
        customtkinter.set_default_color_theme(available_themes_dict[app_settings['theme']])
    except Exception as error_msg:
        app_settings['mode'] = default_mode.lower()
        customtkinter.set_appearance_mode(app_settings['mode'])
        customtkinter.set_default_color_theme(available_themes_dict[default_theme])
        app_settings['successful_load'] = False
        app_settings['failure_reason'] = str(error_msg)
    return app_settings

def merge_custom_settings(default_settings: dict, custom_settings: dict) -> dict: 
    for key in custom_settings:
        if key in default_settings.keys():
            default_settings[key] = custom_settings[key]
    return default_settings

def load_settings(set_file: str):
    app_settings = default_settings
    if not file_exists(set_file):
        create_settings_file(set_file)
        app_settings['initial_start'] = True
    else:
        app_settings['initial_start'] = False

    try:
        custom_app_settings = read_settings_file(set_file)
        app_settings = merge_custom_settings(app_settings, custom_app_settings)
        app_settings['successful_load'] = True
    except Exception as error_msg:
        app_settings['successful_load'] = False
        app_settings['failure_reason'] = str(error_msg)
    return app_settings

if __name__ == "__main__":
    app_settings = load_settings(settings_file) 
    app_settings = load_design(app_settings)
    groppy_app = Groppy(app_settings)
    groppy_app.mainloop()
