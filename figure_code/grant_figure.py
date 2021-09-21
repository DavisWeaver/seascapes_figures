from fears.classes.population_class import Population
import matplotlib.pyplot as plt
from fears.utils import plotter
import numpy as np

np.random.seed(10)

n_sims=10
options = {'n_sims':n_sims,
            # 'mut_rate':10**-9,
#            'plot':True,
            # 'death_rate':0.016,
            'k_abs':0.0008,
            'k_elim':0.0006,
            'max_dose':1000,
#            # 'death_rate':0,
#            'constant_pop':False,
            'curve_type':'pharm',
            'timestep_scale':2.5,
            'n_timestep':4000,
            'plot':False
#            'carrying_cap':True,
            # 'max_cells':10**11
            }

p_continuous = Population(**options)
p_discrete = Population(digital_seascape=True,mic_estimate = 0.2,**options)

p_continuous.simulate()
p_discrete.simulate()

fontsize=11
drug_kwargs = {'color':'black',
               'linewidth':2}
fig_digital, ax_digital = plt.subplots(2,1,figsize=(4,5))
ax_digital[0] = plotter.plot_fitness_curves(p_discrete,ax=ax_digital[0],
                                            show_legend=False,
                                            linewidth=2,
                                            labelsize=fontsize)

c = p_discrete.counts/np.max(p_discrete.counts)
p_discrete.drug_log_scale=True
ax_digital[1] = plotter.plot_timecourse_to_axes(p_discrete,
                                                c,
                                                ax_digital[1],
                                                drug_curve=p_discrete.drug_curve,
                                                linewidth=2,
                                                drug_kwargs=drug_kwargs,
                                                labelsize=fontsize,
                                                drug_ax_sci_notation=False)

fig_sea, ax_sea = plt.subplots(2,1,figsize=(4,5))
ax_sea[0] = plotter.plot_fitness_curves(p_continuous,ax=ax_sea[0],
                                            show_legend=False,
                                            linewidth=2,
                                            labelsize=fontsize)

c = p_continuous.counts/np.max(p_continuous.counts)
p_continuous.drug_log_scale=True
ax_sea[1] = plotter.plot_timecourse_to_axes(p_continuous,
                                                c,
                                                ax_sea[1],
                                                drug_curve=p_discrete.drug_curve,
                                                linewidth=2,
                                                drug_kwargs=drug_kwargs,
                                                labelsize=fontsize,
                                                drug_ax_sci_notation=False)