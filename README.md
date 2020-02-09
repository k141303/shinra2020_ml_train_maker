# shinra2020_ml_train_maker

## How to use

By running the following script, you can get the learning data of all(30) languages.  
Download the necessary data from [here](http://shinra-project.info/shinra2020ml/2020ml_data/?lang=en).(These data are in sections 1.1 and 1.2.)

~~~bash
python3 create_training ENEW_ENEtag_20191023.json.tar.bz2\
                        langlinks-20190120.001.json.bz2
~~~

## When choosing a language

You can select language from following list.

~~~Python
['ar', 'bg', 'ca', 'cs', 'da', 'de', 'el', 'en', 'es', 'fa', 
 'fi', 'fr', 'he', 'hi', 'hu', 'id', 'it', 'ko', 'nl', 'no', 
 'pl', 'pt', 'ro', 'ru', 'sv', 'th', 'tr', 'uk', 'vi', 'zh']
~~~

If you want to make training data of English.

~~~bash
python3 create_training ENEW_ENEtag_20191023.json.tar.bz2\
                        langlinks-20190120.001.json.bz2\
                        --lang en
~~~

## You can change the output directory

~~~bash
python3 create_training ENEW_ENEtag_20191023.json.tar.bz2\
                        langlinks-20190120.001.json.bz2\
                        --output_dir [DIR_PATH]
~~~
