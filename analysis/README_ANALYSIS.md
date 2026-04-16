# Comparative Concepts Analysis Pipeline

Complete analysis framework for studying similarity relationships between linguistic constructions based on shared comparative concepts (CCs).

## Overview

This pipeline analyzes 10 RDF/TTL files representing grammatical constructions from an adjective–adverb subset. It:

1. **Parses** RDF files and extracts construction → slot → comparative concept hierarchy
2. **Computes** multi-level similarity metrics (slots & constructions)
3. **Builds** weighted network graphs
4. **Analyzes** network structure (centrality, communities, statistics)
5. **Visualizes** relationships using static and interactive plots

## Project Structure

```
├── ANALYSIS_STRATEGY.md              # Detailed strategy document
├── parse_rdf_files.py                # RDF parser (Phase 1)
├── compute_similarity.py             # Similarity metrics (Phase 2)
├── build_graphs.py                   # Graph construction (Phase 3)
├── visualize_networks.py             # Visualization & analysis (Phase 4)
├── run_analysis.py                   # Main pipeline script
├── requirements_analysis.txt         # Python dependencies
└── README.md                         # This file
```

## Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements_analysis.txt
```

### Step 2: Verify RDF Files

Ensure the following directory exists with 10 `_compcon.ttl` files:
```
instance/Submissions/cc-project/CASA/
```

## Usage

### Quick Start (Recommended)

Run the complete analysis pipeline with one command:

```bash
python run_analysis.py
```

This will execute all 7 phases and generate 20+ output files.

### Custom Analysis (Advanced)

For more control, run modules individually:

```python
from parse_rdf_files import RDFParser
from compute_similarity import SimilarityAnalyzer
from build_graphs import GraphBuilder, NetworkAnalyzer

# 1. Parse RDF files
parser = RDFParser()
constructions = parser.parse_directory("path/to/CASA")

# 2. Compute similarities
analyzer = SimilarityAnalyzer()
slot_sim = analyzer.compute_slot_similarity_matrix(constructions)
cxn_sim = analyzer.compute_construction_similarity_matrix(constructions)

# 3. Build graphs
builder = GraphBuilder()
cxn_graph = builder.build_construction_graph(constructions, threshold=0.3)

# 4. Analyze networks
net_analyzer = NetworkAnalyzer()
centrality = net_analyzer.compute_centrality_measures(cxn_graph)
```

## Data Structure

### Input Format (RDF/Turtle)

```turtle
@prefix compcon: <https://...#> .
@prefix cx: <http://example.org/cx/> .

cx:engLME_Construction compcon:hasCompCon 
    compcon:cxn_type1 , compcon:sem_type2 , compcon:str_type3 .

cx:engLME_Construction_1 compcon:hasCompCon 
    compcon:inf_ref , compcon:cxn_form .
```

### Parsed Data Model

```
Construction
├── name: str (e.g., "engLME_ComparativeConstruction")
├── slots: Dict[slot_id → Slot]
│   ├── Slot(id, construction_name)
│   │   ├── comparative_concepts: List[ComparativeConcept]
│   │   │   └── ComparativeConcept(name, type)
│   │   │       type ∈ {'cxn', 'sem', 'str', 'inf'}
```

## Similarity Metrics

### Slot-to-Slot Similarity (Three-Part Combined Score)

1. **Jaccard Index** (40% weight)
   - Set-based overlap of CC names
   - Formula: |A ∩ B| / |A ∪ B|

2. **Weighted Jaccard** (35% weight)
   - Accounts for CC type importance
   - Weights: cxn=1.0, sem=0.8, str=0.6, inf=0.4
   - Formula: Σ(min weights) / Σ(max weights)

3. **Type Distribution Similarity** (25% weight)
   - Cosine similarity of type profiles
   - Compares: [cxn_count, sem_count, str_count, inf_count]

**Combined Score**: 
```
similarity = 0.4 × jaccard + 0.35 × weighted_jaccard + 0.25 × type_distribution
```

### Construction-to-Construction Similarity (Averaged Approaches)

1. **Optimal Slot Matching** (Hungarian Algorithm)
   - Finds best correspondence between slots
   
2. **Global CC Profile Comparison**
   - Jaccard on all CCs across all slots
   
3. **Type Distribution Comparison**
   - Cosine similarity of aggregate type profiles

**Combined Score**:
```
similarity = (slot_matching + cc_profile + type_profile) / 3
```

## Output Files

### Data Summaries
- `01_construction_summary.csv` - Overview of each construction
- `02_slot_summary.csv` - Detailed slot information
- `03_cc_inventory.csv` - Complete list of all CCs

### Similarity Matrices
- `04_slot_similarity_matrix.csv` - All slot-to-slot similarities
- `05_construction_similarity_matrix.csv` - Construction-to-construction similarities
- `06_top_similar_slot_pairs.csv` - Top 20 similar slot pairs
- `07_top_similar_construction_pairs.csv` - Top 20 similar construction pairs

### Network Analysis
- `08_construction_centrality.csv` - Centrality measures (degree, betweenness, closeness, eigenvector)
- `09_slot_centrality.csv` - Slot-level centrality measures
- `10_construction_network.graphml` - Cytoscape/Gephi format
- `10_construction_network.json` - Web visualization format
- `11_construction_adjacency.csv` - Adjacency matrix
- `12_slot_network.graphml` - Slot network graph
- `12_slot_network.json` - Slot network JSON

### Visualizations
- `13_construction_network.png` - Network graph visualization
- `14_similarity_heatmap.png` - Similarity matrix heatmap
- `15_degree_distribution.png` - Degree distribution histogram
- `16_weight_distribution.png` - Edge weight distribution
- `17_cc_distribution.png` - CC type distribution across constructions
- `18_construction_network_interactive.html` - Interactive network (requires Plotly)
- `19_similarity_heatmap_interactive.html` - Interactive heatmap (requires Plotly)

### Reports
- `20_analysis_report.txt` - Text summary of findings

## Configuration

Edit `run_analysis.py` or use `SimilarityConfig` class to modify:

```python
class SimilarityConfig:
    CC_TYPE_WEIGHTS = {
        'cxn': 1.0,    # Most important
        'sem': 0.8,
        'str': 0.6,
        'inf': 0.4,    # Least important
    }
    
    METRIC_WEIGHTS = {
        'jaccard': 0.4,
        'weighted_jaccard': 0.35,
        'type_distribution': 0.25,
    }
    
    THRESHOLDS = {
        'high_confidence': 0.7,
        'medium_confidence': 0.5,
        'low_confidence': 0.3,
    }
```

## Interpreting Results

### Similarity Scores

- **0.7-1.0 (High)**: Constructions share significant CC overlap with consistent type patterns
- **0.5-0.7 (Medium)**: Moderate similarity with some shared CCs
- **0.3-0.5 (Low)**: Weak similarity, useful for detecting distant relationships
- **0.0-0.3**: Minimal similarity, often filtered out

### Network Metrics

**Centrality Measures**:
- **Degree**: Number of connections (basic connectivity)
- **Betweenness**: Acts as bridge between other constructions
- **Closeness**: Average distance to all other constructions
- **Eigenvector**: Importance based on connections to important nodes

**Network Density**: 
- Low (< 0.3): Sparse, modular structure
- Medium (0.3-0.7): Mixed structure
- High (> 0.7): Densely connected

**Communities**:
Groups of highly interconnected constructions that share CC patterns

## Visualization Tools

### Static Plots (PNG)
- Generated automatically by `run_analysis.py`
- High quality (300 dpi)
- Good for reports and papers

### Interactive Visualizations (HTML)
- Open in web browser
- Zoom, pan, hover for details
- Requires Plotly library

### Network Visualization Software
- **Cytoscape** (Free, recommended)
  - Import `.graphml` or `.json` files
  - Customize layouts, colors, sizes
  
- **Gephi** (Free)
  - Import `.graphml` files
  - Advanced layout algorithms
  - Community detection visualization

- **Sigma.js** (Web-based, free)
  - Import `.json` files
  - Web-based graph visualization

## Advanced Features

### 1. Experimenting with Thresholds

```python
for threshold in [0.2, 0.3, 0.4, 0.5]:
    graph = builder.build_construction_graph(constructions, threshold=threshold)
    print(f"Threshold {threshold}: {graph.number_of_edges()} edges")
```

### 2. Custom Similarity Metrics

Extend `SimilarityAnalyzer` to implement custom metrics:

```python
class CustomSimilarity(SlotSimilarity):
    def custom_metric(self, slot_a, slot_b):
        # Your custom metric here
        pass
```

### 3. Subgraph Analysis

```python
# Extract specific community or subset
subgraph = cxn_graph.subgraph(nodes_of_interest)
nx.write_graphml(subgraph, 'subgraph.graphml')
```

### 4. Statistical Testing

```python
import scipy.stats as stats

# Test if similarity is significantly different
similar_pairs = [0.8, 0.75, 0.72]
dissimilar_pairs = [0.2, 0.15, 0.18]

t_stat, p_value = stats.ttest_ind(similar_pairs, dissimilar_pairs)
```

## Troubleshooting

### Issue: "No module named 'rdflib'"
**Solution**: Install dependencies: `pip install -r requirements_analysis.txt`

### Issue: RDF files not found
**Solution**: Check path in `run_analysis.py` matches your directory structure
```python
rdf_dir = Path("your/actual/path/to/CASA")
```

### Issue: Out of memory for large graphs
**Solution**: Use higher thresholds to reduce edge count
```python
threshold = 0.5  # Keep only strongest similarities
```

### Issue: Plotly visualizations not generating
**Solution**: Install Plotly (optional)
```bash
pip install plotly
```

## Performance Notes

- **Parsing**: ~1 second for 10 files
- **Similarity computation**: ~2 seconds
- **Graph building**: Depends on threshold (usually < 1 second)
- **Visualization**: ~5-10 seconds

Total runtime: < 30 seconds for complete analysis

## References & Further Reading

### CC Type Meanings
- **cxn** (construction): Grammatical/construction-level patterns
- **sem** (semantic): Meaning and semantic roles
- **str** (structural): Syntactic structure and relationships
- **inf** (information): Information structure and packaging

### Graph Theory Concepts
- **Centrality**: Measures node importance in network
- **Community Detection**: Finding groups of similar nodes
- **Network Density**: Proportion of possible connections present
- **Scale-free networks**: Natural language networks often show this property

## Citation

If you use this pipeline in your research, please cite:

```bibtex
@software{cc_analysis_2025,
  title={Comparative Concepts Analysis Pipeline},
  author={[Your Name]},
  year={2025},
  url={https://your-repo-url}
}
```

## License

[Your License Here]

## Support

For issues, questions, or suggestions:
1. Check ANALYSIS_STRATEGY.md for detailed explanations
2. Review example code in `run_analysis.py`
3. Check inline documentation in source files
4. Experiment with configuration settings

## Version History

- **v1.0** (2025): Initial release
  - RDF parsing
  - 3-part similarity metric
  - Network analysis
  - Visualization suite

---

**Last Updated**: April 16, 2025
