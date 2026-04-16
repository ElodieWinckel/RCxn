# Comparative Concepts Analysis Strategy

## 1. Data Representation

### 1.1 Hierarchical Structure

```
Construction (File)
├── Slot_0 (e.g., engLME_ComparativeConstruction)
│   ├── CC_1 (type: cxn)
│   ├── CC_2 (type: sem)
│   └── CC_3 (type: str)
├── Slot_1 (e.g., engLME_ComparativeConstruction_1)
│   ├── CC_4 (type: cxn)
│   └── CC_5 (type: inf)
└── Slot_2
    └── ...
```

### 1.2 Data Model (Python Classes)

```python
class ComparativeConcept:
    - name: str (e.g., "comparative-relation")
    - type: str ("cxn", "sem", "str", "inf")

class Slot:
    - id: str (e.g., "ComparativeConstruction_1")
    - comparative_concepts: List[ComparativeConcept]
    
class Construction:
    - name: str (e.g., "engLME_ComparativeConstruction")
    - slots: Dict[str, Slot]
```

### 1.3 Storage Format

**Option A (Recommended): Pandas DataFrames**
- Fast, easy to filter and aggregate
- Good for tabular analysis
- Easy export to CSV/analysis tools

**Option B: NetworkX Graphs**
- Natural for graph representation
- Good for network analysis
- Better for visualization

**Hybrid Approach (Recommended):**
1. Parse RDF → Python objects
2. Convert to DataFrames for analysis
3. Build NetworkX graphs for visualization

---

## 2. Similarity Metrics (Multi-level)

### 2.1 Slot-to-Slot Similarity

Metrics to compute:

#### **A. Jaccard Index (Set-based)**
```
J(A, B) = |A ∩ B| / |A ∪ B|
```
Simple overlap of CC names, ignoring types.

#### **B. Weighted Jaccard (Type-aware)**
```
Similarity = Σ(weight[type_i] for shared CCs) / Σ(weight[type_i] for all CCs)
```
Types can have different weights:
- `cxn` (construction): weight 1.0 (most important)
- `sem` (semantic): weight 0.8
- `str` (structural): weight 0.6
- `inf` (information): weight 0.4

#### **C. Type Distribution Similarity**
```
Compare CC type distributions between slots:
- Slot_A: [cxn=3, sem=2, str=1, inf=0]
- Slot_B: [cxn=2, sem=3, str=2, inf=1]
Use cosine similarity on type vectors
```

#### **D. Combined Score (Recommended)**
```
Similarity = 0.5 × Jaccard + 0.3 × Weighted_Jaccard + 0.2 × Type_Distribution
```

### 2.2 Construction-to-Construction Similarity

#### **A. Slot-wise Comparison**
```
1. Compute slot pairs with highest similarity
2. Use optimal matching (Hungarian algorithm)
3. Aggregate slot similarities
```

#### **B. Global CC Profile Comparison**
```
1. Collect all CCs from all slots
2. Count CC occurrences
3. Use profile distance metrics (e.g., Hellinger distance)
```

#### **C. Type Profile Comparison**
```
Compare type distributions across entire construction
Type_Vector = [cxn_count, sem_count, str_count, inf_count]
Use cosine/Euclidean distance
```

### 2.3 Threshold Levels

Suggest edges in graph only if similarity > threshold:
- **High confidence**: threshold = 0.7
- **Medium confidence**: threshold = 0.5
- **Low confidence**: threshold = 0.3

---

## 3. Graph Design

### 3.1 Two-level Graphs

#### **Option A: Slot Graph**
- Nodes: All slots (e.g., ComparativeConstruction_0, ComparativeConstruction_1)
- Edges: Slot-to-slot similarity
- Attributes:
  - `construction`: Which construction the slot belongs to
  - `cc_count`: Number of CCs in slot
  - `type_profile`: Distribution of CC types

#### **Option B: Construction Graph**
- Nodes: Constructions only
- Edges: Construction-to-construction similarity
- Attributes:
  - `slot_count`: Number of slots
  - `avg_cc_count`: Average CCs per slot
  - `type_profile`: Overall type distribution

#### **Option C: Multilayer Graph (Recommended)**
- Layer 1: Construction level (10 nodes)
- Layer 2: Slot level (variable nodes per construction)
- Intra-layer edges: Similarities within level
- Inter-layer edges: Construction→slot containment relationships

### 3.2 Edge Attributes

```python
edge_attributes = {
    'weight': float,                    # Overall similarity (0-1)
    'jaccard': float,                   # Set overlap
    'weighted_jaccard': float,          # Type-aware overlap
    'type_similarity': float,           # Type distribution similarity
    'shared_ccs': List[str],            # Which CCs are shared
    'shared_cc_types': Dict[str, int],  # Count by type
    'confidence': str,                  # 'high', 'medium', 'low'
}
```

---

## 4. Implementation Roadmap

### Phase 1: Data Parsing & Preparation
1. Parse all .ttl files using rdflib
2. Extract constructions, slots, CCs
3. Create Python data objects
4. Store in DataFrames for analysis

### Phase 2: Similarity Computation
1. Implement Jaccard index
2. Implement weighted Jaccard (configurable weights)
3. Implement type distribution similarity
4. Batch compute all slot pairs
5. Aggregate to construction level

### Phase 3: Graph Construction
1. Build NetworkX graphs (slot-level and construction-level)
2. Add edge attributes
3. Apply threshold filtering
4. Export in multiple formats (GML, GraphML, JSON)

### Phase 4: Visualization & Analysis
1. Interactive visualizations (Plotly)
2. Static visualizations (Matplotlib)
3. Community detection analysis
4. Centrality analysis
5. Export analysis reports

---

## 5. Recommended Tools & Libraries

| Task | Library | Reason |
|------|---------|--------|
| RDF Parsing | `rdflib` | Standard for RDF/Turtle parsing |
| Data Analysis | `pandas`, `numpy` | Tabular data manipulation |
| Graph Analysis | `networkx` | Network algorithms, community detection |
| Visualization | `plotly` (interactive), `matplotlib` (static) | Interactive graphs for exploration |
| Matching | `scipy.optimize` | Hungarian algorithm for optimal slot matching |
| Metrics | `scipy.spatial.distance` | Distance metrics (cosine, Euclidean, etc.) |
| Statistics | `sklearn.metrics.pairwise` | Pre-built similarity metrics |

---

## 6. Expected Outputs

1. **CSV Files:**
   - `slot_similarity_matrix.csv` - All slot-to-slot similarities
   - `construction_similarity_matrix.csv` - Construction-to-construction similarities
   - `cc_inventory.csv` - Complete CC catalog with types

2. **Graph Files:**
   - `slot_network.graphml` - Slot-level graph
   - `construction_network.graphml` - Construction-level graph
   - `construction_network.json` - JSON format for web visualization

3. **Analysis Reports:**
   - Community detection results
   - Centrality analysis (degree, betweenness, closeness)
   - Top similar construction/slot pairs

4. **Visualizations:**
   - Interactive slot network plot
   - Interactive construction network plot
   - Similarity heatmaps
   - Type distribution charts

---

## 7. Configuration & Parameters

```python
# Weights for different CC types
CC_TYPE_WEIGHTS = {
    'cxn': 1.0,    # Construction (most important)
    'sem': 0.8,    # Semantic
    'str': 0.6,    # Structural
    'inf': 0.4,    # Information
}

# Similarity metric combination weights
SIMILARITY_WEIGHTS = {
    'jaccard': 0.5,
    'weighted_jaccard': 0.3,
    'type_distribution': 0.2,
}

# Threshold levels
THRESHOLDS = {
    'high': 0.7,
    'medium': 0.5,
    'low': 0.3,
}
```

---

## Next Steps

1. Run `parse_rdf_files.py` to extract data
2. Run `compute_similarity.py` to calculate metrics
3. Run `build_graphs.py` to construct network representations
4. Run `visualize_networks.py` for exploratory analysis
5. Run `analyze_results.py` for statistical insights
