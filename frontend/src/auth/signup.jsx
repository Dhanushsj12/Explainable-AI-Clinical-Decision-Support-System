import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../services/api";

function Signup() {

    const navigate = useNavigate();

    const [form, setForm] = useState({
        name: "",
        email: "",
        password: "",
        role: "doctor"
    });

    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    const handleChange = (event) => {

        setForm({
            ...form,
            [event.target.name]: event.target.value
        });
    };

    const handleSignup = async (event) => {

        event.preventDefault();

        setError("");
        setMessage("");

        try {

            const response = await API.post(
                "/auth/signup",
                form
            );

            setMessage(response.data.message);

            setTimeout(() => {
                navigate("/login");
            }, 1200);

        } catch (error) {

            setError(
                error.response?.data?.message ||
                "Signup failed."
            );
        }
    };

    return (
        <div className="auth-page">

            <div className="auth-card">

                <h1>Clinical CDSS</h1>

                <h2>Create Account</h2>

                {error && (
                    <div className="auth-error">
                        {error}
                    </div>
                )}

                {message && (
                    <div className="auth-success">
                        {message}
                    </div>
                )}

                <form onSubmit={handleSignup}>

                    <input
                        name="name"
                        placeholder="Full Name"
                        value={form.name}
                        onChange={handleChange}
                        required
                    />

                    <input
                        name="email"
                        type="email"
                        placeholder="Email"
                        value={form.email}
                        onChange={handleChange}
                        required
                    />

                    <input
                        name="password"
                        type="password"
                        placeholder="Password (min 6 characters)"
                        value={form.password}
                        onChange={handleChange}
                        required
                    />

                    <select
                        name="role"
                        value={form.role}
                        onChange={handleChange}
                        className="auth-select"
                        style={{
                            width: "100%",
                            height: "44px",
                            padding: "0 12px",
                            marginBottom: "16px",
                            border: "1px solid #cbd5e1",
                            borderRadius: "6px",
                            fontSize: "14px",
                            background: "#ffffff",
                            color: "#0f172a",
                            fontWeight: 600
                        }}
                    >
                        <option value="doctor">Medical Doctor (Full Assessment & Patient History)</option>
                        <option value="staff">Clinical Staff (Diagnostics & Triage)</option>
                    </select>

                    <button type="submit">
                        Create Account
                    </button>

                </form>

                <p>
                    Already have an account?{" "}
                    <Link to="/login">
                        Login
                    </Link>
                </p>

            </div>

        </div>
    );
}

export default Signup;