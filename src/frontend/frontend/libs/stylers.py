from typing import Optional
import pandas as pd


pd_css_styles = [
            {'selector': 'tr', 'props': [
                ("background", "#ffffff"),
            ]
                },
            {'selector': 'th', 'props': [
                ('font-size', '10px'),
                ('text-align', 'center'),
                ('padding', '1px 10px'),
                ('border-style', 'solid'),
                ('border-width', '1px'),
                ('border-collapse', 'collapse'),
            ]
                },
            {'selector': 'td', 'props': [
                ('font-size', '10px'),
                ('text-align', 'center'),
                ('padding', '1px 10px'),
                ('border-style', 'solid'),
                ('border-width', '1px'),
                ('border-collapse', 'collapse'),
            ]},
            {'selector': 'table', 'props': [
                ("margin", "25px auto"),
                ("border-collapse", "collapse"),
                ("border", "1px solid #eee"),
                ("border-bottom", "2px solid #00cccc"),
            ]},
            {'selector': 'caption', 'props': [
                ("caption-side", "bottom"),
            ]},
            {'selector': 'tr:hover', 'props': [
                ("background", "#f4f4f4"),
            ]},
        ]


class ColorTable:
    def cell_color_background_green(self, cell):
        return 'background-color: honeydew'

    def cell_color_background_red(self, cell):
        return 'background-color: mistyrose'

    def cell_color_background_blue(self, cell):
        return 'background-color: aliceblue'

    def cell_color_background_yellow(self, cell):
        return 'background-color: cornsilk'

    def positive_green_negative_red_text(self, cell):
        if type(cell) != str and cell < 0:
            return 'color: red'
        elif type(cell) != str and cell > 0:
            return 'color: green'
        else:
            return 'color: black'

    def negative_red_text(self, cell):
        if type(cell) != str and cell < 0:
            return 'color: red'


class MetricTableStyler:
    def __init__(self, df: pd.DataFrame, sorted_by: Optional[str] = None):
        if sorted_by is not None:
            self.df = df.sort_values(by=sorted_by, ascending=False)
        else:
            self.df = df
        self.df_index = self.df.index
        self.df_columns = self.df.columns

    def style_table_index_with_difference_stats(self):
        """Style "difference" table with data of one metric for all countries."""
        df_styled = self.df.style \
            .background_gradient(cmap='RdYlGn', axis=1, low=0.4, high=0.4, subset=(self.df_columns[:-4])) \
            .applymap(ColorTable().positive_green_negative_red_text, subset=(self.df_columns[-4:-2])) \
            .applymap(lambda x: 'color : white; background-color : green' if x == 'above' else '') \
            .applymap(lambda x: 'color : white; background-color : red' if x == 'below' else '') \
            .format("{:,.2f}", subset=(self.df_index, self.df_columns[:-1])) \
            .format("{:,.0%}", subset=(self.df_index, self.df_columns == 'percentile')) \
            .set_table_styles(pd_css_styles)

        return df_styled

    def style_table_index_with_change_stats(self):
        """Style "difference" table with data of one metric for all countries."""
        df_styled = self.df.style \
            .background_gradient(cmap='RdYlGn', axis=1, low=0.4, high=0.4, subset=(self.df_columns[:-9])) \
            .map(ColorTable().positive_green_negative_red_text, subset=(self.df_columns[-9:-2])) \
            .map(lambda x: 'color : white; background-color : green' if x == 'above' else '') \
            .map(lambda x: 'color : white; background-color : red' if x == 'below' else '') \
            .format("{:,.2f}", subset=(self.df_index, self.df_columns[:-9])) \
            .format("{:,.2%}", subset=(self.df_index, self.df_columns[-5:-3])) \
            .format("{:,.2f}", subset=(self.df_index, self.df_columns[-9:-5])) \
            .format("{:,.2f}", subset=(self.df_index, self.df_columns[-5:])) \
            .format("{:,.0%}", subset=(self.df_index, self.df_columns == 'percentile')) \
            .set_table_styles(pd_css_styles)

        return df_styled

    def style_table_change_with_difference_stats(self):
        """Style "ratio" table with data of one metric for all countries."""
        df_styled = self.df.style \
            .background_gradient(cmap='RdYlGn', axis=1, low=0.4, high=0.4, subset=(self.df_columns[:-4])) \
            .applymap(ColorTable().positive_green_negative_red_text, subset=(self.df_columns[-4:-2])) \
            .applymap(lambda x: 'color : white; background-color : green' if x == 'above' else '') \
            .applymap(lambda x: 'color : white; background-color : red' if x == 'below' else '') \
            .format("{:,.1%}", subset=(self.df_index, self.df_columns[:-1])) \
            .format("{:,.1%}", subset=(self.df_index, self.df_columns[-4:-2])) \
            .format("{:,.0%}", subset=(self.df_index, self.df_columns == 'percentile')) \
            .set_table_styles(pd_css_styles)

        return df_styled
