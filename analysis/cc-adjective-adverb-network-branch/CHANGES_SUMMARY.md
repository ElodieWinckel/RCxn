# Session Changes Summary

## Files Created:
- debug_plot.py
- test_plot.py
- requirements_fixed.txt
- cc_distribution_data.html
- create_broken_plot.py
- cc_distribution_fix_branch/ (this folder)

## Files Modified:
- visualize_networks.py (fixed plotting function, optional seaborn)
- parse_rdf_files.py (Unicode → ASCII)
- compute_similarity.py (Unicode → ASCII)
- build_graphs.py (Unicode → ASCII)
- run_analysis.py (Unicode → ASCII)

## Generated Files:
- All numbered output files (01-20)
- PNG plots (13-17)
- Interactive HTML files (18-19)

## Key Fixes:
1. CC distribution plot stacking bug (CXN bars now visible)
2. Windows Unicode compatibility issues
3. Optional seaborn dependency
4. Virtual environment setup with uv
