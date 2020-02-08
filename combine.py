import os
import json
import tarfile
import bz2
from collections import defaultdict
from multiprocessing import Pool
import multiprocessing as multi

def json_dumps(data):
    return json.dumps(data, ensure_ascii=False)

def output_json(training,lang,output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for ln,training_output in training.items():
        file_name = '{}_ENEW_LIST.json'.format(ln)
        file_path = os.path.join(output_dir, file_name)

        with open(file_path,'w') as f, Pool(multi.cpu_count()) as p:
            dumps = p.map(json_dumps, training_output)
            f.write('\n'.join(dumps))
            f.close()

def create_id_dict(ene_jawiki):
    id_dict = {}
    with tarfile.open(ene_jawiki) as taritems, Pool(multi.cpu_count()) as p:
        for member in taritems.getmembers():
            if '.json' not in member.name:
                continue
            print('Opening {} ...'.format(member.name))
            f_item = taritems.extractfile(member)
            for j in p.imap_unordered(json.loads, f_item):
                id_dict[j['pageid']] = j['ENEs']
    return id_dict

def load_langlink(langlink,lang):
    result = []
    with bz2.BZ2File(langlink) as f, Pool(multi.cpu_count()) as p:
        print('Opening {} ...'.format(langlink))
        for j in p.imap_unordered(json.loads, f):
            if j['source']['lang'] != 'ja':
                continue
            if lang is None or j['destination']['lang'] == lang:
                result.append([j['source'],j['destination']])
    return result

def create_training(langlink_dict,jaID_2_ene):
    result = defaultdict(list)
    print('Creating a training data ...')
    for source, destination in langlink_dict:
        enes = jaID_2_ene.get(source['pageid'])
        if enes is None:
            continue
        d = {'pageid':destination['pageid'],
             'title':destination['title'],
             'ja_pageid':source['pageid'],
             'ja_title':source['title'],
             'ENEs':enes}
        result[destination['lang']].append(d)
    return result

def load_data(ene_jawiki,langlink,lang=None,output_dir=None):
    jaID_2_ene = create_id_dict(ene_jawiki)
    langlink_dict = load_langlink(langlink,lang)

    if __name__ == "__main__":
        print(jaID_2_ene)

    training = create_training(langlink_dict,jaID_2_ene)

    output_json(training,lang,output_dir)
    return training
