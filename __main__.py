import argparse

from combine import load_data

LANG = ['ar', 'bg', 'ca', 'cs', 'da', 'de', 'el', 'en', 'es', 'fa', 'fi', 'fr', 'he', 'hi', 'hu', 'id', 'it', 'ko', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'sv', 'th', 'tr', 'uk', 'vi', 'zh']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ENE classified data set constructor')
    parser.add_argument('ene_jawiki', type=str,
        help='Set path of the data of Japanese Wikipedia articles categorized by ENE.')
    parser.add_argument('langlink', type=str,
        help='Set path of the language link data.')
    parser.add_argument('--lang', choices=LANG, type=str,
        help='If you need only the specific language, set the language code that regularized by ISO 639 (eg. "en" as English). If you did not, this script outputs a training data of whole languages.')
    parser.add_argument('--output', type=str,
        help='If you want a file of constructed output as a same style of the input, set a path of this argument.')

    args = parser.parse_args()

    load_data(args.ene_jawiki,args.langlink,lang=args.lang,output=args.output)
