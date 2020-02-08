import json
import tarfile
import bz2

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
    with tarfile.open(ene_jawiki) as taritems:
        for member in taritems.getmembers():
            if '.json' in member.name:
                print('Opening {} ...'.format(member.name))
                f_item = taritems.extractfile(member)
                for line in f_item:
                    j = json.loads(line)
                    id_dict[j['pageid']] = j['ENEs']
    return id_dict

def load_langlink(langlink,lang):
    result = []
    with bz2.BZ2File(langlink) as f:
        print('Opening {} ...'.format(langlink))
        for line in f:
            j = json.loads(line)
            if j['source']['lang'] == 'ja':
                if lang:
                    if check_ja_to_specific(j,lang):
                        result.append([j['source']['pageid'],j['destination']])
                else:
                    result.append([j['source']['pageid'],j['destination']])
    return result

def check_ja_to_specific(j,lang):
    return (j['destination']['lang'] == lang)

def create_training(langlink_dict,jaID_2_ene):
    result = {}
    print('Creating a training data ...')
    for pair in langlink_dict:
        if pair[0] in jaID_2_ene:
            enes = jaID_2_ene[pair[0]]
            new_id = pair[1]['pageid']
            new_title = pair[1]['title']
            result.setdefault(pair[1]['lang'],[])
            result[pair[1]['lang']].append({'pageid':new_id,'title':new_title,'ENEs':enes})
    return result


def load_data(ene_jawiki,langlink,lang=None,output=None):
    jaID_2_ene = create_id_dict(ene_jawiki)
    langlink_dict = load_langlink(langlink,lang)

    if __name__ == "__main__":
        print(jaID_2_ene)

    training = create_training(langlink_dict,jaID_2_ene)
    if not lang:
        lang = "LIST"
    if output:
        output_json(training,lang,output)
    else:
        output_json(training,lang,'ENEW_{}.json'.format(lang))
    return training

