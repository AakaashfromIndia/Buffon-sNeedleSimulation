import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.cm as cm

class BuffonNeedleSimulation:
    def __init__(self):
        self.line_spacing = 1.0
        self.stick_length = 1.0
        self.sticks = []
        self.num_sticks = 0
        self.num_crosses = 0
        self.pi_estimates = []
        self.stick_counts = []

    def drop_sticks(self, num_sticks, x_range, y_range):
        crosses = 0
        
        for _ in range(num_sticks):
            center_x = np.random.uniform(x_range[0], x_range[1])
            center_y = np.random.uniform(y_range[0], y_range[1])
            angle = np.random.uniform(0, np.pi)
            half_length = self.stick_length / 2.0
            cos_angle = np.cos(angle)
            sin_angle = np.sin(angle)
            x1 = center_x - half_length * cos_angle
            y1 = center_y - half_length * sin_angle
            x2 = center_x + half_length * cos_angle
            y2 = center_y + half_length * sin_angle
            actual_dx = x2 - x1
            actual_dy = y2 - y1
            actual_length = np.sqrt(actual_dx * actual_dx + actual_dy * actual_dy)
            
            if actual_length > 0:
                scale_factor = self.stick_length / actual_length
                final_dx = actual_dx * scale_factor
                final_dy = actual_dy * scale_factor
                x1 = center_x - final_dx / 2.0
                y1 = center_y - final_dy / 2.0
                x2 = center_x + final_dx / 2.0
                y2 = center_y + final_dy / 2.0
            
            if int(np.floor(x1)) != int(np.floor(x2)):
                crosses += 1
            
            self.sticks.append((x1, y1, x2, y2))
        
        self.num_sticks += num_sticks
        self.num_crosses += crosses
        
        if self.num_crosses > 0:
            pi_est = self.estimate_pi()
            if pi_est != float('inf'):
                self.pi_estimates.append(pi_est)
                self.stick_counts.append(self.num_sticks)

    def estimate_pi(self):
        if self.num_crosses == 0:
            return float('inf')
        return (2 * self.stick_length * self.num_sticks) / (self.line_spacing * self.num_crosses)

    def reset(self):
        self.sticks = []
        self.num_sticks = 0
        self.num_crosses = 0
        self.pi_estimates = []
        self.stick_counts = []

sim = BuffonNeedleSimulation()
fig = plt.figure(figsize=(18, 10))
ax1 = plt.axes([0.35, 0.55, 0.55, 0.40])
x_range = (0, 10)
y_range = (0, 4)
ax1.set_xlim(x_range)
ax1.set_ylim(y_range)
ax1.set_yticks([])
ax1.set_xticks(range(x_range[0], x_range[1] + 1))
ax1.set_title("Buffon's Needle Simulation", fontsize=16, weight='bold')
ax1.grid(True, alpha=0.3)

for i in range(x_range[0], x_range[1] + 1):
    ax1.axvline(i, color='black', linewidth=3, alpha=0.8)

ax2 = plt.axes([0.35, 0.05, 0.55, 0.40])
ax2.set_title("π Estimation Convergence", fontsize=16, weight='bold')
ax2.set_xlabel("Number of Sticks", fontsize=12)
ax2.set_ylabel("Estimated π", fontsize=12)
ax2.grid(True, alpha=0.3)
ax2.axhline(y=np.pi, color='crimson', linestyle='--', linewidth=2, 
            label=f'Actual π = {np.pi:.6f}', alpha=0.8)
ax2.legend()

sticks_plot = []
convergence_line = None
colormap = cm.get_cmap('viridis')

text_num_sticks = fig.text(0.02, 0.85, '', fontsize=12, weight='bold', color='navy')
text_num_crosses = fig.text(0.02, 0.82, '', fontsize=12, weight='bold', color='darkgreen')
text_pi_estimate = fig.text(0.02, 0.75, '', fontsize=12, weight='bold', color='darkred')
text_pi_actual = fig.text(0.02, 0.72, f'Actual π: {np.pi:.6f}', fontsize=11, weight='bold')
text_length_info = fig.text(0.02, 0.70, '', fontsize=10, color='purple')

instructions = fig.text(0.02, 0.5, 
    'Instructions:\n'
    '• Click +N buttons to drop N sticks\n'
    '• Each stick is exactly 1 unit long\n'
    '• Vertical lines are 1 unit apart\n'
    '• Watch π estimate converge\n'
    '• Use RESET to clear everything',
    fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))

reset_ax = plt.axes([0.02, 0.05, 0.12, 0.08])
button_reset = Button(reset_ax, 'RESET', color='orangered', hovercolor='darkred')

button_positions = [
    [0.02, 0.30, 0.08, 0.03],  
    [0.12, 0.30, 0.08, 0.03],  
    [0.22, 0.30, 0.08, 0.03],  
    [0.02, 0.26, 0.08, 0.03],  
    [0.12, 0.26, 0.08, 0.03],  
    [0.22, 0.26, 0.08, 0.03],  
    [0.02, 0.22, 0.08, 0.03],  
    [0.12, 0.22, 0.08, 0.03],  
]

stick_counts = [1, 5, 10, 50, 100, 500, 1000, 5000]
buttons = []

def update_display():
    global sticks_plot, convergence_line
    
    for stick_line in sticks_plot:
        stick_line.remove()
    sticks_plot = []
    
    num_sticks = len(sim.sticks)
    for i, (x1, y1, x2, y2) in enumerate(sim.sticks):
        color = colormap(i / max(1, num_sticks - 1)) if num_sticks > 1 else colormap(0.5)
        line, = ax1.plot([x1, x2], [y1, y2], color=color, linewidth=2.5, alpha=0.7)
        sticks_plot.append(line)
    
    if convergence_line:
        convergence_line.remove()
        convergence_line = None
    
    if len(sim.pi_estimates) > 0:
        convergence_line, = ax2.plot(sim.stick_counts, sim.pi_estimates, 
                                   color='mediumblue', marker='o', linewidth=2, 
                                   markersize=4, alpha=0.8, label='Estimated π')
        
        if sim.stick_counts:
            max_sticks = max(sim.stick_counts)
            if max_sticks <= 100:
                ax2.set_xlim(0, 100)
            elif max_sticks <= 1000:
                ax2.set_xlim(0, 1000)
            else:
                ax2.set_xlim(0, max_sticks * 1.1)
        
        current_estimates = sim.pi_estimates
        if current_estimates:
            y_min = min(min(current_estimates), np.pi - 0.5)
            y_max = max(max(current_estimates), np.pi + 0.5)
            ax2.set_ylim(y_min, y_max)
    
    if sim.sticks:
        lengths = []
        for x1, y1, x2, y2 in sim.sticks:
            length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            lengths.append(length)
        
        if lengths:
            min_len = min(lengths)
            max_len = max(lengths)
            variance = max_len - min_len
    else:
        text_length_info.set_text('')
    
    text_num_sticks.set_text(f'Total Sticks: {sim.num_sticks}')
    text_num_crosses.set_text(f'Line Crosses: {sim.num_crosses}')
    
    if sim.num_sticks > 0:
        pi_estimate = sim.estimate_pi()
        if pi_estimate != float('inf'):
            error = abs(pi_estimate - np.pi)
            text_pi_estimate.set_text(f'Estimated π: {pi_estimate:.6f}\nError: {error:.6f}')
        else:
            text_pi_estimate.set_text('Estimated π: No crosses yet')
    else:
        text_pi_estimate.set_text('Estimated π: ---')
    
    fig.canvas.draw_idle()

def drop_sticks_handler(event, count):
    sim.drop_sticks(count, x_range, y_range)
    update_display()

def reset_simulation(event):
    global convergence_line
    sim.reset()
    
    # Clear the convergence plot completely
    ax2.clear()
    ax2.set_title("π Estimation Convergence", fontsize=16, weight='bold')
    ax2.set_xlabel("Number of Sticks", fontsize=12)
    ax2.set_ylabel("Estimated π", fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=np.pi, color='crimson', linestyle='--', linewidth=2, 
                label=f'Actual π = {np.pi:.6f}', alpha=0.8)
    ax2.legend()
    
    # Reset the convergence line variable
    convergence_line = None
    
    update_display()

button_labels = ['+1', '+5', '+10', '+50', '+100', '+500', '+1K', '+5K']
button_colors = ['lightcyan', 'lightblue', 'lightsalmon', 'lightgreen', 
                'plum', 'khaki', 'peachpuff', 'lightpink']

for position, count, label, color in zip(button_positions, stick_counts, button_labels, button_colors):
    button_ax = plt.axes(position)
    button = Button(button_ax, label, color=color, hovercolor='gold')
    button.on_clicked(lambda event, c=count: drop_sticks_handler(event, c))
    buttons.append(button)

button_reset.on_clicked(reset_simulation)
update_display()
plt.tight_layout()
plt.show()
