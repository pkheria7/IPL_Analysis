import os
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

def create_tableau_workbook(csv_files, output_dir):
    """Create Tableau workbook (.twb) files from CSV files"""
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    for csv_file in csv_files:
        try:
            # Check if file exists
            if not os.path.exists(csv_file):
                print(f"File not found: {csv_file}")
                continue
            
            # Read CSV file
            df = pd.read_csv(csv_file)
            
            # Calculate additional metrics
            df['boundary_percentage'] = ((4 * df['fours'] + 6 * df['sixes']) * 100 / df['total_runs']).fillna(0)
            
            # Handle NaN values
            df = df.fillna({
                'dismissal_kind': '',
                'batting_team': '',
                'bowling_team': '',
                'opponent_team': '',
                'batting_strike_rate': 0.0,
                'bowling_economy': 0.0
            })
            
            # Create output filenames
            base_name = os.path.splitext(os.path.basename(csv_file))[0]
            csv_output = os.path.join(output_dir, f"{base_name}_processed.csv")
            twb_output = os.path.join(output_dir, f"{base_name}.twb")
            
            # Save processed CSV
            df.to_csv(csv_output, index=False)
            
            # Create basic Tableau workbook XML
            workbook = ET.Element('workbook')
            workbook.set('version', '10.5')
            
            # Add datasource
            datasources = ET.SubElement(workbook, 'datasources')
            datasource = ET.SubElement(datasources, 'datasource')
            datasource.set('name', 'federated.csv')
            datasource.set('hasconnection', 'true')
            
            connection = ET.SubElement(datasource, 'connection')
            connection.set('class', 'textscan')
            connection.set('directory', os.path.dirname(csv_output))
            connection.set('filename', os.path.basename(csv_output))
            connection.set('type', 'text')
            
            # Add basic worksheet
            worksheets = ET.SubElement(workbook, 'worksheets')
            worksheet = ET.SubElement(worksheets, 'worksheet')
            worksheet.set('name', 'Player Analysis')
            
            # Write the XML to file
            tree = ET.ElementTree(workbook)
            tree.write(twb_output, encoding='utf-8', xml_declaration=True)
            
            print(f"Created Tableau workbook: {twb_output}")
            print(f"Created processed CSV: {csv_output}")
            
        except Exception as e:
            print(f"Error processing {csv_file}: {str(e)}")
            continue

def main():
    # Get current directory
    current_dir = os.getcwd()
    
    # List of CSV files (modify as needed)
    csv_files = [
        'SA_Yadav_IPL2021.csv',
        'SA_Yadav_IPL2022.csv'
    ]
    
    # Convert to full paths
    csv_files = [os.path.join(current_dir, file) for file in csv_files]
    
    # Create output directory
    output_dir = os.path.join(current_dir, 'tableau_files')
    
    # Process files
    create_tableau_workbook(csv_files, output_dir)
    
    print("\nProcess completed! To use these files in Tableau Public:")
    print("1. Open Tableau Public")
    print("2. Connect to Text file (CSV)")
    print("3. Navigate to the processed CSV file in the 'tableau_files' directory")
    print("4. Create your visualizations")
    print("5. Save to Tableau Public")

if __name__ == "__main__":
    main()