# This Python file uses the following encoding: utf-8

"""
Defines languages and vocabulary
"""
#class vocabulary:
EGREEDY = 'E-greedy'
ENASH = 'E-Nash'
NASH = 'Nash'
FREQUENTIST = 'Frequentist'
REPLY_SCORE = 'Reply-score'
XELNAGA = 'Xelnaga'
MEAN_WIN_PERCENT = 'mean_win_percent'

english = {
    EGREEDY: r'$\epsilon$-greedy',
    ENASH: r'$\varepsilon$-Nash',
    FREQUENTIST: 'Frequentist',
    NASH: 'Nash',
    REPLY_SCORE: 'Reply last',
    XELNAGA: 'Single choice',
    MEAN_WIN_PERCENT: 'Mean win percent'
}

portuguese = {
    EGREEDY: r'$\epsilon$-guloso',
    ENASH: r'$\varepsilon$-Nash',
    FREQUENTIST: 'Frequentista',
    NASH: 'Nash',
    REPLY_SCORE: r'Rebater \'ultima', #.decode('utf-8'),
    XELNAGA: r'Escolha \'unica', #.decode('utf-8'),
    MEAN_WIN_PERCENT: r'Percentual m\'edio de vit\'orias', #2.decode('utf-8'),
}

def get_vocabulary(language='en'):
    if language == 'en':
        return english
    elif language == 'pt':
        return portuguese
    else:
        raise RuntimeError("Language '%s' unknown" % language)



