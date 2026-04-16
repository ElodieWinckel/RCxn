from parse_rdf_files import RDFParser
from visualize_networks import NetworkVisualizer
import matplotlib.pyplot as plt
from pathlib import Path

# Parse constructions
parser = RDFParser()
rdf_dir = Path('d:/PhD/RTG Project/1_Project work/RCxn/instance/Submissions/cc-project/CASA')
constructions = parser.parse_directory(rdf_dir)

# Generate CC distribution plot
vis = NetworkVisualizer()
fig = vis.plot_cc_distribution(constructions)
plt.savefig('17_cc_distribution_debug.png', dpi=300, bbox_inches='tight')
print('Saved 17_cc_distribution_debug.png')