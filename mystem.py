import utils
import tempfile
import subprocess
import logging

MYSTEM_NAMES_LEXEMS = ['фам', 'имя', 'отч']
STRANGE_MIDDLE_NAMES = ['оглы', 'кызы']


def get_words_describe(data):
    """
    :rtype data: set[str]
    :rtype: generator 
    """
    with tempfile.NamedTemporaryFile(mode='w') as temp_input:
        temp_input.write('\n'.join(data))
        temp_input.flush()

        with tempfile.NamedTemporaryFile(mode='r') as temp_output:
            try:
                utils.get_output_from_program('./mystem', '-in', '--format', 'json',
                                              temp_input.name, temp_output.name)
                return utils.iload_json(temp_output.read())
            except subprocess.CalledProcessError as e:
                logging.error("Mystem run error: %s. And returned %s code", e.stderr, e.returncode)


def get_word_describe_dict(data):
    """
    Get all words analysis
    :rtype data: list[str] 
    :rtype: dict{str, list[int]} 
    """
    result = dict()
    for word in get_words_describe(set(data)):
        word_analysis = [0, 0, 0]
        for i in range(len(MYSTEM_NAMES_LEXEMS)):
            for lexem in word['analysis']:
                if MYSTEM_NAMES_LEXEMS[i] in lexem['gr']:
                    word_analysis[i] += 1
        result[word['text']] = word_analysis
    return result


def prepare_data(data_string):
    """
    Prepare data, get all characters and make it small
    :type data_string: str 
    :rtype: list[str]
    """
    data = ['']
    is_last_space = True
    for ch in data_string:
        if ch.isalpha():
            data[-1] += ch.lower()
            is_last_space = False
        elif not is_last_space:
            data += ['']
            is_last_space = True
    if is_last_space:
        data = data[:-1]
    return data


def set_upper_letters(s):
    """
    Make first letter upper, and other small, when it need.
    :rtype s: str
    :rtype: str 
    """
    s = s.lower()
    if s in STRANGE_MIDDLE_NAMES:
        return s
    if len(s) < 2:
        logging.error("Name %s it too short", s)
        raise Exception("Process upper letters error")
    return s[0].upper() + s[1:]


def processing_strange_middle_names(data):
    """
    Process middle names with two words
    :type data: list[str] 
    :rtype: (list[str], list[list[str]])
    """
    positions = []
    for i in range(len(data)):
        if data[i] in STRANGE_MIDDLE_NAMES:
            if i < 3:
                raise Exception('Strange middle names process error')
            if len(positions) > 0 and i - positions[-1] < 4:
                raise Exception('Strange middle names process error')
            positions += [i]

    processed = []
    for i in positions[::-1]:
        cur_name = data[i - 3:i + 1]
        processed += [cur_name]
        data = data[:i - 3] + data[i + 1:]

    return data, processed


def gen_is_middle_name_fucntion(data):
    """
    :type data: list[str] 
    """
    word_describe = get_word_describe_dict(data)

    def is_middle_name(s):
        """
        :type s: str  
        :rtype: bool 
        """
        cur_middle_name = word_describe[s][2]
        other = sum(word_describe[s])
        if cur_middle_name > 0 or other == 0:
            return True
        return False
    return is_middle_name


def process_other_names(data):
    """
    :param data: list[str]
    :rtype: list[list[str]]
    """
    processed = []
    cur = 0
    is_middle_name = gen_is_middle_name_fucntion(data)
    for word in data:
        if cur == 0:
            processed.append([word])
        elif cur == 1:
            processed[-1].append(word)
        elif cur == 2:
            if is_middle_name(word):
                processed[-1].append(word)
            else:
                cur = 0
                processed.append([word])
        cur += 1
        if cur == 3:
            cur = 0
    return processed


def process_names(str_data):
    """
    :type str_data: str 
    :rtype: list[str] 
    """
    data = prepare_data(str_data)
    data, processed = processing_strange_middle_names(data)
    processed += process_other_names(data)
    for i in range(len(processed)):
        for j in range(len(processed[i])):
            processed[i][j] = set_upper_letters(processed[i][j])
        processed[i] = ' '.join(processed[i])
    return processed
