from _PyPacwar import battle
import random
import filehelper



def initialize_files(num):
    filehelper.initialize_winners(num)

def sample_population(size):
    population = []
    initial_score=0
    for gene in range(size):
        population.append((gene_generate(), initial_score))
    return population

def gene_generate():
    genes = []
    choices=[0,1,2,3]
    for gene in range(50):
        genes.append(random.choice(choices))
    return genes

def crossover(pop, p,part):

    if part==1:
        topscore = pop[0:2]
        for i in range(len(pop)):
            score=pop[i][1]
            if random.random() < p:
                gene2 = random.choice(topscore)[0]
                pop[i]=(pop[i][0][0:34]+gene2[34:],score)
        return pop
    elif part==2:
        topscore = pop[0:2]
        for i in range(len(pop)):
            score = pop[i][1]
            if random.random() < p:
                gene2 = random.choice(topscore)[0]
                pop[i] = (pop[i][0][0:30] + gene2[30:], score)
        return pop


def mutate(pop, p):
    for i in range(len(pop)):
        score = pop[i][1]
        for j in range(50):
            if random.random() < p:
                choices = [0,1,2,3]
                choice=random.choice(choices)
                pop[i]=(pop[i][0][0:j] +[choice]+pop[i][0][j+1:], score)
    return pop

def main():
    #Hyper Parameters decided for our GA Algorithm
    generations = 10
    GA_rounds = 800
    winners_size = 5
    pop_size = 1024
    mutation_p = 0.02
    crossover_p = 0.4

    initialize_files(winners_size)

    for generation in range(generations):
        pop = sample_population(pop_size)


        for duel_round in range(5):
            pop = duels(pop)


        for GA_round in range(GA_rounds):
            print("GA round ",GA_round)
            scores = get_pop_scores(pop)
            for i in range(len(scores)):
                scores[i] = (pop[i][0], scores[i])
            scores.sort(key=lambda tup: tup[1], reverse=True)
            genes = []
            for s in scores:
                genes.append((s[0], 0))
            pop=genes.copy()
            #crossover level 1
            crossover(pop, crossover_p,1)
            #mutation level 1
            mutate(pop, mutation_p)
            #final crossover level 2
            crossover(pop,crossover_p,2)

        print("checking winners")
        check_winners(pop)

#Scoring functions
def get_pop_scores(pop):
    scores = []
    for g in pop:
        scores.append(r_score(g, pop))
    return scores


def r_score(gene1, pop):
    total = 0
    for g in pop:
        gene2 = g[0]
        s = base_score(gene1[0], gene2)
        total += s
    pscore= total / len(pop)
    return pscore




def duels(population):
    duels = [population[i:i+2] for i in range(0, len(population), 2)]
    newpop = []
    for duel in duels:
        gene1 = duel[0][0]
        gene2 = duel[1][0]
        rounds, survivors1, survivors2 = battle(gene1, gene2)
        if survivors1 > survivors2:
            newpop.append((gene1,duel[0][1] ))
        else:
            newpop.append((gene2,duel[1][1] ))
    return newpop

#Scoring according to tournament rules of pacwar
def base_score(gene1, gene2):
    rounds, survivors1, survivors2 = battle(gene1, gene2)
    i = 0
    if survivors2 > survivors1:
        i=1

    if rounds < 100:
        return (20,0)[i]
    elif rounds < 200:
        return (19,1)[i]
    elif rounds < 300:
        return (18,2)[i]
    elif rounds < 500:
        return (17,3)[i]
    else:
        if survivors1 == 0 or survivors2 == 0:
            return (17,3)[i]
        if survivors1 > survivors2:
            c = survivors1 / survivors2
        else:
            c = survivors2 / survivors1
        if c > 10:
            return (13,7)[i]
        elif c > 3:
            return (12,8)[i]
        elif c > 1.5:
            return (11,9)[i]
        return 10

#Comparing winners.txt to get the best (or) champion gene and return it.
def check_winners(pop):
    champs = filehelper.read_winners()
    new_champs = []
    new_scores = []

    for p in pop:
        gene1 = p[0]

        for champ in champs:
            gene2 = champ[0]
            if (gene2, champ[1]) not in new_champs:
                rounds, survivors1, survivors2 = battle(gene1, gene2)
                gene2_score = r_score((gene2, champ[1]), pop)
                new_champs.append((gene2, champ[1]))
                new_scores.append(gene2_score)

            if (gene1, p[1]) not in new_champs:
                if survivors1 > survivors2:
                        gene1_score = r_score((gene1, p[1]), pop)
                        new_champs.append((gene1, p[1]))
                        new_scores.append(gene1_score)

    for i in range(len(new_scores)):
        new_scores[i] = (new_champs[i][0], new_scores[i])
    new_scores.sort(key=lambda x: x[1], reverse = True)
    new_champs =new_scores[0:5]

    print("New champs",new_champs)

    filehelper.clear_winners()
    filehelper.write_genes(new_champs, "winners.txt")
    print("Best Gene: ", new_champs[0])
    filehelper.write_winners(new_champs[0],"finalchamps.txt")

    return new_champs


main()
