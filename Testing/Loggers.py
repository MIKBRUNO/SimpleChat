def write_to_log(tag, text, log):
    with open(log, 'a') as logf:
        logf.write('[' + tag + ']' + ': ' + text + '\n')


def write_to_main_log(tag, text):
    write_to_log(tag, text, 'Testing/Log.txt')
