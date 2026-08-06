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

    return (

        <div className="container mt-5">

            <div className="card shadow border-0">

                <div className="card-header bg-dark text-white">

                    <h4>📋 Prediction History</h4>

                </div>

                <div className="card-body">

                    <table className="table table-striped">

                        <thead>

                            <tr>

                                <th>ID</th>

                                <th>Patient ID</th>

                                <th>Name</th>

                                <th>Prediction</th>

                                <th>Probability</th>

                                <th>Risk</th>

                                <th>Date</th>

                            </tr>

                        </thead>

                        <tbody>

                            {history.map((item) => (

                                <tr key={item.id}>

                                    <td>{item.id}</td>

                                    <td>{item.patient_id}</td>

                                    <td>{item.patient_name}</td>

                                    <td>{item.prediction}</td>

                                    <td>{item.probability}%</td>

                                    <td>

                                        <span
                                            className={
                                                item.risk_level === "High"
                                                    ? "badge bg-danger"
                                                    : item.risk_level === "Medium"
                                                    ? "badge bg-warning"
                                                    : "badge bg-success"
                                            }
                                        >

                                            {item.risk_level}

                                        </span>

                                    </td>

                                    <td>{item.date}</td>

                                </tr>

                            ))}

                        </tbody>

                    </table>

                </div>

            </div>

        </div>

    );

}

export default History;