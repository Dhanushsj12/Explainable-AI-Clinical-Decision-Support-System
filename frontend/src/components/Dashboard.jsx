import {
    useEffect,
    useState
} from "react";

import {
    IconLayers,
    IconAlertTriangle,
    IconCheckCircle,
    IconTarget
} from "./icons";

import API from "../services/api";


function Dashboard() {

    const [stats, setStats] = useState({
        cases_processed: 0,
        high_risk_flags: 0,
        low_risk_cases: 0
    });

    const [loading, setLoading] = useState(true);


    // =========================================================
    // LOAD DASHBOARD STATISTICS
    // =========================================================

    const loadStats = async () => {

        try {

            const response = await API.get(
                "/stats"
            );

            setStats({

                cases_processed:
                    response.data.cases_processed || 0,

                high_risk_flags:
                    response.data.high_risk_flags || 0,

                low_risk_cases:
                    response.data.low_risk_cases || 0

            });

        } catch (error) {

            console.error(
                "Unable to load dashboard statistics:",
                error
            );

        } finally {

            setLoading(false);

        }
    };


    // =========================================================
    // LOAD WHEN DASHBOARD OPENS
    // =========================================================

    useEffect(() => {

        loadStats();

    }, []);


    // =========================================================
    // DASHBOARD TILES
    // =========================================================

    const tiles = [

        [
            "Cases Processed",
            loading
                ? "..."
                : stats.cases_processed,
            IconLayers,
            "var(--cyan)"
        ],

        [
            "High Risk Flags",
            loading
                ? "..."
                : stats.high_risk_flags,
            IconAlertTriangle,
            "var(--red)"
        ],

        [
            "Low Risk Cases",
            loading
                ? "..."
                : stats.low_risk_cases,
            IconCheckCircle,
            "var(--lime)"
        ],

        [
            "Model Reference",
            "96.7%",
            IconTarget,
            "var(--amber)"
        ]

    ];


    // =========================================================
    // UI
    // =========================================================

    return (

        <div className="wrap mt-24">

            <div className="stat-strip">

                {tiles.map(
                    (
                        [
                            label,
                            value,
                            Icon,
                            accent
                        ]
                    ) => (

                        <div
                            className="stat-tile"
                            key={label}
                        >

                            <div
                                className="stat-tile-accent"
                                style={{
                                    background: accent
                                }}
                            />

                            <div
                                style={{
                                    color: accent
                                }}
                            >
                                <Icon size={17} />
                            </div>

                            <div
                                className="stat-label"
                                style={{
                                    marginTop: 10
                                }}
                            >
                                {label}
                            </div>

                            <div className="stat-value">
                                {value}
                            </div>

                        </div>

                    )
                )}

            </div>

        </div>

    );

}


export default Dashboard;