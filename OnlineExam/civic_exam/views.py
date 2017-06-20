from django.shortcuts import render
from django.db.models import Count
from .models import Answer, Question, User, Cat, Subcat, Practice, Exam, Summary


# utility function
CATS = SUBCATS = False
def get_cat_subcat():
    global CATS, SUBCATS
    if not CATS:
        CATS = Cat.objects.annotate(num_cat=Count('question')).order_by('value')
        SUBCATS = Subcat.objects.annotate(num_subcat=Count('question')).order_by('value')
    return {'Category': CATS, 'Subcat': SUBCATS}


def login(request, err_msg=''):
    sess_id = request.COOKIES['csrftoken']
    usr = User.get_user(sess_id)
    if usr:
        context = {'usernm':usr.name}
    else:
        context = {'usernm':'wes_guest'}
    context['err_msg'] = err_msg
    return render(request, 'login.html', context)


# Create your views here.
def index(request):
    context = {}
    if request.method == 'GET':
        usr = User.get_user(request.COOKIES['csrftoken'])
        if not usr:
            return login(request)
        context['username'] = usr.name
    elif request.method == 'POST':
        if 'go_exam' in request.POST:
            return exam(request)
        elif 'go_practice' in request.POST:
            return practice(request)
        elif 'login' in request.POST:
            usernm = request.POST['username'].strip()
            # print('>>usernm= {}'.format(usernm)) # debug print
            if not usernm:
                return login(request, 'Bad or invalid user name, please change one.')
            context['username'] = request.POST['username']
            User.new_session(context['username'], request.META['REMOTE_ADDR'], request.COOKIES['csrftoken'])
    context.update(get_cat_subcat())
    return render(request, 'index.html', context)


def practice(request):
    qna_set = False # debug
    site_to_render = 'practice.html'
    sess_id = request.COOKIES['csrftoken']
    # print('Cookies: {}'.format(request.COOKIES)) # debug print
    # from pprint import pprint
    # pprint(request.META) # debug print
    if request.method == 'GET':
        qna_set, l_choices, usr, n_cur = Practice.get_next_question(sess_id, Question, User)
        if qna_set:
            context = {'sel_cat':usr.cat, 'sel_order':usr.order, 'qna_set':qna_set, 'choices':l_choices,
                       'n_current':n_cur, 'n_total':usr.num_q}
        else:
            site_to_render = 'index.html'
            context = get_cat_subcat()
    elif request.method == 'POST':
        sel_cat = request.POST['select_cat']
        sel_order = request.POST['select_order']
        sel_num = request.POST['select_num']
        sel_num = -1 if sel_num == 'ALL' else int(sel_num)
        qna_set, l_choices, n_total = Practice.prepare_qlist(sess_id, [sel_cat, sel_order, sel_num], Answer, Question, User)
        # qna_set = Practice.objects.get(id=1)
        # print(qna_set.answer.question.value) # debug print
        # print(qna_set.answer.value) # debug print
        context = {'sel_cat':sel_cat, 'sel_order':sel_order,'qna_set':qna_set, 'choices':l_choices,
                   'n_current':1, 'n_total':n_total}
    return render(request, site_to_render, context)


def exam(request):
    qna_set = False # debug
    site_to_render = 'exam.html'
    sess_id = request.COOKIES['csrftoken']
    if 'go_exam' in request.POST:
        sel_cat = request.POST['select_cat']
        sel_order = request.POST['select_order']
        sel_num = request.POST['select_num']
        sel_num = -1 if sel_num == 'ALL' else int(sel_num)
        qna_set, l_choices, n_total = Exam.prepare_qlist(sess_id, [sel_cat, sel_order, sel_num], Answer, Question, User, True)
        context = {'sel_cat':sel_cat, 'sel_order':sel_order,'qna_set':qna_set, 'choices':l_choices,
                   'n_current':1, 'n_total':n_total}
    else:
        try:
            sel_choice = int(request.POST['optionsRadios'])-1
        except:
            # no selection or invalid anwser
            sel_choice = -1
        print('>>sel_choice = {}'.format(sel_choice)) # debug print
        qna_set, l_choices, usr, n_cur = Exam.get_next_question(sess_id, Question, User, True, sel_choice)
        if qna_set:
            context = {'sel_cat':usr.cat, 'sel_order':usr.order, 'qna_set':qna_set, 'choices':l_choices,
                       'n_current':n_cur, 'n_total':usr.num_q}
        else:
            return summary(request)
    return render(request, site_to_render, context)


def summary(request):
    # site_to_render = 'summary.html'
    sess_id = request.COOKIES['csrftoken']
    summ = Summary(sess_id)
    usr, exam_set, exam_choices, n_correct = summ.get_summary()
    context = {'sel_cat':usr.cat, 'sel_order':usr.order, 'exam_set':zip(exam_set,exam_choices),
               'n_correct': n_correct, 'n_total':usr.num_q, 'percentile':'{:.0f}%'.format(n_correct*100/usr.num_q)}
    return render(request, 'summary.html', context)
