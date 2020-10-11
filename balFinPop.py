############################################################

from __future__ import division
import pp
import random

################################################################
# Introduces mutations into the population
# Returns new population

def mutate(population,mut,bmut,ctr,fit):
    newPop = []
    for ciliate in population:
        if ciliate[0] == 0:
            new = 0
            if random.random() <= mut:
                new += 1
            if random.random() <= mut:
                new += 1
        elif ciliate[0] == 1:
            new = 1
            if random.random() <= mut:
                new += 1
            if random.random() <= bmut:
                new -= 1
        else:
            new = 2
            if random.random() <= bmut:
                new -= 1
            if random.random() <= bmut:
                new -= 1
        if ctr:
            newPop.append([new,new,fit[new]])
        else:
            newPop.append([new,ciliate[1],ciliate[2]])
    return newPop

################################################################
# Function divides population according to fitness
# Returns new population

def divide(population,pop):
    newPop = []
    for ciliate in population:
        if random.random() <= ciliate[2]:
            newPop.append(ciliate)
            newPop.append(ciliate)
        else:
            newPop.append(ciliate)
    return random.sample(newPop,pop)

################################################################
# Calculates allele frequency of population
# Returns fraction of alleles

def check(population,pop):
    tot = sum(cil[0] for cil in population)
    return float(tot)/(2*pop)

################################################################
# Randomly mates population

def mate(population,fit):
    random.shuffle(population)
    
    newPop = []

    while len(population):
        mom = population.pop()
        dad = population.pop()
            
        left,right = 0,0
        if mom[0] == 2:
            left += 1
            right += 1
        elif mom[0] == 1:
            if random.random() < 0.5:
                left+=1
            if random.random() < 0.5:
                right+=1
        if dad[0] == 2:
            left += 1
            right += 1
        elif dad[0] == 1:
            if random.random() < 0.5:
                left+=1
            if random.random() < 0.5:
                right+=1
        newPop.append([left,left,fit[left]])
        newPop.append([right,right,fit[right]])
    return newPop

################################################################
# Master function
# Returns lists of allelic frequencies and average

def trial(pop,wfit,hfit,dfit,en,ctr,mut,bmut):

    qs = []

    initCil = [0,0,wfit]
    population = [initCil for t in range(pop-1)]
    
    if ctr:
        population.append([1,1,hfit])
    else:
        population.append([1,0,wfit])

    ns= random.randint(0,en)
    q=1/(2*pop)

    cont = 1
    gen = 0

    while 1:
        for t in range(en-ns):
            population = mutate(population,mut,bmut, ctr, [wfit,hfit,dfit])
            population = divide(population,pop)
            gen +=1
            q = check(population,pop)
            qs.append(q)
        ns = 0
        if cont:            
            population = mutate(population,mut,bmut, ctr, [wfit,hfit,dfit])
            population = mate(population,[wfit,hfit,dfit])
            population = divide(population,pop)
            gen +=1
            q = check(population,pop)
            qs.append(q)
        if gen >= 100000:
            break
    endq = qs[10000:]
    avg = sum(endq)/(2*len(endq))
    return qs,avg

################################################################
# Change Parameters here

mut = 10**-4                 # Forward Mutation Rate
bmut = 10**-5                # Backward Mutation Rate
wfit,hfit,dfit = 1,0.95,0.95 # Fitness for wildtype, heterozygous, and dominant organisms
output = 'output.csv'        # Name of output file
nums = 32                    # Number of times to repeat simulation

# To run in command line: move to containing directory, enter command
# python balFinPop.py
# Outputs as comma-seperated values (csv), which can be opened in excel.

################################################################
# Code initiates simulation

job_server = pp.Server()
fn = pp.Template(job_server,trial ,(),(),None,(),'default',globals())


for pop in [100,500,1000,3000,10000]:
    for ctr in [0,1]:
        for en in [0,5,25,50,75]:
            if ctr and en==0:
                continue
            jobs = []
            for t in range(nums):
                jobs.append(fn.submit(pop,wfit,hfit,dfit,en,ctr,mut,bmut))

            qss = []
            avgs = []
                
            for job in jobs:
                val = job()
                qss.append(val[0])
                avgs.append(val[1])
        
            out = 'Avgs: ' + str(avgs)+'; pop = ' + str(pop) +'; en = ' + str(en) + '\n'
            print out
            with open(output,'a') as f:   
                f.write(str(avgs).strip('[]') + ',' + str(pop) + ',' + str(en) + ',' + str(ctr) + '\n')


