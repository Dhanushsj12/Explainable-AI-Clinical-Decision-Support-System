function FeatureImportance({ features }) {

    if (!features || features.length === 0) return null;

    return (

        <div className="card shadow-lg border-0 mt-4">

            <div className="card-header bg-success text-white">

                <h4 className="mb-0">
                    📊 Explainable AI - Top Influencing Features
                </h4>

            </div>

            <div className="card-body">

                <p className="text-muted mb-4">
                    These are the most influential clinical features that contributed to the model's prediction.
                </p>

                {features.map((item, index) => {

                    const percentage = Math.min(
                        Math.abs(item.impact) * 50,
                        100
                    );

                    return (

                        <div
                            key={index}
                            className="mb-4"
                        >

                            <div className="d-flex justify-content-between">

                                <strong>

                                    {item.feature}

                                </strong>

                                <span>

                                    {item.impact.toFixed(3)}

                                </span>

                            </div>

                            <div className="progress mt-2">

                                <div
                                    className={`progress-bar ${
                                        item.impact >= 0
                                            ? "bg-success"
                                            : "bg-danger"
                                    }`}
                                    role="progressbar"
                                    style={{
                                        width: `${percentage}%`
                                    }}
                                >

                                </div>

                            </div>

                        </div>

                    );

                })}

            </div>

        </div>

    );

}

export default FeatureImportance;