#!/usr/bin/env python
# -*- coding: utf-8 -*-

import h5py

class H5Graph:
    def __init__(self, path_h5):
        self.path_h5 = path_h5
        self.graph   = None

    def build_h5_graph(self):
        path_h5 = self.path_h5

        graph = {}
        def process_node(node_name, parent_node_path, h5_file_handle):
            '''
            Arguments:
                node_name       : Name of the current node.
                parent_node_path: H5 path to the parent node.
                h5_file_handle  : An opened h5 file handler.
            '''
            # Access the value at the current path...
            node_path = '/'.join([parent_node_path, node_name])
            node_val  = h5_file_handle[node_path]

            # Is it a leaf node???
            if isinstance(node_val, h5py.Dataset):
                # Retrieve metadata at the leaf node...
                graph[node_path] = {
                    'shape' : f'{node_val.shape}',
                    'dtype' : f'{node_val.dtype}',
                }

            # Otherwise...
            else:
                # Go through all children nodes...
                for new_node_name in node_val.keys():
                    process_node(new_node_name, node_path, h5_file_handle)

        with h5py.File(path_h5, 'r') as h5_file_handle:
            process_node(node_name = '', parent_node_path = '', h5_file_handle = h5_file_handle)

        return graph


    def build_bokeh_data_source(self):
        graph = self.build_h5_graph()

        data_source = dict(
            name  = [ key          for key, val in graph.items()],
            shape = [ val['shape'] for key, val in graph.items()],
            dtype = [ val['dtype'] for key, val in graph.items()],
        )

        return data_source
