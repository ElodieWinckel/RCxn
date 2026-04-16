"""
RDF Data Parser for Comparative Concepts Analysis

Parses TTL files and extracts construction/slot/CC hierarchy
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple
import pandas as pd
from rdflib import Graph, Namespace, URIRef
import re


@dataclass
class ComparativeConcept:
    """Represents a single comparative concept"""
    name: str
    type: str  # 'cxn', 'sem', 'str', 'inf'
    
    def __hash__(self):
        return hash((self.name, self.type))
    
    def __eq__(self, other):
        return isinstance(other, ComparativeConcept) and \
               self.name == other.name and self.type == other.type
    
    def __repr__(self):
        return f"CC({self.type}:{self.name})"


@dataclass
class Slot:
    """Represents a slot within a construction"""
    slot_id: str
    construction_name: str
    comparative_concepts: List[ComparativeConcept] = field(default_factory=list)
    
    @property
    def cc_count(self) -> int:
        return len(self.comparative_concepts)
    
    @property
    def type_profile(self) -> Dict[str, int]:
        """Count CCs by type"""
        profile = {'cxn': 0, 'sem': 0, 'str': 0, 'inf': 0}
        for cc in self.comparative_concepts:
            profile[cc.type] = profile.get(cc.type, 0) + 1
        return profile
    
    @property
    def cc_names(self) -> Set[str]:
        """Get all CC names in this slot"""
        return {cc.name for cc in self.comparative_concepts}
    
    def __repr__(self):
        return f"Slot({self.slot_id}, {self.cc_count} CCs)"


@dataclass
class Construction:
    """Represents a construction with multiple slots"""
    name: str
    slots: Dict[str, Slot] = field(default_factory=dict)
    
    @property
    def slot_count(self) -> int:
        return len(self.slots)
    
    @property
    def all_ccs(self) -> List[ComparativeConcept]:
        """Get all CCs from all slots"""
        ccs = []
        for slot in self.slots.values():
            ccs.extend(slot.comparative_concepts)
        return ccs
    
    @property
    def cc_count(self) -> int:
        return len(self.all_ccs)
    
    @property
    def type_profile(self) -> Dict[str, int]:
        """Count all CCs by type"""
        profile = {'cxn': 0, 'sem': 0, 'str': 0, 'inf': 0}
        for cc in self.all_ccs:
            profile[cc.type] = profile.get(cc.type, 0) + 1
        return profile
    
    @property
    def avg_ccs_per_slot(self) -> float:
        if self.slot_count == 0:
            return 0.0
        return self.cc_count / self.slot_count
    
    def __repr__(self):
        return f"Construction({self.name}, {self.slot_count} slots, {self.cc_count} CCs)"


class RDFParser:
    """Parses RDF/TTL files containing construction data"""
    
    def __init__(self):
        self.compcon_ns = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/compcon#")
        self.cx_ns = Namespace("http://example.org/cx/")
    
    @staticmethod
    def extract_cc_type(cc_uri: str) -> str:
        """Extract CC type from URI (prefix before underscore)"""
        # Expected format: compcon:type_name
        match = re.search(r'#(cxn|sem|str|inf)_', cc_uri)
        if match:
            return match.group(1)
        return 'unknown'
    
    @staticmethod
    def extract_cc_name(cc_uri: str) -> str:
        """Extract CC name from URI"""
        # Get the part after '#'
        if '#' in cc_uri:
            local_name = cc_uri.split('#')[-1]
            # Remove type prefix (e.g., 'cxn_', 'sem_')
            local_name = re.sub(r'^(cxn|sem|str|inf)_', '', local_name)
            return local_name
        return str(cc_uri)
    
    def parse_file(self, filepath: Path) -> Construction:
        """Parse a single TTL file and return Construction object"""
        g = Graph()
        g.parse(str(filepath), format='turtle')
        
        # Extract construction name from filename
        construction_name = filepath.stem.replace('_compcon', '')
        construction = Construction(name=construction_name)
        
        # Query all subjects that are constructions
        # They follow pattern: cx:engLME_..._[number]
        for subject in g.subjects():
            subject_str = str(subject)
            
            # Check if this is a construction entity
            if 'example.org/cx/' not in subject_str:
                continue
            
            # Extract slot ID from subject
            slot_id = subject_str.split('/')[-1]
            
            # Create slot if not exists
            if slot_id not in construction.slots:
                construction.slots[slot_id] = Slot(
                    slot_id=slot_id,
                    construction_name=construction_name
                )
            
            # Get all hasCompCon predicates (CCs)
            for obj in g.objects(subject, self.compcon_ns.hasCompCon):
                obj_str = str(obj)
                cc_type = self.extract_cc_type(obj_str)
                cc_name = self.extract_cc_name(obj_str)
                
                cc = ComparativeConcept(name=cc_name, type=cc_type)
                construction.slots[slot_id].comparative_concepts.append(cc)
        
        return construction
    
    def parse_directory(self, directory: Path, pattern: str = "*_compcon.ttl") -> Dict[str, Construction]:
        """Parse all matching TTL files in directory"""
        constructions = {}
        
        files = sorted(directory.glob(pattern))
        print(f"Found {len(files)} files matching pattern '{pattern}'")
        
        for filepath in files:
            try:
                print(f"Parsing {filepath.name}...", end=' ')
                construction = self.parse_file(filepath)
                constructions[construction.name] = construction
                print(f"[OK] ({construction.slot_count} slots, {construction.cc_count} CCs)")
            except Exception as e:
                print(f"[ERROR] {e}")
        
        return constructions


class DataProcessor:
    """Convert parsed constructions to analysis formats"""
    
    @staticmethod
    def constructions_to_dataframe(constructions: Dict[str, Construction]) -> pd.DataFrame:
        """Create summary DataFrame of constructions"""
        data = []
        for name, cxn in constructions.items():
            type_profile = cxn.type_profile
            data.append({
                'construction': name,
                'slot_count': cxn.slot_count,
                'total_ccs': cxn.cc_count,
                'avg_ccs_per_slot': cxn.avg_ccs_per_slot,
                'cxn_count': type_profile['cxn'],
                'sem_count': type_profile['sem'],
                'str_count': type_profile['str'],
                'inf_count': type_profile['inf'],
            })
        return pd.DataFrame(data)
    
    @staticmethod
    def slots_to_dataframe(constructions: Dict[str, Construction]) -> pd.DataFrame:
        """Create detailed DataFrame of all slots"""
        data = []
        for cxn_name, cxn in constructions.items():
            for slot_index, (slot_id, slot) in enumerate(cxn.slots.items()):
                type_profile = slot.type_profile
                
                # Try to extract numeric suffix from slot_id, otherwise use position
                try:
                    last_part = slot_id.split('_')[-1]
                    numeric_index = int(last_part) if last_part.isdigit() else slot_index
                except (ValueError, IndexError):
                    numeric_index = slot_index
                
                data.append({
                    'construction': cxn_name,
                    'slot_id': slot_id,
                    'slot_index': numeric_index,
                    'cc_count': slot.cc_count,
                    'cxn_count': type_profile['cxn'],
                    'sem_count': type_profile['sem'],
                    'str_count': type_profile['str'],
                    'inf_count': type_profile['inf'],
                    'ccs': ', '.join([f"{cc.type}:{cc.name}" for cc in slot.comparative_concepts]),
                })
        return pd.DataFrame(data)
    
    @staticmethod
    def ccs_to_dataframe(constructions: Dict[str, Construction]) -> pd.DataFrame:
        """Create inventory of all comparative concepts"""
        data = []
        cc_set = set()
        
        for cxn_name, cxn in constructions.items():
            for slot_id, slot in cxn.slots.items():
                for cc in slot.comparative_concepts:
                    cc_key = (cc.name, cc.type)
                    if cc_key not in cc_set:
                        cc_set.add(cc_key)
                        data.append({
                            'cc_name': cc.name,
                            'cc_type': cc.type,
                            'full_name': f"{cc.type}:{cc.name}",
                        })
        
        df = pd.DataFrame(data).sort_values(['cc_type', 'cc_name']).reset_index(drop=True)
        return df


# Example usage
if __name__ == "__main__":
    # Parse all compcon files
    parser = RDFParser()
    rdf_dir = Path("d:/PhD/RTG Project/1_Project work/RCxn/instance/Submissions/cc-project/CASA")
    
    constructions = parser.parse_directory(rdf_dir)
    
    print(f"\n[SUCCESS] Parsed {len(constructions)} constructions\n")
    
    # Summary statistics
    for cxn in sorted(constructions.values(), key=lambda x: x.name):
        print(f"  {cxn}")
    
    # Create analysis DataFrames
    processor = DataProcessor()
    
    cxn_df = processor.constructions_to_dataframe(constructions)
    slot_df = processor.slots_to_dataframe(constructions)
    cc_df = processor.ccs_to_dataframe(constructions)
    
    print(f"\n--- Construction Summary ---")
    print(cxn_df.to_string())
    
    print(f"\n--- Slot Summary (first 20) ---")
    print(slot_df.head(20).to_string())
    
    print(f"\n--- CC Inventory ---")
    print(cc_df.to_string())
    
    # Export to CSV for reference
    cxn_df.to_csv('construction_summary.csv', index=False)
    slot_df.to_csv('slot_summary.csv', index=False)
    cc_df.to_csv('cc_inventory.csv', index=False)
    print("\n[SUCCESS] Exported CSV files")
