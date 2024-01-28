#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bokeh.models         import ColumnDataSource, DataTable, TableColumn, TextInput
from bokeh.layouts        import column
from bokeh.io             import curdoc

class H5Viewer:

    def __init__(self, h5graph):
        self.h5graph = h5graph

        data_source = self.h5graph.build_bokeh_data_source()
        self.data_source = ColumnDataSource(data_source)

        self.div_table = None
        self.div_search_input = None

        self.final_layout = None

        self.init_table()
        self.init_search_bar()
        self.init_layout()


    def init_table(self):
        data_source = self.data_source

        # Init columns for the table...
        columns = [
            TableColumn(field='name' , title='Name' , width=400),
            TableColumn(field='shape', title='Shape', width=400),
            TableColumn(field='dtype', title='DType', width=800),
        ]

        # Connect data source to the DataTable
        ## table = DataTable(source=data_source, columns=columns, width=2000, height=2000, sizing_mode='scale_width', fit_columns=True)
        table = DataTable(source=data_source, columns=columns, sizing_mode='scale_width', fit_columns=True)

        self.div_table = table


    def init_search_bar(self):
        data_source   = self.data_source
        original_data = dict(data_source.data)

        # Create a TextInput widget to serve as the search bar
        search_input = TextInput(value="", title="Search:")

        # Callback function to filter the table based on the search input
        def update_table(attr, old, new):
            # If the search bar is cleared, restore the original data
            if not new:
                data_source.data = original_data
            else:
                # Get the current value in the search bar
                search_value = new.strip().lower()

                # Create a new data dictionary with only the rows that match the search term
                new_data = {key: [] for key in original_data}
                for i in range(len(original_data['name'])):
                    if search_value in original_data['name'][i].lower():
                        for key in original_data:
                            new_data[key].append(original_data[key][i])

                # Update the data in the ColumnDataSource
                data_source.data = new_data

        # Attach the update_table function to the search_input so that it triggers on text change
        search_input.on_change('value', update_table)

        self.div_search_input = search_input


    def init_layout(self):
        div_table = self.div_table
        div_search_input = self.div_search_input

        layout_dict = {}
        layout_dict['search_input' ] = div_search_input
        layout_dict['table'   ]      = div_table

        final_layout = column(*tuple(layout_dict.values()), sizing_mode='scale_both')

        self.final_layout = final_layout


    def run(self):
        curdoc().add_root(self.final_layout)
