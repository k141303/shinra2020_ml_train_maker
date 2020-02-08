# shinra2020_ml_train_maker

## How to use

~~~bash
python3 create_training ENEW_ENEtag_20191023.json.tar.bz2\
                        langlinks-20190120.001.json.bz2
~~~

## When choosing a language

You can select language from following list.

~~~
['ar', 'bg', 'ca', 'cs', 'da', 'de', 'el', 'en', 'es', 'fa', 
 'fi', 'fr', 'he', 'hi', 'hu', 'id', 'it', 'ko', 'nl', 'no', 
 'pl', 'pt', 'ro', 'ru', 'sv', 'th', 'tr', 'uk', 'vi', 'zh']
~~~

~~~bash
python3 create_training ENEW_ENEtag_20191023.json.tar.bz2\
                        langlinks-20190120.001.json.bz2\
                        --lang en
~~~
