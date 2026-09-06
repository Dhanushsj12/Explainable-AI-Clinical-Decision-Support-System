import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/authcontext";

function Unauthorized() {
    const navigate = useNavigate();
    const { user } = useAuth();

    const handleReturn = () => {
        if (user?.role === "admin") {
            navigate("/admin");
        }
        else if (user?.role === "doctor") {
            navigate("/doctor");
        }
        else if (user?.role === "staff") {
            navigate("/staff");
        }
        else {
            navigate("/login");
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-card">
                <h1>Access Denied</h1>

                <p>
                    You do not have permission to access this page.
                </p>

                <button
                    className="dashboard-button"
                    onClick={handleReturn}
                >
                    Return to Dashboard
                </button>
            </div>
        </div>
    );
}

export default Unauthorized;