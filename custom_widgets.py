import customtkinter, re
from settings import *
from other_funcs import valid_regex
from tksheet import Sheet

class CustomTabView(customtkinter.CTkTabview):
    
    def __init__(self, *args: any, **kwargs: any):
        super().__init__(*args, **kwargs)
        # Will add font support when tkinter supports it

class CustomSheet(Sheet):
    def __init__(self, *args: any, **kwargs: any):
        super().__init__(*args, 
                         **kwargs, 
                         font=sheet_font,
                         popup_menu_font=sheet_font,
                         header_font=sheet_header_font)
        self.enable_bindings(
                                "single_select",
                                "drag_select",
                                "column_width_resize",
                                "arrowkeys",
                                "right_click_popup_menu",
                                "copy"
        )

     
    def get_patterns(self, pattern_filter_list: list) -> list:
        selected_rows = self.get_selected_rows(get_cells=False, get_cells_as_rows=True)
        for row in selected_rows:
            pattern_name = self.get_cell_data(row, 0)
            if pattern_name not in pattern_filter_list:
                pattern_filter_list.append(pattern_name)
        return pattern_filter_list
    
    def enable_filter_in_menue(self, filter_type: str, func: callable):
        self.popup_menu_add_command(filter_type, func, index_menu = False, header_menu = False)

    def delete_pattern(self, filter_list: list) -> list:
        selected_rows = self.get_selected_rows(get_cells=False, get_cells_as_rows=True)
        selected_rows_data = [self.get_row_data(row, return_copy = True) for row in selected_rows]
     
        for row_with_data in selected_rows_data:
            table_total_rows = self.get_total_rows()
            for row in range(0,table_total_rows):
                if row_with_data == self.get_row_data(row, return_copy=True):
                    self.delete_row(row, deselect_all = True)
                    break
            
            for list in filter_list:
                for pattern in list:
                    if row_with_data[0] == pattern:
                        list.remove(row_with_data[0])

        return filter_list
  
    def update_design(self, main_color: str, second_color: str, third_color: str, text_color:str):
        self.set_options(table_bg=main_color, 
                        top_left_bg=main_color,
                        frame_bg=main_color, 
                        popup_menu_bg=main_color, 
                        header_bg=third_color, 
                        index_bg=third_color,
                        table_fg=text_color,
                        header_fg=second_color,
                        popup_menu_highlight_bg=second_color,
                        table_selected_cells_border_fg=second_color,
                        table_selected_rows_border_fg=second_color,
                        table_selected_columns_border_fg=second_color)
    
class CustomMessagebox(customtkinter.CTkToplevel):
    def __init__(self, title: str="", label: str="", text: str="", geometry: str="400x500", *args: any, **kwargs: any):
        super().__init__(*args, **kwargs)
        self.wm_iconbitmap(app_icon)

        self.title(title)
        self.geometry(geometry)
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0,1), weight=2)
        self.resizable(False,False)
        message_text_row=0
        if len(label) > 0:
            message_label = customtkinter.CTkLabel(self, 
                                                text=label, 
                                                font=small_font)
            message_label.grid(row=0, column=0, padx=50, pady=(20,10),sticky="nsew")
            message_text_row=1
        if text:
            message_text = customtkinter.CTkTextbox(self,
                                                    font=small_font)
            message_text.grid(row=message_text_row, column=0, padx=10, pady=(0,10), sticky="nsew")
            message_text.insert("0.0", text)
            message_text.configure(state="disabled")
        ok_button = customtkinter.CTkButton(self, 
                                            text="OK", 
                                            command=self.destroy, 
                                            width=40, 
                                            font=medium_font)
        ok_button.grid(row=message_text_row+1, column=0, padx=10, pady=(0,10), sticky="s")
            
        self.attributes("-topmost", True)

class RegexHelpMessagebox(customtkinter.CTkToplevel):
     def __init__(self, mode: str="", theme: str="", first_color: str="", second_color: str="", third_color: str="", text_color:str="", geometry: str="", *args: any, **kwargs: any):
        super().__init__(*args, **kwargs)
        self.wm_iconbitmap(app_icon)
        self.title(regex_help_window_title)
        self.geometry("%dx%d" % (regex_window_width, regex_window_height))
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0,1), weight=2)
        self.resizable(False,False)
        self.regex_help_sheet = CustomSheet(self,
                        height=420,
                        theme=mode+" "+theme,
                        show_x_scrollbar = True,
                        show_y_scrollbar = False,
                        empty_horizontal = False,
                        empty_vertical = False,
                        show_top_left = False,
                        show_row_index = True,
                        auto_resize_default_row_index=True,
                        headers=regex_help_headers,
                        data=regex_help_data)
        self.regex_help_sheet.grid(row = 0, column = 0, columnspan=2, sticky = "nswe")
        self.regex_help_sheet.column_width(column=0, width=115)        
        self.regex_help_sheet.column_width(column=1, width=70)   
        self.regex_help_sheet.column_width(column=2, width=850)   
        self.regex_help_sheet.enable_bindings("double_click_column_resize")

        ok_button = customtkinter.CTkButton(self, 
                                            text="OK", 
                                            command=self.destroy, 
                                            width=80, 
                                            font=medium_font)
        ok_button.grid(row=1, column=0, padx=10, pady=(0,10), sticky="s")
        self.attributes("-topmost", True)
        self.regex_help_sheet.update_design(first_color,
                                            second_color, 
                                            third_color,
                                            text_color)
             
class CustomTextBox(customtkinter.CTkTextbox):
    def __init__(self, *args: any, **kwargs: any):
        super().__init__(*args, **kwargs)
        self.tag_config("match", foreground=highlight_fg_color, background="")

    def highlight(self, tag: str, start: str, end: str):
        self.tag_add(tag, start, end)

    def highlight_all(self, pattern: str, tag: str):
        for match in self.search_re(pattern):
            self.highlight(tag, match[0], match[1])

    def clean_highlights(self, tag: str):
        self.tag_remove(tag, "1.0", "end")

    def search_re(self, pattern: str) -> list:
        matches = []
        text = self.get("1.0", customtkinter.END).splitlines()
        for i, line in enumerate(text):
            for match in re.finditer(pattern, line):
                matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}"))
        return matches

    def highlight_pattern(self, pattern: str, tag: str="match"):
        self.clean_highlights(tag)
        if valid_regex(pattern):
            self.highlight_all(pattern, tag)
