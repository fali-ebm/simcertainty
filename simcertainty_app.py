import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("simcertainty.app: Forest Plot Generator")

st.sidebar.header("Input Parameters")

# Input Y-axis labels
y_labels = st.sidebar.text_area("Enter outcome labels (one per line):", 
                                 value="ADR\nPDR\nSSLDR\nAdvanced ADR\nCancer\nDiminutive ADR").split("\n")

n = len(y_labels)

# Input point estimates and CIs
point_estimates = st.sidebar.text_input("Point Estimates (comma-separated):", "77,84,19,9,-2,65")
lower_bounds = st.sidebar.text_input("Lower Bounds (comma-separated):", "-6,54,9,2,-7,44")
upper_bounds = st.sidebar.text_input("Upper Bounds (comma-separated):", "181,118,31,17,7,88")

point_estimates = list(map(float, point_estimates.split(",")))
lower_bounds = list(map(float, lower_bounds.split(",")))
upper_bounds = list(map(float, upper_bounds.split(",")))

# Input x-axis thresholds
x_ticks = st.sidebar.text_input("X-axis Tick Marks (comma-separated):", "-135,-70,-27,0,27,70,135")
x_ticks = list(map(int, x_ticks.split(",")))

# Start plot
fig, ax = plt.subplots(figsize=(10, 6))

# Define colored regions
ax.axvspan(-200, -135, color='deeppink', alpha=0.2)
ax.axvspan(-135, -70, color='orange', alpha=0.2)
ax.axvspan(-70, -27, color='green', alpha=0.2)
ax.axvspan(27, 70, color='green', alpha=0.2)
ax.axvspan(70, 135, color='orange', alpha=0.2)
ax.axvspan(135, 200, color='deeppink', alpha=0.2)

# Plot data
y_pos = np.arange(n)
ax.errorbar(point_estimates, y_pos,
            xerr=[np.array(point_estimates) - np.array(lower_bounds), 
                  np.array(upper_bounds) - np.array(point_estimates)],
            fmt='o', color='black', ecolor='gray', capsize=5)

# Add CI values on each side of the bar
for i in range(n):
    ax.text(lower_bounds[i] - 5, y_pos[i], str(int(lower_bounds[i])), va='center', ha='right', fontsize=9, color='black')
    ax.text(upper_bounds[i] + 5, y_pos[i], str(int(upper_bounds[i])), va='center', ha='left', fontsize=9, color='black')

# Vertical reference line
ax.axvline(x=0, color='red', linestyle='--')

# Axis settings
ax.set_yticks(y_pos)
ax.set_yticklabels(y_labels)
ax.set_xticks(x_ticks)
ax.set_xlim(-200, 200)
ax.set_xlabel("Events per 1,000 individuals")
ax.set_title("simcertainty.app: Forest Plot of Event Rates with Colored Threshold Zones")
ax.invert_yaxis()
ax.grid(True, axis='x', linestyle='--', alpha=0.7)

# Show plot
st.pyplot(fig)
