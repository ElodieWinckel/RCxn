"""
Similarity metrics for comparing slots and constructions

Implements multiple similarity measures accounting for:
- Set overlap (Jaccard)
- Type-aware weighting
- Type distribution similarity
"""

from typing import Dict, List, Tuple
import numpy as np
from scipy.spatial.distance import cosine
from scipy.optimize import linear_sum_assignment
import pandas as pd

from parse_rdf_files import Construction, Slot, ComparativeConcept


class SimilarityConfig:
    """Configuration for similarity calculations"""
    
    # Weights for different CC types (normalized)
    CC_TYPE_WEIGHTS = {
        'cxn': 1.0,
        'str': 1.0,
        'sem': 1.0,
        'inf': 1.0,
    }
    
    # How to combine different similarity measures
    METRIC_WEIGHTS = {
        'jaccard': 0.4,              # Set-based overlap
        'weighted_jaccard': 0.35,    # Type-aware overlap
        'type_distribution': 0.25,   # Type profile similarity
    }
    
    # Thresholds for edge inclusion
    THRESHOLDS = {
        'high_confidence': 0.7,
        'medium_confidence': 0.5,
        'low_confidence': 0.3,
    }


class SlotSimilarity:
    """Compute similarity between two slots"""
    
    def __init__(self, config: SimilarityConfig = None):
        self.config = config or SimilarityConfig()
    
    def jaccard_similarity(self, slot_a: Slot, slot_b: Slot) -> float:
        """
        Jaccard similarity: |A ∩ B| / |A ∪ B|
        Set-based comparison ignoring types
        """
        cc_names_a = slot_a.cc_names
        cc_names_b = slot_b.cc_names
        
        if len(cc_names_a | cc_names_b) == 0:
            return 0.0
        
        intersection = len(cc_names_a & cc_names_b)
        union = len(cc_names_a | cc_names_b)
        
        return intersection / union
    
    def weighted_jaccard_similarity(self, slot_a: Slot, slot_b: Slot) -> float:
        """
        Weighted Jaccard: accounts for CC type importance
        Uses configured weights for different CC types
        """
        # Create weighted sets: {cc: total_weight}
        weights_a = {}
        for cc in slot_a.comparative_concepts:
            weight = self.config.CC_TYPE_WEIGHTS.get(cc.type, 0.5)
            weights_a[cc.name] = weights_a.get(cc.name, 0) + weight
        
        weights_b = {}
        for cc in slot_b.comparative_concepts:
            weight = self.config.CC_TYPE_WEIGHTS.get(cc.type, 0.5)
            weights_b[cc.name] = weights_b.get(cc.name, 0) + weight
        
        # Intersection and union of CCs
        all_ccs = set(weights_a.keys()) | set(weights_b.keys())
        if len(all_ccs) == 0:
            return 0.0
        
        intersection_weight = sum(
            min(weights_a.get(cc, 0), weights_b.get(cc, 0))
            for cc in all_ccs
        )
        union_weight = sum(
            max(weights_a.get(cc, 0), weights_b.get(cc, 0))
            for cc in all_ccs
        )
        
        return intersection_weight / union_weight if union_weight > 0 else 0.0
    
    def type_distribution_similarity(self, slot_a: Slot, slot_b: Slot) -> float:
        """
        Cosine similarity between type distributions
        Compares CC type profiles: [cxn_count, sem_count, str_count, inf_count]
        """
        profile_a = slot_a.type_profile
        profile_b = slot_b.type_profile
        
        # Create vectors in consistent order
        types = ['cxn', 'sem', 'str', 'inf']
        vec_a = np.array([profile_a[t] for t in types], dtype=float)
        vec_b = np.array([profile_b[t] for t in types], dtype=float)
        
        # Normalize vectors (handle zero vectors)
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        vec_a = vec_a / norm_a
        vec_b = vec_b / norm_b
        
        # Cosine similarity
        return float(np.dot(vec_a, vec_b))
    
    def shared_ccs_info(self, slot_a: Slot, slot_b: Slot) -> Dict:
        """Get details about shared CCs"""
        ccs_a = {cc.name: cc.type for cc in slot_a.comparative_concepts}
        ccs_b = {cc.name: cc.type for cc in slot_b.comparative_concepts}
        
        shared = set(ccs_a.keys()) & set(ccs_b.keys())
        shared_by_type = {}
        
        for cc_name in shared:
            type_a = ccs_a[cc_name]
            type_b = ccs_b[cc_name]
            key = f"{type_a}-{type_b}" if type_a == type_b else f"{type_a}/{type_b}"
            shared_by_type[key] = shared_by_type.get(key, 0) + 1
        
        return {
            'shared_ccs': list(shared),
            'shared_count': len(shared),
            'shared_by_type': shared_by_type,
        }
    
    def compute_similarity(self, slot_a: Slot, slot_b: Slot) -> float:
        """
        Compute combined similarity score (0-1)
        Weighted combination of multiple metrics
        """
        jaccard = self.jaccard_similarity(slot_a, slot_b)
        weighted_jaccard = self.weighted_jaccard_similarity(slot_a, slot_b)
        type_dist = self.type_distribution_similarity(slot_a, slot_b)
        
        w = self.config.METRIC_WEIGHTS
        combined = (
            w['jaccard'] * jaccard +
            w['weighted_jaccard'] * weighted_jaccard +
            w['type_distribution'] * type_dist
        )
        
        return combined


class ConstructionSimilarity:
    """Compute similarity between two constructions"""
    
    def __init__(self, config: SimilarityConfig = None):
        self.config = config or SimilarityConfig()
        self.slot_sim = SlotSimilarity(config)
    
    def pairwise_slot_similarity(self, cxn_a: Construction, cxn_b: Construction) -> np.ndarray:
        """
        Create similarity matrix between slots of two constructions
        Rows: slots from cxn_a, Columns: slots from cxn_b
        """
        slots_a = list(cxn_a.slots.values())
        slots_b = list(cxn_b.slots.values())
        
        matrix = np.zeros((len(slots_a), len(slots_b)))
        
        for i, slot_a in enumerate(slots_a):
            for j, slot_b in enumerate(slots_b):
                matrix[i, j] = self.slot_sim.compute_similarity(slot_a, slot_b)
        
        return matrix
    
    def optimal_slot_matching(self, cxn_a: Construction, cxn_b: Construction) -> Tuple[float, np.ndarray]:
        """
        Find optimal matching between slots using Hungarian algorithm
        Returns: (average_similarity, assignment_matrix)
        """
        matrix = self.pairwise_slot_similarity(cxn_a, cxn_b)
        
        # Linear assignment maximizes sum, so use negative values
        row_ind, col_ind = linear_sum_assignment(-matrix)
        
        matched_similarity = matrix[row_ind, col_ind].sum() / max(len(row_ind), 1)
        
        return matched_similarity, matrix
    
    def global_cc_profile_similarity(self, cxn_a: Construction, cxn_b: Construction) -> float:
        """
        Compare global CC profiles
        Uses Jaccard similarity on all CCs across all slots
        """
        all_ccs_a = {cc.name for cc in cxn_a.all_ccs}
        all_ccs_b = {cc.name for cc in cxn_b.all_ccs}
        
        if len(all_ccs_a | all_ccs_b) == 0:
            return 0.0
        
        intersection = len(all_ccs_a & all_ccs_b)
        union = len(all_ccs_a | all_ccs_b)
        
        return intersection / union
    
    def type_profile_similarity(self, cxn_a: Construction, cxn_b: Construction) -> float:
        """
        Cosine similarity between construction-level type profiles
        """
        profile_a = cxn_a.type_profile
        profile_b = cxn_b.type_profile
        
        types = ['cxn', 'sem', 'str', 'inf']
        vec_a = np.array([profile_a[t] for t in types], dtype=float)
        vec_b = np.array([profile_b[t] for t in types], dtype=float)
        
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        vec_a = vec_a / norm_a
        vec_b = vec_b / norm_b
        
        return float(np.dot(vec_a, vec_b))
    
    def compute_similarity(self, cxn_a: Construction, cxn_b: Construction) -> float:
        """
        Compute combined construction similarity
        Averages multiple approaches
        """
        slot_matching = self.optimal_slot_matching(cxn_a, cxn_b)[0]
        cc_profile = self.global_cc_profile_similarity(cxn_a, cxn_b)
        type_profile = self.type_profile_similarity(cxn_a, cxn_b)
        
        # Equal weight to three approaches
        return (slot_matching + cc_profile + type_profile) / 3


class SimilarityAnalyzer:
    """Batch compute similarities and create results matrices"""
    
    def __init__(self, config: SimilarityConfig = None):
        self.config = config or SimilarityConfig()
        self.slot_sim = SlotSimilarity(config)
        self.cxn_sim = ConstructionSimilarity(config)
    
    def compute_slot_similarity_matrix(self, constructions: Dict[str, Construction]) -> pd.DataFrame:
        """
        Compute pairwise similarities for all slots
        Returns DataFrame with MultiIndex (cxn, slot) for rows/cols
        """
        # Collect all slots
        all_slots = []
        slot_labels = []
        
        for cxn_name in sorted(constructions.keys()):
            cxn = constructions[cxn_name]
            for slot_id in sorted(cxn.slots.keys()):
                all_slots.append(cxn.slots[slot_id])
                slot_labels.append((cxn_name, slot_id))
        
        n = len(all_slots)
        similarity_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i, n):
                sim = self.slot_sim.compute_similarity(all_slots[i], all_slots[j])
                similarity_matrix[i, j] = sim
                similarity_matrix[j, i] = sim
        
        # Create DataFrame
        df = pd.DataFrame(
            similarity_matrix,
            index=pd.MultiIndex.from_tuples(slot_labels, names=['construction', 'slot']),
            columns=pd.MultiIndex.from_tuples(slot_labels, names=['construction', 'slot'])
        )
        
        return df
    
    def compute_construction_similarity_matrix(self, constructions: Dict[str, Construction]) -> pd.DataFrame:
        """
        Compute pairwise similarities for all constructions
        """
        cxn_names = sorted(constructions.keys())
        n = len(cxn_names)
        
        similarity_matrix = np.zeros((n, n))
        
        for i, cxn_a_name in enumerate(cxn_names):
            for j, cxn_b_name in enumerate(cxn_names):
                if i == j:
                    similarity_matrix[i, j] = 1.0
                elif j > i:
                    sim = self.cxn_sim.compute_similarity(
                        constructions[cxn_a_name],
                        constructions[cxn_b_name]
                    )
                    similarity_matrix[i, j] = sim
                    similarity_matrix[j, i] = sim
        
        df = pd.DataFrame(
            similarity_matrix,
            index=cxn_names,
            columns=cxn_names
        )
        
        return df
    
    def get_top_similar_pairs(self, similarity_matrix: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
        """Extract top similar pairs from similarity matrix"""
        # Get upper triangle (avoid duplicates and self-similarity)
        results = []
        
        if isinstance(similarity_matrix.index, pd.MultiIndex):
            # Slot-level matrix
            pairs = similarity_matrix.values
            for i in range(len(similarity_matrix)):
                for j in range(i+1, len(similarity_matrix)):
                    results.append({
                        'item_a': similarity_matrix.index[i],
                        'item_b': similarity_matrix.index[j],
                        'similarity': pairs[i, j],
                    })
        else:
            # Construction-level matrix
            for i in range(len(similarity_matrix)):
                for j in range(i+1, len(similarity_matrix)):
                    results.append({
                        'item_a': similarity_matrix.index[i],
                        'item_b': similarity_matrix.columns[j],
                        'similarity': similarity_matrix.iloc[i, j],
                    })
        
        df = pd.DataFrame(results).sort_values('similarity', ascending=False)
        return df.head(top_n).reset_index(drop=True)


# Example usage
if __name__ == "__main__":
    from parse_rdf_files import RDFParser, DataProcessor
    from pathlib import Path
    
    # Parse constructions
    parser = RDFParser()
    rdf_dir = Path("d:/PhD/RTG Project/1_Project work/RCxn/instance/Submissions/cc-project/CASA")
    constructions = parser.parse_directory(rdf_dir)
    
    print(f"Analyzing {len(constructions)} constructions...\n")
    
    # Compute similarities
    analyzer = SimilarityAnalyzer()
    
    print("Computing slot-level similarities...")
    slot_sim_matrix = analyzer.compute_slot_similarity_matrix(constructions)
    slot_sim_matrix.to_csv('slot_similarity_matrix.csv')
    print(f"  Slot matrix shape: {slot_sim_matrix.shape}")
    
    print("\nComputing construction-level similarities...")
    cxn_sim_matrix = analyzer.compute_construction_similarity_matrix(constructions)
    cxn_sim_matrix.to_csv('construction_similarity_matrix.csv')
    print(f"  Construction matrix shape: {cxn_sim_matrix.shape}")
    
    # Top similar pairs
    print("\nTop 15 most similar slot pairs:")
    top_slots = analyzer.get_top_similar_pairs(slot_sim_matrix, top_n=15)
    print(top_slots.to_string())
    top_slots.to_csv('top_similar_slot_pairs.csv', index=False)
    
    print("\nTop 15 most similar construction pairs:")
    top_cxns = analyzer.get_top_similar_pairs(cxn_sim_matrix, top_n=15)
    print(top_cxns.to_string())
    top_cxns.to_csv('top_similar_construction_pairs.csv', index=False)
    
    print("\n[SUCCESS] Similarity analysis complete")
