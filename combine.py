import json
import tarfile
import bz2
from collections import defaultdict
from multiprocessing import Pool
import multiprocessing as multi

def output_json(training,lang,out_path):
    if lang != 'LIST':
        with open(out_path,'w') as f:
            for line in training[lang]:
                f.write(json.dumps(line)+'\n')
            f.close()
    else:
        for ln,training_output in training.items():
            with open('{}_{}'.format(ln,out_path),'w') as f:
                for line in training_output:
                    f.write(json.dumps(line)+'\n')
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
                result.append([j['source']['pageid'],j['destination']])
    return result


def create_training(langlink_dict,jaID_2_ene):
    result = defaultdict(list)
    print('Creating a training data ...')
    for source_id, destination in langlink_dict:
        enes = jaID_2_ene.get(source_id)
        if enes is None:
            continue
        d = {'pageid':destination['pageid'],
             'ja_pageid':source_id,
             'title':destination['title'],
             'ENEs':enes}
        result[destinations['lang']].append(d)
    return result

def load_data(ene_jawiki,langlink,lang=None,output=None):
    jaID_2_ene = create_id_dict(ene_jawiki)
    langlink_dict = load_langlink(langlink,lang)
    assert False, False

    if __name__ == "__main__":
        print(jaID_2_ene)

    training = create_training(langlink_dict,jaID_2_ene)

    if not lang:
        lang = "LIST"
    output = output if output is not None else 'ENEW_{}.json'.format(lang)
    output_json(training,lang,output)
    return training
