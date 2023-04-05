from geneticalgorithm2 import geneticalgorithm2 as ga

def ga_lib(f, dim, varbound, max_inter, max_inter_sem_melhoria, pop_size, mut_prob, prob_crossover,
           percent_ultima_gen, cross_type = 'uniform',
           mut_type = 'uniform_by_center',
           select_type = 'tournament'):

    """
     cross_type: 'one_point', 'two_point', 'uniform', 'segment', 'shuffle'
     mut_type: 'uniform_by_x', 'uniform_by_center', 'gauss_by_x', 'gauss_by_center'
     select_type: 'fully_random', 'roulette', 'stochastic', 'sigma_scaling', 'ranking', 'linear_ranking', 'tournament'
    """
    model = ga(function=f, dimension = dim,
                    variable_type='real',
                    variable_boundaries = varbound,
                    algorithm_parameters={'max_num_iteration': max_inter,
                                           'population_size': pop_size,
                                           'mutation_probability':mut_prob,
                                           'elit_ratio': 0,
                                           'crossover_probability': prob_crossover,
                                           'parents_portion': percent_ultima_gen,
                                           'crossover_type':cross_type,
                                           'mutation_type': mut_type,
                                           'selection_type': select_type,
                                           'max_iteration_without_improv':max_inter_sem_melhoria}
                )
    model.run(no_plot=True,disable_printing=False,disable_progress_bar=False)
    xmin=model.output_dict['variable']
    return model, xmin