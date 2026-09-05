function PredictionCard({ result, disease }) {

    if (!result) return null;


    // ==========================================
    // Risk Color
    // ==========================================

    const riskColor =
        result.risk_level === "High"
            ? "danger"
            : result.risk_level === "Moderate"
            ? "warning"
            : "success";


    // ==========================================
    // Prediction
    // ==========================================

    const isPositive =
        result.prediction_class === 1;


    // ==========================================
    // Disease Name
    // ==========================================

    const getDiseaseName = () => {

        switch (disease) {

            case "heart":
                return "Heart Disease";

            case "diabetes":
                return "Diabetes";

            case "ckd":
                return "Chronic Kidney Disease";

            case "stroke":
                return "Stroke";

            default:
                return "Disease";
        }
    };


    const diseaseName = getDiseaseName();


    // ==========================================
    // Result Message
    // ==========================================

    const getPredictionMessage = () => {

        if (disease === "stroke") {

            return isPositive
                ? `⚠️ Stroke Detected`
                : `💚 No Stroke Detected`;
        }


        if (disease === "ckd") {

            return isPositive
                ? `⚠️ Chronic Kidney Disease Detected`
                : `💚 No Chronic Kidney Disease`;
        }


        if (disease === "diabetes") {

            return isPositive
                ? `⚠️ Diabetes Detected`
                : `💚 No Diabetes`;
        }


        return isPositive
            ? `⚠️ Heart Disease Detected`
            : `💚 No Heart Disease`;
    };


    return (

        <div className="card shadow-lg border-0 mt-4">

            <div className="card-header bg-dark text-white">

                <h4 className="mb-0">
                    📋 Prediction Result
                </h4>

            </div>


            <div className="card-body">

                <div className="text-center mb-4">

                    <h2
                        className={
                            isPositive
                                ? "text-danger"
                                : "text-success"
                        }
                    >

                        {getPredictionMessage()}

                    </h2>

                </div>


                <div className="row text-center">

                    {/* ==================================
                        Probability
                    ================================== */}

                    <div className="col-md-4">

                        <div className="card bg-light">

                            <div className="card-body">

                                <h6>
                                    Probability
                                </h6>

                                <h3 className="text-primary">

                                    {result.probability}%

                                </h3>

                            </div>

                        </div>

                    </div>


                    {/* ==================================
                        Risk
                    ================================== */}

                    <div className="col-md-4">

                        <div className="card bg-light">

                            <div className="card-body">

                                <h6>
                                    Risk Level
                                </h6>

                                <span
                                    className={`badge bg-${riskColor} fs-6`}
                                >

                                    {result.risk_level}

                                </span>

                            </div>

                        </div>

                    </div>


                    {/* ==================================
                        Prediction Class
                    ================================== */}

                    <div className="col-md-4">

                        <div className="card bg-light">

                            <div className="card-body">

                                <h6>
                                    Prediction Class
                                </h6>

                                <h3>

                                    {result.prediction_class}

                                </h3>

                            </div>

                        </div>

                    </div>

                </div>


                {/* ======================================
                    Recommendation
                ====================================== */}

                <div className="alert alert-info mt-4">

                    <h5>
                        💡 Clinical Recommendation
                    </h5>

                    <p className="mb-0">

                        {result.recommendation}

                    </p>

                </div>

            </div>

        </div>

    );

}

export default PredictionCard;