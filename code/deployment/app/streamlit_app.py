# streamlit_app.py
import streamlit as st
import requests

# FastAPI endpoint
FASTAPI_URL = "http://fastapi:8000/predict"

# Streamlit app UI
st.title("Flight delays classifier")

# change to date widget?
month = st.select_slider("Month", options=["c-1", "c-2", "c-3", "c-4", "c-5", "c-6",
                                           "c-7", "c-8", "c-9", "c-10", "c-11", "c-12"])
day_of_month = st.select_slider("Day of Month", options=["c-1", "c-2", "c-3", "c-4", "c-5", "c-6",
                                                         "c-7", "c-8", "c-9", "c-10", "c-11", "c-12",
                                                         "c-13", "c-14", "c-15", "c-16", "c-17", "c-18",
                                                         "c-19", "c-20", "c-21", "c-22", "c-23", "c-24",
                                                         "c-25", "c-26", "c-27", "c-28", "c-29", "c-30",
                                                         "c-31"])
day_of_week = st.select_slider("Day of Week", options=["c-1", "c-2", "c-3", "c-4", "c-5", "c-6", "c-7"])
dep_time = st.number_input("Departure Time", min_value=100, max_value=2459)

unique_carrier = st.selectbox("Unique Carrier, code of a company-career", options=['AA', 'US', 'XE', 'OO', 'WN', 'NW', 'DL', 'OH', 'AS', 'UA', 'MQ',
       'CO', 'EV', 'DH', 'YV', 'F9', 'AQ', 'TZ', 'HP', 'B6', 'FL', 'HA'])

origin = st.selectbox("Origin", options=['ATL', 'PIT', 'RDU', 'DEN', 'MDW', 'MEM', 'PBI', 'MSP', 'ONT',
       'BDL', 'PHX', 'LAS', 'DFW', 'DSM', 'CMH', 'ORF', 'SLC', 'CLT',
       'GSO', 'IAD', 'SMF', 'FLL', 'DAL', 'ORD', 'ITO', 'SAN', 'ROA',
       'LGA', 'SFO', 'GSP', 'SEA', 'DAB', 'SJC', 'LIT', 'LAX', 'OAK',
       'COS', 'OKC', 'GRR', 'JFK', 'BOI', 'MCI', 'BWI', 'BHM', 'CRP',
       'BOS', 'SAT', 'PHL', 'STL', 'CIC', 'AUS', 'IAH', 'COD', 'HNL',
       'RNO', 'BNA', 'TPA', 'MIA', 'EVV', 'PNS', 'EWR', 'RSW', 'ANC',
       'SNA', 'AMA', 'CID', 'DTW', 'DCA', 'LGB', 'MAF', 'MFE', 'BMI',
       'PDX', 'IPL', 'GRB', 'FAR', 'HOU', 'MTJ', 'DRO', 'MLU', 'VPS',
       'TUL', 'CVG', 'SBA', 'PWM', 'IDA', 'MCO', 'ACV', 'CHS', 'BGM',
       'MSY', 'OGG', 'CLE', 'MOB', 'CAK', 'FAY', 'SHV', 'TUS', 'IND',
       'CAE', 'PVD', 'ROC', 'MFR', 'VLD', 'ELP', 'RIC', 'MKE', 'SGF',
       'TYS', 'CHO', 'EGE', 'BIS', 'JAN', 'JAX', 'BUF', 'MSO', 'BGR',
       'CEC', 'ICT', 'MYR', 'ALB', 'LIH', 'SBP', 'AEX', 'GNV', 'SAV',
       'BTM', 'BRO', 'SJU', 'XNA', 'CPR', 'SDF', 'JAC', 'AVL', 'PHF',
       'GPT', 'SYR', 'PSP', 'MHT', 'MRY', 'CLD', 'FAT', 'MSN', 'ISP',
       'BUR', 'PSC', 'MEI', 'LEX', 'LBB', 'GEG', 'LFT', 'OMA', 'ISO',
       'MGM', 'GRK', 'AVP', 'ABQ', 'SRQ', 'BTV', 'FLG', 'BTR', 'MDT',
       'ABI', 'TRI', 'ADQ', 'FSM', 'SMX', 'RST', 'RAP', 'ILM', 'SIT',
       'EKO', 'DBQ', 'CHA', 'BQK', 'BZN', 'MOD', 'MOT', 'MLB', 'TVC',
       'LAN', 'DAY', 'HSV', 'EUG', 'SGU', 'ACT', 'AGS', 'CLL', 'HLN',
       'LNK', 'ASE', 'HRL', 'ATW', 'CMI', 'LWS', 'DHN', 'FNT', 'FLO',
       'RDM', 'TYR', 'KOA', 'FAI', 'OME', 'RDD', 'MCN', 'TLH', 'MQT',
       'AZO', 'FCA', 'CRW', 'TOL', 'HPN', 'FSD', 'FWA', 'SUN', 'LAW',
       'YUM', 'PIA', 'GTF', 'ACY', 'PIH', 'SPS', 'MLI', 'BIL', 'TWF',
       'HTS', 'SBN', 'PFN', 'GJT', 'CSG', 'JNU', 'TXK', 'LRD', 'BQN',
       'CWA', 'SWF', 'GTR', 'BFL', 'OXR', 'KTN', 'PIE', 'SCE', 'PSG',
       'DLH', 'SJT', 'GUC', 'SPI', 'IYK', 'ABY', 'STT', 'ABE', 'GFK',
       'HDN', 'CDV', 'MBS', 'TUP', 'LCH', 'EYW', 'OTZ', 'ADK', 'GGG',
       'VIS', 'GST', 'LYH', 'HVN', 'BRW', 'LSE', 'ERI', 'HKY', 'BET',
       'CDC', 'OAJ', 'WRG', 'ACK', 'DLG', 'YAK', 'AKN', 'TEX', 'STX',
       'SCC', 'APF', 'BPT', 'WYS', 'RFD', 'BLI', 'ILG', 'VCT', 'LWB',
       'PSE'])

dest = st.selectbox("Destination", options=['ATL', 'PIT', 'RDU', 'DEN', 'MDW', 'MEM', 'PBI', 'MSP', 'ONT',
       'BDL', 'PHX', 'LAS', 'DFW', 'DSM', 'CMH', 'ORF', 'SLC', 'CLT',
       'GSO', 'IAD', 'SMF', 'FLL', 'DAL', 'ORD', 'ITO', 'SAN', 'ROA',
       'LGA', 'SFO', 'GSP', 'SEA', 'DAB', 'SJC', 'LIT', 'LAX', 'OAK',
       'COS', 'OKC', 'GRR', 'JFK', 'BOI', 'MCI', 'BWI', 'BHM', 'CRP',
       'BOS', 'SAT', 'PHL', 'STL', 'CIC', 'AUS', 'IAH', 'COD', 'HNL',
       'RNO', 'BNA', 'TPA', 'MIA', 'EVV', 'PNS', 'EWR', 'RSW', 'ANC',
       'SNA', 'AMA', 'CID', 'DTW', 'DCA', 'LGB', 'MAF', 'MFE', 'BMI',
       'PDX', 'IPL', 'GRB', 'FAR', 'HOU', 'MTJ', 'DRO', 'MLU', 'VPS',
       'TUL', 'CVG', 'SBA', 'PWM', 'IDA', 'MCO', 'ACV', 'CHS', 'BGM',
       'MSY', 'OGG', 'CLE', 'MOB', 'CAK', 'FAY', 'SHV', 'TUS', 'IND',
       'CAE', 'PVD', 'ROC', 'MFR', 'VLD', 'ELP', 'RIC', 'MKE', 'SGF',
       'TYS', 'CHO', 'EGE', 'BIS', 'JAN', 'JAX', 'BUF', 'MSO', 'BGR',
       'CEC', 'ICT', 'MYR', 'ALB', 'LIH', 'SBP', 'AEX', 'GNV', 'SAV',
       'BTM', 'BRO', 'SJU', 'XNA', 'CPR', 'SDF', 'JAC', 'AVL', 'PHF',
       'GPT', 'SYR', 'PSP', 'MHT', 'MRY', 'CLD', 'FAT', 'MSN', 'ISP',
       'BUR', 'PSC', 'MEI', 'LEX', 'LBB', 'GEG', 'LFT', 'OMA', 'ISO',
       'MGM', 'GRK', 'AVP', 'ABQ', 'SRQ', 'BTV', 'FLG', 'BTR', 'MDT',
       'ABI', 'TRI', 'ADQ', 'FSM', 'SMX', 'RST', 'RAP', 'ILM', 'SIT',
       'EKO', 'DBQ', 'CHA', 'BQK', 'BZN', 'MOD', 'MOT', 'MLB', 'TVC',
       'LAN', 'DAY', 'HSV', 'EUG', 'SGU', 'ACT', 'AGS', 'CLL', 'HLN',
       'LNK', 'ASE', 'HRL', 'ATW', 'CMI', 'LWS', 'DHN', 'FNT', 'FLO',
       'RDM', 'TYR', 'KOA', 'FAI', 'OME', 'RDD', 'MCN', 'TLH', 'MQT',
       'AZO', 'FCA', 'CRW', 'TOL', 'HPN', 'FSD', 'FWA', 'SUN', 'LAW',
       'YUM', 'PIA', 'GTF', 'ACY', 'PIH', 'SPS', 'MLI', 'BIL', 'TWF',
       'HTS', 'SBN', 'PFN', 'GJT', 'CSG', 'JNU', 'TXK', 'LRD', 'BQN',
       'CWA', 'SWF', 'GTR', 'BFL', 'OXR', 'KTN', 'PIE', 'SCE', 'PSG',
       'DLH', 'SJT', 'GUC', 'SPI', 'IYK', 'ABY', 'STT', 'ABE', 'GFK',
       'HDN', 'CDV', 'MBS', 'TUP', 'LCH', 'EYW', 'OTZ', 'ADK', 'GGG',
       'VIS', 'GST', 'LYH', 'HVN', 'BRW', 'LSE', 'ERI', 'HKY', 'BET',
       'CDC', 'OAJ', 'WRG', 'ACK', 'DLG', 'YAK', 'AKN', 'TEX', 'STX',
       'SCC', 'APF', 'BPT', 'WYS', 'RFD', 'BLI', 'ILG', 'VCT', 'LWB',
       'PSE'])

distance = st.number_input("Distance, distance between Origin and Dest airports, km", min_value=1, max_value=5000)



# Make prediction when the button is clicked
if st.button("Predict"):
    # Prepare the data for the API request
    input_data = {
        "month": month,
        "day_of_month": day_of_month,
        "day_of_week": day_of_week,
        "dep_time": dep_time,
        "unique_carrier": unique_carrier,
        "origin": origin,
        "dest": dest,
        "distance": distance
    }

    # Send a request to the FastAPI prediction endpoint
    response = requests.post(FASTAPI_URL, json=input_data)
    prediction = response.json()["prediction"]

    # Display the result
    st.success(f"The flight is likely {'delayed' if prediction == 1 else 'not delayed'}")