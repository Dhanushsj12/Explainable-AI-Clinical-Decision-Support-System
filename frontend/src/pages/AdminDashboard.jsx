import { useEffect, useState } from "react";
import API from "../services/api";
import { useAuth } from "../auth/authcontext";


function AdminDashboard() {

    const { user, logout } = useAuth();

    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");


    // =========================================================
    // LOAD USERS
    // =========================================================

    const loadUsers = async () => {

        try {

            setLoading(true);
            setError("");

            const response = await API.get("/auth/users");

            setUsers(response.data.users || []);

        } catch (error) {

            setError(
                error.response?.data?.message ||
                "Unable to load users."
            );

        } finally {

            setLoading(false);

        }
    };


    // =========================================================
    // LOAD USERS WHEN PAGE OPENS
    // =========================================================

    useEffect(() => {

        loadUsers();

    }, []);


    // =========================================================
    // CHANGE USER ROLE
    // =========================================================

    const changeRole = async (userId, newRole) => {

        try {

            setError("");
            setMessage("");

            await API.put(
                `/auth/users/${userId}/role`,
                {
                    role: newRole
                }
            );

            setMessage(
                "User role updated successfully."
            );

            loadUsers();

        } catch (error) {

            setError(
                error.response?.data?.message ||
                "Unable to update user role."
            );

        }
    };


    // =========================================================
    // SYSTEM STATISTICS
    // =========================================================

    const totalUsers = users.length;

    const totalDoctors = users.filter(
        (item) => item.role === "doctor"
    ).length;

    const totalStaff = users.filter(
        (item) => item.role === "staff"
    ).length;

    const totalAdmins = users.filter(
        (item) => item.role === "admin"
    ).length;


    // =========================================================
    // PAGE
    // =========================================================

    return (

        <div className="role-dashboard">


            {/* =================================================
                ADMIN TOP BAR
                ================================================= */}

            <div className="admin-topbar">

                <div>

                    <strong>
                        Clinical CDSS
                    </strong>

                    <span>
                        Administrator Panel
                    </span>

                </div>


                <div className="admin-user-area">

                    <div className="admin-user-info">

                        <strong>
                            {user?.name}
                        </strong>

                        <span>
                            {user?.role}
                        </span>

                    </div>


                    <button
                        className="logout-button"
                        onClick={logout}
                    >
                        Logout
                    </button>

                </div>

            </div>


            {/* =================================================
                PAGE TITLE
                ================================================= */}

            <h1>
                Admin Dashboard
            </h1>

            <p>
                Welcome, {user?.name}. Manage users and
                monitor the Clinical Decision Support System.
            </p>


            {/* =================================================
                SYSTEM MONITORING
                ================================================= */}

            <section className="admin-section">

                <div className="admin-section-header">

                    <h2>
                        System Monitoring
                    </h2>

                    <span className="system-status">
                        System Online
                    </span>

                </div>


                {/* STATISTICS */}

                <div className="admin-stats-grid">


                    <div className="admin-stat-card">

                        <span className="admin-stat-label">
                            Total Users
                        </span>

                        <strong>
                            {totalUsers}
                        </strong>

                    </div>


                    <div className="admin-stat-card">

                        <span className="admin-stat-label">
                            Administrators
                        </span>

                        <strong>
                            {totalAdmins}
                        </strong>

                    </div>


                    <div className="admin-stat-card">

                        <span className="admin-stat-label">
                            Doctors
                        </span>

                        <strong>
                            {totalDoctors}
                        </strong>

                    </div>


                    <div className="admin-stat-card">

                        <span className="admin-stat-label">
                            Staff
                        </span>

                        <strong>
                            {totalStaff}
                        </strong>

                    </div>

                </div>


                {/* SYSTEM INFORMATION */}

                <div className="system-info">


                    <div>

                        <span>
                            Backend Status
                        </span>

                        <strong>
                            Connected
                        </strong>

                    </div>


                    <div>

                        <span>
                            Supported Diseases
                        </span>

                        <strong>
                            4
                        </strong>

                    </div>


                    <div>

                        <span>
                            XAI Methods
                        </span>

                        <strong>
                            SHAP + LIME
                        </strong>

                    </div>


                </div>

            </section>


            {/* =================================================
                USER MANAGEMENT
                ================================================= */}

            <section className="admin-section">


                <div className="admin-section-header">

                    <div>

                        <h2>
                            User Management
                        </h2>

                        <p>
                            Manage registered doctors and staff accounts.
                        </p>

                    </div>

                </div>


                {/* SUCCESS MESSAGE */}

                {message && (

                    <div className="admin-success">
                        {message}
                    </div>

                )}


                {/* ERROR MESSAGE */}

                {error && (

                    <div className="admin-error">
                        {error}
                    </div>

                )}


                {/* LOADING */}

                {loading ? (

                    <p className="admin-loading">
                        Loading users...
                    </p>

                ) : users.length === 0 ? (

                    <p className="admin-loading">
                        No users found.
                    </p>

                ) : (

                    <div className="user-table-wrapper">


                        <table className="user-table">


                            <thead>

                                <tr>

                                    <th>
                                        Name
                                    </th>

                                    <th>
                                        Email
                                    </th>

                                    <th>
                                        Role
                                    </th>

                                    <th>
                                        Action
                                    </th>

                                </tr>

                            </thead>


                            <tbody>

                                {users.map((item) => (

                                    <tr key={item.id}>


                                        {/* NAME */}

                                        <td>
                                            {item.name}
                                        </td>


                                        {/* EMAIL */}

                                        <td>
                                            {item.email}
                                        </td>


                                        {/* ROLE */}

                                        <td>

                                            <span
                                                className={`admin-role-badge role-${item.role}`}
                                            >
                                                {item.role}
                                            </span>

                                        </td>


                                        {/* ACTION */}

                                        <td>

                                            {item.role === "admin" ? (

                                                <span className="protected-user">
                                                    Protected
                                                </span>

                                            ) : (

                                                <select
                                                    value={item.role}
                                                    onChange={(event) =>
                                                        changeRole(
                                                            item.id,
                                                            event.target.value
                                                        )
                                                    }
                                                    className="role-select"
                                                >

                                                    <option value="staff">
                                                        Staff
                                                    </option>

                                                    <option value="doctor">
                                                        Doctor
                                                    </option>

                                                </select>

                                            )}

                                        </td>


                                    </tr>

                                ))}

                            </tbody>


                        </table>

                    </div>

                )}

            </section>


        </div>

    );
}


export default AdminDashboard;