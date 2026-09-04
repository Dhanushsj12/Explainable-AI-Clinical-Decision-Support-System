function PatientSummary({ formData, disease }) {

    if (!formData) return null;

    const getGender = () => {
        if (disease === "diabetes") {
            return formData.gender === "1" ? "Male" : "Female";
        }

        return formData.sex === "1" ? "Male" : "Female";
    };

    const yesNo = (value) => {
        return value === "1" ? "Yes" : "No";
    };

    const getChestPain = (value) => {

        const chestPainTypes = {
            "1": "Typical Angina",
            "2": "Atypical Angina",
            "3": "Non-anginal Pain",
            "4": "Asymptomatic"
        };

        return chestPainTypes[value] || value;
    };

    return (

        <div className="card shadow-lg mt-4">

            <div className="card-header bg-info text-white">

                <h4 className="mb-0">
                    👤 Patient Summary
                </h4>

            </div>

            <div className="card-body">

                <h5 className="mb-3">
                    Patient Details
                </h5>

                <p>
                    <b>Patient ID:</b> {formData.patient_id}
                </p>

                <p>
                    <b>Patient Name:</b> {formData.patient_name}
                </p>

                <p>
                    <b>Doctor:</b> {formData.doctor_name}
                </p>

                <p>
                    <b>Hospital:</b> {formData.hospital_name}
                </p>

                <p>
                    <b>Disease:</b>{" "}
                    {disease === "diabetes"
                        ? "Diabetes"
                        : "Heart Disease"}
                </p>

                <hr />

                <h5 className="mb-3">
                    Clinical Information
                </h5>

                {disease === "heart" ? (

                    <table className="table table-bordered">

                        <tbody>

                            <tr>
                                <td><b>Age</b></td>
                                <td>{formData.age}</td>

                                <td><b>Gender</b></td>
                                <td>{getGender()}</td>
                            </tr>

                            <tr>
                                <td><b>Chest Pain</b></td>
                                <td>
                                    {getChestPain(formData.cp)}
                                </td>

                                <td><b>Blood Pressure</b></td>
                                <td>
                                    {formData.trestbps} mmHg
                                </td>
                            </tr>

                            <tr>
                                <td><b>Cholesterol</b></td>
                                <td>
                                    {formData.chol} mg/dL
                                </td>

                                <td><b>Fasting Blood Sugar</b></td>
                                <td>
                                    {yesNo(formData.fbs)}
                                </td>
                            </tr>

                            <tr>
                                <td><b>Resting ECG</b></td>
                                <td>
                                    {formData.restecg}
                                </td>

                                <td><b>Maximum Heart Rate</b></td>
                                <td>
                                    {formData.thalach}
                                </td>
                            </tr>

                            <tr>
                                <td><b>Exercise Angina</b></td>
                                <td>
                                    {yesNo(formData.exang)}
                                </td>

                                <td><b>ST Depression</b></td>
                                <td>
                                    {formData.oldpeak}
                                </td>
                            </tr>

                            <tr>
                                <td><b>ST Segment Slope</b></td>
                                <td>
                                    {formData.slope}
                                </td>

                                <td><b>Major Vessels</b></td>
                                <td>
                                    {formData.ca}
                                </td>
                            </tr>

                            <tr>
                                <td><b>Thalassemia</b></td>
                                <td>
                                    {formData.thal}
                                </td>

                                <td></td>
                                <td></td>
                            </tr>

                        </tbody>

                    </table>

                ) : (

                    <table className="table table-bordered">

                        <tbody>

                            <tr>
                                <td><b>Age</b></td>
                                <td>{formData.age}</td>

                                <td><b>Gender</b></td>
                                <td>{getGender()}</td>
                            </tr>

                            <tr>
                                <td><b>Polyuria</b></td>
                                <td>{yesNo(formData.polyuria)}</td>

                                <td><b>Polydipsia</b></td>
                                <td>{yesNo(formData.polydipsia)}</td>
                            </tr>

                            <tr>
                                <td><b>Sudden Weight Loss</b></td>
                                <td>{yesNo(formData.sudden_weight_loss)}</td>

                                <td><b>Weakness</b></td>
                                <td>{yesNo(formData.weakness)}</td>
                            </tr>

                            <tr>
                                <td><b>Polyphagia</b></td>
                                <td>{yesNo(formData.polyphagia)}</td>

                                <td><b>Genital Thrush</b></td>
                                <td>{yesNo(formData.genital_thrush)}</td>
                            </tr>

                            <tr>
                                <td><b>Visual Blurring</b></td>
                                <td>{yesNo(formData.visual_blurring)}</td>

                                <td><b>Itching</b></td>
                                <td>{yesNo(formData.itching)}</td>
                            </tr>

                            <tr>
                                <td><b>Irritability</b></td>
                                <td>{yesNo(formData.irritability)}</td>

                                <td><b>Delayed Healing</b></td>
                                <td>{yesNo(formData.delayed_healing)}</td>
                            </tr>

                            <tr>
                                <td><b>Partial Paresis</b></td>
                                <td>{yesNo(formData.partial_paresis)}</td>

                                <td><b>Muscle Stiffness</b></td>
                                <td>{yesNo(formData.muscle_stiffness)}</td>
                            </tr>

                            <tr>
                                <td><b>Alopecia</b></td>
                                <td>{yesNo(formData.alopecia)}</td>

                                <td><b>Obesity</b></td>
                                <td>{yesNo(formData.obesity)}</td>
                            </tr>

                        </tbody>

                    </table>

                )}

            </div>

        </div>

    );

}

export default PatientSummary;