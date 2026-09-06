import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../services/api";
import { useAuth } from "./authcontext";


function Login() {

    const navigate = useNavigate();
    const { login } = useAuth();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");


    /* =========================================
       LOGIN
    ========================================= */

    const handleLogin = async (event) => {

        event.preventDefault();

        setError("");

        try {

            const response = await API.post(
                "/auth/login",
                {
                    email,
                    password
                }
            );


            /* =========================
               SAVE JWT TOKEN
            ========================== */

            localStorage.setItem(
                "access_token",
                response.data.token
            );


            /* =========================
               SAVE USER
            ========================== */

            login(response.data.user);


            /* =========================
               ROLE-BASED REDIRECT
            ========================== */

            const role = response.data.user.role;


            if (role === "admin") {

                navigate("/admin");

            }
            else if (role === "doctor") {

                navigate("/doctor");

            }
            else {

                navigate("/staff");

            }

        }
        catch (error) {

            setError(
                error.response?.data?.message ||
                "Login failed."
            );

        }

    };


    /* =========================================
       LOGIN UI
    ========================================= */

    return (

        <div className="auth-page">

            <div className="auth-card">

                <h1>
                    Clinical CDSS
                </h1>

                <p>
                    Explainable AI Clinical Decision Support System
                </p>


                <h2>
                    Login
                </h2>


                {/* Error */}

                {error && (

                    <div className="auth-error">
                        {error}
                    </div>

                )}


                <form onSubmit={handleLogin}>

                    {/* Email */}

                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(event) =>
                            setEmail(event.target.value)
                        }
                        required
                    />


                    {/* Password */}

                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(event) =>
                            setPassword(event.target.value)
                        }
                        required
                    />


                    {/* Login Button */}

                    <button type="submit">
                        Login
                    </button>

                </form>


                {/* Signup */}

                <p>

                    Don't have an account?{" "}

                    <Link to="/signup">
                        Create account
                    </Link>

                </p>

            </div>

        </div>

    );

}


export default Login;