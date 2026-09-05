import { useState } from "react";
import API from "../services/api";
import PredictionCard from "./PredictionCard";
import FeatureImportance from "./FeatureImportance";
import PatientSummary from "./PatientSummary";
import {
    IconHeart,
    IconDroplet,
    IconKidney,
    IconBrain,
    IconDownload,
    IconRefresh
} from "./icons";

function PatientForm() {

    // ==========================================
    // DISEASE
    // ==========================================

    const [disease, setDisease] = useState("heart");

    const diseaseTabs = [
        { value: "heart", label: "Heart Disease", icon: IconHeart },
        { value: "diabetes", label: "Diabetes", icon: IconDroplet },
        { value: "ckd", label: "Chronic Kidney Disease", icon: IconKidney },
        { value: "stroke", label: "Stroke", icon: IconBrain }
    ];

    // ==========================================
    // INITIAL FORM DATA
    // ==========================================

    const initialFormData = {

        patient_id: "",
        patient_name: "",
        doctor_name: "",
        hospital_name: "",

        // ==========================================
        // HEART DISEASE
        // ==========================================

        age: "",
        sex: "1",
        cp: "1",
        trestbps: "",
        chol: "",
        fbs: "0",
        restecg: "0",
        thalach: "",
        exang: "0",
        oldpeak: "",
        slope: "2",
        ca: "0",
        thal: "3",

        // ==========================================
        // DIABETES
        // ==========================================

        gender: "1",
        polyuria: "0",
        polydipsia: "0",
        sudden_weight_loss: "0",
        weakness: "0",
        polyphagia: "0",
        genital_thrush: "0",
        visual_blurring: "0",
        itching: "0",
        irritability: "0",
        delayed_healing: "0",
        partial_paresis: "0",
        muscle_stiffness: "0",
        alopecia: "0",
        obesity: "0",

        // ==========================================
        // CKD
        // ==========================================

        bp: "",
        sg: "",
        al: "0",
        su: "0",
        rbc: "0",
        pc: "0",
        pcc: "0",
        ba: "0",
        bgr: "",
        bu: "",
        sc: "",
        sod: "",
        pot: "",
        hemo: "",
        pcv: "",
        wbcc: "",
        rbcc: "",
        htn: "0",
        dm: "0",
        cad: "0",
        appet: "0",
        pe: "0",
        ane: "0",

        // ==========================================
        // STROKE
        // ==========================================

        stroke_gender: "Male",
        stroke_age: "",
        hypertension: "0",
        heart_disease: "0",
        ever_married: "Yes",
        work_type: "Private",
        Residence_type: "Urban",
        avg_glucose_level: "",
        bmi: "",
        smoking_status: "never smoked"
    };

    const [formData, setFormData] = useState(initialFormData);

    const [result, setResult] = useState(null);

    const [loading, setLoading] = useState(false);


    // ==========================================
    // HEART DISEASE FIELDS
    // ==========================================

    const heartFields = [

        { name: "age", label: "Age", type: "number" },

        {
            name: "sex",
            label: "Gender",
            options: [
                { value: "1", label: "Male" },
                { value: "0", label: "Female" }
            ]
        },

        {
            name: "cp",
            label: "Chest Pain Type",
            options: [
                { value: "1", label: "Typical Angina" },
                { value: "2", label: "Atypical Angina" },
                { value: "3", label: "Non-anginal Pain" },
                { value: "4", label: "Asymptomatic" }
            ]
        },

        {
            name: "trestbps",
            label: "Resting Blood Pressure (mm Hg)",
            type: "number"
        },

        {
            name: "chol",
            label: "Cholesterol (mg/dL)",
            type: "number"
        },

        {
            name: "fbs",
            label: "Fasting Blood Sugar > 120 mg/dL",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "restecg",
            label: "Resting ECG",
            options: [
                { value: "0", label: "Normal" },
                { value: "1", label: "ST-T Wave Abnormality" },
                { value: "2", label: "Left Ventricular Hypertrophy" }
            ]
        },

        {
            name: "thalach",
            label: "Maximum Heart Rate",
            type: "number"
        },

        {
            name: "exang",
            label: "Exercise Induced Angina",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "oldpeak",
            label: "ST Depression",
            type: "number"
        },

        {
            name: "slope",
            label: "Slope of ST Segment",
            options: [
                { value: "1", label: "Upsloping" },
                { value: "2", label: "Flat" },
                { value: "3", label: "Downsloping" }
            ]
        },

        {
            name: "ca",
            label: "Major Vessels (0-3)",
            options: [
                { value: "0", label: "0" },
                { value: "1", label: "1" },
                { value: "2", label: "2" },
                { value: "3", label: "3" }
            ]
        },

        {
            name: "thal",
            label: "Thalassemia",
            options: [
                { value: "3", label: "Normal" },
                { value: "6", label: "Fixed Defect" },
                { value: "7", label: "Reversible Defect" }
            ]
        }

    ];


    // ==========================================
    // DIABETES FIELDS
    // ==========================================

    const diabetesFields = [

        {
            name: "age",
            label: "Age",
            type: "number"
        },

        {
            name: "gender",
            label: "Gender",
            options: [
                { value: "1", label: "Male" },
                { value: "0", label: "Female" }
            ]
        },

        {
            name: "polyuria",
            label: "Polyuria",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "polydipsia",
            label: "Polydipsia",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "sudden_weight_loss",
            label: "Sudden Weight Loss",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "weakness",
            label: "Weakness",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "polyphagia",
            label: "Polyphagia",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "genital_thrush",
            label: "Genital Thrush",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "visual_blurring",
            label: "Visual Blurring",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "itching",
            label: "Itching",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "irritability",
            label: "Irritability",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "delayed_healing",
            label: "Delayed Healing",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "partial_paresis",
            label: "Partial Paresis",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "muscle_stiffness",
            label: "Muscle Stiffness",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "alopecia",
            label: "Alopecia",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "obesity",
            label: "Obesity",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        }

    ];


    // ==========================================
    // CKD FIELDS
    // ==========================================

    const ckdFields = [

        {
            name: "age",
            label: "Age",
            type: "number"
        },

        {
            name: "bp",
            label: "Blood Pressure",
            type: "number"
        },

        {
            name: "sg",
            label: "Specific Gravity",
            type: "number",
            step: "0.001"
        },

        {
            name: "al",
            label: "Albumin",
            options: [
                { value: "0", label: "0" },
                { value: "1", label: "1" },
                { value: "2", label: "2" },
                { value: "3", label: "3" },
                { value: "4", label: "4" },
                { value: "5", label: "5" }
            ]
        },

        {
            name: "su",
            label: "Sugar",
            options: [
                { value: "0", label: "0" },
                { value: "1", label: "1" },
                { value: "2", label: "2" },
                { value: "3", label: "3" },
                { value: "4", label: "4" },
                { value: "5", label: "5" }
            ]
        },

        {
            name: "rbc",
            label: "Red Blood Cells",
            options: [
                { value: "0", label: "Normal" },
                { value: "1", label: "Abnormal" }
            ]
        },

        {
            name: "pc",
            label: "Pus Cell",
            options: [
                { value: "0", label: "Normal" },
                { value: "1", label: "Abnormal" }
            ]
        },

        {
            name: "pcc",
            label: "Pus Cell Clumps",
            options: [
                { value: "0", label: "Not Present" },
                { value: "1", label: "Present" }
            ]
        },

        {
            name: "ba",
            label: "Bacteria",
            options: [
                { value: "0", label: "Not Present" },
                { value: "1", label: "Present" }
            ]
        },

        {
            name: "bgr",
            label: "Blood Glucose Random",
            type: "number"
        },

        {
            name: "bu",
            label: "Blood Urea",
            type: "number"
        },

        {
            name: "sc",
            label: "Serum Creatinine",
            type: "number",
            step: "0.1"
        },

        {
            name: "sod",
            label: "Sodium",
            type: "number"
        },

        {
            name: "pot",
            label: "Potassium",
            type: "number",
            step: "0.1"
        },

        {
            name: "hemo",
            label: "Hemoglobin",
            type: "number",
            step: "0.1"
        },

        {
            name: "pcv",
            label: "Packed Cell Volume",
            type: "number"
        },

        {
            name: "wbcc",
            label: "White Blood Cell Count",
            type: "number"
        },

        {
            name: "rbcc",
            label: "Red Blood Cell Count",
            type: "number",
            step: "0.1"
        },

        {
            name: "htn",
            label: "Hypertension",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "dm",
            label: "Diabetes Mellitus",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "cad",
            label: "Coronary Artery Disease",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "appet",
            label: "Appetite",
            options: [
                { value: "0", label: "Good" },
                { value: "1", label: "Poor" }
            ]
        },

        {
            name: "pe",
            label: "Pedal Edema",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "ane",
            label: "Anemia",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        }

    ];


    // ==========================================
    // STROKE FIELDS
    // ==========================================

    const strokeFields = [

        {
            name: "stroke_gender",
            label: "Gender",
            type: "select",
            options: [
                { value: "Male", label: "Male" },
                { value: "Female", label: "Female" },
                { value: "Other", label: "Other" }
            ]
        },

        {
            name: "stroke_age",
            label: "Age",
            type: "number"
        },

        {
            name: "hypertension",
            label: "Hypertension",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "heart_disease",
            label: "Heart Disease",
            options: [
                { value: "1", label: "Yes" },
                { value: "0", label: "No" }
            ]
        },

        {
            name: "ever_married",
            label: "Ever Married",
            options: [
                { value: "Yes", label: "Yes" },
                { value: "No", label: "No" }
            ]
        },

        {
            name: "work_type",
            label: "Work Type",
            options: [
                { value: "Private", label: "Private" },
                { value: "Self-employed", label: "Self-employed" },
                { value: "Govt_job", label: "Government Job" },
                { value: "children", label: "Children" },
                { value: "Never_worked", label: "Never Worked" }
            ]
        },

        {
            name: "Residence_type",
            label: "Residence Type",
            options: [
                { value: "Urban", label: "Urban" },
                { value: "Rural", label: "Rural" }
            ]
        },

        {
            name: "avg_glucose_level",
            label: "Average Glucose Level",
            type: "number",
            step: "0.01"
        },

        {
            name: "bmi",
            label: "Body Mass Index (BMI)",
            type: "number",
            step: "0.1"
        },

        {
            name: "smoking_status",
            label: "Smoking Status",
            options: [
                {
                    value: "never smoked",
                    label: "Never Smoked"
                },
                {
                    value: "formerly smoked",
                    label: "Formerly Smoked"
                },
                {
                    value: "smokes",
                    label: "Currently Smokes"
                },
                {
                    value: "Unknown",
                    label: "Unknown"
                }
            ]
        }

    ];


    // ==========================================
    // GET CURRENT DISEASE FIELDS
    // ==========================================

    const getCurrentFields = () => {

        switch (disease) {

            case "heart":
                return heartFields;

            case "diabetes":
                return diabetesFields;

            case "ckd":
                return ckdFields;

            case "stroke":
                return strokeFields;

            default:
                return heartFields;
        }

    };

    const fields = getCurrentFields();


    // ==========================================
    // DISEASE DISPLAY NAME
    // ==========================================

    const getDiseaseName = () => {

        switch (disease) {

            case "heart":
                return "Heart Disease";

            case "diabetes":
                return "Diabetes";

            case "ckd":
                return "Chronic Kidney Disease";

            case "stroke":
                return "Stroke";

            default:
                return "Clinical Condition";
        }

    };

    const diseaseName = getDiseaseName();


    // ==========================================
    // CLINICAL SECTION TITLE
    // ==========================================

    const getClinicalTitle = () => {

        switch (disease) {

            case "heart":
                return "Heart Disease Clinical Features";

            case "diabetes":
                return "Diabetes Clinical Features";

            case "ckd":
                return "Chronic Kidney Disease Clinical Features";

            case "stroke":
                return "Stroke Clinical Features";

            default:
                return "Clinical Features";
        }

    };


    // ==========================================
    // HANDLE INPUT CHANGE
    // ==========================================

    const handleChange = (e) => {

        const { name, value } = e.target;

        setFormData((previousData) => ({
            ...previousData,
            [name]: value
        }));

    };


    // ==========================================
    // HANDLE DISEASE CHANGE
    // ==========================================

    const handleDiseaseChange = (e) => {

        const selectedDisease = e.target.value;

        setDisease(selectedDisease);

        setResult(null);

    };


    // ==========================================
    // BUILD FEATURES
    // ==========================================

    const buildFeatures = () => {

        // ==========================================
        // HEART
        // ==========================================

        if (disease === "heart") {

            return [
                Number(formData.age),
                Number(formData.sex),
                Number(formData.cp),
                Number(formData.trestbps),
                Number(formData.chol),
                Number(formData.fbs),
                Number(formData.restecg),
                Number(formData.thalach),
                Number(formData.exang),
                Number(formData.oldpeak),
                Number(formData.slope),
                Number(formData.ca),
                Number(formData.thal)
            ];

        }


        // ==========================================
        // DIABETES
        // ==========================================

        if (disease === "diabetes") {

            return [
                Number(formData.age),
                Number(formData.gender),
                Number(formData.polyuria),
                Number(formData.polydipsia),
                Number(formData.sudden_weight_loss),
                Number(formData.weakness),
                Number(formData.polyphagia),
                Number(formData.genital_thrush),
                Number(formData.visual_blurring),
                Number(formData.itching),
                Number(formData.irritability),
                Number(formData.delayed_healing),
                Number(formData.partial_paresis),
                Number(formData.muscle_stiffness),
                Number(formData.alopecia),
                Number(formData.obesity)
            ];

        }


        // ==========================================
        // CKD
        // ==========================================

        if (disease === "ckd") {

            return [
                Number(formData.age),
                Number(formData.bp),
                Number(formData.sg),
                Number(formData.al),
                Number(formData.su),
                Number(formData.rbc),
                Number(formData.pc),
                Number(formData.pcc),
                Number(formData.ba),
                Number(formData.bgr),
                Number(formData.bu),
                Number(formData.sc),
                Number(formData.sod),
                Number(formData.pot),
                Number(formData.hemo),
                Number(formData.pcv),
                Number(formData.wbcc),
                Number(formData.rbcc),
                Number(formData.htn),
                Number(formData.dm),
                Number(formData.cad),
                Number(formData.appet),
                Number(formData.pe),
                Number(formData.ane)
            ];

        }


        // ==========================================
        // STROKE
        // ==========================================

        if (disease === "stroke") {

            return {
                gender: formData.stroke_gender,
                age: Number(formData.stroke_age),
                hypertension: Number(formData.hypertension),
                heart_disease: Number(formData.heart_disease),
                ever_married: formData.ever_married,
                work_type: formData.work_type,
                Residence_type: formData.Residence_type,
                avg_glucose_level: Number(formData.avg_glucose_level),
                bmi: Number(formData.bmi),
                smoking_status: formData.smoking_status
            };

        }


        return [];

    };


    // ==========================================
    // SUBMIT FORM
    // ==========================================

    const handleSubmit = async (e) => {

        e.preventDefault();

        setResult(null);

        setLoading(true);

        try {

            const features = buildFeatures();

            const requestData = {
                disease: disease,
                features: features,
                patient_id: formData.patient_id,
                patient_name: formData.patient_name,
                doctor_name: formData.doctor_name,
                hospital_name: formData.hospital_name
            };

            console.log(
                "Sending prediction request:",
                requestData
            );

            const response = await API.post(
                "/predict",
                requestData
            );

            console.log(
                "Prediction response:",
                response.data
            );

            setResult(response.data);

        }

        catch (error) {

            console.error(
                "Prediction error:",
                error
            );

            if (error.response) {

                alert(
                    `Prediction Failed\n\n` +
                    `Status: ${error.response.status}\n\n` +
                    `${JSON.stringify(
                        error.response.data,
                        null,
                        2
                    )}`
                );

            }

            else {

                alert(
                    "Cannot connect to Flask backend.\n\n" +
                    "Please make sure the backend server is running."
                );

            }

        }

        finally {

            setLoading(false);

        }

    };


    // ==========================================
    // RESET FORM
    // ==========================================

    const clearForm = () => {

        setFormData({
            ...initialFormData
        });

        setResult(null);

    };


    // ==========================================
    // DOWNLOAD CLINICAL REPORT
    // ==========================================

    const downloadReport = async () => {

        try {

            const features = buildFeatures();

            // ==========================================
            // IMPORTANT:
            // Send the SAME LIME explanation that was
            // already generated during /predict.
            //
            // This prevents /report from generating
            // another random/different LIME explanation.
            // ==========================================

            const requestData = {
                disease: disease,
                features: features,
                patient_id: formData.patient_id,
                patient_name: formData.patient_name,
                doctor_name: formData.doctor_name,
                hospital_name: formData.hospital_name,

                lime_features: result?.lime_features || []
            };

            console.log(
                "Sending report request:",
                requestData
            );

            console.log(
                "Using existing LIME explanation:",
                result?.lime_features
            );

            const response = await API.post(
                "/report",
                requestData,
                {
                    responseType: "blob"
                }
            );

            const blob = new Blob(
                [response.data],
                {
                    type: "application/pdf"
                }
            );

            const url =
                window.URL.createObjectURL(blob);

            const link =
                document.createElement("a");

            link.href = url;

            link.download =
                `${disease}_Clinical_Report.pdf`;

            document.body.appendChild(link);

            link.click();

            document.body.removeChild(link);

            window.URL.revokeObjectURL(url);

        }

        catch (error) {

            console.error(
                "Report generation error:",
                error
            );

            alert(
                "Unable to download clinical report."
            );

        }

    };


    // ==========================================
    // RENDER
    // ==========================================

    return (

        <div className="wrap mt-24">

            <div className="panel">

                <div className="panel-header">

                    <div className="icon-badge">
                        <IconHeart size={17} />
                    </div>

                    <div>

                        <div className="panel-title">
                            Assessment Console
                        </div>

                        <div className="panel-title-sub">
                            Select one condition · enter observed clinical parameters · run inference
                        </div>

                    </div>

                </div>


                <div className="tabs">

                    {diseaseTabs.map((tab) => {

                        const Icon = tab.icon;

                        return (

                            <button
                                key={tab.value}
                                type="button"
                                className={`tab ${
                                    disease === tab.value
                                        ? "active"
                                        : ""
                                }`}
                                onClick={() =>
                                    handleDiseaseChange({
                                        target: {
                                            value: tab.value
                                        }
                                    })
                                }
                            >

                                <Icon size={16} />

                                {tab.label}

                            </button>

                        );

                    })}

                </div>


                <form onSubmit={handleSubmit}>

                    <div className="section-block">

                        <div className="section-heading">

                            <span className="section-marker"></span>

                            <h3>
                                01 · Patient Identification
                            </h3>

                            <span className="section-index">
                                REQUIRED
                            </span>

                        </div>


                        <div className="field-grid">

                            {[
                                [
                                    "patient_id",
                                    "Patient ID",
                                    "text",
                                    "Enter patient ID"
                                ],
                                [
                                    "patient_name",
                                    "Patient Name",
                                    "text",
                                    "Enter patient name"
                                ],
                                [
                                    "doctor_name",
                                    "Doctor Name",
                                    "text",
                                    "Enter clinician name"
                                ],
                                [
                                    "hospital_name",
                                    "Hospital / Clinic",
                                    "text",
                                    "Enter facility name"
                                ]
                            ].map(
                                ([
                                    name,
                                    label,
                                    type,
                                    placeholder
                                ]) => (

                                    <div
                                        className="field"
                                        key={name}
                                    >

                                        <label className="field-label">
                                            {label}
                                        </label>

                                        <input
                                            type={type}
                                            name={name}
                                            value={formData[name]}
                                            onChange={handleChange}
                                            placeholder={placeholder}
                                            required
                                        />

                                    </div>

                                )
                            )}

                        </div>

                    </div>


                    <div className="section-block">

                        <div className="section-heading">

                            <span className="section-marker"></span>

                            <h3>
                                02 · {getClinicalTitle()}
                            </h3>

                            <span className="section-index">

                                {fields.length
                                    .toString()
                                    .padStart(2, "0")}{" "}
                                PARAMETERS

                            </span>

                        </div>


                        <div className="field-grid">

                            {fields.map((field) => (

                                <div
                                    key={field.name}
                                    className="field"
                                >

                                    <label className="field-label">
                                        {field.label}
                                    </label>


                                    {field.options ? (

                                        <select
                                            name={field.name}
                                            value={
                                                formData[field.name]
                                            }
                                            onChange={handleChange}
                                            required
                                        >

                                            {field.options.map(
                                                (option) => (

                                                    <option
                                                        key={
                                                            option.value
                                                        }
                                                        value={
                                                            option.value
                                                        }
                                                    >
                                                        {option.label}
                                                    </option>

                                                )
                                            )}

                                        </select>

                                    ) : (

                                        <input
                                            type={
                                                field.type ||
                                                "number"
                                            }
                                            name={field.name}
                                            value={
                                                formData[field.name]
                                            }
                                            onChange={handleChange}
                                            placeholder={
                                                `Enter ${field.label}`
                                            }
                                            min="0"
                                            step={
                                                field.step ||
                                                "any"
                                            }
                                            required
                                        />

                                    )}

                                </div>

                            ))}

                        </div>

                    </div>


                    <div className="btn-row">

                        <button
                            type="submit"
                            className="btn btn-primary btn-block"
                            disabled={loading}
                        >

                            {loading ? (

                                <>
                                    <span className="spinner"></span>
                                    Running Model
                                </>

                            ) : (

                                <>
                                    ⚡ Run {diseaseName} Assessment
                                </>

                            )}

                        </button>


                        <button
                            type="button"
                            className="btn btn-outline btn-block"
                            onClick={clearForm}
                        >

                            <IconRefresh size={15} />

                            Clear Case

                        </button>

                    </div>

                </form>

            </div>


            {result && (

                <>

                    <PatientSummary
                        formData={formData}
                        disease={disease}
                    />

                    <div className="summary-actions">

                        <button
                            className="btn btn-outline"
                            onClick={downloadReport}
                        >

                            <IconDownload size={16} />

                            Export Clinical PDF

                        </button>

                    </div>

                </>

            )}


            <PredictionCard
                result={result}
                disease={disease}
            />


            <FeatureImportance
                features={result?.top_features}
                limeFeatures={result?.lime_features}
            />

        </div>

    );

}

export default PatientForm;