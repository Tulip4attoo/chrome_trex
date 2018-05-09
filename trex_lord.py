import numpy as np
import trex_nn
import capturing_objects
import time
import logging


###### PART 1: PREPARE FIXED VARs AND FUNCTIONs ######
######################################################
######################################################

URL = "http://www.trex-game.skipser.com/"

N_X = 3
N_H = 3
N_Y = 1

POP_SIZE = 12
MUTATION_PROB = 0.1
N_SIZE = 4
RANDOM_SET = [6, 5, 4, 3]
BODY_KEYS = ["W1", "W2", "b1", "b2"]
MUTATION_RANGE = [0.005, 0.5, 0.2, 0.05]

def cv_to_sequence(body):
    """
    cv body aka parameters_set to ADN aka sequence
    """
    sequence = []
    for key in BODY_KEYS:
        sequence.append(body[key])
    sequence_str = str(sequence)
    sequence_str = sequence_str.replace("[", "").replace("array", "")
    sequence_str = sequence_str.replace("]", "").replace("\n", "")
    sequence_str = sequence_str.replace("(", "").replace(")", "")
    sequence_str = sequence_str.replace(" ", "")
    sequence_adj = list(map(float, sequence_str.split(",")))
    return sequence_adj


def cv_to_body(adn):
    """
    cv ADN aka sequence to body aka parameters_set
    tam thoi hard code 1 ty chu ko chac chet luon =))
    """
    params = {}
    params["W1"] = np.reshape(adn[:9], (3, 3))
    params["W2"] = np.reshape(adn[9:12], (1, 3))
    params["b1"] = np.reshape(adn[12:15], (3, 1))
    params["b2"] = np.reshape(adn[15], (1, 1))
    return params


def genesis(pop_size = POP_SIZE):
    trex_clan = [trex_nn.initialize_parameters(N_X, N_H, N_Y) for i in range(POP_SIZE)]
    trex_clan = np.array(trex_clan)
    return trex_clan


def random_match(random_set = RANDOM_SET):
    number = -1
    curr_number = sum(RANDOM_SET)
    lucky_number = np.random.randint(0, curr_number)
    while lucky_number < curr_number:
        number += 1
        curr_number -= RANDOM_SET[number]
    return number


def do_mutation(child, mutation_prob = MUTATION_PROB):
    mutation_rate = np.random.random(16)
    new_child = child[:]
    for ind in range(16):
        if mutation_rate[ind] < mutation_prob:
            if ind < 9:
                new_child[ind] += np.random.randn() * MUTATION_RANGE[0]
            elif ind < 12:
                new_child[ind] += np.random.randn() * MUTATION_RANGE[1]
            elif ind < 15:
                new_child[ind] += np.random.randn() * MUTATION_RANGE[2]
            else:
                new_child[ind] += np.random.randn() * MUTATION_RANGE[3]
    return new_child


def crossver(adam, eva):
    weight_adam = adam[:12]
    weight_eva = eva[:12]
    bias_adam = adam[12:]
    bias_eva = eva[12:]

    cut_1 = np.random.randint(0, 12)
    cut_2 = np.random.randint(12, 16) - 12

    childs = []
    childs.append(weight_adam[:cut_1] + weight_eva[cut_1:] + bias_adam[:cut_2] + bias_eva[cut_2:])
    childs.append(weight_adam[:cut_1] + weight_eva[cut_1:] + bias_eva[:cut_2] + bias_adam[cut_2:])
    childs.append(weight_eva[:cut_1] + weight_adam[cut_1:] + bias_adam[:cut_2] + bias_eva[cut_2:])
    childs.append(weight_eva[:cut_1] + weight_adam[cut_1:] + bias_eva[:cut_2] + bias_adam[cut_2:])
    selected_child = np.random.randint(0, 4)
    return childs[selected_child]


def breed_a_child(survivals):
    """
    chon 2 cha me tu survivals va crossver
    sau do cho child mutation
    """
    adam_ind = random_match(RANDOM_SET)
    eva_ind = random_match(RANDOM_SET)
    # boi vi so ok kha it --> co the cu de tu breed cung dc di
    # while adam_ind == eva_ind:
    #     eva_ind = random_match(RANDOM_SET)
    expected_cain = crossver(survivals[adam_ind], survivals[eva_ind])
    real_cain = do_mutation(expected_cain)
    return real_cain


def gen_to_max_size(survivals, pop_size = POP_SIZE):
    """

    """
    curr_len = N_SIZE
    dna_survivals = list(map(cv_to_sequence, survivals))
    dna_tribal = dna_survivals[:]
    while curr_len < pop_size:
        new_born = breed_a_child(dna_survivals)
        dna_tribal.append(new_born)
        curr_len += 1
    new_gen = list(map(cv_to_body, dna_tribal))
    new_gen = np.array(new_gen)
    return new_gen


def select_survivals(tribal, score):
    fitness_scores = np.array(score)
    survival_inds = (-fitness_scores).argsort()[:4]
    return tribal[survival_inds], survival_inds



######  PART 2: EVOLVE                          ######
######################################################
######################################################

def evolve():
    adam_eva = genesis(POP_SIZE)
    curr_gen = adam_eva.copy()
    count_gen = 0
    while True:
        log1.info("-------------------------------------------------------")
        log2.info("-------------------------------------------------------")
        print("-------------------------------------------------------")
        log1.info("Generation: {}".format(count_gen))
        log1.info("a new day has come")
        score = []
        for trex in curr_gen:
            count_cactus = capturing_objects.play_game(trex)
            score.append(count_cactus)
        log1.info(score)
        survivals, survival_inds = select_survivals(curr_gen, score)
        log1.info(survival_inds)
        log1.info("genarating next gen")
        curr_gen = gen_to_max_size(survivals, POP_SIZE)
        count_gen += 1
        log2.info(survivals)
        if max(score) > 15:
            log1.info(survivals)
            continue
        elif count_gen % 10 == 0:
            log1.info(survivals)
        log1.info("")

def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)    


log_file_name_1 = time.strftime("./logs/%Y-%m-%d_%H:%M:%S_brief.log")
log_file_name_2 = time.strftime("./logs/%Y-%m-%d_%H:%M:%S_survival.log")

setup_logger('log1', log_file_name_1)
setup_logger('log2', log_file_name_2)

log1 = logging.getLogger('log1')
log2 = logging.getLogger('log2')

logging.basicConfig(filename=log_file_name_1, level=logging.INFO, 
                    format="%(asctime)s %(levelname)s %(message)s")
logging.basicConfig(filename=log_file_name_2, level=logging.INFO, 
                    format="%(asctime)s %(levelname)s %(message)s")
log1.info("Start")
log2.info("Start")

capturing_objects.chrome_setup(URL)
time.sleep(3)
evolve()