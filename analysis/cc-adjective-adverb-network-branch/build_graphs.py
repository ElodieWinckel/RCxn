"""
Graph construction and network analysis

Builds NetworkX graphs at multiple levels with similarity-based edges
"""

from typing import Dict, Tuple
import networkx as nx
import pandas as pd
import json
from pathlib import Path

from parse_rdf_files import Construction
from compute_similarity import SimilarityAnalyzer, SimilarityConfig


class GraphBuilder:
    """Build NetworkX graphs from construction data"""
    
    def __init__(self, config: SimilarityConfig = None):
        self.config = config or SimilarityConfig()
        self.analyzer = SimilarityAnalyzer(config)
    
    def build_slot_graph(self, constructions: Dict[str, Construction], 
                        threshold: float = 0.3) -> nx.Graph:
        """
        Build slot-level graph
        - Nodes: All slots
        - Edges: Slot pairs with similarity >= threshold
        """
        G = nx.Graph()
        
        # Add nodes with attributes
        for cxn_name, cxn in constructions.items():
            for slot_id, slot in cxn.slots.items():
                node_id = f"{cxn_name}#{slot_id}"
                G.add_node(node_id, 
                          construction=cxn_name,
                          slot_id=slot_id,
                          cc_count=slot.cc_count,
                          type_profile=slot.type_profile)
        
        # Add edges based on similarity
        slot_sim_matrix = self.analyzer.compute_slot_similarity_matrix(constructions)
        
        for i, idx_i in enumerate(slot_sim_matrix.index):
            for j, idx_j in enumerate(slot_sim_matrix.columns):
                if i < j:
                    sim = slot_sim_matrix.iloc[i, j]
                    if sim >= threshold:
                        cxn_a, slot_a = idx_i
                        cxn_b, slot_b = idx_j
                        
                        node_a = f"{cxn_a}#{slot_a}"
                        node_b = f"{cxn_b}#{slot_b}"
                        
                        G.add_edge(node_a, node_b,
                                  weight=sim,
                                  confidence=self._get_confidence(sim))
        
        return G
    
    def build_construction_graph(self, constructions: Dict[str, Construction],
                                threshold: float = 0.3) -> nx.Graph:
        """
        Build construction-level graph
        - Nodes: Constructions
        - Edges: Construction pairs with similarity >= threshold
        """
        G = nx.Graph()
        
        # Add nodes with attributes
        for cxn_name, cxn in constructions.items():
            G.add_node(cxn_name,
                      slot_count=cxn.slot_count,
                      cc_count=cxn.cc_count,
                      avg_ccs_per_slot=cxn.avg_ccs_per_slot,
                      type_profile=cxn.type_profile)
        
        # Add edges based on similarity
        cxn_sim_matrix = self.analyzer.compute_construction_similarity_matrix(constructions)
        
        cxn_names = list(constructions.keys())
        for i, cxn_a_name in enumerate(cxn_names):
            for j, cxn_b_name in enumerate(cxn_names):
                if i < j:
                    sim = cxn_sim_matrix.loc[cxn_a_name, cxn_b_name]
                    if sim >= threshold:
                        G.add_edge(cxn_a_name, cxn_b_name,
                                  weight=sim,
                                  confidence=self._get_confidence(sim))
        
        return G
    
    def build_multilayer_graph(self, constructions: Dict[str, Construction],
                              slot_threshold: float = 0.3,
                              cxn_threshold: float = 0.3) -> Dict[str, nx.Graph]:
        """
        Build multilayer graph with construction and slot layers
        """
        return {
            'construction': self.build_construction_graph(constructions, cxn_threshold),
            'slot': self.build_slot_graph(constructions, slot_threshold),
        }
    
    @staticmethod
    def _get_confidence(similarity: float) -> str:
        """Classify similarity into confidence level"""
        if similarity >= 0.7:
            return 'high'
        elif similarity >= 0.5:
            return 'medium'
        else:
            return 'low'


class NetworkAnalyzer:
    """Analyze network properties and structure"""
    
    @staticmethod
    def compute_centrality_measures(G: nx.Graph) -> pd.DataFrame:
        """
        Compute multiple centrality measures for all nodes
        """
        degree_centrality = nx.degree_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G, weight='weight')
        closeness_centrality = nx.closeness_centrality(G, distance='weight')
        
        # For weighted graphs, eigenvector centrality may require special handling
        try:
            eigenvector_centrality = nx.eigenvector_centrality(G, weight='weight', max_iter=1000)
        except:
            eigenvector_centrality = {node: 0.0 for node in G.nodes()}
        
        results = []
        for node in G.nodes():
            results.append({
                'node': node,
                'degree': G.degree(node),
                'weighted_degree': sum(d['weight'] for _, d in G[node].items()),
                'degree_centrality': degree_centrality[node],
                'betweenness_centrality': betweenness_centrality[node],
                'closeness_centrality': closeness_centrality[node],
                'eigenvector_centrality': eigenvector_centrality.get(node, 0.0),
            })
        
        return pd.DataFrame(results).sort_values('betweenness_centrality', ascending=False)
    
    @staticmethod
    def detect_communities(G: nx.Graph) -> Dict[int, list]:
        """
        Detect communities using modularity-based algorithm
        """
        try:
            from networkx.algorithms import community
            communities_generator = community.louvain_communities(G, weight='weight', seed=42)
            
            communities_dict = {}
            for i, comm in enumerate(communities_generator):
                communities_dict[i] = list(comm)
            
            return communities_dict
        except ImportError:
            print("Warning: Community detection requires python-louvain or higher networkx version")
            return {}
    
    @staticmethod
    def get_network_stats(G: nx.Graph) -> Dict:
        """Get overall network statistics"""
        return {
            'num_nodes': G.number_of_nodes(),
            'num_edges': G.number_of_edges(),
            'density': nx.density(G),
            'is_connected': nx.is_connected(G),
            'num_components': nx.number_connected_components(G),
            'average_clustering': nx.average_clustering(G) if G.number_of_nodes() > 0 else 0,
        }
    
    @staticmethod
    def get_edge_statistics(G: nx.Graph) -> pd.DataFrame:
        """Get statistics on edges (weights, confidence levels)"""
        edges_data = []
        for u, v, data in G.edges(data=True):
            edges_data.append({
                'node_a': u,
                'node_b': v,
                'weight': data.get('weight', 0),
                'confidence': data.get('confidence', 'unknown'),
            })
        
        df = pd.DataFrame(edges_data)
        
        if len(df) > 0:
            summary = {
                'total_edges': len(df),
                'avg_weight': df['weight'].mean(),
                'min_weight': df['weight'].min(),
                'max_weight': df['weight'].max(),
                'high_confidence': len(df[df['confidence'] == 'high']),
                'medium_confidence': len(df[df['confidence'] == 'medium']),
                'low_confidence': len(df[df['confidence'] == 'low']),
            }
            return df, summary
        else:
            return df, {}


class GraphExporter:
    """Export graphs to various formats"""
    
    @staticmethod
    def export_graphml(G: nx.Graph, filepath: str):
        """Export to GraphML format (compatible with Cytoscape, Gephi)"""
        def sanitize_value(value):
            if isinstance(value, (list, tuple)):
                return json.dumps(value)
            return value

        def flatten_attrs(attrs: dict) -> dict:
            flattened = {}
            for key, value in attrs.items():
                if key == 'type_profile' and isinstance(value, dict):
                    for subtype, count in value.items():
                        flattened[f'type_profile_{subtype}'] = count
                elif isinstance(value, dict):
                    flattened[key] = json.dumps(value)
                else:
                    flattened[key] = sanitize_value(value)
            return flattened

        try:
            H = G.__class__()
            H.graph.update(flatten_attrs(G.graph))

            for node, attrs in G.nodes(data=True):
                sanitized_attrs = flatten_attrs(attrs)
                H.add_node(node, **sanitized_attrs)

            for u, v, attrs in G.edges(data=True):
                sanitized_attrs = flatten_attrs(attrs)
                H.add_edge(u, v, **sanitized_attrs)

            nx.write_graphml(H, filepath)
            print(f"  Exported to {filepath}")
        except ImportError:
            print(f"  ⚠ Skipping GraphML export (requires lxml): pip install lxml")
        except Exception as e:
            print(f"  ⚠ Error exporting GraphML: {e}")
    
    @staticmethod
    def export_gexf(G: nx.Graph, filepath: str):
        """Export to GEXF format"""
        try:
            nx.write_gexf(G, filepath)
            print(f"  Exported to {filepath}")
        except Exception as e:
            print(f"  ⚠ Error exporting GEXF: {e}")
    
    @staticmethod
    def export_json(G: nx.Graph, filepath: str):
        """Export to JSON format for web visualization"""
        try:
            data = nx.node_link_data(G)
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"  Exported to {filepath}")
        except Exception as e:
            print(f"  ⚠ Error exporting JSON: {e}")
    
    @staticmethod
    def export_adjacency_matrix(G: nx.Graph, filepath: str):
        """Export adjacency matrix to CSV"""
        try:
            adj_matrix = nx.to_pandas_adjacency(G, weight='weight')
            adj_matrix.to_csv(filepath)
            print(f"  Exported to {filepath}")
        except Exception as e:
            print(f"  ⚠ Error exporting adjacency matrix: {e}")


# Example usage
if __name__ == "__main__":
    from parse_rdf_files import RDFParser
    
    # Parse constructions
    print("Parsing RDF files...")
    parser = RDFParser()
    rdf_dir = "d:/PhD/RTG Project/1_Project work/RCxn/instance/Submissions/cc-project/CASA"
    constructions = parser.parse_directory(rdf_dir)
    
    # Build graphs
    print("\nBuilding graphs...")
    builder = GraphBuilder()
    
    # Construction-level graph
    print("  Building construction graph...")
    cxn_graph = builder.build_construction_graph(constructions, threshold=0.3)
    print(f"    Nodes: {cxn_graph.number_of_nodes()}, Edges: {cxn_graph.number_of_edges()}")
    
    # Slot-level graph
    print("  Building slot graph...")
    slot_graph = builder.build_slot_graph(constructions, threshold=0.3)
    print(f"    Nodes: {slot_graph.number_of_nodes()}, Edges: {slot_graph.number_of_edges()}")
    
    # Analyze networks
    print("\nAnalyzing networks...")
    analyzer = NetworkAnalyzer()
    
    print("\nConstruction-level statistics:")
    cxn_stats = analyzer.get_network_stats(cxn_graph)
    for key, value in cxn_stats.items():
        print(f"  {key}: {value}")
    
    print("\nConstruction centrality measures:")
    cxn_centrality = analyzer.compute_centrality_measures(cxn_graph)
    print(cxn_centrality.to_string())
    cxn_centrality.to_csv('construction_centrality.csv', index=False)
    
    print("\nSlot-level statistics:")
    slot_stats = analyzer.get_network_stats(slot_graph)
    for key, value in slot_stats.items():
        print(f"  {key}: {value}")
    
    print("\nSlot centrality measures (top 20):")
    slot_centrality = analyzer.compute_centrality_measures(slot_graph)
    print(slot_centrality.head(20).to_string())
    slot_centrality.to_csv('slot_centrality.csv', index=False)
    
    # Export graphs
    print("\nExporting graphs...")
    exporter = GraphExporter()
    
    exporter.export_graphml(cxn_graph, 'construction_network.graphml')
    exporter.export_json(cxn_graph, 'construction_network.json')
    exporter.export_adjacency_matrix(cxn_graph, 'construction_adjacency.csv')
    
    exporter.export_graphml(slot_graph, 'slot_network.graphml')
    exporter.export_json(slot_graph, 'slot_network.json')
    
    # Community detection
    print("\nDetecting communities...")
    cxn_communities = analyzer.detect_communities(cxn_graph)
    if cxn_communities:
        for comm_id, nodes in cxn_communities.items():
            print(f"  Community {comm_id}: {nodes}")
    
    print("\n[SUCCESS] Graph analysis complete")
