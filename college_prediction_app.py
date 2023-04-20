import streamlit as st
import pandas as pd
import pickle
import torch


st.set_page_config(page_title="home_page",page_icon="Digital Docter\IMG_20211110_171634.jpg")

hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("Predict the college based on your cut off")


st.code(torch.cuda.is_available())


df = pd.read_csv(r"college_cuttoff_all_years.csv")
full_df = df

Cut_off = st.text_input("enter the cut off")
community = st.selectbox("Enter your community", [ "None","OC","BC","BCM","MBC","MBCDNC","MBCV","SC","SCA","ST"] )
Department = st.selectbox("Enetr the department",list(full_df["Branch Name"]))
no_of_data_show = st.select_slider("Select number of colleges to show",[ i for i in range(1,500)])
st.write("add extra filter")
district_list = list(set(list(full_df["District"])))
district_list.insert(0,"None")
district = st.selectbox("Enter the district", district_list)

submit = st.button("SUBMIT")

try:
    if submit == True:
 
        community_dataset =pd.DataFrame(data = full_df[community.upper()])
        selected_dataset = pd.concat([full_df.iloc[:,:7] ,community_dataset],axis=1,join="inner")

        dataset = selected_dataset
        if district == "None":
            predicted = dataset[ (dataset[community]  < int(Cut_off) ) & (dataset["Branch Name"] == Department) ]
        else:
            predicted = dataset[ (dataset[community]  < int(Cut_off) ) & (dataset["Branch Name"] == Department) & (dataset["District"] == district) ]
        predicted =  predicted.sort_values(community.upper())
        predicted = predicted.iloc[::-1]
        predicted = predicted.reset_index(drop=True)
        predicted_select =  predicted.iloc[:int(no_of_data_show),1:10]
        st.subheader("Predicted college for your cut off !!!")
        
        if len(predicted) <= 0 :
            st.success("no one college is predicted for this cut off with this department")
        else:
            
            st.table(predicted_select)
            
            
            st.subheader("Predicted college for your cut off in 2017 !!!")
            st.dataframe( predicted[ predicted["Year"] == 2017 ].iloc[:,1:10])
            st.subheader("Predicted college for your cut off in 2018 !!!")
            st.dataframe( predicted[ predicted["Year"] == 2018 ].iloc[:,1:10])
            st.subheader("Predicted college for your cut off in 2019 !!!")
            st.dataframe( predicted[ predicted["Year"] == 2019 ].iloc[:,1:10])
            st.subheader("Predicted college for your cut off in 2020 !!!")
            st.dataframe( predicted[ predicted["Year"] == 2020 ].iloc[:,1:10])
            st.subheader("Predicted college for your cut off in 2021 !!!")
            st.dataframe( predicted[ predicted["Year"] == 2021 ].iloc[:,1:10])

except:
    st.error("Enter all the given information")
    
district_list_for_all = list(set(list(full_df["District"])))
district_list_for_all.insert(0,"None")


st.subheader("Enter the district ")
college_district_list =  pickle.load(open("college_dritrict.pickle","rb"))
predicted_college = [ z for x,y,z in college_district_list ]

district_name = st.selectbox("Enter the district :", predicted_college)
college_list_button = st.button("SUBMIT..")

result_college = []
if college_list_button == True:
    for x,y,z in college_district_list:
        if z == district_name:
            result_college.append(y)
    st.dataframe(pd.DataFrame(data=result_college,columns=["College"]))
    

    
# year = st.selectbox("Select the year ",["None",2017,2018,2019,2020,2021])

