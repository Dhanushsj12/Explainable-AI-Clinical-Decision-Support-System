import { useState } from "react";
import API from "../services/api";
import PredictionCard from "./PredictionCard";
import FeatureImportance from "./FeatureImportance";
import PatientSummary from "./PatientSummary";

function PatientForm() {

    const [formData, setFormData] = useState({
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
        thal: "3"
    });

    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const fields = [

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

    const handleChange = (e) => {

        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });

    };

    const handleSubmit = async (e) => {

        e.preventDefault();

        setResult(null);

        const features = [

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

        setLoading(true);

        try {

            const response = await API.post("/predict", {
                features
            });

            setResult(response.data);

        }
        catch (error) {

            console.error(error);

            if (error.response) {

                alert(
                    `Prediction Failed\nStatus: ${error.response.status}\n${JSON.stringify(error.response.data)}`
                );

            }
            else {

                alert("Cannot connect to Flask backend.");

            }

        }
        finally {

            setLoading(false);

        }

    };

    const clearForm = () => {

        setFormData({

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
            thal: "3"

        });

        setResult(null);

    };
        return (

        <div className="container mt-5 mb-5">

            <div className="card shadow-lg border-0">

                <div className="card-header bg-primary text-white py-4">

                    <h3 className="mb-1">

                        🩺 Heart Disease Prediction

                    </h3>

                    <small>

                        Enter the patient's clinical information

                    </small>

                </div>

                <div className="card-body p-4">

                    <form onSubmit={handleSubmit}>

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
                                            value={formData[field.name]}
                                            onChange={handleChange}
                                        >

                                            {field.options.map((option) => (

                                                <option
                                                    key={option.value}
                                                    value={option.value}
                                                >

                                                    {option.label}

                                                </option>

                                            ))}

                                        </select>

                                    ) : (

                                        <input
                                            type="number"
                                            className="form-control"
                                            name={field.name}
                                            value={formData[field.name]}
                                            onChange={handleChange}
                                            placeholder={`Enter ${field.label}`}
                                            min="0"
                                            step="any"
                                            required
                                        />

                                    )}

                                </div>

                            ))}

                        </div>

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

                                    "🔍 Predict Heart Disease"

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

            {result && (

                <PatientSummary
                    formData={formData}
                />

            )}

            <PredictionCard
                result={result}
            />

            <FeatureImportance
                features={result?.top_features}
            />

        </div>

    );

}

export default PatientForm;