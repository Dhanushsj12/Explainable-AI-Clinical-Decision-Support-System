import { useState } from "react";
import API from "../services/api";
import PredictionCard from "./PredictionCard";
import FeatureImportance from "./FeatureImportance";
import PatientSummary from "./PatientSummary";

function PatientForm() {

    const [disease, setDisease] = useState("heart");

    const [formData, setFormData] = useState({
        patient_id: "",
        patient_name: "",
        doctor_name: "",
        hospital_name: "",

        // =========================
        // Heart Disease
        // =========================
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

        // =========================
        // Diabetes
        // =========================
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

        // =========================
        // CKD
        // =========================
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
        ane: "0"
    });

    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);


    // ==========================================
    // HEART DISEASE FIELDS
    // ==========================================

    const heartFields = [

        {
            name: "age",
            label: "Age",
            type: "number"
        },

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
    // CURRENT FIELDS
    // ==========================================

    const fields =
        disease === "heart"
            ? heartFields
            : disease === "diabetes"
                ? diabetesFields
                : ckdFields;


    // ==========================================
    // HANDLE CHANGE
    // ==========================================

    const handleChange = (e) => {

        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });

    };


    // ==========================================
    // DISEASE CHANGE
    // ==========================================

    const handleDiseaseChange = (e) => {

        setDisease(e.target.value);

        setResult(null);

    };


    // ==========================================
    // BUILD FEATURES
    // ==========================================

    const buildFeatures = () => {

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

        // CKD - 24 features
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

    };


    // ==========================================
    // SUBMIT
    // ==========================================

    const handleSubmit = async (e) => {

        e.preventDefault();

        setResult(null);
        setLoading(true);

        const features = buildFeatures();

        try {

            const requestData = {

                disease,

                features,

                patient_id: formData.patient_id,

                patient_name: formData.patient_name,

                doctor_name: formData.doctor_name,

                hospital_name: formData.hospital_name

            };

            console.log(
                "Sending to backend:",
                requestData
            );

            const response = await API.post(
                "/predict",
                requestData
            );

            setResult(response.data);

        }

        catch (error) {

            console.error(error);

            if (error.response) {

                alert(
                    `Prediction Failed\nStatus: ${error.response.status}\n${JSON.stringify(error.response.data)}`
                );

            } else {

                alert(
                    "Cannot connect to Flask backend."
                );

            }

        }

        finally {

            setLoading(false);

        }

    };


    // ==========================================
    // RESET
    // ==========================================

    const clearForm = () => {

        setFormData({

            patient_id: "",
            patient_name: "",
            doctor_name: "",
            hospital_name: "",

            // Heart
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

            // Diabetes
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

            // CKD
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
            ane: "0"

        });

        setResult(null);

    };


    // ==========================================
    // DOWNLOAD REPORT
    // ==========================================

    const downloadReport = async () => {

        const features = buildFeatures();

        try {

            const response = await API.post(

                "/report",

                {

                    disease,

                    features,

                    patient_id: formData.patient_id,

                    patient_name: formData.patient_name,

                    doctor_name: formData.doctor_name,

                    hospital_name: formData.hospital_name

                },

                {

                    responseType: "blob"

                }

            );

            const url =
                window.URL.createObjectURL(
                    new Blob([response.data])
                );

            const link =
                document.createElement("a");

            link.href = url;

            link.download =
                `${disease}_Clinical_Report.pdf`;

            document.body.appendChild(link);

            link.click();

            link.remove();

            window.URL.revokeObjectURL(url);

        }

        catch (error) {

            console.error(error);

            alert(
                "Unable to download report."
            );

        }

    };


    // ==========================================
    // DISPLAY LABEL
    // ==========================================

    const diseaseName =
        disease === "heart"
            ? "Heart Disease"
            : disease === "diabetes"
                ? "Diabetes"
                : "Chronic Kidney Disease";


    return (

        <div className="container mt-5 mb-5">

            <div className="card shadow-lg border-0">

                {/* HEADER */}

                <div className="card-header bg-primary text-white py-4">

                    <h3 className="mb-1">

                        🩺 {diseaseName} Prediction

                    </h3>

                    <small>

                        Enter the patient's clinical information

                    </small>

                </div>


                <div className="card-body p-4">

                    {/* DISEASE SELECTOR */}

                    <div className="mb-4">

                        <label className="form-label fw-bold">

                            Select Disease

                        </label>

                        <select
                            className="form-select form-select-lg"
                            value={disease}
                            onChange={handleDiseaseChange}
                        >

                            <option value="heart">
                                Heart Disease
                            </option>

                            <option value="diabetes">
                                Diabetes
                            </option>

                            <option value="ckd">
                                Chronic Kidney Disease
                            </option>

                        </select>

                    </div>


                    <form onSubmit={handleSubmit}>

                        {/* PATIENT DETAILS */}

                        <div className="row">

                            <div className="col-md-6 mb-3">

                                <label className="form-label fw-bold">
                                    Patient ID
                                </label>

                                <input
                                    type="text"
                                    className="form-control"
                                    name="patient_id"
                                    value={formData.patient_id}
                                    onChange={handleChange}
                                    placeholder="Enter Patient ID"
                                    required
                                />

                            </div>


                            <div className="col-md-6 mb-3">

                                <label className="form-label fw-bold">
                                    Patient Name
                                </label>

                                <input
                                    type="text"
                                    className="form-control"
                                    name="patient_name"
                                    value={formData.patient_name}
                                    onChange={handleChange}
                                    placeholder="Enter Patient Name"
                                    required
                                />

                            </div>


                            <div className="col-md-6 mb-3">

                                <label className="form-label fw-bold">
                                    Doctor Name
                                </label>

                                <input
                                    type="text"
                                    className="form-control"
                                    name="doctor_name"
                                    value={formData.doctor_name}
                                    onChange={handleChange}
                                    placeholder="Enter Doctor Name"
                                    required
                                />

                            </div>


                            <div className="col-md-6 mb-3">

                                <label className="form-label fw-bold">
                                    Hospital Name
                                </label>

                                <input
                                    type="text"
                                    className="form-control"
                                    name="hospital_name"
                                    value={formData.hospital_name}
                                    onChange={handleChange}
                                    placeholder="Enter Hospital Name"
                                    required
                                />

                            </div>

                        </div>


                        <hr />


                        {/* DISEASE FIELDS */}

                        <h5 className="mb-3">

                            {disease === "heart"
                                ? "Heart Disease Clinical Features"
                                : disease === "diabetes"
                                    ? "Diabetes Clinical Features"
                                    : "Chronic Kidney Disease Clinical Features"}

                        </h5>


                        <div className="row">

                            {fields.map((field) => (

                                <div
                                    key={field.name}
                                    className="col-md-6 mb-3"
                                >

                                    <label className="form-label fw-bold">

                                        {field.label}

                                    </label>


                                    {field.options ? (

                                        <select
                                            className="form-select"
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
                                                        key={option.value}
                                                        value={option.value}
                                                    >

                                                        {option.label}

                                                    </option>

                                                )
                                            )}

                                        </select>

                                    ) : (

                                        <input
                                            type={
                                                field.type || "number"
                                            }
                                            className="form-control"
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
                                                field.step || "any"
                                            }
                                            required
                                        />

                                    )}

                                </div>

                            ))}

                        </div>


                        {/* BUTTONS */}

                        <div className="d-flex gap-3 mt-3">

                            <button
                                type="submit"
                                className="btn btn-primary btn-lg flex-fill"
                                disabled={loading}
                            >

                                {loading ? (

                                    <>

                                        <span
                                            className="spinner-border spinner-border-sm me-2"
                                            role="status"
                                            aria-hidden="true"
                                        ></span>

                                        Predicting...

                                    </>

                                ) : (

                                    `Predict ${diseaseName}`

                                )}

                            </button>


                            <button
                                type="button"
                                className="btn btn-outline-secondary btn-lg flex-fill"
                                onClick={clearForm}
                            >

                                🔄 Reset

                            </button>

                        </div>

                    </form>

                </div>

            </div>


            {/* RESULTS */}

            {result && (

                <>

                    <PatientSummary
                        formData={formData}
                        disease={disease}
                    />

                    <div className="text-center mt-4 mb-4">

                        <button
                            className="btn btn-success btn-lg"
                            onClick={downloadReport}
                        >

                            📄 Download Clinical Report

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