function Hero() {

    return (

        <div
            className="text-center text-white py-5"
            style={{
                background: "linear-gradient(135deg,#0d6efd,#00b4d8)",
                borderRadius: "0 0 25px 25px",
                marginBottom: "40px"
            }}
        >

            <h1 className="display-5 fw-bold">

                🏥 Explainable AI Clinical Decision Support System

            </h1>

            <p className="lead mt-3">

                AI-powered Heart Disease Prediction using
                Explainable Artificial Intelligence (SHAP + LIME)

            </p>

        </div>

    );

}

export default Hero;