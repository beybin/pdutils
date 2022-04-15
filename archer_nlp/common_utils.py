import hashlib
import json
import uuid
from datetime import datetime

import Levenshtein
import numpy as np
import pandas as pd


def generate_uuid():
    try:
        uuid4 = uuid.uuid4()
        return str(uuid4).upper().replace('-', '')
    except Exception as e:
        print('generate_uuid error:', e)
        return None


def generate_uuid_md5(data, start='C1'):
    try:
        md5 = hashlib.md5(data.encode(encoding='utf8')).hexdigest().upper()[2:]
        return start + md5[0:6] + '-' + md5[6:10] + '-' + md5[10:14] + '-' + md5[14:18] + '-' + md5[18:]
    except Exception as e:
        print('get_md5 error:', e)
        return None


def get_time():
    # 2022-03-03 16:12:30
    return datetime.now().strftime("%Y-%m-%d %X")


def read_excel(path, sheet_index=0, is_value=True):
    df = pd.read_excel(path, sheet_name=sheet_index)
    # nan替换为空字符串
    df1 = df.replace(np.nan, '', regex=True)
    if is_value:
        return df1.values
    else:
        return df1


def write_excel(path, result_list=[], columns=[], df=None, sheet_index=0):
    if df is None:
        df = pd.DataFrame(result_list, columns=columns)
    df.to_excel(path, index=sheet_index)


def df_to_sql(path_df, table, engine, is_df=False):
    """
    df import to sql
    :param path_df:
    :param table: sql table
    :param engine: sqlalchemy engine
    :param is_df: True为DataFrame，False为Excel路径
    :return:
    """
    # pandas批量导入mysql
    if is_df:
        df = path_df
    else:
        df = read_excel(path_df, is_value=False)
    df.to_sql(table, engine, if_exists='append', index=False)


def read_txt(path):
    data_list = []
    with open(path, encoding='utf8') as f:
        for line in f:
            data_list.append(line.strip())
    return data_list


def dump_json(obj, path):
    json.dump(obj, open(path, 'w', encoding='utf8'), ensure_ascii=False)


def load_json(path):
    return json.load(open(path, encoding='utf8'))


def generate_dict(list1, list2=[]):
    try:
        if list2:
            return dict(zip(list1, list2))
        else:
            return dict(zip(list1, range(len(list1))))
    except Exception as e:
        print(f"generate_dict error:{e}")
        return {}


def get_max_check(check_base_list, check_refer_list, max_ratio=0.5, is_ret_lr=False):
    result_list = []
    for check_base in check_base_list:
        max_lr = -1
        max_check = ''
        for check_refer in check_refer_list:
            rcc_lr = Levenshtein.ratio(check_base, check_refer)
            if rcc_lr < max_ratio:
                continue
            if rcc_lr > max_lr:
                max_lr = rcc_lr
                max_check = check_refer
        if max_lr >= max_ratio:
            if is_ret_lr:
                result_list.append([check_base, max_check, max_lr])
            else:
                result_list.append([check_base, max_check])
        else:
            if is_ret_lr:
                result_list.append([check_base, '', max_lr])
            else:
                result_list.append([check_base, ''])
    return result_list
