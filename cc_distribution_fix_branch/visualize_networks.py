"""
Visualization and interactive analysis

Creates visualizations and interactive plots for network exploration
"""

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False
from typing import Dict

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False
    print("Note: Install plotly for interactive visualizations: pip install plotly")

from pathlib import Path


class NetworkVisualizer:
    """Create visualizations of networks"""
    
    @staticmethod
    def plot_construction_network(G: nx.Graph, figsize=(14, 10)):
        """
        Static plot of construction-level graph using spring layout
        Node size based on CC count, edge width based on similarity
        """
        plt.figure(figsize=figsize)
        
        # Layout
        pos = nx.spring_layout(G, k=2, iterations=50, weight='weight', seed=42)
        
        # Node sizes (based on degree or CC count)
        node_sizes = [G.nodes[node].get('cc_count', 1) * 100 for node in G.nodes()]
        
        # Edge widths (based on similarity weight)
        edge_widths = [G[u][v]['weight'] * 3 for u, v in G.edges()]
        
        # Edge colors (based on confidence)
        edge_colors = []
        for u, v in G.edges():
            confidence = G[u][v].get('confidence', 'low')
            if confidence == 'high':
                edge_colors.append('#2ecc71')  # Green
            elif confidence == 'medium':
                edge_colors.append('#f39c12')  # Orange
            else:
                edge_colors.append('#e74c3c')  # Red
        
        # Draw
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                              node_color='#3498db', alpha=0.9)
        nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.6, 
                              edge_color=edge_colors)
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        plt.title('Construction-level Similarity Network', fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        return plt.gcf()
    
    @staticmethod
    def plot_similarity_heatmap(similarity_matrix: pd.DataFrame, figsize=(12, 10)):
        """
        Heatmap of similarity matrix
        """
        plt.figure(figsize=figsize)
        
        # Get labels (construction names)
        if isinstance(similarity_matrix.index, pd.MultiIndex):
            labels = [f"{idx[0]}\n{idx[1]}" for idx in similarity_matrix.index]
        else:
            labels = list(similarity_matrix.index)
        
        if HAS_SEABORN:
            sns.heatmap(similarity_matrix, annot=True, fmt='.2f', cmap='RdYlGn',
                       vmin=0, vmax=1, cbar_kws={'label': 'Similarity'},
                       xticklabels=labels, yticklabels=labels, square=True)
        else:
            # Fallback to matplotlib imshow
            plt.imshow(similarity_matrix.values, cmap='RdYlGn', vmin=0, vmax=1)
            plt.colorbar(label='Similarity')
            
            # Add text annotations
            for i in range(len(similarity_matrix)):
                for j in range(len(similarity_matrix)):
                    plt.text(j, i, f'{similarity_matrix.values[i, j]:.2f}', 
                           ha='center', va='center', color='black', fontsize=8)
            
            plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
            plt.yticks(range(len(labels)), labels)
        
        plt.title('Similarity Matrix Heatmap', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        
        return plt.gcf()
    
    @staticmethod
    def plot_degree_distribution(G: nx.Graph):
        """Plot degree distribution"""
        degrees = dict(G.degree())
        
        plt.figure(figsize=(10, 6))
        plt.hist(degrees.values(), bins=20, color='#3498db', edgecolor='black', alpha=0.7)
        plt.xlabel('Node Degree', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.title('Degree Distribution', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        return plt.gcf()
    
    @staticmethod
    def plot_weight_distribution(G: nx.Graph):
        """Plot distribution of edge weights"""
        weights = [G[u][v]['weight'] for u, v in G.edges()]
        
        plt.figure(figsize=(10, 6))
        plt.hist(weights, bins=20, color='#e74c3c', edgecolor='black', alpha=0.7)
        plt.xlabel('Edge Weight (Similarity)', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.title('Edge Weight Distribution', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        return plt.gcf()
    
    @staticmethod
    def plot_cc_distribution(constructions: Dict) -> None:
        """Plot CC type distribution across constructions"""
        # Prepare data for plotting
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

        # Create stacked bar chart
        fig, ax = plt.subplots(figsize=(14, 6))

        # Plot each layer
        ax.bar(construction_names, cxn_counts, label='CXN', color='#3498db', alpha=0.8)
        ax.bar(construction_names, sem_counts, bottom=cxn_counts, label='SEM', color='#e74c3c', alpha=0.8)
        ax.bar(construction_names, str_counts, bottom=[cxn + sem for cxn, sem in zip(cxn_counts, sem_counts)], label='STR', color='#2ecc71', alpha=0.8)
        ax.bar(construction_names, inf_counts, bottom=[cxn + sem + str for cxn, sem, str in zip(cxn_counts, sem_counts, str_counts)], label='INF', color='#f39c12', alpha=0.8)

        plt.xlabel('Construction', fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.title('CC Type Distribution across Constructions', fontsize=14, fontweight='bold')
        plt.legend(title='CC Type')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()

class InteractiveVisualizer:
    """Create interactive visualizations using Plotly"""
    
    @staticmethod
    def create_interactive_network(G: nx.Graph, title: str = "Network Graph") -> go.Figure:
        """
        Create interactive network visualization with Plotly
        """
        if not HAS_PLOTLY:
            print("Plotly not available. Install with: pip install plotly")
            return None
        
        # Spring layout
        pos = nx.spring_layout(G, k=2, iterations=50, weight='weight', seed=42)
        
        # Extract edge info
        edge_x = []
        edge_y = []
        edge_colors = []
        edge_texts = []
        
        for u, v in G.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
            weight = G[u][v].get('weight', 0)
            confidence = G[u][v].get('confidence', 'unknown')
            edge_texts.append(f"{u} - {v}<br>Similarity: {weight:.3f}<br>Confidence: {confidence}")
            
            # Color based on confidence
            if confidence == 'high':
                edge_colors.append('#2ecc71')
            elif confidence == 'medium':
                edge_colors.append('#f39c12')
            else:
                edge_colors.append('#e74c3c')
        
        # Edge trace
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            mode='lines',
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            showlegend=False
        )
        
        # Node positions
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        node_color = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            # Node info
            node_attrs = G.nodes[node]
            info_text = f"<b>{node}</b><br>"
            for key, value in node_attrs.items():
                if isinstance(value, dict):
                    info_text += f"{key}: {value}<br>"
                else:
                    info_text += f"{key}: {value}<br>"
            node_text.append(info_text)
            
            # Size based on degree or CC count
            size = G.degree(node) * 15 + 20
            node_size.append(size)
            
            # Color based on component or metric
            node_color.append('#3498db')
        
        # Node trace
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=[n.split('#')[1] if '#' in n else n for n in G.nodes()],
            textposition="top center",
            hovertext=node_text,
            hoverinfo="text",
            marker=dict(
                showscale=False,
                color=node_color,
                size=node_size,
                line_width=2,
                line_color='#2c3e50'
            ),
            showlegend=False
        )
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title=dict(text=title, x=0.5, xanchor='center'),
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20, l=5, r=5, t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           plot_bgcolor='#f8f9fa',
                       ))
        
        return fig
    
    @staticmethod
    def create_interactive_heatmap(similarity_matrix: pd.DataFrame, title: str = "Similarity Matrix") -> go.Figure:
        """Create interactive heatmap"""
        if not HAS_PLOTLY:
            print("Plotly not available")
            return None
        
        # Get labels
        if isinstance(similarity_matrix.index, pd.MultiIndex):
            labels = [f"{idx[0]}<br>{idx[1]}" for idx in similarity_matrix.index]
        else:
            labels = list(similarity_matrix.index)
        
        fig = go.Figure(data=go.Heatmap(
            z=similarity_matrix.values,
            x=labels,
            y=labels,
            colorscale='RdYlGn',
            zmin=0,
            zmax=1,
            text=similarity_matrix.values.round(3),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Similarity")
        ))
        
        fig.update_layout(
            title=dict(text=title, x=0.5, xanchor='center'),
            xaxis_title="",
            yaxis_title="",
            height=600,
            width=800,
        )
        
        return fig


class AnalysisReport:
    """Generate comprehensive analysis report"""
    
    @staticmethod
    def create_summary_report(constructions: Dict, G: nx.Graph, 
                            centrality_df: pd.DataFrame, 
                            output_file: str = "analysis_report.txt"):
        """Create text report summarizing analysis"""
        
        with open(output_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("COMPARATIVE CONCEPTS ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            # Overall statistics
            f.write("OVERALL STATISTICS\n")
            f.write("-" * 40 + "\n")
            f.write(f"Number of constructions: {len(constructions)}\n")
            f.write(f"Total slots: {sum(c.slot_count for c in constructions.values())}\n")
            f.write(f"Total CCs: {sum(c.cc_count for c in constructions.values())}\n")
            f.write(f"Network nodes: {G.number_of_nodes()}\n")
            f.write(f"Network edges: {G.number_of_edges()}\n")
            f.write(f"Network density: {nx.density(G):.3f}\n\n")
            
            # Top central nodes
            f.write("TOP 10 MOST CENTRAL NODES\n")
            f.write("-" * 40 + "\n")
            for idx, row in centrality_df.head(10).iterrows():
                f.write(f"{row['node']}: {row['betweenness_centrality']:.3f}\n")
            f.write("\n")
            
            # CC type summary
            f.write("CC TYPE DISTRIBUTION\n")
            f.write("-" * 40 + "\n")
            total_by_type = {'cxn': 0, 'sem': 0, 'str': 0, 'inf': 0}
            for cxn in constructions.values():
                profile = cxn.type_profile
                for cc_type, count in profile.items():
                    total_by_type[cc_type] += count
            
            for cc_type, count in total_by_type.items():
                percentage = count / sum(total_by_type.values()) * 100
                f.write(f"  {cc_type.upper()}: {count} ({percentage:.1f}%)\n")
            f.write("\n")
            
            # Top similar pairs
            f.write("CONSTRUCTION SIMILARITY INFORMATION\n")
            f.write("-" * 40 + "\n")
            edges = [(u, v, G[u][v]['weight']) for u, v in G.edges()]
            edges.sort(key=lambda x: x[2], reverse=True)
            f.write("Top 10 most similar construction pairs:\n")
            for u, v, weight in edges[:10]:
                f.write(f"  {u} <-> {v}: {weight:.3f}\n")
        
        print(f"[SUCCESS] Report saved to {output_file}")


# Example usage
if __name__ == "__main__":
    from parse_rdf_files import RDFParser
    from compute_similarity import SimilarityAnalyzer
    from build_graphs import GraphBuilder, NetworkAnalyzer
    
    # Parse
    parser = RDFParser()
    rdf_dir = "d:/PhD/RTG Project/1_Project work/RCxn/instance/Submissions/cc-project/CASA"
    constructions = parser.parse_directory(rdf_dir)
    
    # Build graph
    builder = GraphBuilder()
    cxn_graph = builder.build_construction_graph(constructions, threshold=0.3)
    
    # Analyze
    analyzer = NetworkAnalyzer()
    centrality = analyzer.compute_centrality_measures(cxn_graph)
    
    # Visualize (static)
    print("Creating static visualizations...")
    vis = NetworkVisualizer()
    
    fig1 = vis.plot_construction_network(cxn_graph)
    plt.savefig('construction_network.png', dpi=300, bbox_inches='tight')
    print("  Saved construction_network.png")
    
    similarity_matrix = SimilarityAnalyzer().compute_construction_similarity_matrix(constructions)
    fig2 = vis.plot_similarity_heatmap(similarity_matrix)
    plt.savefig('similarity_heatmap.png', dpi=300, bbox_inches='tight')
    print("  Saved similarity_heatmap.png")
    
    fig3 = vis.plot_degree_distribution(cxn_graph)
    plt.savefig('degree_distribution.png', dpi=300, bbox_inches='tight')
    print("  Saved degree_distribution.png")
    
    fig4 = vis.plot_cc_distribution(constructions)
    plt.savefig('cc_distribution.png', dpi=300, bbox_inches='tight')
    print("  Saved cc_distribution.png")
    
    # Interactive visualizations (if Plotly available)
    if HAS_PLOTLY:
        print("\nCreating interactive visualizations...")
        ivis = InteractiveVisualizer()
        
        fig_net = ivis.create_interactive_network(cxn_graph, "Construction Similarity Network")
        fig_net.write_html('construction_network_interactive.html')
        print("  Saved construction_network_interactive.html")
        
        fig_heat = ivis.create_interactive_heatmap(similarity_matrix, "Construction Similarity Matrix")
        fig_heat.write_html('similarity_heatmap_interactive.html')
        print("  Saved similarity_heatmap_interactive.html")
    
    # Report
    print("\nGenerating report...")
    AnalysisReport.create_summary_report(constructions, cxn_graph, centrality)
    
    print("\n[SUCCESS] Visualization complete")
