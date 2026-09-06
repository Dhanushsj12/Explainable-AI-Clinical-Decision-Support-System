import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/authcontext";

function DoctorDashboard() {

    const navigate = useNavigate();
    const { user } = useAuth();

    return (
        <div className="role-dashboard">

            <h1>Doctor Dashboard</h1>

            <p>
                Welcome, Dr. {user?.name}. Access clinical
                decision support and explainable AI tools.
            </p>


            <div className="role-dashboard-grid">

                <div className="role-card">
                    <h3>Patient Assessment</h3>

                    <p>
                        Enter patient information for clinical
                        assessment.
                    </p>
                </div>


                <div className="role-card">
                    <h3>Disease Prediction</h3>

                    <p>
                        Perform predictions for Heart Disease,
                        Diabetes, CKD and Stroke.
                    </p>
                </div>


                <div className="role-card">
                    <h3>Explainable AI</h3>

                    <p>
                        Review SHAP and LIME explanations
                        for clinical predictions.
                    </p>
                </div>


                <div className="role-card">
                    <h3>Patient History</h3>

                    <p>
                        Review previous clinical assessments
                        and prediction records.
                    </p>
                </div>

            </div>


            <button
                className="dashboard-button"
                onClick={() => navigate("/")}
            >
                Open Clinical CDSS
            </button>

        </div>
    );
}

export default DoctorDashboard;