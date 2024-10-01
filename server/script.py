import sys
import pandas as pd
import json
from datetime import datetime


def card_1(plant, item):
    # Load your dataset
    df_production = pd.read_excel('production.xlsx')


    # Convert SCHEDDATE to datetime
    df_production['SCHEDDATE'] = pd.to_datetime(df_production['SCHEDDATE'])


    # Get today's date
    today = datetime.today()


    # Filter data based on selected plant, item, and future dates
    df_filtered = df_production[
        (df_production['PLANT'] == plant) &
        (df_production['ITEM'] == int(item)) &
        (df_production['SCHEDDATE'] >= today)
    ]


    # Sort by SCHEDDATE in ascending order (from older to newer)
    df_sorted = df_filtered.sort_values(by='SCHEDDATE', ascending=True)
   
    # Format date as 'DD-MM-YYYY'
    df_sorted['DATE'] = df_sorted['SCHEDDATE'].dt.strftime('%d-%m-%Y')


    # Select columns to return
    columns_to_return = ['ITEM', 'PLANT', 'BRANDTECH', 'MARSYPW', 'DATE']
    final_df = df_sorted[columns_to_return].head()


    # Convert final DataFrame to JSON format
    result_json = final_df.to_json(orient='records')


    return result_json

def card_2(plant, material):
    # Load your dataset
    df_mrp = pd.read_excel('mrp.xlsx')  # Ensure you have the correct file name

    # Convert REQUIREMENT_DATE to datetime
    df_mrp['REQUIREMENT_DATE'] = pd.to_datetime(df_mrp['REQUIREMENT_DATE'])

    # Convert MATERIAL_NO to string for consistency
    df_mrp['MATERIAL_NO'] = df_mrp['MATERIAL_NO'].astype(str)

    # Create a new column 'WEEK' to extract the week number from REQUIREMENT_DATE
    df_mrp['WEEK'] = df_mrp['REQUIREMENT_DATE'].dt.isocalendar().week

    # Group by MATERIAL_NO, PLANT, and WEEK, and then select the row with the latest REQUIREMENT_DATE
    df_latest_per_week = df_mrp.sort_values('REQUIREMENT_DATE').groupby(['MATERIAL_NO', 'PLANT', 'WEEK'], as_index=False).last()

    # Filter the data based on input parameters and future dates
    today_date = pd.Timestamp.today()
    filtered_df = df_latest_per_week[
        (df_latest_per_week['PLANT'] == plant) &
        (df_latest_per_week['MATERIAL_NO'] == str(material)) &
        (df_latest_per_week['REQUIREMENT_DATE'] >= today_date)
    ]

    # Select only the required columns
    columns_to_return = ['MATERIAL_NO', 'PLANT', 'MATERIAL_DESCRIPTION', 'MARSYPW', 
                         'REQUIREMENT_DATE', 'AVAILABLE_STOCK', 'SAFETY_STOCK']
    final_df = filtered_df[columns_to_return].head()  # Limit to 5 rows

    # Convert dates to string format
    final_df['REQUIREMENT_DATE'] = final_df['REQUIREMENT_DATE'].dt.strftime('%Y-%m-%d')

    # Convert final DataFrame to JSON format
    result_json = final_df.to_json(orient='records')

    return result_json

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Insufficient arguments provided"}))
        sys.stdout.flush()
        sys.exit(1)

    function = sys.argv[1]
    
    try:
        if function == "card_1":
            if len(sys.argv) != 4:
                raise ValueError("Plant and Item arguments are required for card_1")
            plant = sys.argv[2]
            item = sys.argv[3]
            result = card_1(plant, item)
        elif function == "card_2":
            if len(sys.argv) != 4:
                raise ValueError("Plant and Material arguments are required for card_2")
            plant = sys.argv[2]
            material = sys.argv[3]
            result = card_2(plant, material)
        else:
            raise ValueError(f"Unknown function: {function}")
        
        print(result)  # This will be captured by Node.js
        sys.stdout.flush()
    except Exception as e:
        print(json.dumps({"error": str(e)}))  # Return errors as JSON
        sys.stdout.flush()
   




