import math
import random 

class Node:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

def dist(A, B):
    return math.sqrt((A.x_pos - B.x_pos)**2 + (A.y_pos - B.y_pos)**2)

def possibilites_generator(num):
    result = []
    for i in range(num):
        result.append(i)
    return result


def greedy(A, start):
    posibilities = possibilites_generator(len(A))
    path = []
    current = start
    while(len(path) < len(A)):
        shortest = 1000000
        shortest_i = 0
        for i in range(len(posibilities)):
            if(current != i and A[posibilities[i]] != -1 and dist(A[current],A[posibilities[i]]) < shortest):
                shortest = dist(A[current],A[i])
                shortest_i = i
        path.append(shortest_i)
        current = shortest_i
        posibilities[shortest_i] = -1
    for i in range(len(posibilities)):
        if(posibilities[i] != -1):
            path[len(path)-1] = posibilities[i]
    print(posibilities)
    return path

p1 = Node(4,5)

p2 = Node(7,6)
p3 = Node(7,7)
p4 = Node(10,10)

p = [p1,p2,p3,p4]

print(greedy(p,0))

cities = [p1,p2,p3,p4]



# Number of individuals in each generation 
POPULATION_SIZE = 1000

# Valid genes 
GENES = possibilites_generator(len(cities))

# Target string to be generated 
TARGET = 10

class Individual(object): 
	''' 
	Class representing individual in population 
	'''
	def __init__(self, chromosome): 
        #path
		self.chromosome = chromosome 
		self.fitness = self.cal_fitness() 

	@classmethod
	def mutated_genes(self): 
		''' 
		create random genes for mutation 
		'''
		global GENES 
		gene = random.choice(GENES) 
		return gene 

	@classmethod
	def create_gnome(self): 
		''' 
		create chromosome or string of genes 
		'''
		global cities 
		#gnome_len = len(cities) 
		#random.choices(list, k=5)
		result = []
		while len(result) < len(cities):
			x = random.choice(GENES)
			if x not in result:
				result.append(x)
		return result
		#[self.mutated_genes() for _ in range(gnome_len)] 

	def mate(self, par2): 
		''' 
		Perform mating and produce new offspring 
		'''

		# chromosome for offspring 
		child_chromosome = [] 
		for gp1, gp2 in zip(self.chromosome, par2.chromosome):	 

			# random probability 
			prob = random.random() 

			# if prob is less than 0.45, insert gene 
			# from parent 1 
			if prob < 0.45: 
				child_chromosome.append(gp1) 

			# if prob is between 0.45 and 0.90, insert 
			# gene from parent 2 
			elif prob < 0.90: 
				child_chromosome.append(gp2) 

			# otherwise insert random gene(mutate), 
			# for maintaining diversity 
			else: 
				child_chromosome.append(self.mutated_genes()) 

		# create new Individual(offspring) using 
		# generated chromosome for offspring 
		return Individual(child_chromosome) 

	def cal_fitness(self): 
		''' 
		Calculate fittness score, it is the number of 
		characters in string which differ from target 
		string. 
		'''
		global TARGET 
		fitness = 0
		for i in range(len(self.chromosome)-1):
			fitness -= dist(cities[self.chromosome[i]],cities[self.chromosome[i+1]])
		unique_entries = []
		for x in self.chromosome:
			if x not in unique_entries:
				unique_entries.append(x)
		fitness += (len(self.chromosome) - len(unique_entries))*10
		return fitness 

def genetic(cit):
	global POPULATION_SIZE

	global cities

	cities = cit

	#current generation 
	generation = 1

	found = False
	population = [] 

	# create initial population 
	for _ in range(POPULATION_SIZE): 
				gnome = Individual.create_gnome() 
				population.append(Individual(gnome)) 

	while not found: 

		# sort the population in increasing order of fitness score 
		population = sorted(population, key = lambda x:x.fitness) 

		# if the individual having lowest fitness score ie. 
		# 0 then we know that we have reached to the target 
		# and break the loop 
		if generation == 100: 
			found = True
			break

		# Otherwise generate new offsprings for new generation 
		new_generation = [] 

		# Perform Elitism, that mean 10% of fittest population 
		# goes to the next generation 
		s = int((10*POPULATION_SIZE)/100) 
		new_generation.extend(population[:s]) 

		# From 50% of fittest population, Individuals 
		# will mate to produce offspring 
		s = int((90*POPULATION_SIZE)/100) 
		for _ in range(s): 
			parent1 = random.choice(population[:50]) 
			parent2 = random.choice(population[:50]) 
			child = parent1.mate(parent2) 
			new_generation.append(child) 

		population = new_generation 
		print("Generation: " + str(generation) + " fitness: " + str(population[0].fitness))
		print(population[0].chromosome)

		generation += 1

	
	print("Generation: " + str(generation) + " fitness: " + str(population[0].fitness))
	print(population[0].chromosome) 
	return population[0].chromosome



genetic(cities)