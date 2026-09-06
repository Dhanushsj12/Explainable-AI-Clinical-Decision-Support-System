import { IconPulse } from "./icons";
import { useAuth } from "../auth/authcontext";

function Navbar() {

    const { user, logout } = useAuth();

    return (
        <header className="navbar">

            <div className="navbar-inner">

                {/* =========================
                    BRAND
                ========================== */}

                <div className="brand">

                    <div className="brand-mark">
                        <IconPulse size={20} />
                    </div>

                    <div>

                        <span className="brand-title">
                            XAI Clinical Command
                        </span>

                        <span className="brand-sub">
                            Decision Support System / v1.0
                        </span>

                    </div>

                </div>


                {/* =========================
                    RIGHT SIDE
                ========================== */}

                <div className="navbar-right">

                    {/* Backend Status */}

                    <div className="status-pill">

                        <span className="status-dot" />

                        Backend Link · Ready

                    </div>


                    {/* User Information */}

                    {user && (

                        <div className="user-section">

                            <div className="user-info">

                                <span className="user-name">
                                    {user.name}
                                </span>

                                <span className="user-role">
                                    {user.role}
                                </span>

                            </div>


                            {/* Role Badge */}

                            <span
                                className={`role-badge role-${user.role}`}
                            >
                                {user.role}
                            </span>


                            {/* Logout */}

                            <button
                                className="logout-button"
                                onClick={logout}
                            >
                                Logout
                            </button>

                        </div>

                    )}

                </div>

            </div>

        </header>
    );
}

export default Navbar;