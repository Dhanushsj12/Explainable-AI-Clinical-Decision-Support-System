import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Dashboard from "./components/Dashboard";
import PatientForm from "./components/PatientForm";
import History from "./components/History";
import Footer from "./components/Footer";

function App() {

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

export default App;
