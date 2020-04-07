import argparse

from combine import load_data

LANG = ['ar', 'bg', 'ca', 'cs', 'da', 'de', 'el', 'en', 'es', 'fa',
        'fi', 'fr', 'he', 'hi', 'hu', 'id', 'it', 'ko', 'nl', 'no',
        'pl', 'pt', 'ro', 'ru', 'sv', 'th', 'tr', 'uk', 'vi', 'zh']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ENE classified data set constructor')
    parser.add_argument('ene_jawiki', type=str,
        help='Set path of the data of Japanese Wikipedia articles categorized by ENE.')
    parser.add_argument('langlink', type=str,
        help='Set path of the language link data.')
    parser.add_argument('--output_dir', type=str, default='training_alllanguages',
        help='You can change the output folder.')
    parser.add_argument('--definition_path', type=str, default=None,
        help='In default, training data have only ENE_id.If you want ENE_name, have to specify the definition file.')
    parser.add_argument('--lang', choices=LANG, type=str,
        help='If you need only the specific language, set the language code that regularized by ISO 639 (eg. "en" as English). If you did not, this script outputs a training data of whole languages.')
    parser.add_argument('--add_prob', action="store_true",
        help='Add probability assigned by Japanese ENE classifier.')

    args = parser.parse_args()

    load_data(args.ene_jawiki,
              args.langlink,
              output_dir=args.output_dir,
              definition=args.definition_path,
              lang=args.lang,
              add_prob=args.add_prob)
