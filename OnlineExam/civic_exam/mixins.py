# Load up models
# from models import Answer, Question, User

class CommonMixin:

    @classmethod
    def prepare_qlist(cls, username, sel_ary, Answer, Question, User, examMode=False):
        # check in new practice session
        sel_cat, sel_order, sel_num = sel_ary
        usr = User(name=username, cat=sel_cat, order=sel_order, num_q=sel_num)
        # Clear history related to user
        # cls.objects.filter(user=username).delete()
        l_idx, questions = Question.sample_questions(sel_ary)
        if sel_num < 0:
            usr.num_q = len(questions)
        usr.save()
        # print('>>usr_id= {}'.format(usr.id))
        for idx in l_idx:
            q = cls(user=usr, answer=Answer.objects.get(question=questions[idx]))
            q.save()
        q, l_choices, _ , _  = cls.get_next_question(username, Question, User, examMode)
        return q, l_choices, usr.num_q

    @classmethod
    def get_next_question(cls, username, Question, User, scramble=False, sel_choice=-1):
        usr = User.get_user(username)
        if sel_choice >= 0:
            q_last = cls.objects.filter(user=usr).filter(viewed=True).order_by('-id').first()
            select = q_last.choices.split(',')[sel_choice]
            print('>>select = {}'.format(select)) # debug print
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
