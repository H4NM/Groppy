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

    def adapt_theme(self, mode):
        if mode == "dark":
            table_bg="#3D3D3D" 
            top_left_bg="#3D3D3D"
            popup_menu_bg="#3D3D3D" 
            header_bg="#4E4E4E" 
            index_bg="#4E4E4E"
        else:
            table_bg="#3D3D3D" 
            top_left_bg="#3D3D3D"
            popup_menu_bg="#3D3D3D" 
            header_bg="#4E4E4E" 
            index_bg="#4E4E4E"

        theme = {
            "popup_menu_fg": "#000000",
            "popup_menu_bg": popup_menu_bg,
            "popup_menu_highlight_bg": "#DCDEE0",
            "popup_menu_highlight_fg": "#000000",
            "index_hidden_rows_expander_bg": "gray30",
            "header_hidden_columns_expander_bg": "gray30",
            "header_bg": header_bg,
            "header_border_fg": "#ababab",
            "header_grid_fg": "#ababab",
            "header_fg": "black",
            "header_selected_cells_bg": "#d6d4d2",
            "header_selected_cells_fg": "#217346",
            "index_bg": index_bg,
            "index_border_fg": "#ababab",
            "index_grid_fg": "#ababab",
            "index_fg": "black",
            "index_selected_cells_bg": "#d6d4d2",
            "index_selected_cells_fg": "#217346",
            "top_left_bg": top_left_bg,
            "top_left_fg": "#b7b7b7",
            "top_left_fg_highlight": "#5f6368",
            "table_bg": table_bg,
            "table_grid_fg": "#bfbfbf",
            "table_fg": "black",
            "table_selected_cells_border_fg": "#217346",
            "table_selected_cells_bg": "#E3E3E3",
            "table_selected_cells_fg": "black",
            "resizing_line_fg": "black",
            "drag_and_drop_bg": "black",
            "outline_color": "gray2",
            "header_selected_columns_bg": "#d3f0e0",
            "header_selected_columns_fg": "#217346",
            "index_selected_rows_bg": "#d3f0e0",
            "index_selected_rows_fg": "#217346",
            "table_selected_rows_border_fg": "#217346",
            "table_selected_rows_bg": "#E3E3E3",
            "table_selected_rows_fg": "black",
            "table_selected_columns_border_fg": "#217346",
            "table_selected_columns_bg": "#E3E3E3",
            "table_selected_columns_fg": "black",
        }
        return theme
    
    def update_color_scheme(self, mode=default_main_color, **kwargs):
        #£ Add color update based on the imported theme
        #£ C:\Users\Asus\Desktop\Programmering\git\Groppy\Lib\site-packages\tksheet\_tksheet_vars
        #Pseudo: After theme is imported, retrieve defined colors to update sheet with
        # Check appearance switch function for white dark mode
        # continue here theme = self.adapt_theme(mode, )
        self.set_options(**theme, redraw=False)
        self.config(bg=theme["table_bg"])

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
    
    def dark_mode(self, light_header_color):
        self.set_options(table_bg="#3D3D3D", 
                        top_left_bg="#3D3D3D",
                        frame_bg="#3D3D3D", 
                        popup_menu_bg="#3D3D3D", 
                        header_bg="#4E4E4E", 
                        index_bg="#4E4E4E",
                        table_fg="#F5F5F5",
                        header_fg=light_header_color,
                        popup_menu_highlight_bg=light_header_color,
                        table_selected_cells_border_fg=light_header_color,
                        table_selected_rows_border_fg=light_header_color,
                        table_selected_columns_border_fg=light_header_color)
        
    def light_mode(self, dark_header_color):
        self.set_options(table_bg="#F5F5F5", 
                        top_left_bg="#F5F5F5",
                        frame_bg="#F5F5F5", 
                        popup_menu_bg="#F5F5F5", 
                        header_bg="#ECECEC", 
                        index_bg="#ECECEC",
                        table_fg="#3D3D3D",
                        header_fg=dark_header_color,
                        popup_menu_highlight_bg=dark_header_color,
                        table_selected_cells_border_fg=dark_header_color,
                        table_selected_rows_border_fg=dark_header_color,
                        table_selected_columns_border_fg=dark_header_color)
    
class CustomMessagebox(customtkinter.CTkToplevel):
    def __init__(self, title: str="", label: str="", text: str="", geometry: str="", *args: any, **kwargs: any):
        super().__init__(*args, **kwargs)
        self.wm_iconbitmap(app_icon)

        self.title(title)
        self.geometry(geometry)
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)
        self.resizable(False,False)
        message_label = customtkinter.CTkLabel(self, 
                                               text=label, 
                                               font=small_font)
        message_label.grid(row=0, column=0, padx=50, pady=(20,10),sticky="nsew")
        if text:
            message_text = customtkinter.CTkTextbox(self,
                                                    height=70,
                                                    font=small_font)
            message_text.grid(row=1, column=0, padx=10, pady=(0,10), sticky="nsew")
            message_text.insert("0.0", text)
            message_text.configure(state="disabled")
        ok_button = customtkinter.CTkButton(self, 
                                            text="OK", 
                                            command=self.destroy, 
                                            width=40, 
                                            font=medium_font)
        ok_button.grid(row=2, column=0, padx=10, pady=(0,10), sticky="ns")
            
        self.attributes("-topmost", True)

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
