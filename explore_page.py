import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title of the web app
st.title('Mobile Network Churn EDA')


# Load the dataset
def load_data():
    data = pd.read_csv('feature_values.csv')
    return data


data = load_data()


def show_explore_page():
    st.write(data.head())
    st.write('Descriptive Statistics:', data.describe())

    # Visualization of One-Hot Encoded Data
    st.header('Visualization of Categorical Features')

    # Define the mapping of features to their respective columns
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

    def simplify_category_name(data_frame, original_column):
        data_frame[original_column] = data_frame[original_column].apply(lambda x: x.split('_')[-1])
        return data_frame

    # Generate summary tables for each feature group
    def generate_summary(data, feature_columns):
        feature_data = data[feature_columns].sum().reset_index()
        feature_data.columns = ['Category', 'Count']
        return simplify_category_name(feature_data, 'Category')

    st.header('Feature Group Summaries')
    selected_feature_group = st.selectbox('Select Feature Group', list(feature_groups.keys()))

    # Show aggregated data for selected feature group
    if st.checkbox('Show Grouped Data'):
        feature_columns = feature_groups[selected_feature_group]
        summary_data = generate_summary(data, feature_columns)
        st.write(f'Summary for {selected_feature_group}:', summary_data)

    # Visualization of One-Hot Encoded Data
    st.header('Visualization of Categorical Features')
    feature_columns = feature_groups[selected_feature_group]

    # Data processing to sum each category
    feature_data = generate_summary(data, feature_columns)

    # Visualization with pie chart or bar chart
    chart_type = st.radio("Select Chart Type", ('Pie Chart', 'Bar Chart'))
    if chart_type == 'Pie Chart':
        plt.figure(figsize=(8, 8))
        plt.pie(feature_data['Count'], labels=feature_data['Category'], autopct='%1.1f%%')
        plt.title(f'Distribution of {selected_feature_group}')
        st.pyplot(plt)
    elif chart_type == 'Bar Chart':
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Category', y='Count', data=feature_data)
        plt.title(f'Distribution of {selected_feature_group}')
        plt.xticks(rotation=45)
        st.pyplot(plt)

    # Additional app features
    st.sidebar.header('Dataset Quick Look:')
    st.sidebar.write(f'Number of Datapoints: {data.shape[0]}')
    st.sidebar.write(f'Number of Features: {data.shape[1]}')