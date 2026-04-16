
import matplotlib.pyplot as plt
from parse_rdf_files import RDFParser
from pathlib import Path

# Parse constructions
parser = RDFParser()
rdf_dir = Path('d:/PhD/RTG Project/1_Project work/RCxn/instance/Submissions/cc-project/CASA')
constructions = parser.parse_directory(rdf_dir)

# Create broken version manually (simulating the old buggy DataFrame approach)
construction_names = []
cxn_counts = []
sem_counts = []
str_counts = []
inf_counts = []

for cxn_name, cxn in constructions.items():
    display_name = cxn_name.replace('engLME_', '')
    construction_names.append(display_name)
    
    profile = cxn.type_profile
    cxn_counts.append(profile.get('cxn', 0))
    sem_counts.append(profile.get('sem', 0))
    str_counts.append(profile.get('str', 0))
    inf_counts.append(profile.get('inf', 0))

# Create the BROKEN version - CXN bars will be hidden under other bars
fig, ax = plt.subplots(figsize=(14, 6))

# This is the BROKEN stacking - CXN bars get drawn first but then overwritten
ax.bar(construction_names, cxn_counts, label='CXN', color='#3498db', alpha=0.8)
ax.bar(construction_names, sem_counts, label='SEM', color='#e74c3c', alpha=0.8)  # Overwrites CXN
ax.bar(construction_names, str_counts, label='STR', color='#2ecc71', alpha=0.8)  # Overwrites SEM
ax.bar(construction_names, inf_counts, label='INF', color='#f39c12', alpha=0.8)  # Overwrites STR

plt.xlabel('Construction', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.title('CC Type Distribution across Constructions (BROKEN VERSION - CXN bars hidden)', fontsize=14, fontweight='bold')
plt.legend(title='CC Type')
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()

plt.savefig('17_cc_distribution_broken_version.png', dpi=300, bbox_inches='tight')
print('Saved broken version: 17_cc_distribution_broken_version.png')
