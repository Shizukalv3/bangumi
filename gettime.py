import re

def get_time(input_str, date_patterns=None):
    # 日期的正则表达式模式（包含中文字符）
    default_date_patterns = [
    r'\d{4}年\d{1,2}月\d{1,2}日',
    r'\d{4}-\d{1,2}-\d{1,2}'
    ]
    
    date_patterns = date_patterns or default_date_patterns

    date_regex = re.compile('|'.join(date_patterns))
    matches = date_regex.findall(input_str)
    return matches
