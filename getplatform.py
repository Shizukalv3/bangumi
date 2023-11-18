import re

def get_platform(input_str):
    platform_match = re.search(r'.*?\/(.*?)\/', input_str)
    if platform_match:
        return platform_match.group(1)
    else:
        pass
