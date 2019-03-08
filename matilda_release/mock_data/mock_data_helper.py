""" 8/07/2018, 05:17 PM """
# coding=utf-8
# !/usr/bin/env python

from flask import json
import os
import logging as log


class MockDataHelper(object):

    def __init__(self):
        self.mock_data_dir = 'mock_data'
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, self.mock_data_dir))

    def get_servers(self):
        try:
            with open(self.data_dir + '/servers.json') as f:
                data = json.load(f)
            return data
        except EnvironmentError as e:
            return str(e.message)

    def get_vnfs(self):
        try:
            with open(self.data_dir + '/vnf.json') as f:
                data = json.load(f)
            return data
        except EnvironmentError as e:
            return str(e.message)

    def get_applications(self):
        try:
            with open(self.data_dir + '/applications.json') as f:
                data = json.load(f)
            return data
        except EnvironmentError as e:
            return str(e.message)

    def get_server_metrics_data(self):
        try:
            with open(self.data_dir + '/server_metrics.json') as f:
                data = json.load(f)
            return data
        except EnvironmentError as e:
            return str(e.message)

    def get_test_status(self):
        try:
            with open(self.data_dir + '/HPALMMetrics.json') as f:
                data = json.load(f)
            return data
        except EnvironmentError as e:
            return str(e.message)