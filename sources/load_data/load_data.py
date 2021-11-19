''' Load informations to analysis '''

from typing import List, Tuple, Type
import locale

import pandas as pd
from pandas import DataFrame

from .data_analyse import DataAnalyse


class DataExtructure(DataAnalyse):
    ''' object to load, analyse and export data '''

    def __init__(self, data_frame: List, porcents: Tuple, state: bool) -> None:
        ''' Extruture elements of object
        :data_frame = [[datetime, int, (+ or -)], ...]
        :porcents = ((int,int,int),(int,int,int), ...)
        '''
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
        self.data_frame = self.set_data_frame(data_frame)
        self.__incidences = self.set_incidences(data_frame)
        self.__result_faturation = self.set_data_frame_faturation(porcents, state)


    def set_data_frame(self, data_frame: List) -> Type[DataFrame]:
        ''' set a data_frame with data list '''
        collumns = ['date-time', 'valor', 'operation']
        pd_data_frame = pd.DataFrame(data_frame, columns=collumns, index=None)
        pd_data_frame['valor'] = pd_data_frame['valor'].map(locale.currency)
        return pd_data_frame


    def set_data_frame_faturation(
        self, porcents: Tuple, state: bool
    ) -> Type[DataFrame]:
        ''' set a data with faturation '''
        collumns = ['valor', 'amount', 'operation', 'porcent', 'receved', 'revenue']
        data_frame, total = self.analyse_faturation(porcents, state)
        df_data = pd.DataFrame(data_frame, columns=collumns, index=None)
        df_total = pd.DataFrame([total], columns=collumns, index=None)
        df_data['valor'] = df_data['valor'].map(locale.currency)
        df_final = df_data.append(df_total)
        df_final['receved'] = df_final['receved'].map(locale.currency)
        df_final['revenue'] = df_final['revenue'].map(locale.currency)
        df_final['porcent'] = df_final['porcent'].astype(str) + ' %'
        return df_final


    def get_incidences(self) -> List:
        ''' access to incidences of values '''
        return self.__incidences


    def get_data_frame(self) -> Type[DataFrame]:
        ''' access to DataExtructure data frame '''
        return self.data_frame


    def get_result_faturation(self):
        ''' access to result of fturation data frame '''
        return self.__result_faturation



    def get_result_faturation_view(self):
        ''' visualization for result of faturation '''
        return print(self.__result_faturation.to_markdown())