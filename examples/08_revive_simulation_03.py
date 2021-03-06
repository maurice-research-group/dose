'''
Example 08 - Reviving a simulation (Example 03) from simulation logging
database and run the simulation for another 200 generations.

Example 03 ran the simulation for 1000 generations and logged the events 
into case_study_01.db file. This example revived the logged simulation 
from case_study_01.db file using the simulation start time as identifier 
(2013-10-19-1382200534.1) and run the simulation from generation 1001 to 
1200. The events of generation 1001 to 1200 are logged in case_study_01.db 
file.
'''

try: 
	import run_examples_without_installation
except ImportError: pass

import dose
import os, random

'''
Needs pre-existing 03_no_migration_isolated_mating.py.
Change simulation_time below to the corresponding starting time 
of the said simulation.
'''

rev_parameters = {"database_source" : "case_study_01.db",
                  "simulation_time": "2013-10-19-1382200534.1",
                  "population_locations": [[(x,y,z) 
                                            for x in range(5) 
                                                for y in range(5) 
                                                    for z in range(1)]],
                  "rev_start" : [1000],
                  "extend_gen" : 200,
                  "simulation_name": "08_revive_simulation_03",
                  "chromosome_bases": ['0','1'],
                  "background_mutation": 0.1,
                  "additional_mutation": 0,
                  "mutation_type": 'point',
                  "max_tape_length": 50,
                  "clean_cell": True,
                  "interpret_chromosome": True,
                  "max_codon": 2000,
                  "goal": 0,
                  "eco_cell_capacity": 100,
                  "fossilized_ratio": 0.01,
                  "fossilized_frequency": 20,
                  "print_frequency": 10,
                  "ragaraja_version": 0,
                  "ragaraja_instructions": ['000', '001', '010',
                                            '011', '100', '101'],
                  "eco_buried_frequency": 100,
                  "database_file": "case_study_01.db",
                  "database_logging_frequency": 1
                  }

class simulation_functions(dose.dose_functions):

    def organism_movement(self, Populations, pop_name, World): pass

    def organism_location(self, Populations, pop_name, World): pass

    def ecoregulate(self, World): pass

    def update_ecology(self, World, x, y, z): pass

    def update_local(self, World, x, y, z): pass

    def report(self, World): pass

    def fitness(self, Populations, pop_name): pass

    def mutation_scheme(self, organism): 
        organism.genome[0].rmutate(rev_parameters["mutation_type"],
                                   rev_parameters["additional_mutation"])

    def prepopulation_control(self, Populations, pop_name): pass

    def mating(self, Populations, pop_name): 
        for location in rev_parameters["population_locations"][0]:
            group = dose.filter_location(location, Populations[pop_name].agents)
            for x in range(len(group)//2):
                parents = []
                for i in range(2):
                    parents.append(random.choice(Populations[pop_name].agents))
                    while parents[i] not in group:
                        parents[i] = random.choice(Populations[pop_name].agents)
                    Populations[pop_name].agents.remove(parents[i])
                crossover_pt = random.randint(0, len(parents[0].genome[0].sequence))
                (new_chromo1, new_chromo2) = dose.genetic.crossover(parents[0].genome[0], 
                                                               parents[1].genome[0], 
                                                               crossover_pt)
                children = [dose.genetic.Organism([new_chromo1],
                                             rev_parameters["mutation_type"],
                                             rev_parameters["additional_mutation"]),
                            dose.genetic.Organism([new_chromo2],
                                             rev_parameters["mutation_type"],
                                             rev_parameters["additional_mutation"])]
                for child in children:
                    child.status['location'] = location
                    child.generate_name()
                    child.status['deme'] = pop_name
                    Populations[pop_name].agents.append(child)

    def postpopulation_control(self, Populations, pop_name): pass

    def generation_events(self, Populations, pop_name): pass

    def population_report(self, Populations, pop_name):
        report_list = []
        for organism in Populations[pop_name].agents:
            chromosome = ''.join(organism.genome[0].sequence)
            location = str(organism.status['location'])
            report_list.append(chromosome + '  ' + location)
        return '\n'.join(report_list)

    def database_report(self, con, cur, start_time, 
                        Populations, World, generation_count):
        try:
            dose.database_report_populations(con, cur, start_time, 
                                             Populations, generation_count)
        except: pass
        try:
            dose.database_report_world(con, cur, start_time, 
                                       World, generation_count)
        except: pass

    def deployment_scheme(self, Populations, pop_name, World): pass

dose.revive_simulation(rev_parameters, simulation_functions)