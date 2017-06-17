# coding: utf-8
# ---------------------------------------------------------------------------------
# Civic exam test quetion loader
# Input: csv with exam civic exam question & answers
# Output: csv summary of group dem features
# ---------------------------------------------------------------------------------

# Load global libs
import pandas as pd
import os, sys, imp
from datetime import date

# Load up Django environment
import django
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections
# os.environ['env'] = 'prod' # set environ to non-dev
sys.path.append(os.path.abspath('../')) # jump to upper level folder for settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

# Load up models
from civic_exam.models import Question, Anwser, Cat, Subcat

def help():
    print('Usage: {} [civic_exam csv]'.format(sys.argv[0]))


def init_cats():
    l_cat = ['AMERICAN GOVERNMENT','AMERICAN HISTORY','INTEGRATED CIVICS']
    l_subcat = (['1A: Principles of American Democracy', '1B: System of Government', '1C: Rights and Responsibilities'],
                ['2A: Colonial Period and Independence', '2B: 1800s', '2C: Recent American History and Other Important Historical Information'],
                ['3A: Geography', '3B: Symbols', '3C: Holidays'])

    # Truncate table
    # Cat.objects.all().delete()
    # Subcat.objects.all().delete() # Truncate table
    for idx, cat in enumerate(l_cat):
        c = Cat(value=cat)
        c.save()
        for subcat in l_subcat[idx]:
            sc = Subcat(value=subcat, cat=c)
            sc.save()
    print('Cat and subcat uploaded!')


def main():
    if len(sys.argv)<2:
        help()
        exit('Need csv input')

    # Load input csv group
    inp_csv = sys.argv[1]
    df_inp_exam = pd.read_csv(inp_csv)
    print('Input csv: {}'.format(inp_csv))

    init_cats()
    # Question.objects.all().delete()
    # Anwser.objects.all().delete()
    count = 0
    for _, row in df_inp_exam.iterrows():
        d = dict(row)
        c = Cat.objects.get(value=row['cat'])
        sc = Subcat.objects.get(value=row['subcat'])
        q = Question(value=row['question'], cat=c, subcat=sc)
        q.save()
        a = Anwser(question=q, value=row['anwser'])
        a.save()
        print('Uploaded: qes={}, anw={}'.format(q.value, a.value))
        count += 1

    print('Total uploaded: {}'.format(count))

if __name__ == '__main__':
    main()
