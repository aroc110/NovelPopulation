############################################################

from __future__ import division
import pp
import random

################################################################
# Function divides population according to fitness

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

def trial(pop,wfit,hfit,dfit,en,ctr):

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
            population = divide(population,pop)
            gen +=1
            q = check(population,pop)
            if q == 1:
                cont = 0
                fix = 1
                break
            if q == 0:
                cont = 0
                fix = 0
                break
        ns = 0
        if cont:            
            population = mate(population,[wfit,hfit,dfit])
            population = divide(population,pop)
            gen +=1
            q = check(population,pop)
        if q == 1:
            fix = 1
            break
        if q == 0:
            fix = 0
            break
        
        if gen >= 5000:
            fix = 0
            break

    return gen, fix

################################################################
# Change parameters here

nums = 100000                # Determines precision and accuracy
rep = 3                    # Number of times to repeat the simulation
wfit,hfit,dfit = 0.99,1,1   # Fitness for wildtype, heterozygous, and dominant organisms
output = 'output.csv'             # Name of output file

# To run in command line: move to containing directory, enter command
# python finPop.py
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
            for t in range(rep):
                jobs = []
                for x in range(nums):
                    jobs.append(fn.submit(pop,wfit,hfit,dfit,en,ctr))

                gens = []
                fixes = []

                for job in jobs:
                    val = job()
                    gens.append(val[0])
                    fixes.append(val[1])

                fixprob = sum(fixes)/float(nums)
                avggens=sum(gens)/nums

                out = 'Fixation probability: ' + str(fixprob)+'; AvgGens: ' + str(avggens) + '; pop = ' + str(pop) +'; en = ' + str(en) + '\n'
                print out
                with open(output,'a') as f:
                    f.write(str(fixprob) + ',' + str(avggens) + ',' + str(pop) + ',' + str(en) + ',' + str(ctr) + ',' + str(nums) + '\n')
print 'done'
