# Quick Reference Guide: Comparative Concepts Analysis

## Getting Started (5 minutes)

### 1. Install Dependencies
```bash
cd "d:\PhD\RTG Project\1_Project work\RCxn"
python -m pip install --break-system-packages -r requirements_analysis.txt
```

### 2. Run Complete Analysis
```bash
python run_analysis.py
```

This generates 20+ analysis files in the current directory.

---

## Key Concepts

### Your Data Structure
```
10 RDF files (CASA constructions)
    ↓
Construction (e.g., engLME_ComparativeConstruction)
    ├─ Slot 0: cxn_comparative-construction, sem_comparative-relation, ...
    ├─ Slot 1: cxn_comparative-form, sem_comparative-degree, ...
    └─ Slot 2: sem_entity, sem_event, sem_comparee, ...
```

### Similarity Metric (What Makes Two Things Similar?)

**Example: Compare Slot A and Slot B**

| Aspect | Slot A | Slot B | Overlap |
|--------|--------|--------|---------|
| CCs | {comp-rel, comp-form, entity} | {comp-rel, comparee, entity} | comp-rel, entity |
| Types | cxn(1), sem(2) | sem(2), sem(1) | Different! |

**Similarity = 0.4 × Jaccard + 0.35 × Weighted_Jaccard + 0.25 × TypeDist**

- **Jaccard**: How many CCs in common? → 2/4 = 0.5
- **Weighted Jaccard**: Account for type importance → 0.55 (sem weights less)
- **Type Distribution**: Do they have same types? → 0.3 (one has more 'cxn')
- **Combined**: 0.4(0.5) + 0.35(0.55) + 0.25(0.3) = **0.46** (medium similarity)

### Thresholds
- **0.7-1.0**: Very similar (strong connection)
- **0.5-0.7**: Somewhat similar
- **0.3-0.5**: Weak similarity
- **< 0.3**: Minimal (usually excluded)

---

## Output Files Explained

### Data Files (Start Here)
- **01_construction_summary.csv** - Overview: how many slots/CCs per construction
- **02_slot_summary.csv** - Detailed breakdown of each slot
- **03_cc_inventory.csv** - Complete CC catalog (useful for understanding CC types)

### Similarity Results
- **04_slot_similarity_matrix.csv** - All vs all slot comparisons (large!)
- **05_construction_similarity_matrix.csv** - Small 10×10 matrix of construction pairs
- **06_top_similar_slot_pairs.csv** - Top 20 most similar slots
- **07_top_similar_construction_pairs.csv** - Top 20 most similar constructions ✓ **READ THIS FIRST**

### Network Files
- **08_construction_centrality.csv** - Most "central" (connected) constructions
- **10_construction_network.graphml** - Import to Cytoscape/Gephi
- **10_construction_network.json** - Web visualization format

### Visualizations
- **13_construction_network.png** - Network graph (nodes=constructions, edges=similarity)
- **14_similarity_heatmap.png** - Color matrix showing all similarities
- **17_cc_distribution.png** - Bar chart: how many CCs of each type per construction
- **18_construction_network_interactive.html** - **Recommended**: Open in browser, hover for details

### Reports
- **20_analysis_report.txt** - Human-readable summary of findings

---

## Interpretation Examples

### Example 1: Reading the Similarity Matrix

```csv
construction1,engLME_AdjectiveConstruction,engLME_ComparativeConstruction,engLME_PremodifierofAdjectiveConstruction
engLME_AdjectiveConstruction,1.0,0.65,0.48
engLME_ComparativeConstruction,0.65,1.0,0.72
engLME_PremodifierofAdjectiveConstruction,0.48,0.72,1.0
```

→ "ComparativeConstruction and PremodifierConstruction are most similar (0.72)"
→ "AdjectiveConstruction and ComparativeConstruction share moderate overlap (0.65)"

### Example 2: Top Similar Slot Pairs

```csv
item_a,item_b,similarity
(ComparativeConstruction, Slot_1),(MostLeastConstruction, Slot_1),0.82
(AdjectiveConstruction, Slot_0),(PremodifierConstruction, Slot_0),0.71
```

→ "Both constructions have similar Slot 1 structure"
→ "AdjectiveConstruction's core (Slot 0) resembles PremodifierConstruction's core"

### Example 3: Network Centrality

```csv
node,degree,betweenness_centrality
engLME_ComparativeConstruction,7,0.45
engLME_AdjectiveConstruction,5,0.12
```

→ "ComparativeConstruction connects to 7 others (highly interconnected)"
→ "ComparativeConstruction acts as 'bridge' between other constructions"

---

## Customization: Experiment with Parameters

### Change Type Weights

Edit `run_analysis.py`:

```python
config.CC_TYPE_WEIGHTS = {
    'cxn': 2.0,    # Make construction type MORE important
    'sem': 0.5,    # Make semantic type LESS important
    'str': 0.6,
    'inf': 0.4,
}
```

Then run: `python run_analysis.py`

### Change Similarity Threshold

```python
# Line in build_construction_graph()
cxn_graph = builder.build_construction_graph(constructions, threshold=0.5)
```

- Higher threshold (0.6-0.7): Keep only strongest connections
- Lower threshold (0.2-0.3): Include weaker connections

### Analyze Specific Constructions

```python
# In python console
from parse_rdf_files import RDFParser
parser = RDFParser()
constructions = parser.parse_directory("instance/Submissions/cc-project/CASA")

# Focus on one construction
cxn = constructions['engLME_ComparativeConstruction']
print(cxn)  # Shows slots and CCs
```

---

## Visualization Guide

### Open Files in Browsers/Software

| File | Software | Purpose |
|------|----------|---------|
| `.html` | Any browser | Interactive exploration (zoom, pan, hover) |
| `.graphml` | Cytoscape, Gephi | Publication-quality graphs |
| `.json` | d3.js, Sigma.js | Web integration |
| `.png` | Any image viewer | Static reports |
| `.csv` | Excel, R, Python | Statistical analysis |

### Recommended Workflow

1. **Quick overview**: Open `18_construction_network_interactive.html` in browser
2. **Detailed data**: Import `10_construction_network.graphml` to Cytoscape
3. **Statistical analysis**: Load CSVs into Python/R for further exploration
4. **Presentation**: Use PNG files in slides/papers

---

## Common Questions

### Q: What does "cxn_modification-construction" mean?

A: It's a Comparative Concept where:
- `cxn` = type (grammatical/construction)
- `modification-construction` = name (the specific concept)

The CC type tells you what level of linguistic description it belongs to.

### Q: Why is similarity 0.65 and not 1.0?

A: Constructions share *some* CCs and types, but not *all*. That's what makes them interesting - they're related but distinct.

Similarity < 1.0 means: "These constructions share patterns but also have unique features."

### Q: Can I increase the number of CCs analyzed?

A: The current analysis uses all CCs from all slots. You can't increase the count, but you can change weights to emphasize/de-emphasize certain types.

### Q: Which similarity threshold should I use?

A: It depends on your research question:
- **0.7+**: "Core similar constructions" (high confidence)
- **0.5-0.7**: "Related constructions" (medium)
- **0.3+**: "Distant relationships" (exploratory)

Start with 0.5 and adjust based on your findings.

---

## Troubleshooting

### "No module named 'X'"
**Solution**: Run `python -m pip install --break-system-packages -r requirements_analysis.txt`

### RDF files not found
**Solution**: Check path in `run_analysis.py` matches your installation
```python
rdf_dir = Path("your/actual/path/CASA")  # Adjust this
```

### Out of memory
**Solution**: Use higher threshold to reduce graph edges
```python
builder.build_construction_graph(constructions, threshold=0.6)
```

### Graphs look ugly/cluttered
**Solution**: Use Cytoscape/Gephi for better layouts
1. Export `.graphml`
2. Import to Cytoscape
3. Use Layout menu → Force-Directed Layout
4. Adjust node size, edge width, colors

---

## Next Steps

1. ✓ Run `python run_analysis.py`
2. ✓ Open `20_analysis_report.txt` for findings summary
3. ✓ Read `07_top_similar_construction_pairs.csv` for key insights
4. ✓ Visualize: `18_construction_network_interactive.html`
5. ✓ Dive deeper: Open `.graphml` in Cytoscape, customize layout
6. ✓ Experiment: Adjust parameters in `SimilarityConfig`, rerun analysis

---

## Files Created

**Quick Start (Read These):**
- `20_analysis_report.txt` - Main findings
- `07_top_similar_construction_pairs.csv` - Key relationships
- `18_construction_network_interactive.html` - Visual exploration

**For Detailed Analysis:**
- `05_construction_similarity_matrix.csv` - All pairwise similarities
- `08_construction_centrality.csv` - Importance rankings
- `10_construction_network.graphml` - For Cytoscape

**For Data Deep-Dive:**
- `01_construction_summary.csv` - Overview statistics
- `03_cc_inventory.csv` - Complete CC catalog

---

**Last Updated**: April 2025
