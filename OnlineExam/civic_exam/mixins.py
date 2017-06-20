from .utils import _tstamp


class CommonMixin:

    @classmethod
    def prepare_qlist(cls, sess_id, sel_ary, Answer, Question, User, examMode=False):
        # check in new practice/exam session
        usr = User.get_user(sess_id)
        usr.cat, usr.order, usr.num_q = sel_ary
        l_idx, questions = Question.sample_questions(sel_ary)
        if usr.num_q < 0:
            usr.num_q = len(questions)
        usr.save()
        print('{ts}>>[INFO] usr_id= {uid}'.format(ts=_tstamp(), uid=usr.id)) # debug pring
        for idx in l_idx:
            q = cls(user=usr, answer=Answer.objects.get(question=questions[idx]))
            q.save()
        q, l_choices, _ , _  = cls.get_next_question(sess_id, Question, User, examMode)
        return q, l_choices, usr.num_q

    @classmethod
    def get_next_question(cls, sess_id, Question, User, scramble=False, sel_choice=-1):
        usr = User.get_user(sess_id)
        if sel_choice >= 0:
            q_last = cls.objects.filter(user=usr).filter(viewed=True).order_by('-id').first()
            select = q_last.choices.split(',')[sel_choice]
            # print('>>select = {}'.format(select)) # debug print
            q_last.select = select
            q_last.save()
        q = cls.objects.filter(user=usr).filter(viewed=False).order_by('id').first()
        if q:
            q.viewed = True
            # prepare choices
            l_qid, l_choices = Question.get_choices(q.answer.question_id, scramble)
            # save choices for summary
            if scramble:
                q.choices = ','.join([str(i) for i in l_qid])
            q.save()
        else:
            l_choices = None
        n_cur = cls.objects.filter(user=usr).filter(viewed=True).count()
        n_total = usr.num_q
        return q, l_choices, usr, n_cur
