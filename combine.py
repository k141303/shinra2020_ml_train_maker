import os
import re
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
                id_dict[j['pageid']] = select_latest_enes(j['ENEs'])
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

            # DEBUG:
            #if len(result) >= 100000:
            #    break
    return result

def select_latest_enes(enes):
    hand = [key for key in enes if re.match("^HAND\.", key)]
    if hand:
        conf_key = sorted(hand, key=lambda x:x.split(".")[-1])[-1]
    else:
        conf_key = sorted(enes, key=lambda x:x.split(".")[-1])[-1]
    return enes[conf_key], conf_key

def create_training(langlink_dict,jaID_2_ene):
    result = defaultdict(list)
    print('Creating a training data ...')
    for source, destination in langlink_dict:
        enes, stamp = jaID_2_ene.get(source['pageid'])
        if enes is None:
            continue
        d = {'pageid':destination['pageid'],
             'title':destination['title'],
             'ja_pageid':source['pageid'],
             'ja_title':source['title'],
             '_stamp':stamp,
             'ENEs':enes}
        result[destination['lang']].append(d)
    return result

def load_ene_id2name(json_path):
    ene_id2name = {}
    with open(json_path, "r") as f:
        data = list(map(json.loads, f))
    for d in data:
        ene_id2name[d["ENE_id"]] = d["name"]["en"]
    return ene_id2name

def add_ene_name(jaID_2_ene, definition):
    ene_id2name = load_ene_id2name(definition)
    for pageid, (enes, stamp) in jaID_2_ene.items():
        for ene in enes:
            ene["ENE_name"] = ene_id2name[ene["ENE_id"]]
    return jaID_2_ene

def remove_prob(training):
    for lang, data in training.items():
        for d in data:
            for ene in d["ENEs"]:
                if ene.get("prob") is not None:
                    del ene["prob"]
    return training

def load_data(ene_jawiki, langlink, lang=None, output_dir=None, definition=None, add_prob=False):
    jaID_2_ene = create_id_dict(ene_jawiki)
    langlink_dict = load_langlink(langlink,lang)

    if __name__ == "__main__":
        print(jaID_2_ene)

    if definition is not None:
        jaID_2_ene = add_ene_name(jaID_2_ene, definition)

    training = create_training(langlink_dict,jaID_2_ene)

    if not add_prob:
        remove_prob(training)

    output_json(training,lang,output_dir)
    return training
