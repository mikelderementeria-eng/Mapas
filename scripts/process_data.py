#!/usr/bin/env python3
"""
Data Pipeline for Valparaíso Electoral Maps
============================================
This script processes raw census and election data into JSON format for the maps.

Usage:
    python scripts/process_data.py --censo data/raw/censo.csv --elecciones data/raw/elecciones.csv --output data/

Requirements:
    pip install pandas geopandas
"""

import json
import os
import argparse
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("Installing required packages...")
    os.system("pip install pandas")
    import pandas as pd


def load_census_data(filepath):
    """Load and clean census data from CSV."""
    print(f"Loading census data from {filepath}...")
    df = pd.read_csv(filepath, encoding='utf-8')
    
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Ensure UV identifier exists
    if 'uv' not in df.columns and 'uv_j' not in df.columns:
        raise ValueError("Census file must contain 'uv' or 'uv_j' column")
    
    return df


def load_election_data(filepath):
    """Load and clean election results from CSV."""
    print(f"Loading election data from {filepath}...")
    df = pd.read_csv(filepath, encoding='utf-8')
    
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    return df


def transform_census_to_json(df):
    """Transform census DataFrame to JSON format indexed by UV."""
    print("Transforming census data...")
    
    # Create dictionary indexed by UV
    result = {}
    for _, row in df.iterrows():
        uv_key = int(row.get('uv', row.get('uv_j', 0)))
        if uv_key:
            result[uv_key] = row.to_dict()
    
    return result


def transform_election_to_json(df):
    """Transform election DataFrame to JSON format indexed by UV."""
    print("Transforming election data...")
    
    result = {}
    for _, row in df.iterrows():
        uv_key = int(row.get('uv', row.get('uv_j', 0)))
        if uv_key:
            # Calculate percentages and derived fields
            election_data = row.to_dict()
            
            # Add calculated fields if votes are available
            if 'votos_totales' in election_data and election_data['votos_totales'] > 0:
                total = election_data['votos_totales']
                # Example: calculate percentages for each pact
                for col in ['d_uxch', 'd_chgu', 'd_cxch', 'd_pdg', 'd_vryh']:
                    if col in election_data:
                        election_data[f'{col}_pct'] = (election_data[col] / total * 100) if total > 0 else 0
            
            result[uv_key] = election_data
    
    return result


def merge_datasets(censo_dict, elec_dict):
    """Merge census and election data by UV."""
    print("Merging datasets...")
    
    all_uvs = set(censo_dict.keys()) | set(elec_dict.keys())
    merged = {}
    
    for uv in all_uvs:
        merged[uv] = {
            **censo_dict.get(uv, {}),
            **elec_dict.get(uv, {})
        }
    
    return merged


def save_json(data, filepath, indent=2):
    """Save data to JSON file."""
    print(f"Saving to {filepath}...")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    print(f"✓ Saved {len(data)} records")


def generate_sample_data(output_dir):
    """Generate sample data files for testing."""
    print("\nGenerating sample data...")
    
    # Sample census data
    sample_censo = {
        28: {"uv": 28, "nombre": "Cerro Concepción", "poblacion": 1250, "viviendas": 480, "edad_promedio": 42.5},
        30: {"uv": 30, "nombre": "Quebrada Verde", "poblacion": 2100, "viviendas": 620, "edad_promedio": 35.2},
        31: {"uv": 31, "nombre": "Valencia Sur", "poblacion": 1890, "viviendas": 550, "edad_promedio": 38.7},
        35: {"uv": 35, "nombre": "Cerro Toro", "poblacion": 3200, "viviendas": 890, "edad_promedio": 33.1},
        39: {"uv": 39, "nombre": "Porvenir Alto", "poblacion": 2750, "viviendas": 720, "edad_promedio": 36.4},
    }
    
    # Sample election data
    sample_elecciones = {
        28: {"uv": 28, "inscritos": 890, "votos_totales": 623, "participacion": 70.0, "d_uxch": 180, "d_chgu": 120, "d_cxch": 95, "d_pdg": 85, "d_vryh": 143},
        30: {"uv": 30, "inscritos": 1450, "votos_totales": 1015, "participacion": 70.0, "d_uxch": 290, "d_chgu": 195, "d_cxch": 165, "d_pdg": 140, "d_vryh": 225},
        31: {"uv": 31, "inscritos": 1320, "votos_totales": 924, "participacion": 70.0, "d_uxch": 265, "d_chgu": 178, "d_cxch": 150, "d_pdg": 128, "d_vryh": 203},
        35: {"uv": 35, "inscritos": 2180, "votos_totales": 1526, "participacion": 70.0, "d_uxch": 438, "d_chgu": 294, "d_cxch": 248, "d_pdg": 211, "d_vryh": 335},
        39: {"uv": 39, "inscritos": 1890, "votos_totales": 1323, "participacion": 70.0, "d_uxch": 380, "d_chgu": 255, "d_cxch": 215, "d_pdg": 183, "d_vryh": 290},
    }
    
    censo_path = output_dir / 'censo_2024.json'
    elecciones_path = output_dir / 'elecciones_nov2025.json'
    merged_path = output_dir / 'datos_completos.json'
    
    save_json(sample_censo, censo_path)
    save_json(sample_elecciones, elecciones_path)
    save_json({**sample_censo, **{k: {**v, **sample_elecciones.get(k, {})} for k, v in sample_censo.items()}}, merged_path)
    
    return censo_path, elecciones_path


def main():
    parser = argparse.ArgumentParser(description='Process electoral and census data for Valparaíso maps')
    parser.add_argument('--censo', type=str, help='Path to census CSV file')
    parser.add_argument('--elecciones', type=str, help='Path to election results CSV file')
    parser.add_argument('--output', type=str, default='data/', help='Output directory for JSON files')
    parser.add_argument('--generate-sample', action='store_true', help='Generate sample data files')
    
    args = parser.parse_args()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.generate_sample or (not args.censo and not args.elecciones):
        print("=" * 60)
        print("DATA PIPELINE · VALPARAÍSO ELECTORAL MAPS")
        print("=" * 60)
        censo_path, elecciones_path = generate_sample_data(output_dir)
        print(f"\n✓ Sample data generated successfully!")
        print(f"  - Census: {censo_path}")
        print(f"  - Elections: {elecciones_path}")
        print(f"  - Merged: {output_dir / 'datos_completos.json'}")
        print("\nNext steps:")
        print("  1. Replace sample data with real CSV files")
        print("  2. Run: python scripts/process_data.py --censo your_censo.csv --elecciones your_elecciones.csv")
        return
    
    # Process real data
    print("=" * 60)
    print("DATA PIPELINE · VALPARAÍSO ELECTORAL MAPS")
    print("=" * 60)
    
    censo_df = load_census_data(args.censo)
    elec_df = load_election_data(args.elecciones)
    
    censo_json = transform_census_to_json(censo_df)
    elec_json = transform_election_to_json(elec_df)
    merged_json = merge_datasets(censo_json, elec_json)
    
    save_json(censo_json, output_dir / 'censo_2024.json')
    save_json(elec_json, output_dir / 'elecciones_nov2025.json')
    save_json(merged_json, output_dir / 'datos_completos.json')
    
    print("\n✓ Data processing completed successfully!")


if __name__ == '__main__':
    main()
