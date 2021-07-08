from fears.utils import results_manager, plotter
import os
import numpy as np
import matplotlib.pyplot as plt

fig,ax = plt.subplots(figsize=(4,7.75))

data_folder = 'results_07082021_0001'
exp_info_file = 'experiment_info_07082021_0001.p'
exp_folders,exp_info = results_manager.get_experiment_results(data_folder,
                                                             exp_info_file)
max_cells = exp_info.populations[0].max_cells
n_sims = exp_info.n_sims
k_abs = exp_info.slopes
barchart_data = np.ones(len(k_abs))*100

# make a dummy barchart
x = np.arange(len(k_abs))
rects = ax.barh(x,barchart_data,color='slategrey',facecolor='w')

tc_axes = []
drug_axes = []

for exp in exp_folders:
    k_abs_t = exp[exp.find('=')+1:]
    k_abs_t = float(k_abs_t)
    num = np.argwhere(k_abs == k_abs_t)
    num = num[0,0]
    
    # generate timecourse axes
    
    width = 100
    height = rects.patches[num].get_height()
    ypos = rects.patches[num].get_y()
    xpos = 120
    
    tcax = ax.inset_axes([xpos,ypos,width,height],transform=ax.transData)
    # da = tcax.twinx()
    
    sim_files = os.listdir(path=exp)
    sim_files = sorted(sim_files)
    survive_count = 0
    counts_total = None
    
    for sim in sim_files:
        sim = exp + os.sep + sim
        data = results_manager.get_data(sim)
        dc = data[:,-1]
        data = data[:,0:-1]
        data_t = data[-1,:]
        
        # check to see if any genotypes are at least 10% of the max cell count
        if any(data_t >= 0.1*max_cells):
            survive_count += 1
            if counts_total is None:
                counts_total = data
            else:
                counts_total += data
        data = data/np.max(data)
        
        tcax,drug_ax = plotter.plot_timecourse_to_axes(exp_info.populations[num],
                                                    data,
                                                    tcax,
                                                    drug_curve=dc,
                                                    grayscale=True,
                                                    color='gray',
                                                    linewidth=1,
                                                    # alpha=0.5
                                                    )
        drug_ax.set_ylim(0,10**4)
        drug_ax.set_ylabel('')
        
    if survive_count > 0:
        counts_avg = counts_total/survive_count
        counts_avg = counts_avg/np.max(counts_avg)        
        tcax,temp = plotter.plot_timecourse_to_axes(exp_info.populations[num],
                                               counts_avg,
                                               tcax)
    
    # t = np.arange(len(dc))
    # t = t*exp_info.populations[0].timestep_scale/24
    # da.plot(t,dc)
    
    tc_axes.append( tcax )
    barchart_data[num] = survive_count   

rects = ax.barh(x,barchart_data,color='slategrey')
ax.set_xlabel('% Resistant',fontsize=12)
ax.set_ylabel('$k_{abs}$',fontsize=15)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)