import os
from more_itertools import unique_everseen
from credentials.config import scrape_path, clean_path
def dedup_meta_scrape(scrape_path, clean_path):
    with open(scrape_path,'r') as f, open(clean_path,'w', encoding='utf-8') as out_file:
        out_file.writelines(unique_everseen(f))
    return True