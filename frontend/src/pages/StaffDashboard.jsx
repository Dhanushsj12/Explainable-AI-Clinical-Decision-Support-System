import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/authcontext";

function StaffDashboard() {

    const navigate = useNavigate();
    const { user } = useAuth();

    return (
        <div className="role-dashboard">

            <h1>Staff Dashboard</h1>

            <p>
                Welcome, {user?.name}. Access clinical data
                entry and decision support tools.
            </p>


            <div className="role-dashboard-grid">

                <div className="role-card">
                    <h3>Patient Assessment</h3>

                    <p>
                        Enter patient information for assessment.
                    </p>
                </div>


                <div className="role-card">
                    <h3>Disease Prediction</h3>

                    <p>
                        Run supported clinical predictions.
                    </p>
                </div>


                <div className="role-card">
                    <h3>Clinical Reports</h3>

                    <p>
                        View generated clinical reports.
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

export default StaffDashboard;