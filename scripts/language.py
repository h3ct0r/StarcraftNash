"""
Defines languages and vocabulary
"""
#class vocabulary:
EGREEDY = 'E-greedy'
ENASH = 'E-Nash'
REPLY_SCORE = 'Reply-score'
XELNAGA = 'Xelnaga'
MEAN_WIN_PERCENT = 'mean_win_percent'

english = {
    EGREEDY: r'$\epsilon$-greedy',
    ENASH: r'$\varepsilon$-Nash',
    REPLY_SCORE: 'Reply last',
    XELNAGA: 'Single choice',
    MEAN_WIN_PERCENT: 'Mean win percent'
}

portuguese = {
    EGREEDY: r'$\epsilon$-guloso',
    ENASH: r'$\varepsilon$-Nash',
    REPLY_SCORE: 'Rebater última',
    XELNAGA: 'Escolha única',
    MEAN_WIN_PERCENT: 'Percentual médio de vitórias'
}

def get_vocabulary(language='en'):
    if language == 'en':
        return english
    elif language == 'pt':
        return portuguese
    else:
        raise RuntimeError("Language '%s' unknown" % language)



