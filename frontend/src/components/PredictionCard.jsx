function PredictionCard({ result }) {

    if (!result) return null;

    const riskColor =
        result.risk_level === "High"
            ? "danger"
            : result.risk_level === "Medium"
            ? "warning"
            : "success";

    const predictionColor =
        result.prediction === "Heart Disease"
            ? "danger"
            : "success";

    return (

        <div className="card shadow-lg border-0 mt-4">

            <div className="card-header bg-dark text-white">

                <h4 className="mb-0">
                    📋 Prediction Result
                </h4>

            </div>

            <div className="card-body">

                <div className="text-center mb-4">

                    <h2 className={`text-${predictionColor}`}>

                        {result.prediction === "Heart Disease"
                            ? "❤️ Heart Disease Detected"
                            : "💚 No Heart Disease"}

                    </h2>

                </div>

                <div className="row text-center">

                    <div className="col-md-4">

                        <div className="card bg-light">

                            <div className="card-body">

                                <h6>Probability</h6>

                                <h3 className="text-primary">

                                    {result.probability}%

                                </h3>

                            </div>

                        </div>

                    </div>

                    <div className="col-md-4">

                        <div className="card bg-light">

                            <div className="card-body">

                                <h6>Risk Level</h6>

                                <span
                                    className={`badge bg-${riskColor} fs-6`}
                                >
                                    {result.risk_level}
                                </span>

                            </div>

                        </div>

                    </div>

                    <div className="col-md-4">

                        <div className="card bg-light">

                            <div className="card-body">

                                <h6>Prediction Class</h6>

                                <h3>

                                    {result.prediction_class}

                                </h3>

                            </div>

                        </div>

                    </div>

                </div>

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