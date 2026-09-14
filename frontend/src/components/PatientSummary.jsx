import {
    IconUser,
    IconLayers
} from "./icons";


/* ============================================================
   HELPERS
============================================================ */

function displayValue(value) {

    if (
        value === undefined ||
        value === null ||
        value === ""
    ) {
        return "—";
    }

    return String(value);
}


function yesNo(value) {

    if (
        value === "1" ||
        value === 1 ||
        value === true ||
        String(value).toLowerCase() === "yes"
    ) {
        return "Yes";
    }

    if (
        value === "0" ||
        value === 0 ||
        value === false ||
        String(value).toLowerCase() === "no"
    ) {
        return "No";
    }

    return displayValue(value);
}


function diseaseName(disease) {

    const names = {

        heart: "Heart Disease",

        diabetes: "Diabetes",

        ckd: "Chronic Kidney Disease",

        stroke: "Stroke"

    };

    return names[disease] || "Clinical Condition";
}


function formatFeatureName(feature) {

    if (!feature) {
        return "";
    }

    const names = {

        /* HEART */

        age: "Age",
        sex: "Gender",
        gender: "Gender",
        cp: "Chest Pain Type",
        trestbps: "Resting Blood Pressure",
        chol: "Serum Cholesterol",
        fbs: "Fasting Blood Sugar",
        restecg: "Resting ECG",
        thalach: "Maximum Heart Rate",
        exang: "Exercise Induced Angina",
        oldpeak: "ST Depression",
        slope: "ST Segment Slope",
        ca: "Major Vessels",
        thal: "Thalassemia",

        /* DIABETES */

        polyuria: "Polyuria",
        polydipsia: "Polydipsia",
        sudden_weight_loss: "Sudden Weight Loss",
        weakness: "Weakness",
        polyphagia: "Polyphagia",
        genital_thrush: "Genital Thrush",
        visual_blurring: "Visual Blurring",
        itching: "Itching",
        irritability: "Irritability",
        delayed_healing: "Delayed Healing",
        partial_paresis: "Partial Paresis",
        muscle_stiffness: "Muscle Stiffness",
        alopecia: "Alopecia",
        obesity: "Obesity",

        /* CKD */

        bp: "Blood Pressure",
        sg: "Specific Gravity",
        al: "Albumin",
        su: "Sugar",
        rbc: "Red Blood Cells",
        pc: "Pus Cell",
        pcc: "Pus Cell Clumps",
        ba: "Bacteria",
        bgr: "Blood Glucose",
        bu: "Blood Urea",
        sc: "Serum Creatinine",
        sod: "Sodium",
        pot: "Potassium",
        hemo: "Hemoglobin",
        pcv: "Packed Cell Volume",
        wbcc: "White Blood Cell Count",
        rbcc: "Red Blood Cell Count",
        htn: "Hypertension",
        dm: "Diabetes Mellitus",
        cad: "Coronary Artery Disease",
        appet: "Appetite",
        pe: "Pedal Edema",
        ane: "Anemia",

        /* STROKE */

        hypertension: "Hypertension",
        heart_disease: "Heart Disease",
        ever_married: "Ever Married",
        work_type: "Work Type",
        Residence_type: "Residence Type",
        avg_glucose_level: "Average Glucose Level",
        bmi: "Body Mass Index",
        smoking_status: "Smoking Status"

    };

    return (
        names[feature] ||
        String(feature)
            .replaceAll("_", " ")
            .replace(/\b\w/g, (char) =>
                char.toUpperCase()
            )
    );
}


function formatCounterfactualValue(value) {

    if (
        value === undefined ||
        value === null ||
        value === ""
    ) {
        return "—";
    }

    if (
        value === true ||
        String(value).toLowerCase() === "yes"
    ) {
        return "Yes";
    }

    if (
        value === false ||
        String(value).toLowerCase() === "no"
    ) {
        return "No";
    }

    return String(value);
}


function safeArray(value) {

    return Array.isArray(value)
        ? value
        : [];
}


function formatNumber(value, decimals = 2) {

    if (
        value === undefined ||
        value === null ||
        value === ""
    ) {
        return "—";
    }

    const number = Number(value);

    if (Number.isNaN(number)) {
        return String(value);
    }

    return number.toFixed(decimals);
}


/* ============================================================
   COUNTERFACTUAL HELPERS
============================================================ */

function getCounterfactualChanges(counterfactual) {

    if (!counterfactual) {
        return {};
    }

    const rawChanges =
        counterfactual.changes ||
        counterfactual.feature_changes ||
        counterfactual.changed_features ||
        {};

    /*
     * Backend may return:
     *
     * {
     *   feature: {
     *      old: 1,
     *      new: 0
     *   }
     * }
     *
     * OR:
     *
     * [
     *   {
     *      feature: "...",
     *      old: "...",
     *      new: "..."
     *   }
     * ]
     */

    if (Array.isArray(rawChanges)) {

        const normalized = {};

        rawChanges.forEach((item) => {

            if (!item) {
                return;
            }

            const feature =
                item.feature ||
                item.name ||
                item.feature_name ||
                item.key;

            if (!feature) {
                return;
            }

            normalized[feature] = {

                old:
                    item.old ??
                    item.original ??
                    item.from ??
                    item.current ??
                    "—",

                new:
                    item.new ??
                    item.counterfactual ??
                    item.to ??
                    item.value ??
                    "—"

            };

        });

        return normalized;
    }


    if (
        rawChanges &&
        typeof rawChanges === "object"
    ) {

        const normalized = {};

        Object.entries(rawChanges).forEach(
            ([feature, value]) => {

                if (
                    value &&
                    typeof value === "object" &&
                    !Array.isArray(value)
                ) {

                    normalized[feature] = {

                        old:
                            value.old ??
                            value.original ??
                            value.from ??
                            value.current ??
                            "—",

                        new:
                            value.new ??
                            value.counterfactual ??
                            value.to ??
                            value.value ??
                            "—"

                    };

                } else {

                    normalized[feature] = {

                        old: "—",

                        new: value

                    };

                }

            }
        );

        return normalized;
    }

    return {};
}


function getCounterfactualPrediction(counterfactual) {

    if (!counterfactual) {
        return "—";
    }

    if (
        counterfactual.prediction_text !==
        undefined &&
        counterfactual.prediction_text !==
        null
    ) {
        return String(
            counterfactual.prediction_text
        );
    }

    if (
        counterfactual.prediction_label !==
        undefined &&
        counterfactual.prediction_label !==
        null
    ) {
        return String(
            counterfactual.prediction_label
        );
    }

    if (
        counterfactual.prediction !==
        undefined &&
        counterfactual.prediction !==
        null
    ) {

        const prediction =
            Number(
                counterfactual.prediction
            );

        if (prediction === 1) {

            return diseasePredictionText(
                counterfactual,
                true
            );

        }

        if (prediction === 0) {

            return diseasePredictionText(
                counterfactual,
                false
            );

        }

        return String(
            counterfactual.prediction
        );
    }

    return "—";
}


function diseasePredictionText(
    counterfactual,
    positive
) {

    const disease =
        String(
            counterfactual?.disease ||
            ""
        ).toLowerCase();


    if (disease === "heart") {

        return positive
            ? "Heart Disease"
            : "No Heart Disease";

    }

    if (disease === "diabetes") {

        return positive
            ? "Diabetes"
            : "No Diabetes";

    }

    if (disease === "ckd") {

        return positive
            ? "Chronic Kidney Disease"
            : "No Chronic Kidney Disease";

    }

    if (disease === "stroke") {

        return positive
            ? "Stroke"
            : "No Stroke";

    }

    return positive
        ? "Positive"
        : "Negative";
}


/* ============================================================
   COUNTERFACTUAL CARD
============================================================ */

function CounterfactualCard({
    counterfactual,
    index
}) {

    const changes =
        getCounterfactualChanges(
            counterfactual
        );

    const changeEntries =
        Object.entries(
            changes || {}
        );


    const prediction =
        getCounterfactualPrediction(
            counterfactual
        );


    const numberOfChanges =
        counterfactual?.number_of_changes ??
        counterfactual?.num_changes ??
        changeEntries.length;


    const normalizedChange =
        counterfactual?.normalized_change;


    return (

        <div
            style={{
                border:
                    "1px solid var(--line, #dbe4ee)",
                borderRadius:
                    "10px",
                padding:
                    "18px",
                background:
                    "var(--panel-soft, #f8fafc)"
            }}
        >

            {/* =================================================
                HEADER
            ================================================= */}

            <div
                style={{
                    display:
                        "flex",
                    justifyContent:
                        "space-between",
                    alignItems:
                        "center",
                    gap:
                        "12px",
                    flexWrap:
                        "wrap",
                    marginBottom:
                        "16px"
                }}
            >

                <strong
                    style={{
                        fontSize:
                            "14px"
                    }}
                >
                    Counterfactual #{index + 1}
                </strong>


                <span
                    className="badge badge-neutral"
                >
                    Prediction Changed
                </span>

            </div>


            {/* =================================================
                SUMMARY METRICS
            ================================================= */}

            <div
                className="metric-row"
                style={{
                    marginTop: 0,
                    gridTemplateColumns:
                        normalizedChange !==
                        undefined &&
                        normalizedChange !==
                        null
                            ? "repeat(3, 1fr)"
                            : "repeat(2, 1fr)"
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
                            fontSize:
                                "18px"
                        }}
                    >
                        {prediction}
                    </div>

                </div>


                <div
                    className="metric-tile"
                >

                    <div
                        className="metric-tile-label"
                    >
                        Features Changed
                    </div>

                    <div
                        className="metric-tile-value"
                    >
                        {numberOfChanges}
                    </div>

                </div>


                {
                    normalizedChange !==
                    undefined &&
                    normalizedChange !==
                    null && (

                        <div
                            className="metric-tile"
                        >

                            <div
                                className="metric-tile-label"
                            >
                                Change Magnitude
                            </div>

                            <div
                                className="metric-tile-value"
                            >
                                {
                                    formatNumber(
                                        normalizedChange,
                                        4
                                    )
                                }
                            </div>

                        </div>

                    )
                }

            </div>


            {/* =================================================
                FEATURE CHANGES
            ================================================= */}

            <div
                style={{
                    marginTop:
                        "18px"
                }}
            >

                <div
                    style={{
                        fontSize:
                            "11px",
                        fontWeight:
                            700,
                        textTransform:
                            "uppercase",
                        letterSpacing:
                            "0.05em",
                        color:
                            "var(--muted-text, #64748b)",
                        marginBottom:
                            "8px"
                    }}
                >
                    Changed Clinical Features
                </div>


                {
                    changeEntries.length > 0
                        ? (

                            <div
                                style={{
                                    display:
                                        "grid",
                                    gap:
                                        "8px"
                                }}
                            >

                                {
                                    changeEntries.map(
                                        (
                                            [
                                                feature,
                                                values
                                            ]
                                        ) => (

                                            <div
                                                key={
                                                    feature
                                                }
                                                style={{
                                                    display:
                                                        "grid",
                                                    gridTemplateColumns:
                                                        "1.4fr 1fr 1fr",
                                                    gap:
                                                        "10px",
                                                    alignItems:
                                                        "center",
                                                    padding:
                                                        "10px 12px",
                                                    border:
                                                        "1px solid var(--line, #dbe4ee)",
                                                    background:
                                                        "#ffffff"
                                                }}
                                            >

                                                <strong
                                                    style={{
                                                        fontSize:
                                                            "12px"
                                                    }}
                                                >
                                                    {
                                                        formatFeatureName(
                                                            feature
                                                        )
                                                    }
                                                </strong>


                                                <div>

                                                    <div
                                                        style={{
                                                            fontSize:
                                                                "9px",
                                                            color:
                                                                "var(--dim, #64748b)",
                                                            textTransform:
                                                                "uppercase",
                                                            marginBottom:
                                                                "3px"
                                                        }}
                                                    >
                                                        Original
                                                    </div>

                                                    <span
                                                        style={{
                                                            fontSize:
                                                                "12px"
                                                        }}
                                                    >
                                                        {
                                                            formatCounterfactualValue(
                                                                values?.old
                                                            )
                                                        }
                                                    </span>

                                                </div>


                                                <div>

                                                    <div
                                                        style={{
                                                            fontSize:
                                                                "9px",
                                                            color:
                                                                "var(--dim, #64748b)",
                                                            textTransform:
                                                                "uppercase",
                                                            marginBottom:
                                                                "3px"
                                                        }}
                                                    >
                                                        Alternative
                                                    </div>

                                                    <strong
                                                        style={{
                                                            fontSize:
                                                                "12px"
                                                        }}
                                                    >
                                                        {
                                                            formatCounterfactualValue(
                                                                values?.new
                                                            )
                                                        }
                                                    </strong>

                                                </div>

                                            </div>

                                        )
                                    )
                                }

                            </div>

                        )
                        : (

                            <div
                                className="clinical-note"
                            >
                                No feature-level changes were
                                returned for this counterfactual.
                            </div>

                        )
                }

            </div>

        </div>

    );

}


/* ============================================================
   COUNTERFACTUAL SECTION
   ALL FOUR DISEASES
============================================================ */

function CounterfactualSection({
    counterfactuals,
    disease
}) {

    const items =
        safeArray(
            counterfactuals
        ).slice(0, 5);


    return (

        <div
            className="wrap mt-24"
        >

            <div
                className="panel"
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

                        <IconLayers
                            size={17}
                        />

                    </div>


                    <div>

                        <div
                            className="panel-title"
                        >
                            Counterfactual Explanation
                        </div>

                        <div
                            className="panel-title-sub"
                        >
                            Model-based what-if analysis ·{" "}
                            {diseaseName(
                                disease
                            )}
                        </div>

                    </div>

                </div>


                <div
                    className="panel-body"
                >

                    <p
                        style={{
                            marginTop: 0,
                            lineHeight: 1.6,
                            color:
                                "var(--muted-text, #64748b)"
                        }}
                    >
                        Counterfactual analysis identifies
                        hypothetical alternative patient profiles
                        in which one or more clinical features are
                        changed to determine whether the model
                        prediction can change.
                    </p>


                    {
                        items.length > 0
                            ? (

                                <div
                                    style={{
                                        display:
                                            "grid",
                                        gap:
                                            "18px",
                                        marginTop:
                                            "20px"
                                    }}
                                >

                                    {
                                        items.map(
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
                                                />

                                            )
                                        )
                                    }

                                </div>

                            )
                            : (

                                <div
                                    className="clinical-note"
                                    style={{
                                        marginTop:
                                            "18px"
                                    }}
                                >

                                    <strong>
                                        No counterfactual profile
                                        was returned.
                                    </strong>

                                    <br />

                                    The model did not return a
                                    valid alternative profile for
                                    this{" "}
                                    {
                                        diseaseName(
                                            disease
                                        ).toLowerCase()
                                    }{" "}
                                    assessment within the configured
                                    search space.

                                </div>

                            )
                    }


                    {/* =================================================
                        INTERPRETATION
                    ================================================= */}

                    <div
                        className="recommend-box"
                        style={{
                            marginTop:
                                "20px"
                        }}
                    >

                        <h4>
                            How to interpret
                        </h4>

                        <p>
                            Counterfactual explanations are
                            hypothetical model-based scenarios.
                            They describe feature changes that may
                            alter the model output and must not be
                            interpreted as treatment recommendations
                            or clinically prescribed targets.
                            They should be interpreted together with
                            clinical assessment and professional
                            judgement.
                        </p>

                    </div>

                </div>

            </div>

        </div>

    );

}


/* ============================================================
   MAIN PATIENT SUMMARY
============================================================ */

function PatientSummary({
    formData,
    disease,
    counterfactuals = []
}) {

    if (!formData) {
        return null;
    }


    /* =========================================================
       GENDER
    ========================================================= */

    let gender = "";


    if (disease === "stroke") {

        gender =
            formData.stroke_gender ||
            "";

    } else if (disease === "diabetes") {

        gender =
            formData.gender === "1" ||
            formData.gender === 1
                ? "Male"
                : "Female";

    } else {

        gender =
            formData.sex === "1" ||
            formData.sex === 1
                ? "Male"
                : "Female";

    }


    /* =========================================================
       CLINICAL PARAMETERS
    ========================================================= */

    let rows = [];


    /* =========================================================
       HEART
    ========================================================= */

    if (disease === "heart") {

        rows = [

            [
                "Age",
                formData.age
            ],

            [
                "Gender",
                gender
            ],

            [
                "Chest Pain Type",
                formData.cp
            ],

            [
                "Resting Blood Pressure",
                formData.trestbps
            ],

            [
                "Cholesterol",
                formData.chol
            ],

            [
                "Fasting Blood Sugar",
                yesNo(formData.fbs)
            ],

            [
                "Resting ECG",
                formData.restecg
            ],

            [
                "Maximum Heart Rate",
                formData.thalach
            ],

            [
                "Exercise Angina",
                yesNo(formData.exang)
            ],

            [
                "ST Depression",
                formData.oldpeak
            ],

            [
                "ST Segment Slope",
                formData.slope
            ],

            [
                "Major Vessels",
                formData.ca
            ],

            [
                "Thalassemia",
                formData.thal
            ]

        ];

    }


    /* =========================================================
       DIABETES
    ========================================================= */

    else if (disease === "diabetes") {

        rows = [

            [
                "Age",
                formData.age
            ],

            [
                "Gender",
                gender
            ],

            [
                "Polyuria",
                yesNo(formData.polyuria)
            ],

            [
                "Polydipsia",
                yesNo(formData.polydipsia)
            ],

            [
                "Sudden Weight Loss",
                yesNo(
                    formData.sudden_weight_loss
                )
            ],

            [
                "Weakness",
                yesNo(formData.weakness)
            ],

            [
                "Polyphagia",
                yesNo(formData.polyphagia)
            ],

            [
                "Genital Thrush",
                yesNo(
                    formData.genital_thrush
                )
            ],

            [
                "Visual Blurring",
                yesNo(
                    formData.visual_blurring
                )
            ],

            [
                "Itching",
                yesNo(formData.itching)
            ],

            [
                "Irritability",
                yesNo(
                    formData.irritability
                )
            ],

            [
                "Delayed Healing",
                yesNo(
                    formData.delayed_healing
                )
            ],

            [
                "Partial Paresis",
                yesNo(
                    formData.partial_paresis
                )
            ],

            [
                "Muscle Stiffness",
                yesNo(
                    formData.muscle_stiffness
                )
            ],

            [
                "Alopecia",
                yesNo(formData.alopecia)
            ],

            [
                "Obesity",
                yesNo(formData.obesity)
            ]

        ];

    }


    /* =========================================================
       CHRONIC KIDNEY DISEASE
    ========================================================= */

    else if (disease === "ckd") {

        rows = [

            [
                "Age",
                formData.age
            ],

            [
                "Blood Pressure",
                formData.bp
            ],

            [
                "Specific Gravity",
                formData.sg
            ],

            [
                "Albumin",
                formData.al
            ],

            [
                "Sugar",
                formData.su
            ],

            [
                "Red Blood Cells",
                formData.rbc
            ],

            [
                "Pus Cell",
                formData.pc
            ],

            [
                "Pus Cell Clumps",
                formData.pcc
            ],

            [
                "Bacteria",
                formData.ba
            ],

            [
                "Blood Glucose",
                formData.bgr
            ],

            [
                "Blood Urea",
                formData.bu
            ],

            [
                "Serum Creatinine",
                formData.sc
            ],

            [
                "Sodium",
                formData.sod
            ],

            [
                "Potassium",
                formData.pot
            ],

            [
                "Hemoglobin",
                formData.hemo
            ],

            [
                "Packed Cell Volume",
                formData.pcv
            ],

            [
                "White Blood Cell Count",
                formData.wbcc
            ],

            [
                "Red Blood Cell Count",
                formData.rbcc
            ],

            [
                "Hypertension",
                yesNo(formData.htn)
            ],

            [
                "Diabetes Mellitus",
                yesNo(formData.dm)
            ],

            [
                "Coronary Artery Disease",
                yesNo(formData.cad)
            ],

            [
                "Appetite",
                formData.appet
            ],

            [
                "Pedal Edema",
                yesNo(formData.pe)
            ],

            [
                "Anemia",
                yesNo(formData.ane)
            ]

        ];

    }


    /* =========================================================
       STROKE
    ========================================================= */

    else if (disease === "stroke") {

        rows = [

            [
                "Age",
                formData.stroke_age
            ],

            [
                "Gender",
                formData.stroke_gender
            ],

            [
                "Hypertension",
                yesNo(formData.hypertension)
            ],

            [
                "Heart Disease",
                yesNo(formData.heart_disease)
            ],

            [
                "Ever Married",
                formData.ever_married
            ],

            [
                "Work Type",
                formData.work_type
            ],

            [
                "Residence Type",
                formData.Residence_type
            ],

            [
                "Average Glucose Level",
                formData.avg_glucose_level
            ],

            [
                "Body Mass Index",
                formData.bmi
            ],

            [
                "Smoking Status",
                formData.smoking_status
            ]

        ];

    }


    /* =========================================================
       RENDER
    ========================================================= */

    return (

        <>

            {/* =================================================
                PATIENT SUMMARY
            ================================================= */}

            <div
                className="wrap mt-24"
            >

                <div
                    className="panel"
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

                            <IconUser
                                size={17}
                            />

                        </div>


                        <div>

                            <div
                                className="panel-title"
                            >
                                Case Record
                            </div>


                            <div
                                className="panel-title-sub"
                            >
                                Submitted patient context /{" "}
                                {
                                    diseaseName(
                                        disease
                                    ).toUpperCase()
                                }
                            </div>

                        </div>

                    </div>


                    <div
                        className="panel-body"
                    >

                        {/* =================================================
                            PATIENT INFORMATION
                        ================================================= */}

                        <div
                            style={{
                                display:
                                    "grid",
                                gridTemplateColumns:
                                    "repeat(4, 1fr)",
                                gap:
                                    "1px",
                                background:
                                    "var(--line, #dbe4ee)",
                                border:
                                    "1px solid var(--line, #dbe4ee)"
                            }}
                        >

                            <div
                                className="metric-tile"
                            >

                                <div
                                    className="metric-tile-label"
                                >
                                    Patient ID
                                </div>

                                <div
                                    className="metric-tile-value"
                                >
                                    {
                                        displayValue(
                                            formData.patient_id
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
                                    Patient
                                </div>

                                <div
                                    className="metric-tile-value"
                                    style={{
                                        fontSize:
                                            "18px"
                                    }}
                                >
                                    {
                                        displayValue(
                                            formData.patient_name
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
                                    Clinician
                                </div>

                                <div
                                    className="metric-tile-value"
                                    style={{
                                        fontSize:
                                            "18px"
                                    }}
                                >
                                    {
                                        displayValue(
                                            formData.doctor_name
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
                                    Hospital / Clinic
                                </div>

                                <div
                                    className="metric-tile-value"
                                    style={{
                                        fontSize:
                                            "18px"
                                    }}
                                >
                                    {
                                        displayValue(
                                            formData.hospital_name
                                        )
                                    }
                                </div>

                            </div>

                        </div>


                        {/* =================================================
                            CLINICAL PARAMETERS
                        ================================================= */}

                        <div
                            style={{
                                marginTop:
                                    "24px"
                            }}
                        >

                            <div
                                className="panel-title"
                                style={{
                                    fontSize:
                                        "18px",
                                    marginBottom:
                                        "12px"
                                }}
                            >
                                Clinical Parameters
                            </div>


                            <div
                                style={{
                                    display:
                                        "grid",
                                    gridTemplateColumns:
                                        "repeat(2, minmax(0, 1fr))",
                                    border:
                                        "1px solid var(--line, #dbe4ee)"
                                }}
                            >

                                {
                                    rows.map(
                                        (
                                            [label, value],
                                            index
                                        ) => (

                                            <div
                                                key={
                                                    `${label}-${index}`
                                                }
                                                style={{
                                                    display:
                                                        "grid",
                                                    gridTemplateColumns:
                                                        "1fr 1fr",
                                                    gap:
                                                        "12px",
                                                    padding:
                                                        "12px 14px",
                                                    borderBottom:
                                                        "1px solid var(--line, #dbe4ee)",
                                                    borderRight:
                                                        index % 2 === 0
                                                            ? "1px solid var(--line, #dbe4ee)"
                                                            : "none",
                                                    background:
                                                        "#ffffff"
                                                }}
                                            >

                                                <span
                                                    style={{
                                                        fontSize:
                                                            "11px",
                                                        fontWeight:
                                                            700,
                                                        color:
                                                            "var(--dim, #64748b)",
                                                        textTransform:
                                                            "uppercase",
                                                        letterSpacing:
                                                            ".03em"
                                                    }}
                                                >
                                                    {label}
                                                </span>


                                                <strong
                                                    style={{
                                                        fontSize:
                                                            "12px",
                                                        color:
                                                            "var(--ink, #172033)",
                                                        textAlign:
                                                            "right",
                                                        overflowWrap:
                                                            "anywhere"
                                                    }}
                                                >
                                                    {
                                                        displayValue(
                                                            value
                                                        )
                                                    }
                                                </strong>

                                            </div>

                                        )
                                    )
                                }

                            </div>

                        </div>

                    </div>

                </div>

            </div>


            {/* =================================================
                COUNTERFACTUAL
                HEART / DIABETES / CKD / STROKE
            ================================================= */}

            <CounterfactualSection
                counterfactuals={
                    counterfactuals
                }
                disease={
                    disease
                }
            />

        </>

    );

}


export default PatientSummary;