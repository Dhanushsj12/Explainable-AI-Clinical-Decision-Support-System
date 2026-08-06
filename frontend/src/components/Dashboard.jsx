function Dashboard() {

    // Temporary values
    // Later we'll connect these to the backend

    const totalPredictions = 18;
    const highRisk = 7;
    const lowRisk = 11;
    const accuracy = 96.7;

    return (

        <div className="container mt-4">

            <div className="row g-4">

                <div className="col-md-3">

                    <div className="card shadow border-0 text-center">

                        <div className="card-body">

                            <h6 className="text-muted">
                                Total Predictions
                            </h6>

                            <h2 className="text-primary fw-bold">
                                {totalPredictions}
                            </h2>

                        </div>

                    </div>

                </div>

                <div className="col-md-3">

                    <div className="card shadow border-0 text-center">

                        <div className="card-body">

                            <h6 className="text-muted">
                                High Risk
                            </h6>

                            <h2 className="text-danger fw-bold">
                                {highRisk}
                            </h2>

                        </div>

                    </div>

                </div>

                <div className="col-md-3">

                    <div className="card shadow border-0 text-center">

                        <div className="card-body">

                            <h6 className="text-muted">
                                Low Risk
                            </h6>

                            <h2 className="text-success fw-bold">
                                {lowRisk}
                            </h2>

                        </div>

                    </div>

                </div>

                <div className="col-md-3">

                    <div className="card shadow border-0 text-center">

                        <div className="card-body">

                            <h6 className="text-muted">
                                Model Accuracy
                            </h6>

                            <h2 className="text-warning fw-bold">
                                {accuracy}%
                            </h2>

                        </div>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default Dashboard;