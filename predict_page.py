import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('LogisticRegression(L1).pickle', 'rb') as file:
        model = pickle.load(file)
    return model


model = load_model()


def show_predict_page():
    st.title("Mobile Network Churn Predictor")

    st.write("""### We need some information to predict the salary""")

    payM = (
        "Bank transfer",
        "Credit card (automatic)",
        "Electronic check",
        "Mailed check"
    )

    TechS = (
        "No internet service",
        "No",
        "Yes"
    )

    IntS = (
        "DSL",
        "Fiber optic",
        "No"
    )

    Partner = (
        "No",
        "Yes"
    )

    Contr = (
        "Month-to-month",
        "One year",
        "Two year"
    )

    OnlBackup = (
        "No internet service",
        "No",
        "Yes"
    )

    DevP = (
        "No internet service",
        "No",
        "Yes"
    )

    OnlSec = (
        "No internet service",
        "No",
        "Yes"
    )

    StrTV = (
        "No internet service",
        "No",
        "Yes"
    )

    SenC = (
        "No",
        "Yes"
    )

    PprB = (
        "No",
        "Yes"
    )

    Depe = (
        "No",
        "Yes"
    )

    tenure = st.slider("tenure in months", 0, 50, 3)
    monthlyc = st.slider("monthly charges", 0, 50, 3)
    totc = monthlyc * tenure
    PaymentMethod = st.selectbox("Payment Method", payM)
    Contract = st.selectbox("Contract", Contr)
    InternetService = st.selectbox("Internet Service", IntS)
    SeniorCitizen = st.selectbox("Senior Citizen", SenC)
    PaperlessBilling = st.selectbox("Paperless Billing", PprB)
    Partner = st.selectbox("Partner", Partner)
    Dependents = st.selectbox("Dependents", Depe)

    disabled = InternetService == "No"  # Disable options if "No" is selected

    TechSupport = st.selectbox("Tech Support", TechS, disabled=disabled)
    OnlineBackup = st.selectbox("Online Backup", OnlBackup, disabled=disabled)
    DeviceProtection = st.selectbox("Device Protection", DevP, disabled=disabled)
    OnlineSecurity = st.selectbox("Online Security", OnlSec, disabled=disabled)
    StreamingTV = st.selectbox("Streaming TV", StrTV, disabled=disabled)

    def generate_feature_values(tenure, monthlyc, totc, PaymentMethod, TechSupport, InternetService, Partner,
                                Contract,
                                OnlineBackup, DeviceProtection, OnlineSecurity, StreamingTV, SeniorCitizen,
                                PaperlessBilling, Dependents):

        feature_values = [tenure, monthlyc, totc]

        if PaymentMethod == 'Bank transfer':
            feature_values.extend([True, False, False, False])
        elif PaymentMethod == 'Credit card (automatic)':
            feature_values.extend([False, True, False, False])
        elif PaymentMethod == 'Electronic check':
            feature_values.extend([False, False, True, False])
        else:
            feature_values.extend([False, False, False, True])

        if TechSupport == 'No':
            feature_values.extend([True, False, False])
        elif TechSupport == 'No internet service':
            feature_values.extend([False, True, False])
        else:
            feature_values.extend([False, False, True])

        if InternetService == 'DSL':
            feature_values.extend([True, False, False])
        elif InternetService == 'Fiber optic':
            feature_values.extend([False, True, False])
        else:
            feature_values.extend([False, False, True])

        if Partner == 'No':
            feature_values.extend([True, False])
        else:
            feature_values.extend([False, True])

        if Contract == 'Month-to-month':
            feature_values.extend([True, False, False])
        elif Contract == 'One year':
            feature_values.extend([False, True, False])
        else:
            feature_values.extend([False, False, True])

        if OnlineBackup == 'No':
            feature_values.extend([True, False, False])
        elif OnlineBackup == 'No internet service':
            feature_values.extend([False, True, False])
        else:
            feature_values.extend([False, False, True])

        if DeviceProtection == 'No':
            feature_values.extend([True, False, False])
        elif DeviceProtection == 'No internet service':
            feature_values.extend([False, True, False])
        else:
            feature_values.extend([False, False, True])

        if OnlineSecurity == 'No':
            feature_values.extend([True, False, False])
        elif OnlineSecurity == 'No internet service':
            feature_values.extend([False, True, False])
        else:
            feature_values.extend([False, False, True])

        if StreamingTV == 'No':
            feature_values.extend([True, False, False])
        elif StreamingTV == 'No internet service':
            feature_values.extend([False, True, False])
        else:
            feature_values.extend([False, False, True])

        if SeniorCitizen == 'No':
            feature_values.extend([True, False])
        else:
            feature_values.extend([False, True])

        if PaperlessBilling == 'No':
            feature_values.extend([True, False])
        else:
            feature_values.extend([False, True])

        if Dependents == 'No':
            feature_values.extend([True, False])
        else:
            feature_values.extend([False, True])

        return feature_values

    ok = st.button("Calculate Salary")
    if ok:
        feature_values = generate_feature_values(tenure, monthlyc, totc, PaymentMethod, TechSupport, InternetService,
                                                 Partner, Contract, OnlineBackup, DeviceProtection, OnlineSecurity,
                                                 StreamingTV, SeniorCitizen, PaperlessBilling, Dependents)
        print(feature_values)

        prediction = model.predict([feature_values])
        print(prediction)
        st.subheader(prediction)
