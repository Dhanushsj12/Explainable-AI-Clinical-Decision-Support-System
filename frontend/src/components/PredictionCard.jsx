import {
    IconAlertTriangle,
    IconCheckCircle,
    IconLayers
} from "./icons";


// ============================================================
// SAFE HELPERS
// ============================================================

function safeArray(value) {
    return Array.isArray(value) ? value : [];
}


function safeObject(value) {
    return (
        value &&
        typeof value === "object" &&
        !Array.isArray(value)
    )
        ? value
        : {};
}


function numberValue(value, fallback = 0) {
    const n = Number(value);

    return Number.isFinite(n)
        ? n
        : fallback;
}


function formatPercentage(value) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return "N/A";
    }

    const n = Number(value);

    if (!Number.isFinite(n)) {
        return "N/A";
    }

    /*
     * Backend may return:
     *
     * 0.82  -> 82.00%
     * 82    -> 82.00%
     */

    const percentage =
        Math.abs(n) <= 1
            ? n * 100
            : n;

    return `${percentage.toFixed(2)}%`;
}


function formatNumber(value, digits = 2) {

    const n = Number(value);

    if (!Number.isFinite(n)) {
        return "N/A";
    }

    return n.toFixed(digits);
}


// ============================================================
// DISEASE HELPERS
// ============================================================

function normalizeDisease(disease) {

    return String(
        disease || "heart"
    )
        .trim()
        .toLowerCase()
        .replace(/\s+/g, "_");
}


function getDiseaseName(disease) {

    const names = {

        heart:
            "Heart Disease",

        diabetes:
            "Diabetes",

        ckd:
            "Chronic Kidney Disease",

        stroke:
            "Stroke"

    };

    const normalized =
        normalizeDisease(disease);

    return (
        names[normalized] ||
        String(
            disease || "Disease"
        )
    );
}


function getPredictionText(
    result,
    positive,
    disease
) {

    const normalized =
        normalizeDisease(disease);


    /*
     * Prefer backend-provided text whenever available.
     */

    if (
        result &&
        typeof result.prediction_text === "string" &&
        result.prediction_text.trim()
    ) {
        return result.prediction_text;
    }


    if (
        result &&
        typeof result.predictionText === "string" &&
        result.predictionText.trim()
    ) {
        return result.predictionText;
    }


    const messages = {

        heart: positive
            ? "Heart disease detected"
            : "No heart disease detected",

        diabetes: positive
            ? "Diabetes detected"
            : "No diabetes detected",

        ckd: positive
            ? "Chronic kidney disease detected"
            : "No chronic kidney disease detected",

        stroke: positive
            ? "Stroke risk detected"
            : "No stroke risk detected"

    };


    return (
        messages[normalized] ||
        (
            positive
                ? `${getDiseaseName(disease)} detected`
                : `No ${getDiseaseName(disease)} detected`
        )
    );
}


// ============================================================
// COUNTERFACTUAL FEATURE NAME
// ============================================================

function formatFeatureName(feature) {

    if (
        feature === null ||
        feature === undefined ||
        feature === ""
    ) {
        return "Clinical Feature";
    }


    let value =
        String(feature)
            .trim()
            .toLowerCase();


    /*
     * Remove LIME-style numeric conditions.
     *
     * Example:
     *
     * cp <= -0.16
     *
     * becomes:
     *
     * cp
     */

    value =
        value.replace(
            /\s*(<=|>=|<|>)\s*-?\d+(\.\d+)?/g,
            ""
        );


    value =
        value
            .replace(/_/g, " ")
            .trim();


    const aliases = {

        age:
            "Age",

        sex:
            "Gender",

        gender:
            "Gender",

        cp:
            "Chest Pain Type",

        chestpain:
            "Chest Pain Type",

        chest_pain:
            "Chest Pain Type",

        trestbps:
            "Resting Blood Pressure",

        chol:
            "Serum Cholesterol",

        cholesterol:
            "Serum Cholesterol",

        fbs:
            "Fasting Blood Sugar",

        restecg:
            "Resting ECG",

        thalach:
            "Maximum Heart Rate",

        exang:
            "Exercise Induced Angina",

        oldpeak:
            "ST Depression",

        slope:
            "ST Segment Slope",

        ca:
            "Major Vessels",

        thal:
            "Thalassemia",

        polyuria:
            "Polyuria",

        polydipsia:
            "Polydipsia",

        sudden_weight_loss:
            "Sudden Weight Loss",

        weakness:
            "Weakness",

        polyphagia:
            "Polyphagia",

        genital_thrush:
            "Genital Thrush",

        visual_blurring:
            "Visual Blurring",

        itching:
            "Itching",

        irritability:
            "Irritability",

        delayed_healing:
            "Delayed Healing",

        partial_paresis:
            "Partial Paresis",

        muscle_stiffness:
            "Muscle Stiffness",

        alopecia:
            "Alopecia",

        obesity:
            "Obesity",

        bp:
            "Blood Pressure",

        sg:
            "Specific Gravity",

        al:
            "Albumin",

        su:
            "Sugar",

        rbc:
            "Red Blood Cells",

        pc:
            "Pus Cell",

        pcc:
            "Pus Cell Clumps",

        ba:
            "Bacteria",

        bgr:
            "Blood Glucose Random",

        bu:
            "Blood Urea",

        sc:
            "Serum Creatinine",

        sod:
            "Sodium",

        pot:
            "Potassium",

        hemo:
            "Hemoglobin",

        pcv:
            "Packed Cell Volume",

        wbcc:
            "White Blood Cell Count",

        rbcc:
            "Red Blood Cell Count",

        htn:
            "Hypertension",

        dm:
            "Diabetes Mellitus",

        cad:
            "Coronary Artery Disease",

        appet:
            "Appetite",

        pe:
            "Pedal Edema",

        ane:
            "Anemia",

        hypertension:
            "Hypertension",

        heart_disease:
            "Heart Disease",

        ever_married:
            "Ever Married",

        work_type:
            "Work Type",

        residence_type:
            "Residence Type",

        avg_glucose_level:
            "Average Glucose Level",

        bmi:
            "Body Mass Index",

        smoking_status:
            "Smoking Status"

    };


    if (aliases[value]) {
        return aliases[value];
    }


    return value
        .split(" ")
        .filter(Boolean)
        .map(
            word =>
                word.charAt(0).toUpperCase() +
                word.slice(1)
        )
        .join(" ");
}


// ============================================================
// COUNTERFACTUAL VALUE HELPERS
// ============================================================

function getChangeValues(change) {

    if (
        Array.isArray(change)
    ) {

        return {

            oldValue:
                change.length > 0
                    ? change[0]
                    : "",

            newValue:
                change.length > 1
                    ? change[1]
                    : ""

        };

    }


    if (
        change &&
        typeof change === "object"
    ) {

        return {

            oldValue:
                change.oldValue ??
                change.old_value ??
                change.original ??
                change.original_value ??
                change.from ??
                change.before ??
                "",

            newValue:
                change.newValue ??
                change.new_value ??
                change.alternative ??
                change.alternative_value ??
                change.to ??
                change.after ??
                ""

        };

    }


    return {

        oldValue: "",

        newValue: change ?? ""

    };
}


function getCounterfactualChanges(
    counterfactual
) {

    const cf =
        safeObject(counterfactual);


    const rawChanges =
        cf.changes ??
        cf.feature_changes ??
        cf.featureChanges ??
        [];


    /*
     * Backend Heart counterfactual format:
     *
     * {
     *     changes: {
     *         age: [55, 52],
     *         ca: [2, 0]
     *     }
     * }
     *
     * Other disease implementations may return:
     *
     * [
     *     {
     *         feature: "...",
     *         oldValue: "...",
     *         newValue: "..."
     *     }
     * ]
     */


    if (
        Array.isArray(rawChanges)
    ) {

        return rawChanges
            .map(
                item => {

                    const itemObject =
                        safeObject(item);


                    const feature =
                        itemObject.feature ??
                        itemObject.name ??
                        itemObject.feature_name ??
                        itemObject.featureName ??
                        "";


                    return {

                        feature,

                        oldValue:
                            itemObject.oldValue ??
                            itemObject.old_value ??
                            itemObject.original ??
                            itemObject.original_value ??
                            itemObject.from ??
                            "",

                        newValue:
                            itemObject.newValue ??
                            itemObject.new_value ??
                            itemObject.alternative ??
                            itemObject.alternative_value ??
                            itemObject.to ??
                            ""

                    };

                }
            )
            .filter(
                item =>
                    item.feature !== ""
            );

    }


    if (
        rawChanges &&
        typeof rawChanges === "object"
    ) {

        return Object.entries(
            rawChanges
        )
            .map(
                ([feature, change]) => {

                    const values =
                        getChangeValues(
                            change
                        );


                    return {

                        feature,

                        oldValue:
                            values.oldValue,

                        newValue:
                            values.newValue

                    };

                }
            );

    }


    return [];
}


// ============================================================
// COUNTERFACTUAL PREDICTION TEXT
// ============================================================

function getCounterfactualPredictionText(
    counterfactual,
    disease
) {

    const cf =
        safeObject(counterfactual);


    const suppliedText =
        cf.prediction_text ??
        cf.predictionText ??
        cf.new_prediction_text ??
        cf.newPredictionText;


    if (
        suppliedText !== null &&
        suppliedText !== undefined &&
        String(suppliedText).trim()
    ) {

        return String(
            suppliedText
        );

    }


    const predictionClass =
        cf.prediction ??
        cf.prediction_class ??
        cf.predictionClass ??
        cf.new_prediction ??
        cf.newPrediction;


    if (
        predictionClass !== null &&
        predictionClass !== undefined
    ) {

        return Number(
            predictionClass
        ) === 1

            ? getDiseaseName(disease)

            : `No ${getDiseaseName(disease)}`;

    }


    return "Prediction changed";

}


// ============================================================
// COUNTERFACTUAL CARD
// ============================================================

function CounterfactualCard({
    counterfactual,
    index,
    disease
}) {

    const cf =
        safeObject(
            counterfactual
        );


    const changes =
        getCounterfactualChanges(
            cf
        );


    const predictionText =
        getCounterfactualPredictionText(
            cf,
            disease
        );


    const probability =
        cf.probability ??
        cf.new_probability ??
        cf.newProbability ??
        null;


    const numberOfChanges =
        cf.number_of_changes ??
        cf.numberOfChanges ??
        cf.num_changes ??
        changes.length;


    const normalizedChange =
        cf.normalized_change ??
        cf.normalizedChange ??
        null;


    const predictionLower =
        String(
            predictionText
        ).toLowerCase();


    const positive =
        !predictionLower.includes(
            "no "
        ) &&
        (
            predictionLower.includes(
                "detected"
            ) ||
            predictionLower.includes(
                "risk"
            ) ||
            Number(
                cf.prediction ??
                cf.prediction_class ??
                -1
            ) === 1
        );


    return (

        <div
            className="panel"
            style={{
                marginTop: 18
            }}
        >

            {/* =================================================
                HEADER
            ================================================= */}

            <div
                className="panel-header"
            >

                <div
                    className="icon-badge"
                >

                    {
                        positive

                            ? (
                                <IconAlertTriangle
                                    size={17}
                                />
                            )

                            : (
                                <IconCheckCircle
                                    size={17}
                                />
                            )
                    }

                </div>


                <div>

                    <div className="panel-title">

                        Counterfactual #{index + 1}

                    </div>


                    <div
                        className="panel-title-sub"
                    >

                        Alternative {getDiseaseName(disease)} profile

                    </div>

                </div>


                <div
                    style={{
                        marginLeft: "auto"
                    }}
                >

                    <span
                        className={
                            positive
                                ? "badge badge-high"
                                : "badge badge-low"
                        }
                    >

                        Prediction Changed

                    </span>

                </div>

            </div>


            <div
                className="panel-body"
            >

                {/* =================================================
                    TOP METRICS
                ================================================= */}

                <div
                    className="metric-row"
                    style={{
                        marginTop: 0
                    }}
                >

                    <div
                        className="metric-tile"
                    >

                        <div
                            className="metric-tile-label"
                        >

                            New Prediction

                        </div>


                        <div
                            className="metric-tile-value"
                            style={{
                                fontSize: 20
                            }}
                        >

                            {predictionText}

                        </div>

                    </div>


                    <div
                        className="metric-tile"
                    >

                        <div
                            className="metric-tile-label"
                        >

                            Probability

                        </div>


                        <div
                            className="metric-tile-value"
                        >

                            {formatPercentage(
                                probability
                            )}

                        </div>

                    </div>


                    <div
                        className="metric-tile"
                    >

                        <div
                            className="metric-tile-label"
                        >

                            Feature Changes

                        </div>


                        <div
                            className="metric-tile-value"
                        >

                            {numberOfChanges}

                        </div>

                    </div>

                </div>


                {/* =================================================
                    FEATURE CHANGES
                ================================================= */}

                <div
                    className="agreement-section"
                    style={{
                        marginTop: 22
                    }}
                >

                    <h4>
                        Changed Clinical Features
                    </h4>


                    {
                        changes.length > 0

                            ? (

                                <div
                                    className="counterfactual-change-list"
                                >

                                    {
                                        changes.map(
                                            (
                                                change,
                                                changeIndex
                                            ) => (

                                                <div
                                                    key={
                                                        changeIndex
                                                    }
                                                    className="counterfactual-change"
                                                    style={{
                                                        display:
                                                            "flex",
                                                        justifyContent:
                                                            "space-between",
                                                        alignItems:
                                                            "center",
                                                        gap:
                                                            "20px",
                                                        padding:
                                                            "12px 0",
                                                        borderBottom:
                                                            "1px solid #e5eef5",
                                                        flexWrap:
                                                            "wrap"
                                                    }}
                                                >

                                                    <strong>

                                                        {
                                                            formatFeatureName(
                                                                change.feature
                                                            )
                                                        }

                                                    </strong>


                                                    <span>

                                                        {
                                                            String(
                                                                change.oldValue ??
                                                                ""
                                                            )
                                                        }

                                                        {" → "}

                                                        <strong>

                                                            {
                                                                String(
                                                                    change.newValue ??
                                                                    ""
                                                                )
                                                            }

                                                        </strong>

                                                    </span>

                                                </div>

                                            )
                                        )
                                    }

                                </div>

                            )

                            : (

                                <div
                                    className="clinical-note"
                                    style={{
                                        marginTop: 10
                                    }}
                                >

                                    No individual feature changes
                                    were returned for this
                                    counterfactual.

                                </div>

                            )

                    }

                </div>


                {/* =================================================
                    CHANGE MAGNITUDE
                ================================================= */}

                {
                    normalizedChange !== null &&
                    normalizedChange !== undefined &&
                    normalizedChange !== ""

                        ? (

                            <div
                                className="counterfactual-result"
                                style={{
                                    marginTop: 16
                                }}
                            >

                                <div>

                                    <span
                                        className="counterfactual-small-label"
                                    >

                                        Change Magnitude

                                    </span>


                                    <strong>

                                        {
                                            formatNumber(
                                                normalizedChange,
                                                2
                                            )
                                        }

                                    </strong>

                                </div>

                            </div>

                        )

                        : null
                }

            </div>

        </div>

    );

}


// ============================================================
// COUNTERFACTUAL EXPLANATION
// ============================================================

function CounterfactualExplanation({

    counterfactuals,

    originalProbability,

    originalPrediction,

    disease

}) {

    const list =
        safeArray(
            counterfactuals
        );


    /*
     * Important:
     *
     * Do NOT restrict this to Heart Disease.
     *
     * Diabetes, CKD and Stroke can now render the
     * exact same section when the backend supplies
     * counterfactual results.
     */


    if (
        list.length === 0
    ) {

        return null;

    }


    return (

        <div
            className="wrap mt-24"
        >

            <div
                className="panel"
            >

                <div
                    className="panel-header"
                >

                    <div
                        className="icon-badge"
                    >

                        <IconLayers
                            size={18}
                        />

                    </div>


                    <div>

                        <div className="panel-title">

                            Counterfactual Explanation

                        </div>


                        <div
                            className="panel-title-sub"
                        >

                            Multi-feature alternative
                            clinical scenarios

                        </div>

                    </div>

                </div>


                <div
                    className="panel-body"
                >

                    {/* =================================================
                        ORIGINAL PREDICTION
                    ================================================= */}

                    <div
                        className="counterfactual-original"
                    >

                        <div
                            className="counterfactual-label"
                        >

                            Original Prediction

                        </div>


                        <div
                            className="counterfactual-original-value"
                        >

                            {
                                originalPrediction ??
                                "Original Prediction"
                            }


                            {
                                originalProbability !==
                                    null &&
                                originalProbability !==
                                    undefined && (

                                    <span>

                                        {
                                            formatPercentage(
                                                originalProbability
                                            )
                                        }

                                    </span>

                                )
                            }

                        </div>

                    </div>


                    {/* =================================================
                        COUNTERFACTUAL RESULTS
                    ================================================= */}

                    <div
                        className="counterfactual-list"
                    >

                        {
                            list.map(
                                (
                                    counterfactual,
                                    index
                                ) => (

                                    <CounterfactualCard

                                        key={
                                            index
                                        }

                                        counterfactual={
                                            counterfactual
                                        }

                                        index={
                                            index
                                        }

                                        disease={
                                            disease
                                        }

                                    />

                                )
                            )
                        }

                    </div>


                    {/* =================================================
                        EXPLANATION
                    ================================================= */}

                    <div
                        className="counterfactual-description"
                    >

                        <h4>
                            What does this mean?
                        </h4>


                        <p>

                            Counterfactual explanations show
                            hypothetical patient profiles in
                            which one or more clinical features
                            are changed within the configured
                            model search space.

                        </p>


                        <p>

                            The system evaluates these
                            alternatives and identifies profiles
                            that produce a different model
                            prediction.

                        </p>


                        <p>

                            These results describe the model's
                            decision boundary and must not be
                            interpreted as clinical treatment
                            recommendations, prescriptions,
                            or required patient targets.

                        </p>

                    </div>

                </div>

            </div>

        </div>

    );

}


// ============================================================
// PREDICTION CARD
// ============================================================

function PredictionCard({

    result,

    disease = "heart",

    counterfactuals

}) {

    if (!result) {
        return null;
    }


    const positive =
        Number(
            result.prediction_class
        ) === 1;


    const risk =
        result.risk_level ||
        result.riskLevel ||
        (
            positive
                ? "High"
                : "Low"
        );


    const diseaseName =
        getDiseaseName(
            disease
        );


    const message =
        getPredictionText(
            result,
            positive,
            disease
        );


    /*
     * Accept every backend naming convention.
     *
     * This is important because the backend may return:
     *
     * counterfactuals
     * counterfactual_explanations
     *
     * and PatientForm may also pass the list directly.
     */

    const directCounterfactuals =
        safeArray(
            counterfactuals
        );


    const resultCounterfactuals =
        safeArray(
            result.counterfactuals
        );


    const resultExplanationCounterfactuals =
        safeArray(
            result.counterfactual_explanations
        );


    const finalCounterfactuals =
        directCounterfactuals.length > 0

            ? directCounterfactuals

            : resultCounterfactuals.length > 0

                ? resultCounterfactuals

                : resultExplanationCounterfactuals;


    const probability =
        result.probability ??
        result.prediction_probability ??
        result.predictionProbability ??
        result.risk_probability ??
        0;


    const predictionClass =
        result.prediction_class ??
        result.predictionClass ??
        result.prediction ??
        0;


    return (

        <>

            {/* =================================================
                MODEL ASSESSMENT
            ================================================= */}

            <div
                className="panel mt-24"
            >

                {/* =================================================
                    HEADER
                ================================================= */}

                <div
                    className="panel-header"
                >

                    <div
                        className="icon-badge"
                    >

                        {
                            positive

                                ? (
                                    <IconAlertTriangle
                                        size={18}
                                    />
                                )

                                : (
                                    <IconCheckCircle
                                        size={18}
                                    />
                                )
                        }

                    </div>


                    <div>

                        <div
                            className="panel-title"
                        >

                            Model Assessment

                        </div>


                        <div
                            className="panel-title-sub"
                        >

                            {
                                String(
                                    diseaseName
                                ).toUpperCase()
                            }

                            {" / final inference output"}

                        </div>

                    </div>

                </div>


                {/* =================================================
                    RESULT
                ================================================= */}

                <div
                    className="result-shell"
                >

                    {/* =================================================
                        VERDICT
                    ================================================= */}

                    <div
                        className="verdict-panel"
                    >

                        <div
                            className={
                                `verdict ${
                                    positive
                                        ? "is-high"
                                        : "is-clear"
                                }`
                            }
                        >

                            {
                                positive

                                    ? (
                                        <IconAlertTriangle
                                            size={22}
                                        />
                                    )

                                    : (
                                        <IconCheckCircle
                                            size={22}
                                        />
                                    )
                            }


                            <span
                                className="verdict-text"
                            >

                                {message}

                            </span>

                        </div>


                        {/* =================================================
                            METRICS
                        ================================================= */}

                        <div
                            className="metric-row"
                        >

                            <div
                                className="metric-tile"
                            >

                                <div
                                    className="metric-tile-label"
                                >

                                    Probability

                                </div>


                                <div
                                    className="metric-tile-value"
                                >

                                    {
                                        formatPercentage(
                                            probability
                                        )
                                    }

                                </div>

                            </div>


                            <div
                                className="metric-tile"
                            >

                                <div
                                    className="metric-tile-label"
                                >

                                    Risk Level

                                </div>


                                <div
                                    style={{
                                        marginTop: 6
                                    }}
                                >

                                    <span
                                        className={
                                            `badge ${
                                                String(
                                                    risk
                                                ).toLowerCase()
                                                    === "high"

                                                    ? "badge-high"

                                                    : String(
                                                        risk
                                                    ).toLowerCase()
                                                        === "moderate"

                                                        ? "badge-mod"

                                                        : "badge-low"
                                            }`
                                        }
                                    >

                                        {risk}

                                    </span>

                                </div>

                            </div>


                            <div
                                className="metric-tile"
                            >

                                <div
                                    className="metric-tile-label"
                                >

                                    Class

                                </div>


                                <div
                                    className="metric-tile-value"
                                >

                                    {
                                        String(
                                            predictionClass
                                        )
                                    }

                                </div>

                            </div>

                        </div>


                        {/* =================================================
                            RECOMMENDATION
                        ================================================= */}

                        <div
                            className="recommend-box"
                        >

                            <h4>

                                Clinical Recommendation

                            </h4>


                            <p>

                                {
                                    result.recommendation ||
                                    result.clinical_recommendation ||
                                    result.clinicalRecommendation ||
                                    (
                                        positive

                                            ? `High likelihood of ${diseaseName.toLowerCase()}. Consultation with a healthcare professional is strongly recommended for further clinical evaluation and appropriate diagnostic testing.`

                                            : `No significant indication of ${diseaseName.toLowerCase()} was detected. Maintain appropriate clinical follow-up and healthy lifestyle practices.`
                                    )
                                }

                            </p>

                        </div>

                    </div>


                    {/* =================================================
                        PROBABILITY ORB
                    ================================================= */}

                    <div
                        className="result-orb"
                    >

                        <div>

                            <div
                                className="score-ring"
                            >

                                <div>

                                    <div
                                        className="score-number"
                                    >

                                        {
                                            formatPercentage(
                                                probability
                                            )
                                        }

                                    </div>


                                    <div
                                        className="score-label"
                                    >

                                        model probability

                                    </div>

                                </div>

                            </div>

                        </div>

                    </div>

                </div>


                {/* =================================================
                    CLINICAL WARNING
                ================================================= */}

                <div
                    className="clinical-note"
                >

                    ⚠ Decision support only. This model output
                    should be interpreted with clinical assessment
                    and professional judgement.

                </div>

            </div>




        </>

    );

}


export default PredictionCard;