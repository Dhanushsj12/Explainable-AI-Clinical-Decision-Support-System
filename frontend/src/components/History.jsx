import { useEffect, useState } from "react";
import API from "../services/api";

function History() {

    const [history, setHistory] = useState([]);

    useEffect(() => {

        fetchHistory();

    }, []);

    const fetchHistory = async () => {

        try {

            const response = await API.get("/history");

            console.log("History Data:", response.data);

            setHistory(response.data);

        }
        catch (error) {

            console.error(error);

        }

    };

    const getRiskClass = (risk) => {

        if (risk === "High") {
            return "badge bg-danger";
        }

        if (risk === "Moderate") {
            return "badge bg-warning text-dark";
        }

        return "badge bg-success";

    };

    const getDiseaseName = (disease) => {

        if (!disease) {
            return "—";
        }

        return disease;

    };

    return (

        <div className="container mt-5 mb-5">

            <div className="card shadow border-0">

                <div className="card-header bg-dark text-white">

                    <h4 className="mb-0">
                        📋 Prediction History
                    </h4>

                </div>

                <div className="card-body">

                    {history.length === 0 ? (

                        <div className="text-center text-muted py-4">

                            No prediction history available.

                        </div>

                    ) : (

                        <div className="table-responsive">

                            <table className="table table-striped table-hover align-middle">

                                <thead>

                                    <tr>

                                        <th>ID</th>

                                        <th>Patient ID</th>

                                        <th>Name</th>

                                        <th>Disease</th>

                                        <th>Prediction</th>

                                        <th>Probability</th>

                                        <th>Risk</th>

                                        <th>Date</th>

                                    </tr>

                                </thead>

                                <tbody>

                                    {history.map((item) => (

                                        <tr key={item.id}>

                                            <td>
                                                {item.id}
                                            </td>

                                            <td>
                                                {item.patient_id}
                                            </td>

                                            <td>
                                                {item.patient_name}
                                            </td>

                                            <td>

                                                <span className="badge bg-info text-dark">

                                                    {getDiseaseName(
                                                        item.disease
                                                    )}

                                                </span>

                                            </td>

                                            <td>
                                                {item.prediction}
                                            </td>

                                            <td>
                                                {item.probability}%
                                            </td>

                                            <td>

                                                <span
                                                    className={
                                                        getRiskClass(
                                                            item.risk_level
                                                        )
                                                    }
                                                >

                                                    {item.risk_level}

                                                </span>

                                            </td>

                                            <td>
                                                {item.date}
                                            </td>

                                        </tr>

                                    ))}

                                </tbody>

                            </table>

                        </div>

                    )}

                </div>

            </div>

        </div>

    );

}

export default History;