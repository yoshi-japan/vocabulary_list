from bs4 import BeautifulSoup
import requests
import csv
import time, random
import re


url = 'https://www.lexico.com/definition/'


def scraping(word):
    scraping_url = url + word
    try:
        response = requests.get(scraping_url)
        rnum = random.randint(10, 20)
        time.sleep(rnum)
    except:
        i = 0
        while i <3:
            print('in while trying again: ')
            rnum = random.randint(10, 20)
            time.sleep(rnum)
            response = requests.get(scraping_url)
            if response.status_code == 200:
                break

            i += 1

            if i == 2:
                raise ValueError('Error' + word)


    data = response.text
    # replace all white space to '' no string.
    html = re.sub(r'^\s+', '', data, flags = re.MULTILINE).replace('\n', '')
    soup = BeautifulSoup(html, 'html.parser')

    definition_list = soup.select('section.gramb')

    # if a word searched for doesn't exist in lexico.com, go to a next loop(word)
    if definition_list:
        for d_item in definition_list:

            examples = d_item.select('div.examples')
            for example in examples:
                example.decompose()

            ol_list = d_item.select('ol')
            for ol in ol_list:
                ol.name = 'ul'

            a_tag = d_item.select('[data-behaviour=ga-event-synonyms]')
            for a in a_tag:
                a.decompose()

            hyper_ref_list = d_item.select('[href]') # list
            for hyper_ref_tagObj in hyper_ref_list:
                del hyper_ref_tagObj['href']

            sub_senses_list = d_item.select('ul.subSenses')
            for sub_sense in sub_senses_list:
                sub_sense.wrap(soup.new_tag('p'))

            grammatical_note_list = d_item.select('span.grammatical_note')
            for grama in grammatical_note_list:
                grama.wrap(soup.new_tag('u'))

        def_list = []
        for def_el in definition_list:
            def_list.append(str(def_el))

        sections_string = '<hr>'.join(def_list)
        return sections_string

    else:
        return None


def main():
    # parameter(file_name, r)
    read_input = input('Read Mode Enter file name e.g.) svl1.csv:')
    write_input = input('Write Mode Enter name e.g.) new_svl1.csv:')
    with open(read_input, 'r', encoding='utf-8-sig') as csv_file,\
        open(write_input, 'w', encoding='utf-8', newline='') as new_file:
        csv_reader = csv.reader(csv_file)
        csv_writer = csv.writer(new_file)

        # csv_reader contains each line of csv, csv_reader is a list object.
        not_first_word = 0
        for line in csv_reader:

            if not not_first_word:
                definition = scraping(line[0].lstrip('\ufeff'))
                not_first_word =+1
            else:
                definition = scraping(line[0])

            if not definition:
                print('no web for:' + line[0])
                csv_writer.writerow([line[0],''])
            else:
                csv_writer.writerow([line[0],definition])


if __name__ == "__main__":
    main()