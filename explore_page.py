import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
from streamlit_gsheets import GSheetsConnection

# Set the title of the web app
st.title('Mobile Network Churn EDA')


@st.cache_data
def load_data():
    """ Load the dataset from a file """
    return pd.read_csv('/mount/src/predictapp/ftdata.csv')


data = load_data()

Hcontainer = st.container(border=True)
Fcontainer = st.container(border=True)
HMcontainer = st.container(border=True)
Icontainer = st.container(border=True)


def simplify_category_name(data_frame, original_column):
    """ Simplify category name for better visualization """
    data_frame[original_column] = data_frame[original_column].apply(lambda x: x.split('_')[-1])
    return data_frame


def generate_summary(data, feature_columns):
    """ Generate summary data for a feature group """
    feature_data = data[feature_columns].sum().reset_index()
    feature_data.columns = ['Category', 'Count']
    return simplify_category_name(feature_data, 'Category')


def generate_heatmap(data, group_x, group_y):
    """ Generate a heatmap between two feature groups """
    columns_x = feature_groups[group_x]
    columns_y = feature_groups[group_y]
    agg_data = pd.DataFrame(index=columns_x, columns=columns_y, data=0)

    for col_x in columns_x:
        for col_y in columns_y:
            count = data[(data[col_x] == True) & (data[col_y] == True)].shape[0]
            agg_data.loc[col_x, col_y] = count

    agg_data.columns = [col.split('_')[-1] for col in agg_data.columns]
    agg_data.index = [idx.split('_')[-1] for idx in agg_data.index]

    plt.figure(figsize=(10, 8))
    sns.heatmap(agg_data, annot=True, fmt="d", cmap='coolwarm')
    plt.title(f'Heatmap between {group_x} and {group_y}')
    plt.xlabel(group_y)
    plt.ylabel(group_x)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    HMcontainer.pyplot(plt)


def show_explore_page():
    Hcontainer.header('Data Analysis of Dataset')
    Hcontainer.markdown('Here you are able to go through the Dataset and an analysis of said data.\n')

    Hcontainer.markdown('Sample of Dataset data\n')
    Hcontainer.write(data.head())
    Hcontainer.markdown('Summary of numerical data in Dataset\n')
    selected_columns = ['tenure', 'MonthlyCharges', 'TotalCharges']
    Hcontainer.write(data[selected_columns].describe())

    Fcontainer.header('Feature Group Summaries')
    selected_feature_group = Fcontainer.selectbox('Select Feature Group', list(feature_groups.keys()))

    if Fcontainer.checkbox('Show Grouped Data'):
        summary_data = generate_summary(data, feature_groups[selected_feature_group])
        Fcontainer.write(summary_data)

    Fcontainer.header('Visualization of Categorical Features')
    chart_type = Fcontainer.radio("Select Chart Type", ('Pie Chart', 'Bar Chart'))
    if chart_type:
        feature_data = generate_summary(data, feature_groups[selected_feature_group])
        if chart_type == 'Pie Chart':
            fig = px.pie(feature_data, values='Count', names=f'Category',
                         title=f'Distribution of {selected_feature_group}')
        elif chart_type == 'Bar Chart':
            fig = px.bar(feature_data, x='Category', y='Count', title=f'Distribution of {selected_feature_group}',
                         color='Category')
        Fcontainer.plotly_chart(fig, use_container_width=True)

    HMcontainer.header('Heatmaps for specific features')

    selected_group_x = HMcontainer.selectbox('Select Group X', list(feature_groups.keys()), index=0)
    selected_group_y = HMcontainer.selectbox('Select Group Y', list(feature_groups.keys()), index=1)

    if HMcontainer.button('Generate Heatmap'):
        generate_heatmap(data, selected_group_x, selected_group_y)

    st.sidebar.header('Dataset Quick Look:')
    st.sidebar.write(f'Number of Datapoints: {data.shape[0]}')
    st.sidebar.write(f'Number of Features: {data.shape[1] - 1}')


# Define feature groups globally
feature_groups = {
    'PaperlessBilling': ['PaperlessBilling_No', 'PaperlessBilling_Yes'],
    'Partner': ['Partner_No', 'Partner_Yes'],
    'InternetService': ['InternetService_DSL', 'InternetService_Fiber optic', 'InternetService_No'],
    'OnlineBackup': ['OnlineBackup_No', 'OnlineBackup_No internet service', 'OnlineBackup_Yes'],
    'Dependents': ['Dependents_No', 'Dependents_Yes'],
    'SeniorCitizen': ['SeniorCitizen_No', 'SeniorCitizen_Yes'],
    'DeviceProtection': ['DeviceProtection_No', 'DeviceProtection_No internet service', 'DeviceProtection_Yes'],
    'OnlineSecurity': ['OnlineSecurity_No', 'OnlineSecurity_No internet service', 'OnlineSecurity_Yes'],
    'TechSupport': ['TechSupport_No', 'TechSupport_No internet service', 'TechSupport_Yes'],
    'Contract': ['Contract_Month-to-month', 'Contract_One year', 'Contract_Two year'],
    'StreamingTV': ['StreamingTV_No', 'StreamingTV_No internet service', 'StreamingTV_Yes'],
    'PaymentMethod': ['PaymentMethod_Bank transfer (automatic)', 'PaymentMethod_Credit card (automatic)',
                      'PaymentMethod_Electronic check', 'PaymentMethod_Mailed check']
}
