function PatientSummary({ formData, disease }) {

    if (!formData) return null;

    // ==========================================
    // Gender
    // ==========================================

    const getGender = () => {

        if (disease === "diabetes") {
            return formData.gender === "1"
                ? "Male"
                : "Female";
        }

        if (disease === "stroke") {
            return formData.stroke_gender || formData.gender || "";
        }

        return formData.sex === "1"
            ? "Male"
            : "Female";
    };


    // ==========================================
    // Yes / No
    // ==========================================

    const yesNo = (value) => {

        if (value === "1" || value === 1 || value === true) {
            return "Yes";
        }

        return "No";
    };


    // ==========================================
    // Disease Name
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
                return "";
        }
    };


    // ==========================================
    // Heart Chest Pain
    // ==========================================

    const getChestPain = (value) => {

        const chestPainTypes = {

            "1": "Typical Angina",
            "2": "Atypical Angina",
            "3": "Non-anginal Pain",
            "4": "Asymptomatic"

        };

        return chestPainTypes[value] || value;
    };


    // ==========================================
    // Stroke Yes / No
    // ==========================================

    const strokeYesNo = (value) => {

        if (
            value === "1" ||
            value === 1 ||
            value === true ||
            value === "Yes"
        ) {
            return "Yes";
        }

        if (
            value === "0" ||
            value === 0 ||
            value === false ||
            value === "No"
        ) {
            return "No";
        }

        return value;
    };


    // ==========================================
    // Main UI
    // ==========================================

    return (

        <div className="card shadow-lg mt-4">

            <div className="card-header bg-info text-white">

                <h4 className="mb-0">
                    👤 Patient Summary
                </h4>

            </div>


            <div className="card-body">

                {/* ======================================
                    Patient Details
                ====================================== */}

                <h5 className="mb-3">
                    Patient Details
                </h5>


                <p>
                    <b>Patient ID:</b>{" "}
                    {formData.patient_id}
                </p>


                <p>
                    <b>Patient Name:</b>{" "}
                    {formData.patient_name}
                </p>


                <p>
                    <b>Doctor:</b>{" "}
                    {formData.doctor_name}
                </p>


                <p>
                    <b>Hospital:</b>{" "}
                    {formData.hospital_name}
                </p>


                <p>
                    <b>Disease:</b>{" "}
                    {getDiseaseName()}
                </p>


                <hr />


                <h5 className="mb-3">
                    Clinical Information
                </h5>


                {/* ======================================
                    HEART DISEASE
                ====================================== */}

                {disease === "heart" && (

                    <table className="table table-bordered">

                        <tbody>

                            <tr>

                                <td>
                                    <b>Age</b>
                                </td>

                                <td>
                                    {formData.age}
                                </td>

                                <td>
                                    <b>Gender</b>
                                </td>

                                <td>
                                    {getGender()}
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>Chest Pain</b>
                                </td>

                                <td>
                                    {getChestPain(formData.cp)}
                                </td>

                                <td>
                                    <b>Blood Pressure</b>
                                </td>

                                <td>
                                    {formData.trestbps} mmHg
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>Cholesterol</b>
                                </td>

                                <td>
                                    {formData.chol} mg/dL
                                </td>

                                <td>
                                    <b>Fasting Blood Sugar</b>
                                </td>

                                <td>
                                    {yesNo(formData.fbs)}
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>Resting ECG</b>
                                </td>

                                <td>
                                    {formData.restecg}
                                </td>

                                <td>
                                    <b>Maximum Heart Rate</b>
                                </td>

                                <td>
                                    {formData.thalach}
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>Exercise Angina</b>
                                </td>

                                <td>
                                    {yesNo(formData.exang)}
                                </td>

                                <td>
                                    <b>ST Depression</b>
                                </td>

                                <td>
                                    {formData.oldpeak}
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>ST Segment Slope</b>
                                </td>

                                <td>
                                    {formData.slope}
                                </td>

                                <td>
                                    <b>Major Vessels</b>
                                </td>

                                <td>
                                    {formData.ca}
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>Thalassemia</b>
                                </td>

                                <td>
                                    {formData.thal}
                                </td>

                                <td></td>
                                <td></td>

                            </tr>

                        </tbody>

                    </table>

                )}


                {/* ======================================
                    DIABETES
                ====================================== */}

                {disease === "diabetes" && (

                    <table className="table table-bordered">

                        <tbody>

                            <tr>

                                <td>
                                    <b>Age</b>
                                </td>

                                <td>
                                    {formData.age}
                                </td>

                                <td>
                                    <b>Gender</b>
                                </td>

                                <td>
                                    {getGender()}
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>Polyuria</b>
                                </td>

                                <td>
                                    {yesNo(formData.polyuria)}
                                </td>

                                <td>
                                    <b>Polydipsia</b>
                                </td>

                                <td>
                                    {yesNo(formData.polydipsia)}
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>Sudden Weight Loss</b>
                                </td>

                                <td>
                                    {yesNo(formData.sudden_weight_loss)}
                                </td>

                                <td>
                                    <b>Weakness</b>
                                </td>

                                <td>
                                    {yesNo(formData.weakness)}
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>Polyphagia</b>
                                </td>

                                <td>
                                    {yesNo(formData.polyphagia)}
                                </td>

                                <td>
                                    <b>Genital Thrush</b>
                                </td>

                                <td>
                                    {yesNo(formData.genital_thrush)}
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>Visual Blurring</b>
                                </td>

                                <td>
                                    {yesNo(formData.visual_blurring)}
                                </td>

                                <td>
                                    <b>Itching</b>
                                </td>

                                <td>
                                    {yesNo(formData.itching)}
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>Irritability</b>
                                </td>

                                <td>
                                    {yesNo(formData.irritability)}
                                </td>

                                <td>
                                    <b>Delayed Healing</b>
                                </td>

                                <td>
                                    {yesNo(formData.delayed_healing)}
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>Partial Paresis</b>
                                </td>

                                <td>
                                    {yesNo(formData.partial_paresis)}
                                </td>

                                <td>
                                    <b>Muscle Stiffness</b>
                                </td>

                                <td>
                                    {yesNo(formData.muscle_stiffness)}
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>Alopecia</b>
                                </td>

                                <td>
                                    {yesNo(formData.alopecia)}
                                </td>

                                <td>
                                    <b>Obesity</b>
                                </td>

                                <td>
                                    {yesNo(formData.obesity)}
                                </td>

                            </tr>

                        </tbody>

                    </table>

                )}


                {/* ======================================
                    CKD
                ====================================== */}

                {disease === "ckd" && (

                    <table className="table table-bordered">

                        <tbody>

                            <tr>
                                <td><b>Age</b></td>
                                <td>{formData.age}</td>

                                <td><b>Blood Pressure</b></td>
                                <td>{formData.bp}</td>
                            </tr>

                            <tr>
                                <td><b>Specific Gravity</b></td>
                                <td>{formData.sg}</td>

                                <td><b>Albumin</b></td>
                                <td>{formData.al}</td>
                            </tr>

                            <tr>
                                <td><b>Sugar</b></td>
                                <td>{formData.su}</td>

                                <td><b>Red Blood Cells</b></td>
                                <td>{formData.rbc}</td>
                            </tr>

                            <tr>
                                <td><b>Pus Cell</b></td>
                                <td>{formData.pc}</td>

                                <td><b>Pus Cell Clumps</b></td>
                                <td>{formData.pcc}</td>
                            </tr>

                            <tr>
                                <td><b>Bacteria</b></td>
                                <td>{formData.ba}</td>

                                <td><b>Blood Glucose Random</b></td>
                                <td>{formData.bgr}</td>
                            </tr>

                            <tr>
                                <td><b>Blood Urea</b></td>
                                <td>{formData.bu}</td>

                                <td><b>Serum Creatinine</b></td>
                                <td>{formData.sc}</td>
                            </tr>

                            <tr>
                                <td><b>Sodium</b></td>
                                <td>{formData.sod}</td>

                                <td><b>Potassium</b></td>
                                <td>{formData.pot}</td>
                            </tr>

                            <tr>
                                <td><b>Hemoglobin</b></td>
                                <td>{formData.hemo}</td>

                                <td><b>Packed Cell Volume</b></td>
                                <td>{formData.pcv}</td>
                            </tr>

                            <tr>
                                <td><b>White Blood Cell Count</b></td>
                                <td>{formData.wbcc}</td>

                                <td><b>Red Blood Cell Count</b></td>
                                <td>{formData.rbcc}</td>
                            </tr>

                            <tr>
                                <td><b>Hypertension</b></td>
                                <td>{formData.htn}</td>

                                <td><b>Diabetes Mellitus</b></td>
                                <td>{formData.dm}</td>
                            </tr>

                            <tr>
                                <td><b>Coronary Artery Disease</b></td>
                                <td>{formData.cad}</td>

                                <td><b>Appetite</b></td>
                                <td>{formData.appet}</td>
                            </tr>

                            <tr>
                                <td><b>Pedal Edema</b></td>
                                <td>{formData.pe}</td>

                                <td><b>Anemia</b></td>
                                <td>{formData.ane}</td>
                            </tr>

                        </tbody>

                    </table>

                )}


                {/* ======================================
                    STROKE
                ====================================== */}

                {disease === "stroke" && (

                    <table className="table table-bordered">

                        <tbody>

                            <tr>

                                <td>
                                    <b>Age</b>
                                </td>

                                <td>
                                    {formData.stroke_age || formData.age}
                                </td>

                                <td>
                                    <b>Gender</b>
                                </td>

                                <td>
                                    {formData.stroke_gender || formData.gender}
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>Hypertension</b>
                                </td>

                                <td>
                                    {strokeYesNo(formData.hypertension)}
                                </td>

                                <td>
                                    <b>Heart Disease</b>
                                </td>

                                <td>
                                    {strokeYesNo(formData.heart_disease)}
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>Ever Married</b>
                                </td>

                                <td>
                                    {formData.ever_married}
                                </td>

                                <td>
                                    <b>Work Type</b>
                                </td>

                                <td>
                                    {formData.work_type}
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>Residence Type</b>
                                </td>

                                <td>
                                    {formData.Residence_type}
                                </td>

                                <td>
                                    <b>Average Glucose Level</b>
                                </td>

                                <td>
                                    {formData.avg_glucose_level}
                                </td>

                            </tr>


                            <tr>

                                <td>
                                    <b>Body Mass Index (BMI)</b>
                                </td>

                                <td>
                                    {formData.bmi}
                                </td>

                                <td>
                                    <b>Smoking Status</b>
                                </td>

                                <td>
                                    {formData.smoking_status}
                                </td>

                            </tr>

                        </tbody>

                    </table>

                )}

            </div>

        </div>

    );

}

export default PatientSummary;