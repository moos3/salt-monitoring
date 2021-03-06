# -*- coding: utf-8 -*-
'''
CPU monitoring state

Monitor the state of cpu resources
'''

# Import python libs
import logging

try:
    from salt.utils.monitoring import check_thresholds
except ImportError as e:  # TODO: Get rid of this
    def check_thresholds(*args, **kwargs):
        return __salt__['monitoringbp.check_thresholds'](*args, **kwargs)


__monitor__ = [
    'status',
]


log = logging.getLogger(__name__)

def status(maximum=None,
           minimum=None,
           thresholds=None,
           url=None):
    '''
    Return the current cpu usage stats
    '''
    # Monitoring state, no changes will be made so no test interface needed
    ret = {'name': 'cpu_usage',
           'result': False,
           'comment': '',
           'changes': {},
           'data': {}}

    data = {'name': 'cpu_usage',
	    'check': 'cpu.status'}

    if thresholds is None:
        thresholds = [
            {'failure':
                {'minimum': minimum,
                 'maximum': maximum,
                 'result': False}},
        ]

    info = __salt__['ps.cpu_percent']()
    log.info(info)
    cap = 100

    status, level, threshold, result = check_thresholds(cap, thresholds)

    if threshold:
        threshold = float(threshold)

    warning = ''
    if result is False:
        if level == 'high':
            warning = ' (above {0}% threshold)'.format(threshold)
        elif level == 'low':
            warning = ' (below {0}% threshold)'.format(threshold)

    message = ('CPU Usage is at {0}% ').format(cap, warning)
    ret['comment'] = '{0}'.format(status, message)

    data['message'] = message
    data['status'] = status

    if level:
        data['threshold'] = [level, threshold]

    data['info'] = {'cpu_precent': info}

    data['metrics'] = {'cpu_precent': info}
    if url:
        data['url'] = url

    ret['data'] = data
    ret['result'] = result
    return ret
