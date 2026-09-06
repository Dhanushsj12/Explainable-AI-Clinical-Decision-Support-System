import { Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Dashboard from "./components/Dashboard";
import PatientForm from "./components/PatientForm";
import History from "./components/History";
import Footer from "./components/Footer";

import Login from "./auth/login";
import Signup from "./auth/signup";
import ProtectedRoute from "./auth/protectedroute";

import AdminDashboard from "./pages/AdminDashboard";
import DoctorDashboard from "./pages/DoctorDashboard";
import StaffDashboard from "./pages/StaffDashboard";
import Unauthorized from "./pages/Unauthorized";


/* =========================================
   MAIN CLINICAL CDSS
   DOCTOR + STAFF
========================================= */

function MainCDSS() {

    return (
        <>
            <Navbar />

            <main className="app-main">

                <Hero />

                <Dashboard />

                <PatientForm />

                <History />

            </main>

            <Footer />
        </>
    );
}


/* =========================================
   APPLICATION ROUTES
========================================= */

function App() {

    return (

        <Routes>

            {/* =========================
                PUBLIC ROUTES
            ========================== */}

            <Route
                path="/login"
                element={<Login />}
            />

            <Route
                path="/signup"
                element={<Signup />}
            />


            {/* =========================
                MAIN CLINICAL CDSS
                DOCTOR + STAFF ONLY
            ========================== */}

            <Route
                path="/"
                element={
                    <ProtectedRoute
                        allowedRoles={[
                            "doctor",
                            "staff"
                        ]}
                    >
                        <MainCDSS />
                    </ProtectedRoute>
                }
            />


            {/* =========================
                ADMIN DASHBOARD
                ADMIN ONLY
            ========================== */}

            <Route
                path="/admin"
                element={
                    <ProtectedRoute
                        allowedRoles={[
                            "admin"
                        ]}
                    >
                        <AdminDashboard />
                    </ProtectedRoute>
                }
            />


            {/* =========================
                DOCTOR DASHBOARD
                DOCTOR ONLY
            ========================== */}

            <Route
                path="/doctor"
                element={
                    <ProtectedRoute
                        allowedRoles={[
                            "doctor"
                        ]}
                    >
                        <DoctorDashboard />
                    </ProtectedRoute>
                }
            />


            {/* =========================
                STAFF DASHBOARD
                STAFF ONLY
            ========================== */}

            <Route
                path="/staff"
                element={
                    <ProtectedRoute
                        allowedRoles={[
                            "staff"
                        ]}
                    >
                        <StaffDashboard />
                    </ProtectedRoute>
                }
            />


            {/* =========================
                UNAUTHORIZED
            ========================== */}

            <Route
                path="/unauthorized"
                element={<Unauthorized />}
            />

        </Routes>

    );
}


export default App;