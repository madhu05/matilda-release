import pandas as pd
import json


class ThriventInfraLoader():

    APP_DATA = ['Applications / Components', 'Folder or Test Set', 'Platforms', 'September 10 &11 SYS, INT (Linux)',
                 'September 13 SYS, INT (Windows)', 'September 16 PROD', 'IT Contacts Primary', 'Tester SYSTST or INTTST', 'Tester PROD']

    SERVER_DATA = ['Computer System Name', 'Computer System Status', 'Related Status', 'Related Type', 'Related Item']

    def __init__(self):
        self.server_file = 'server_data.xlsx'
        self.server_sheet = None
        self.app_file = 'app_server.xlsx'
        self.app_sheet = 'Testing'

    def read_server_data(self):
        server_data = pd.read_excel(self.server_file, sheet_name=self.server_sheet)
        return server_data[[self.SERVER_DATA]]

    def read_app_data(self):
        app_data = pd.read_excel(self.app_file, sheet_name=self.app_sheet)
        return app_data[[self.APP_DATA]]

    def load_to_db(self):
        pass

    def load_data(self):
        pass
