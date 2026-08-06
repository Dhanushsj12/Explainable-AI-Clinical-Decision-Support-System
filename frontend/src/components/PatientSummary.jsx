function PatientSummary({ formData }) {

    if (!formData) return null;

    return (

        <div className="card shadow-lg mt-4">

            <div className="card-header bg-info text-white">

                <h4>

                    👤 Patient Summary

                </h4>

            </div>

            <div className="card-body">

                <table className="table">

                    <tbody>

                        <tr>

                            <td><b>Age</b></td>
                            <td>{formData.age}</td>

                            <td><b>Gender</b></td>
                            <td>{formData.sex === "1" ? "Male" : "Female"}</td>

                        </tr>

                        <tr>

                            <td><b>Blood Pressure</b></td>
                            <td>{formData.trestbps} mmHg</td>

                            <td><b>Cholesterol</b></td>
                            <td>{formData.chol} mg/dL</td>

                        </tr>

                        <tr>

                            <td><b>Maximum Heart Rate</b></td>
                            <td>{formData.thalach}</td>

                            <td><b>Chest Pain</b></td>
                            <td>{formData.cp}</td>

                        </tr>

                    </tbody>

                </table>

            </div>

        </div>

    );

}

export default PatientSummary;