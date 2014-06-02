#-*- coding: utf-8

def viterbi(observe, states, start_prob, trans_prob, emit_prob):
    '''Viterbi algorithm.

    :param observe: The observe space.
    :param states: The state space.
    :param start_prob: The initial probabilities.
    :param trans_prob: The transition probabilities.
    :param emit_prob: The emit probabilities.
    '''
    path = {}
    path_prob = [{}]

    for each in states:
        path[each] = [each]
        path_prob[0][each] = (start_prob[each] *
                              emit_prob[each].get(observe[0], 0))

    for t in xrange(1, len(observe)):
        path_prob.append({})
        newpath = {}
        
        for each in states:
            (prob, state) = max(
                [(path_prob[t-1][_s] *
                  trans_prob[_s].get(each, 0) *
                  emit_prob[each].get(observe[t], 0), _s)
                 for _s in states if path_prob[t-1][_s] >= 0])
            path_prob[t][each] = prob
            newpath[each] = path[state] + [each]

        path = newpath

    if emit_prob['M'].get(observe[-1], 0) > emit_prob['S'].get(observe[-1], 0):
        (prob, state) = max(
            [(path_prob[len(observe) - 1][_s], _s) for _s in ('E', 'M')])
    else:
        (prob, state) = max(
            [(path_prob[len(observe) - 1][_s], _s) for _s in states])

    return (prob, path[state])
