import numpy as np
import matplotlib.pyplot as plt
import agentpy as ap
import src.Model.model as battle_model
import src.Model.Sample_dict_model as sample

def animation_plot_single(m: battle_model.BattleModel, ax):
    ax.set_title(f"Boids Flocking Model t={m.t}")
    pos = m.battle_field.positions.values()
    colors = m.return_soldiers_colors()
    pos = np.array(list(pos)).T  # Transform
    ax.scatter(*pos, s=1, c=colors)
    ax.set_xlim(0, 300)
    ax.set_ylim(0, 300)
    ax.set_axis_off()

def animation_plot(m, p, steps):
    fig = plt.figure(figsize=(7,7))
    ax = fig.add_subplot(111)
    animation = ap.animate(m(p, steps=steps), fig, ax, animation_plot_single)
    animation.save('battle.gif', dpi=150, fps=3, writer='Pillow')


if __name__ == '__main__':
    animation_plot(battle_model.BattleModel, sample.sample_model2, 80)
