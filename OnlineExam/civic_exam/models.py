from datetime import datetime
from django.db import models
from django.db.models import Q, F
from .mixins import CommonMixin
import random


# Utility class
class Choices:
    def __init__(self, qid, val, info=''):
        self.qid = qid
        self.value = val
        self.info = info
        # self.selected = False

    def __str__(self):
        return [self.qid, self.value, self.info]

# DB models here.
class Cat(models.Model):
    """
    general category
    """
    value = models.CharField(max_length=255)


class Subcat(models.Model):
    """
    subcategory info
    """
    cat = models.ForeignKey(Cat)
    value = models.CharField(max_length=255)


class Question(models.Model):
    """
    basic info of a question
    """
    value = models.CharField(max_length=500, default='')
    cat = models.ForeignKey(Cat)
    subcat = models.ForeignKey(Subcat)

    @classmethod
    def get_choices(cls, key_id, scramble, n_choices=4):
        """
        prepare a list of choices with true Answer mixed in
        """
        a = Answer.objects.get(question__id=key_id)
        l_choices = [Choices(key_id, a.value, 'img/check.png')]
        l_qid = [i for i in range(1, Question.objects.count()+1)]
        l_qid.remove(key_id)
        for qid in random.sample(l_qid, n_choices-1):
            a = Answer.objects.get(question__id=qid)
            l_choices.append(Choices(qid, a.value, 'img/cross.png'))
        # scramble if needed
        if scramble:
            l_qid = random.sample([i for i in range(0,n_choices)], n_choices)
            l_choices_new = [l_choices[i] for i in l_qid]
            l_choices = l_choices_new

        l_qid = [c.qid for c in l_choices]
        return l_qid, l_choices

    @classmethod
    def sample_questions(cls, sel_ary):
        """
        sample a list of questions based on select options
        """
        # Get satisfying items
        sel_cat, sel_order, sel_num = sel_ary
        # print('>>{}'.format(sel_ary)) # debug print
        if sel_cat == 'ALL':
            questions = Question.objects.order_by('id')
        else:
            questions = Question.objects.filter(Q(cat__value=sel_cat) | Q(subcat__value=sel_cat)).order_by('id')

        if sel_num < 0: # ALL case
            n_qs = n_len = len(questions)
        else:
            n_len = max(sel_num, len(questions))
            n_qs = min(sel_num, len(questions))
        print('>>{} {}'.format(n_len, n_qs))
        l_idx = [i for i in range(0, n_qs)]
        if sel_order[0] == 'D':
            l_idx.reverse()
        elif sel_order[0] == 'S':
            l_idx = random.sample(range(0, n_len), n_qs)

        return l_idx, questions

    def __str__(self):
        """
        text output
        """
        return 'content:{} cat:{} subcat:{}'.format(self.value, self.cat.value, self.subcat.value)


class Answer(models.Model, CommonMixin):
    """
    answer to one question
    """
    question = models.OneToOneField(Question, primary_key=True)
    value = models.CharField(max_length=1000, blank=True)


class User(models.Model):
    """
    user name and custom selections
    """
    name = models.CharField(max_length=255, default='')
    cat = models.CharField(max_length=255)
    order = models.CharField(max_length=255)
    num_q = models.IntegerField(blank=True, null=True)
    exam_mode = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_user(cls, username):
        return cls.objects.filter(name=username).order_by('-created_at').first()


class Practice(models.Model, CommonMixin):
    """
    practice question set for each user
    """
    user = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)
    viewed = models.BooleanField(default=False)


class Exam(models.Model, CommonMixin):
    """
    exam question for one user
    """
    user = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)
    viewed = models.BooleanField(default=False)
    select = models.IntegerField(default=-1)
    choices = models.CharField(max_length=50, default='')
    # def record_selection(cls, username, sel_id):
    #     usr = User.get_user(username)
    #     e = cls.objects.filter(user=usr).filter(viewed=True).order_by('-id').first()
    #     e.select = sel_id
    #     e.save()


class Summary():
    def __init__(self, username):
        self.usr = User.get_user(username)
        self.exam_set = Exam.objects.filter(Q(user=self.usr) & ~Q(choices='')).order_by('id')

    def get_all_choices(self):
        all_choices = []
        for e in self.exam_set:
            chos = []
            for c in e.choices.split(','):
                cid, qid = int(c), e.answer_id
                if cid == e.select:
                    n_show = 1
                elif cid == qid:
                    n_show = 2
                else:
                    n_show = 0
                a = Answer.objects.get(question__id=cid)
                info = 'img/check.png' if cid == qid else 'img/cross.png'
                # print('>>chos= {}'.format([n_show, a.value, info])) # debug print
                chos.append(Choices(n_show, a.value, info))
            all_choices.append(chos)
        return all_choices

    def get_summary(self):
        exam_choices = self.get_all_choices()
        n_correct = self.exam_set.filter(answer_id=F('select')).count()
        return self.usr, self.exam_set, exam_choices, n_correct
