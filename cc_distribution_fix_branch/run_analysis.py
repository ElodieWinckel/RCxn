"""
Main execution script - Complete analysis pipeline

Run this to execute the entire analysis workflow:
1. Parse RDF files
2. Compute similarity metrics
3. Build graphs
4. Analyze networks
5. Create visualizations
"""

from pathlib import Path
import pandas as pd

from parse_rdf_files import RDFParser, DataProcessor
from compute_similarity import SimilarityAnalyzer, SimilarityConfig
from build_graphs import GraphBuilder, NetworkAnalyzer, GraphExporter
from visualize_networks import NetworkVisualizer, InteractiveVisualizer, AnalysisReport


def main():
    """Execute complete analysis pipeline"""
    
    print("=" * 80)
    print("COMPARATIVE CONCEPTS ANALYSIS PIPELINE")
    print("=" * 80)
    
    # Configuration
    rdf_dir = Path("d:/PhD/RTG Project/1_Project work/RCxn/instance/Submissions/cc-project/CASA")
    output_dir = Path.cwd()
    
    # Similarity thresholds for different analyses
    SLOT_THRESHOLD = 0.3
    CXN_THRESHOLD = 0.3
    
    # =========================================================================
    # PHASE 1: Parse RDF Files
    # =========================================================================
    print("\n[PHASE 1] Parsing RDF Files...")
    print("-" * 80)
    
    parser = RDFParser()
    constructions = parser.parse_directory(rdf_dir)
    print(f"\n[OK] Loaded {len(constructions)} constructions")
    
    # Export data summaries
    processor = DataProcessor()
    cxn_df = processor.constructions_to_dataframe(constructions)
    slot_df = processor.slots_to_dataframe(constructions)
    cc_df = processor.ccs_to_dataframe(constructions)
    
    cxn_df.to_csv('01_construction_summary.csv', index=False)
    slot_df.to_csv('02_slot_summary.csv', index=False)
    cc_df.to_csv('03_cc_inventory.csv', index=False)
    
    print(f"\nConstruction Overview:")
    print(cxn_df[['construction', 'slot_count', 'total_ccs', 'avg_ccs_per_slot']].to_string())
    
    # =========================================================================
    # PHASE 2: Compute Similarity Metrics
    # =========================================================================
    print("\n[PHASE 2] Computing Similarity Metrics...")
    print("-" * 80)
    
    config = SimilarityConfig()
    analyzer = SimilarityAnalyzer(config)
    
    print("Computing slot-to-slot similarities...")
    slot_sim_matrix = analyzer.compute_slot_similarity_matrix(constructions)
    slot_sim_matrix.to_csv('04_slot_similarity_matrix.csv')
    print(f"  Slot similarity matrix: {slot_sim_matrix.shape}")
    
    print("Computing construction-to-construction similarities...")
    cxn_sim_matrix = analyzer.compute_construction_similarity_matrix(constructions)
    cxn_sim_matrix.to_csv('05_construction_similarity_matrix.csv')
    print(f"  Construction similarity matrix: {cxn_sim_matrix.shape}")
    
    # Top similar pairs
    print("\nTop 20 most similar slot pairs:")
    top_slot_pairs = analyzer.get_top_similar_pairs(slot_sim_matrix, top_n=20)
    print(top_slot_pairs.to_string())
    top_slot_pairs.to_csv('06_top_similar_slot_pairs.csv', index=False)
    
    print("\nTop 20 most similar construction pairs:")
    top_cxn_pairs = analyzer.get_top_similar_pairs(cxn_sim_matrix, top_n=20)
    print(top_cxn_pairs.to_string())
    top_cxn_pairs.to_csv('07_top_similar_construction_pairs.csv', index=False)
    
    # =========================================================================
    # PHASE 3: Build Graphs
    # =========================================================================
    print("\n[PHASE 3] Building Networks...")
    print("-" * 80)
    
    builder = GraphBuilder(config)
    
    print("Building construction-level graph...")
    cxn_graph = builder.build_construction_graph(constructions, threshold=CXN_THRESHOLD)
    print(f"  Nodes: {cxn_graph.number_of_nodes()}, Edges: {cxn_graph.number_of_edges()}")
    
    print("Building slot-level graph...")
    slot_graph = builder.build_slot_graph(constructions, threshold=SLOT_THRESHOLD)
    print(f"  Nodes: {slot_graph.number_of_nodes()}, Edges: {slot_graph.number_of_edges()}")
    
    # =========================================================================
    # PHASE 4: Analyze Networks
    # =========================================================================
    print("\n[PHASE 4] Network Analysis...")
    print("-" * 80)
    
    net_analyzer = NetworkAnalyzer()
    
    # Construction-level analysis
    print("\nConstruction-level network statistics:")
    cxn_stats = net_analyzer.get_network_stats(cxn_graph)
    for key, value in cxn_stats.items():
        print(f"  {key}: {value}")
    
    print("\nConstruction centrality measures:")
    cxn_centrality = net_analyzer.compute_centrality_measures(cxn_graph)
    print(cxn_centrality.to_string())
    cxn_centrality.to_csv('08_construction_centrality.csv', index=False)
    
    print("\nDetecting construction-level communities...")
    cxn_communities = net_analyzer.detect_communities(cxn_graph)
    if cxn_communities:
        for comm_id, nodes in sorted(cxn_communities.items()):
            print(f"  Community {comm_id}: {nodes}")
    
    # Slot-level analysis
    print("\nSlot-level network statistics:")
    slot_stats = net_analyzer.get_network_stats(slot_graph)
    for key, value in slot_stats.items():
        print(f"  {key}: {value}")
    
    print("\nSlot centrality measures (top 20):")
    slot_centrality = net_analyzer.compute_centrality_measures(slot_graph)
    print(slot_centrality.head(20).to_string())
    slot_centrality.to_csv('09_slot_centrality.csv', index=False)
    
    print("\nDetecting slot-level communities...")
    slot_communities = net_analyzer.detect_communities(slot_graph)
    if slot_communities:
        for comm_id, nodes in sorted(slot_communities.items()):
            print(f"  Community {comm_id}: {nodes}")
    
    # =========================================================================
    # PHASE 5: Export Graphs
    # =========================================================================
    print("\n[PHASE 5] Exporting Graphs...")
    print("-" * 80)
    
    exporter = GraphExporter()
    
    print("Exporting construction graph...")
    exporter.export_graphml(cxn_graph, '10_construction_network.graphml')
    exporter.export_json(cxn_graph, '10_construction_network.json')
    exporter.export_adjacency_matrix(cxn_graph, '11_construction_adjacency.csv')
    
    print("Exporting slot graph...")
    exporter.export_graphml(slot_graph, '12_slot_network.graphml')
    exporter.export_json(slot_graph, '12_slot_network.json')
    
    # =========================================================================
    # PHASE 6: Visualizations
    # =========================================================================
    print("\n[PHASE 6] Creating Visualizations...")
    print("-" * 80)
    
    import matplotlib.pyplot as plt
    
    vis = NetworkVisualizer()
    
    print("Generating static visualizations...")
    
    fig = vis.plot_construction_network(cxn_graph)
    plt.savefig('13_construction_network.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Saved construction_network.png")
    
    fig = vis.plot_similarity_heatmap(cxn_sim_matrix)
    plt.savefig('14_similarity_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Saved similarity_heatmap.png")
    
    fig = vis.plot_degree_distribution(cxn_graph)
    plt.savefig('15_degree_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Saved degree_distribution.png")
    
    fig = vis.plot_weight_distribution(cxn_graph)
    plt.savefig('16_weight_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Saved weight_distribution.png")
    
    fig = vis.plot_cc_distribution(constructions)
    plt.savefig('17_cc_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  Saved cc_distribution.png")
    
    # Interactive visualizations
    try:
        print("\nGenerating interactive visualizations...")
        ivis = InteractiveVisualizer()
        
        fig_net = ivis.create_interactive_network(cxn_graph, "Construction Similarity Network")
        fig_net.write_html('18_construction_network_interactive.html')
        print("  Saved construction_network_interactive.html")
        
        fig_heat = ivis.create_interactive_heatmap(cxn_sim_matrix, "Construction Similarity Matrix")
        fig_heat.write_html('19_similarity_heatmap_interactive.html')
        print("  Saved similarity_heatmap_interactive.html")
    except Exception as e:
        print(f"  Note: Interactive visualizations skipped ({e})")
    
    # =========================================================================
    # PHASE 7: Report
    # =========================================================================
    print("\n[PHASE 7] Generating Report...")
    print("-" * 80)
    
    AnalysisReport.create_summary_report(
        constructions, 
        cxn_graph, 
        cxn_centrality,
        output_file='20_analysis_report.txt'
    )
    
    # =========================================================================
    # Configuration Summary
    # =========================================================================
    print("\n[CONFIGURATION SUMMARY]")
    print("-" * 80)
    print(f"CC Type Weights: {config.CC_TYPE_WEIGHTS}")
    print(f"Similarity Metric Weights: {config.METRIC_WEIGHTS}")
    print(f"Construction Graph Threshold: {CXN_THRESHOLD}")
    print(f"Slot Graph Threshold: {SLOT_THRESHOLD}")
    
    # =========================================================================
    # Complete
    # =========================================================================
    print("\n" + "=" * 80)
    print("[SUCCESS] ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nOutput files generated (numbered for easy organization):")
    print("  01_construction_summary.csv")
    print("  02_slot_summary.csv")
    print("  03_cc_inventory.csv")
    print("  04_slot_similarity_matrix.csv")
    print("  05_construction_similarity_matrix.csv")
    print("  06_top_similar_slot_pairs.csv")
    print("  07_top_similar_construction_pairs.csv")
    print("  08_construction_centrality.csv")
    print("  09_slot_centrality.csv")
    print("  10_construction_network.graphml")
    print("  10_construction_network.json")
    print("  11_construction_adjacency.csv")
    print("  12_slot_network.graphml")
    print("  12_slot_network.json")
    print("  13_construction_network.png")
    print("  14_similarity_heatmap.png")
    print("  15_degree_distribution.png")
    print("  16_weight_distribution.png")
    print("  17_cc_distribution.png")
    print("  18_construction_network_interactive.html (if Plotly available)")
    print("  19_similarity_heatmap_interactive.html (if Plotly available)")
    print("  20_analysis_report.txt")
    print("\nVisualize graphs with:")
    print("  - Cytoscape (import .graphml or .json)")
    print("  - Gephi (import .graphml)")
    print("  - Web browsers (open .html files)")


if __name__ == "__main__":
    main()
