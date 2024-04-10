import streamlit as st
import pickle
import numpy as np


def load_lrmodel():
    with open('/mount/src/predictapp/LogisticRegression(L1).pickle', 'rb') as file:
        model = pickle.load(file)
    return model


def load_svmmodel():
    with open('/mount/src/predictapp/SVC.pickle', 'rb') as file:
        model = pickle.load(file)
    return model


lrmodel = load_lrmodel()
svmmodel = load_svmmodel()


def show_predict_page():
    st.title("Mobile Network Churn Predictor")

    st.write("""### We need some information to predict churn""")

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

    Pcontainer = st.container(border=True)
    Pcontainer.header("Payment information")
    col1, col2 = Pcontainer.columns(2)
    with col1:
        monthlyc = st.slider("monthly charges", 0.00, 120.00, 35.00)
    with col2:
        tenure = st.slider("tenure in months", 0, 72, 3)
        totc = monthlyc * tenure
    Pcontainer.markdown(f"Your total charges for your tenure is :green[${totc:.2f}]")
    col1, col2, col3 = Pcontainer.columns(3)
    with col1:
        Contract = st.selectbox("Contract", Contr)
    with col2:
        PaymentMethod = st.selectbox("Payment Method", payM)
    with col3:
        PaperlessBilling = st.selectbox("Paperless Billing", PprB)

    Ccontainer = st.container(border=True)
    Ccontainer.header("Customer information")
    col1, col2, col3 = Ccontainer.columns(3)
    with col1:
        SeniorCitizen = st.selectbox("Senior Citizen", SenC)
    with col2:
        Partner = st.selectbox("Partner", Partner)
    with col3:
        Dependents = st.selectbox("Dependents", Depe)

    Icontainer = st.container(border=True)
    Icontainer.header("Internet services information")
    InternetService = Icontainer.selectbox("Internet Service", IntS)
    Icontainer.markdown("*If you don't have internet service, Services below will not be available*")
    disabled = InternetService == "No"  # Disable options if "No" is selected

    col1, col2 = Icontainer.columns(2)

    with col1:
        TechSupport = st.selectbox("Tech Support", TechS, disabled=disabled)
    with col2:
        DeviceProtection = st.selectbox("Device Protection", DevP, disabled=disabled)

    col1, col2, col3 = Icontainer.columns(3)

    with col1:
        OnlineSecurity = st.selectbox("Online Security", OnlSec, disabled=disabled)
    with col2:
        OnlineBackup = st.selectbox("Online Backup", OnlBackup, disabled=disabled)
    with col3:
        StreamingTV = st.selectbox("Streaming TV", StrTV, disabled=disabled)

    def generate_feature_values(tenure, monthlyc, totc, PaymentMethod, TechSupport, InternetService, Partner,
                                Contract,
                                OnlineBackup, DeviceProtection, OnlineSecurity, StreamingTV, SeniorCitizen,
                                PaperlessBilling, Dependents):

        feature_values = [tenure, monthlyc, totc]

        if PaperlessBilling == 'No':
            feature_values.extend([True, False])
        else:
            feature_values.extend([False, True])

        if Partner == 'No':
            feature_values.extend([True, False])
        else:
            feature_values.extend([False, True])

        if InternetService == 'DSL':
            feature_values.extend([True, False, False])
        elif InternetService == 'Fiber optic':
            feature_values.extend([False, True, False])
        else:
            feature_values.extend([False, False, True])

        if OnlineBackup == 'No':
            feature_values.extend([True, False, False])
        elif OnlineBackup == 'No internet service':
            feature_values.extend([False, True, False])
        else:
            feature_values.extend([False, False, True])

        if Dependents == 'No':
            feature_values.extend([True, False])
        else:
            feature_values.extend([False, True])

        if SeniorCitizen == 'No':
            feature_values.extend([True, False])
        else:
            feature_values.extend([False, True])

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

        if TechSupport == 'No':
            feature_values.extend([True, False, False])
        elif TechSupport == 'No internet service':
            feature_values.extend([False, True, False])
        else:
            feature_values.extend([False, False, True])

        if Contract == 'Month-to-month':
            feature_values.extend([True, False, False])
        elif Contract == 'One year':
            feature_values.extend([False, True, False])
        else:
            feature_values.extend([False, False, True])

        if StreamingTV == 'No':
            feature_values.extend([True, False, False])
        elif StreamingTV == 'No internet service':
            feature_values.extend([False, True, False])
        else:
            feature_values.extend([False, False, True])

        if PaymentMethod == 'Bank transfer':
            feature_values.extend([True, False, False, False])
        elif PaymentMethod == 'Credit card (automatic)':
            feature_values.extend([False, True, False, False])
        elif PaymentMethod == 'Electronic check':
            feature_values.extend([False, False, True, False])
        else:
            feature_values.extend([False, False, False, True])

        return feature_values

    ok = st.button("Predict churn")
    if ok:
        feature_values = generate_feature_values(tenure, monthlyc, totc, PaymentMethod, TechSupport, InternetService,
                                                 Partner, Contract, OnlineBackup, DeviceProtection, OnlineSecurity,
                                                 StreamingTV, SeniorCitizen, PaperlessBilling, Dependents)
        print(feature_values)

        lrprediction = lrmodel.predict([feature_values])
        svmprediction = svmmodel.predict([feature_values])
        st.markdown(f"Logistic regression predicts that you will :yellow[{lrprediction}]")
        st.markdown(f"SVM predicts that you will :blue[{svmprediction}]")
