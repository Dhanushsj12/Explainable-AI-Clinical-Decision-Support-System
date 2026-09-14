import {
    IconAlertTriangle,
    IconCheckCircle
} from "./icons";


/* ============================================================
   DISEASE / FEATURE HELPERS
============================================================ */

function cleanFeatureName(feature) {

    if (feature === null || feature === undefined) {
        return "";
    }

    let value = String(feature).trim();

    /*
     * LIME can return rules such as:
     *
     * "-0.99 < Polyuria <= 1.01"
     * "age > 0.78"
     * "hemo > 0.81"
     *
     * Extract the actual feature name from the rule.
     */

    value = value
        .replace(
            /^[-+]?\d*\.?\d+\s*<\s*/,
            ""
        )
        .replace(
            /\s*<=\s*[-+]?\d*\.?\d+.*$/,
            ""
        )
        .replace(
            /\s*<\s*[-+]?\d*\.?\d+.*$/,
            ""
        )
        .replace(
            /\s*>=\s*[-+]?\d*\.?\d+.*$/,
            ""
        )
        .replace(
            /\s*>\s*[-+]?\d*\.?\d+.*$/,
            ""
        )
        .replace(
            /\s*=\s*[-+]?\d*\.?\d+.*$/,
            ""
        )
        .trim();

    return value;
}


/*
 * Canonical feature aliases.
 *
 * This is important because SHAP and LIME may use different
 * representations of the same model feature.
 *
 * Examples:
 *
 * hemo  -> hemoglobin
 * pcv   -> packed cell volume
 * rbcc  -> red blood cell count
 * dm    -> diabetes mellitus
 * htn   -> hypertension
 * sg    -> specific gravity
 * avg_glucose_level -> average glucose level
 */

const FEATURE_ALIASES = {

    /* =========================
       COMMON
    ========================= */

    age: "age",

    sex: "gender",
    gender: "gender",

    /* =========================
       HEART DISEASE
    ========================= */

    cp: "chest pain type",
    chestpain: "chest pain type",
    chest_pain_type: "chest pain type",

    trestbps: "resting blood pressure",
    restingbp: "resting blood pressure",
    resting_blood_pressure: "resting blood pressure",

    chol: "serum cholesterol",
    cholesterol: "serum cholesterol",
    serum_cholesterol: "serum cholesterol",

    fbs: "fasting blood sugar",
    fasting_blood_sugar: "fasting blood sugar",

    restecg: "resting ecg",
    resting_ecg: "resting ecg",

    thalach: "maximum heart rate",
    max_heart_rate: "maximum heart rate",
    maximum_heart_rate: "maximum heart rate",

    exang: "exercise induced angina",
    exercise_angina: "exercise induced angina",
    exercise_induced_angina: "exercise induced angina",

    oldpeak: "st depression",
    st_depression: "st depression",

    slope: "st segment slope",
    st_segment_slope: "st segment slope",

    ca: "major vessels",
    major_vessels: "major vessels",

    thal: "thalassemia",
    thalassemia: "thalassemia",


    /* =========================
       DIABETES
    ========================= */

    polyuria: "polyuria",

    polydipsia: "polydipsia",

    sudden_weight_loss: "sudden weight loss",
    suddenweightloss: "sudden weight loss",

    weakness: "weakness",

    polyphagia: "polyphagia",

    genital_thrush: "genital thrush",
    genitalthrush: "genital thrush",

    visual_blurring: "visual blurring",
    visualblurring: "visual blurring",

    itching: "itching",

    irritability: "irritability",

    delayed_healing: "delayed healing",
    delayedhealing: "delayed healing",

    partial_paresis: "partial paresis",
    partialparesis: "partial paresis",

    muscle_stiffness: "muscle stiffness",
    musclestiffness: "muscle stiffness",

    alopecia: "alopecia",

    obesity: "obesity",


    /* =========================
       CKD
    ========================= */

    bp: "blood pressure",
    blood_pressure: "blood pressure",

    sg: "specific gravity",
    specific_gravity: "specific gravity",

    al: "albumin",
    albumin: "albumin",

    su: "sugar",
    sugar: "sugar",

    rbc: "red blood cells",
    red_blood_cells: "red blood cells",

    pc: "pus cell",
    pus_cell: "pus cell",

    pcc: "pus cell clumps",
    pus_cell_clumps: "pus cell clumps",

    ba: "bacteria",
    bacteria: "bacteria",

    bgr: "blood glucose",
    blood_glucose: "blood glucose",

    bu: "blood urea",
    blood_urea: "blood urea",

    sc: "serum creatinine",
    serum_creatinine: "serum creatinine",

    sod: "sodium",
    sodium: "sodium",

    pot: "potassium",
    potassium: "potassium",

    hemo: "hemoglobin",
    hb: "hemoglobin",
    hemoglobin: "hemoglobin",

    pcv: "packed cell volume",
    packed_cell_volume: "packed cell volume",

    wc: "white blood cell count",
    white_blood_cell_count: "white blood cell count",

    wbcc: "white blood cell count",

    rc: "red blood cell count",
    rbcc: "red blood cell count",
    red_blood_cell_count: "red blood cell count",

    htn: "hypertension",
    hypertension: "hypertension",

    dm: "diabetes mellitus",
    diabetes_mellitus: "diabetes mellitus",

    cad: "coronary artery disease",
    coronary_artery_disease: "coronary artery disease",

    appet: "appetite",
    appetite: "appetite",

    pe: "pedal edema",
    pedal_edema: "pedal edema",

    ane: "anemia",
    anemia: "anemia",


    /* =========================
       STROKE
    ========================= */

    heart_disease: "heart disease",

    ever_married: "ever married",

    work_type: "work type",
    worktype: "work type",

    residence_type: "residence type",
    residencetype: "residence type",

    avg_glucose_level: "average glucose level",
    average_glucose_level: "average glucose level",

    bmi: "body mass index",
    body_mass_index: "body mass index",

    smoking_status: "smoking status",
    smokingstatus: "smoking status"

};


function normalizeFeatureName(feature) {

    const cleaned =
        cleanFeatureName(feature)
            .toLowerCase()
            .trim()
            .replaceAll("-", "_")
            .replaceAll(" ", "_");


    if (FEATURE_ALIASES[cleaned]) {
        return FEATURE_ALIASES[cleaned];
    }


    const withoutUnderscores =
        cleaned.replaceAll("_", "");


    for (
        const [alias, canonical]
        of Object.entries(FEATURE_ALIASES)
    ) {

        if (
            alias.replaceAll("_", "") ===
            withoutUnderscores
        ) {

            return canonical;

        }

    }


    return cleaned
        .replaceAll("_", " ")
        .replace(/\s+/g, " ")
        .trim();
}


function formatFeatureName(feature) {

    const canonical =
        normalizeFeatureName(feature);


    if (!canonical) {
        return "";
    }


    const names = {

        age: "Age",

        gender: "Gender",

        "chest pain type":
            "Chest Pain Type",

        "resting blood pressure":
            "Resting Blood Pressure",

        "serum cholesterol":
            "Serum Cholesterol",

        "fasting blood sugar":
            "Fasting Blood Sugar",

        "resting ecg":
            "Resting ECG",

        "maximum heart rate":
            "Maximum Heart Rate",

        "exercise induced angina":
            "Exercise Induced Angina",

        "st depression":
            "ST Depression",

        "st segment slope":
            "ST Segment Slope",

        "major vessels":
            "Major Vessels",

        thalassemia:
            "Thalassemia",


        /* Diabetes */

        polyuria:
            "Polyuria",

        polydipsia:
            "Polydipsia",

        "sudden weight loss":
            "Sudden Weight Loss",

        weakness:
            "Weakness",

        polyphagia:
            "Polyphagia",

        "genital thrush":
            "Genital Thrush",

        "visual blurring":
            "Visual Blurring",

        itching:
            "Itching",

        irritability:
            "Irritability",

        "delayed healing":
            "Delayed Healing",

        "partial paresis":
            "Partial Paresis",

        "muscle stiffness":
            "Muscle Stiffness",

        alopecia:
            "Alopecia",

        obesity:
            "Obesity",


        /* CKD */

        "blood pressure":
            "Blood Pressure",

        "specific gravity":
            "Specific Gravity",

        albumin:
            "Albumin",

        sugar:
            "Sugar",

        "red blood cells":
            "Red Blood Cells",

        "pus cell":
            "Pus Cell",

        "pus cell clumps":
            "Pus Cell Clumps",

        bacteria:
            "Bacteria",

        "blood glucose":
            "Blood Glucose",

        "blood urea":
            "Blood Urea",

        "serum creatinine":
            "Serum Creatinine",

        sodium:
            "Sodium",

        potassium:
            "Potassium",

        hemoglobin:
            "Hemoglobin",

        "packed cell volume":
            "Packed Cell Volume",

        "white blood cell count":
            "White Blood Cell Count",

        "red blood cell count":
            "Red Blood Cell Count",

        hypertension:
            "Hypertension",

        "diabetes mellitus":
            "Diabetes Mellitus",

        "coronary artery disease":
            "Coronary Artery Disease",

        appetite:
            "Appetite",

        "pedal edema":
            "Pedal Edema",

        anemia:
            "Anemia",


        /* Stroke */

        "heart disease":
            "Heart Disease",

        "ever married":
            "Ever Married",

        "work type":
            "Work Type",

        "residence type":
            "Residence Type",

        "average glucose level":
            "Average Glucose Level",

        "body mass index":
            "Body Mass Index",

        "smoking status":
            "Smoking Status"

    };


    return (
        names[canonical] ||
        canonical
            .replace(/\b\w/g, (c) =>
                c.toUpperCase()
            )
    );
}


/* ============================================================
   SHAP VALUE HELPERS
============================================================ */

function getFeatureName(item) {

    if (!item) {
        return "";
    }


    if (
        typeof item === "object" &&
        !Array.isArray(item)
    ) {

        return (
            item.feature ??
            item.name ??
            item.feature_name ??
            item.featureName ??
            ""
        );

    }


    if (Array.isArray(item)) {
        return item[0];
    }


    return "";
}


function getFeatureValue(item) {

    if (!item) {
        return "";
    }


    if (
        typeof item === "object" &&
        !Array.isArray(item)
    ) {

        return (
            item.value ??
            item.contribution ??
            item.weight ??
            item.importance ??
            item.shap_value ??
            item.shap ??
            ""
        );

    }


    if (Array.isArray(item)) {
        return item[1];
    }


    return "";
}


/* ============================================================
   LIME HELPERS
============================================================ */

function getLimeFeatureName(item) {

    if (!item) {
        return "";
    }


    if (
        typeof item === "object" &&
        !Array.isArray(item)
    ) {

        return (
            item.feature ??
            item.name ??
            item.feature_name ??
            item.featureName ??
            item.rule ??
            ""
        );

    }


    if (Array.isArray(item)) {
        return item[0];
    }


    return "";
}


function getLimeValue(item) {

    if (!item) {
        return "";
    }


    if (
        typeof item === "object" &&
        !Array.isArray(item)
    ) {

        return (
            item.weight ??
            item.value ??
            item.contribution ??
            item.score ??
            ""
        );

    }


    if (Array.isArray(item)) {
        return item[1];
    }


    return "";
}


/* ============================================================
   SAFE VALUE FORMATTER
============================================================ */

function formatNumericValue(value) {

    if (
        typeof value === "number" &&
        Number.isFinite(value)
    ) {

        return value.toFixed(3);

    }


    if (
        typeof value === "string" &&
        value.trim() !== "" &&
        Number.isFinite(Number(value))
    ) {

        return Number(value).toFixed(3);

    }


    return String(value ?? "");
}


/* ============================================================
   AGREEMENT NORMALIZATION
============================================================ */

function normalizeAgreement(agreement) {

    if (
        agreement === null ||
        agreement === undefined
    ) {

        return null;

    }


    if (
        typeof agreement === "number" ||
        typeof agreement === "string"
    ) {

        return {

            score:
                agreement,

            shapLimeOverlap:
                null,

            agreementFeatures:
                [],

            shapOnly:
                [],

            limeOnly:
                []

        };

    }


    if (
        typeof agreement !== "object"
    ) {

        return null;

    }


    const score =
        agreement.agreement_score ??
        agreement.agreementScore ??
        agreement.score ??
        agreement.overlap_score ??
        agreement.overlap_percentage ??
        agreement.similarity ??
        agreement.percentage ??
        null;


    const agreementFeatures =
        agreement.agreement_features ??
        agreement.agreementFeatures ??
        agreement.common_features ??
        agreement.commonFeatures ??
        agreement.overlapping_features ??
        agreement.overlappingFeatures ??
        agreement.shared_features ??
        agreement.sharedFeatures ??
        agreement.agreement ??
        [];


    const shapOnly =
        agreement.shap_only_features ??
        agreement.shapOnlyFeatures ??
        agreement.shap_only ??
        [];


    const limeOnly =
        agreement.lime_only_features ??
        agreement.limeOnlyFeatures ??
        agreement.lime_only ??
        [];


    const shapLimeOverlap =
        agreement.overlap ??
        agreement.overlap_count ??
        agreement.overlapCount ??
        agreement.common_count ??
        agreement.commonCount ??
        agreement.shared_count ??
        agreement.sharedCount ??
        null;


    return {

        score,

        shapLimeOverlap,

        agreementFeatures:
            Array.isArray(agreementFeatures)
                ? agreementFeatures
                : [],

        shapOnly:
            Array.isArray(shapOnly)
                ? shapOnly
                : [],

        limeOnly:
            Array.isArray(limeOnly)
                ? limeOnly
                : []

    };

}


/* ============================================================
   FALLBACK SHAP-LIME AGREEMENT
============================================================ */

function buildFallbackAgreement(
    features,
    limeFeatures
) {

    if (
        !Array.isArray(features) ||
        !Array.isArray(limeFeatures)
    ) {

        return null;

    }


    if (
        features.length === 0 ||
        limeFeatures.length === 0
    ) {

        return null;

    }


    const shapNames =
        features
            .map(getFeatureName)
            .filter(Boolean)
            .map(normalizeFeatureName)
            .filter(Boolean);


    const limeNames =
        limeFeatures
            .map(getLimeFeatureName)
            .filter(Boolean)
            .map(normalizeFeatureName)
            .filter(Boolean);


    if (
        shapNames.length === 0 ||
        limeNames.length === 0
    ) {

        return null;

    }


    const uniqueShap =
        [...new Set(shapNames)];


    const uniqueLime =
        [...new Set(limeNames)];


    const common =
        uniqueShap.filter(
            (name) =>
                uniqueLime.includes(name)
        );


    const uniqueCommon =
        [...new Set(common)];


    /*
     * Agreement is calculated against the larger explanation
     * list so that the score represents the proportion of the
     * displayed evidence that both methods share.
     */

    const denominator =
        Math.max(
            uniqueShap.length,
            uniqueLime.length
        );


    const score =
        denominator > 0
            ? Math.round(
                (
                    uniqueCommon.length /
                    denominator
                ) * 100
            )
            : 0;


    return {

        score,

        shapLimeOverlap:
            uniqueCommon.length,

        agreementFeatures:
            uniqueCommon,

        shapOnly:
            uniqueShap.filter(
                (name) =>
                    !uniqueCommon.includes(name)
            ),

        limeOnly:
            uniqueLime.filter(
                (name) =>
                    !uniqueCommon.includes(name)
            )

    };

}


/* ============================================================
   EXPLANATION CARD
============================================================ */

function ExplanationCard({
    title,
    subtitle,
    items,
    type
}) {

    const safeItems =
        Array.isArray(items)
            ? items
            : [];


    return (

        <div className="panel">

            <div className="panel-header">

                <div className="icon-badge">

                    {
                        type === "shap"
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
                        {title}
                    </div>

                    <div className="panel-title-sub">
                        {subtitle}
                    </div>

                </div>

            </div>


            <div className="panel-body">

                {
                    safeItems.length === 0
                        ? (

                            <div className="clinical-note">
                                No explanation data returned.
                            </div>

                        )
                        : (

                            <div
                                style={{
                                    display: "grid",
                                    gap: "8px"
                                }}
                            >

                                {
                                    safeItems
                                        .slice(0, 10)
                                        .map(
                                            (
                                                item,
                                                index
                                            ) => {

                                                const rawName =
                                                    type === "shap"
                                                        ? getFeatureName(item)
                                                        : getLimeFeatureName(item);


                                                const value =
                                                    type === "shap"
                                                        ? getFeatureValue(item)
                                                        : getLimeValue(item);


                                                const displayName =
                                                    formatFeatureName(
                                                        rawName
                                                    );


                                                return (

                                                    <div
                                                        key={
                                                            `${displayName}-${index}`
                                                        }
                                                        style={{
                                                            display:
                                                                "flex",
                                                            justifyContent:
                                                                "space-between",
                                                            alignItems:
                                                                "center",
                                                            gap:
                                                                "15px",
                                                            padding:
                                                                "9px 10px",
                                                            borderBottom:
                                                                "1px solid var(--line, #e5e7eb)"
                                                        }}
                                                    >

                                                        <span
                                                            style={{
                                                                fontSize:
                                                                    "13px"
                                                            }}
                                                        >
                                                            {
                                                                displayName
                                                            }
                                                        </span>


                                                        <strong
                                                            style={{
                                                                fontSize:
                                                                    "13px"
                                                            }}
                                                        >
                                                            {
                                                                formatNumericValue(
                                                                    value
                                                                )
                                                            }
                                                        </strong>

                                                    </div>

                                                );

                                            }
                                        )
                                }

                            </div>

                        )
                }

            </div>

        </div>

    );

}


/* ============================================================
   AGREEMENT SECTION
============================================================ */

function AgreementSection({
    agreement,
    features,
    limeFeatures
}) {

    const normalized =
        normalizeAgreement(
            agreement
        );


    const fallback =
        buildFallbackAgreement(
            features,
            limeFeatures
        );


    /*
     * Backend agreement is preferred.
     * Fallback is used only when backend agreement is absent.
     */

    const data =
        normalized ||
        fallback;


    if (!data) {
        return null;
    }


    const score =
        data.score;


    const agreementFeatures =
        Array.isArray(data.agreementFeatures)
            ? data.agreementFeatures
            : [];


    const shapOnly =
        Array.isArray(data.shapOnly)
            ? data.shapOnly
            : [];


    const limeOnly =
        Array.isArray(data.limeOnly)
            ? data.limeOnly
            : [];


    const sharedCount =
        data.shapLimeOverlap ??
        agreementFeatures.length;


    return (

        <div className="wrap mt-24">

            <div className="panel">

                <div className="panel-header">

                    <div className="icon-badge">

                        <IconCheckCircle
                            size={17}
                        />

                    </div>


                    <div>

                        <div className="panel-title">
                            SHAP-LIME Agreement
                        </div>

                        <div className="panel-title-sub">
                            Consistency between local explanation methods
                        </div>

                    </div>

                </div>


                <div className="panel-body">

                    <div
                        style={{
                            display: "grid",
                            gridTemplateColumns:
                                "repeat(3, minmax(0, 1fr))",
                            gap: "1px",
                            background:
                                "var(--line, #dbe4ee)",
                            border:
                                "1px solid var(--line, #dbe4ee)"
                        }}
                    >

                        <div className="metric-tile">

                            <div className="metric-tile-label">
                                Agreement Score
                            </div>

                            <div className="metric-tile-value">

                                {
                                    score !== null &&
                                    score !== undefined
                                        ? (
                                            typeof score === "number"
                                                ? `${score.toFixed(2)}%`
                                                : `${String(score).replace(
                                                    /%$/,
                                                    ""
                                                )}%`
                                        )
                                        : "—"
                                }

                            </div>

                        </div>


                        <div className="metric-tile">

                            <div className="metric-tile-label">
                                Shared Features
                            </div>

                            <div className="metric-tile-value">
                                {sharedCount}
                            </div>

                        </div>


                        <div className="metric-tile">

                            <div className="metric-tile-label">
                                Evidence Sources
                            </div>

                            <div className="metric-tile-value">
                                SHAP + LIME
                            </div>

                        </div>

                    </div>


                    {
                        agreementFeatures.length > 0 && (

                            <div
                                style={{
                                    marginTop: "18px"
                                }}
                            >

                                <div
                                    style={{
                                        fontSize: "11px",
                                        fontWeight: 700,
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
                                    Shared Evidence
                                </div>


                                <div
                                    style={{
                                        display: "flex",
                                        flexWrap: "wrap",
                                        gap: "7px"
                                    }}
                                >

                                    {
                                        agreementFeatures
                                            .slice(0, 10)
                                            .map(
                                                (
                                                    feature,
                                                    index
                                                ) => {

                                                    const name =
                                                        typeof feature ===
                                                        "string"
                                                            ? feature
                                                            : getFeatureName(
                                                                feature
                                                            );


                                                    return (

                                                        <span
                                                            key={
                                                                `${name}-${index}`
                                                            }
                                                            className="badge badge-neutral"
                                                        >
                                                            {
                                                                formatFeatureName(
                                                                    name
                                                                )
                                                            }
                                                        </span>

                                                    );

                                                }
                                            )
                                    }

                                </div>

                            </div>

                        )
                    }


                    {
                        shapOnly.length > 0 && (

                            <div
                                style={{
                                    marginTop: "15px"
                                }}
                            >

                                <strong
                                    style={{
                                        fontSize: "12px"
                                    }}
                                >
                                    SHAP-only features:
                                </strong>{" "}


                                <span
                                    style={{
                                        color:
                                            "var(--muted-text, #64748b)"
                                    }}
                                >

                                    {
                                        shapOnly
                                            .slice(0, 8)
                                            .map(
                                                (
                                                    item
                                                ) => {

                                                    const name =
                                                        typeof item ===
                                                        "string"
                                                            ? item
                                                            : getFeatureName(
                                                                item
                                                            );


                                                    return formatFeatureName(
                                                        name
                                                    );

                                                }
                                            )
                                            .join(", ")
                                    }

                                </span>

                            </div>

                        )
                    }


                    {
                        limeOnly.length > 0 && (

                            <div
                                style={{
                                    marginTop: "8px"
                                }}
                            >

                                <strong
                                    style={{
                                        fontSize: "12px"
                                    }}
                                >
                                    LIME-only features:
                                </strong>{" "}


                                <span
                                    style={{
                                        color:
                                            "var(--muted-text, #64748b)"
                                    }}
                                >

                                    {
                                        limeOnly
                                            .slice(0, 8)
                                            .map(
                                                (
                                                    item
                                                ) => {

                                                    const name =
                                                        typeof item ===
                                                        "string"
                                                            ? item
                                                            : getLimeFeatureName(
                                                                item
                                                            );


                                                    return formatFeatureName(
                                                        name
                                                    );

                                                }
                                            )
                                            .join(", ")
                                    }

                                </span>

                            </div>

                        )
                    }


                    <div
                        className="clinical-note"
                        style={{
                            marginTop: "18px"
                        }}
                    >

                        Agreement measures consistency between
                        SHAP and LIME explanations for this model
                        prediction. It indicates explanation
                        consistency, not clinical certainty.

                    </div>

                </div>

            </div>

        </div>

    );

}


/* ============================================================
   COUNTERFACTUAL HELPERS
============================================================ */

function getCounterfactualChanges(cf) {

    if (!cf || typeof cf !== "object") {
        return {};
    }


    return (
        cf.changes ??
        cf.feature_changes ??
        cf.featureChanges ??
        cf.changed_features ??
        cf.changedFeatures ??
        {}
    );

}


function getCounterfactualPrediction(cf) {

    if (!cf) {
        return "—";
    }


    return (
        cf.prediction_text ??
        cf.prediction_label ??
        cf.new_prediction ??
        cf.newPrediction ??
        (
            cf.prediction !== undefined
                ? Number(cf.prediction) === 1
                    ? "Positive"
                    : "Negative"
                : "—"
        )
    );

}


function getCounterfactualProbability(cf) {

    if (!cf) {
        return null;
    }


    const value =
        cf.probability ??
        cf.new_probability ??
        cf.newProbability ??
        cf.prediction_probability ??
        cf.predictionProbability ??
        null;


    if (value === null || value === undefined) {
        return null;
    }


    const numeric =
        Number(value);


    if (
        Number.isFinite(numeric) &&
        numeric <= 1
    ) {

        return numeric * 100;

    }


    return numeric;

}


/* ============================================================
   COUNTERFACTUAL SECTION
============================================================ */

function CounterfactualSection({
    counterfactuals,
    disease
}) {

    const items =
        Array.isArray(counterfactuals)
            ? counterfactuals.slice(0, 5)
            : [];


    const diseaseLabel =
        disease
            ? String(disease)
                .replaceAll("_", " ")
                .replace(/\b\w/g, c => c.toUpperCase())
            : "Disease";


    return (

        <div className="wrap mt-24">

            <div className="panel">

                <div className="panel-header">

                    <div className="icon-badge">

                        <span
                            style={{
                                fontSize: "18px"
                            }}
                        >
                            ⧉
                        </span>

                    </div>


                    <div>

                        <div className="panel-title">
                            Multi-Feature Counterfactual Explanation
                        </div>

                        <div className="panel-title-sub">
                            Model-based what-if analysis · {diseaseLabel}
                        </div>

                    </div>

                </div>


                <div className="panel-body">

                    <p
                        style={{
                            marginTop: 0,
                            lineHeight: 1.6,
                            color:
                                "var(--muted-text, #64748b)"
                        }}
                    >

                        Counterfactual explanations identify
                        alternative patient profiles where one
                        or more clinical features may be changed
                        simultaneously to determine whether the
                        model prediction can change.

                    </p>


                    {
                        items.length > 0
                            ? (

                                <div
                                    style={{
                                        display: "grid",
                                        gap: "18px",
                                        marginTop: "20px"
                                    }}
                                >

                                    {
                                        items.map(
                                            (
                                                cf,
                                                index
                                            ) => {

                                                const changes =
                                                    getCounterfactualChanges(
                                                        cf
                                                    );


                                                const entries =
                                                    Object.entries(
                                                        changes || {}
                                                    );


                                                const probability =
                                                    getCounterfactualProbability(
                                                        cf
                                                    );


                                                const prediction =
                                                    getCounterfactualPrediction(
                                                        cf
                                                    );


                                                const numberOfChanges =
                                                    cf.number_of_changes ??
                                                    cf.numberOfChanges ??
                                                    cf.num_changes ??
                                                    entries.length;


                                                const magnitude =
                                                    cf.normalized_change ??
                                                    cf.normalizedChange ??
                                                    cf.change_magnitude ??
                                                    cf.changeMagnitude ??
                                                    null;


                                                return (

                                                    <div
                                                        key={
                                                            index
                                                        }
                                                        style={{
                                                            border:
                                                                "1px solid var(--border, #dbe4ee)",
                                                            borderRadius:
                                                                "10px",
                                                            padding:
                                                                "18px",
                                                            background:
                                                                "var(--panel-soft, #f8fafc)"
                                                        }}
                                                    >

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
                                                                    "15px"
                                                            }}
                                                        >

                                                            <strong>
                                                                Counterfactual #
                                                                {
                                                                    index +
                                                                    1
                                                                }
                                                            </strong>


                                                            <span className="badge badge-high">

                                                                {
                                                                    probability !==
                                                                    null
                                                                        ? `${probability.toFixed(
                                                                            2
                                                                        )}%`
                                                                        : "Prediction Changed"
                                                                }

                                                            </span>

                                                        </div>


                                                        <div
                                                            style={{
                                                                fontSize:
                                                                    "12px",
                                                                fontWeight:
                                                                    700,
                                                                textTransform:
                                                                    "uppercase",
                                                                letterSpacing:
                                                                    "0.05em",
                                                                color:
                                                                    "var(--muted-text, #64748b)",
                                                                marginBottom:
                                                                    "9px"
                                                            }}
                                                        >
                                                            Changed Clinical Features
                                                        </div>


                                                        {
                                                            entries.length > 0
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
                                                                            entries.map(
                                                                                (
                                                                                    [
                                                                                        feature,
                                                                                        values
                                                                                    ],
                                                                                    changeIndex
                                                                                ) => {

                                                                                    let oldValue =
                                                                                        "—";

                                                                                    let newValue =
                                                                                        "—";


                                                                                    if (
                                                                                        Array.isArray(
                                                                                            values
                                                                                        )
                                                                                    ) {

                                                                                        oldValue =
                                                                                            values[0];

                                                                                        newValue =
                                                                                            values[1];

                                                                                    }
                                                                                    else if (
                                                                                        values &&
                                                                                        typeof values ===
                                                                                        "object"
                                                                                    ) {

                                                                                        oldValue =
                                                                                            values.old ??
                                                                                            values.original ??
                                                                                            values.from ??
                                                                                            values.before ??
                                                                                            "—";

                                                                                        newValue =
                                                                                            values.new ??
                                                                                            values.counterfactual ??
                                                                                            values.to ??
                                                                                            values.after ??
                                                                                            "—";

                                                                                    }
                                                                                    else {

                                                                                        newValue =
                                                                                            values;

                                                                                    }


                                                                                    return (

                                                                                        <div
                                                                                            key={
                                                                                                changeIndex
                                                                                            }
                                                                                            style={{
                                                                                                display:
                                                                                                    "grid",
                                                                                                gridTemplateColumns:
                                                                                                    "minmax(150px, 1.5fr) minmax(60px, 1fr) 30px minmax(60px, 1fr)",
                                                                                                alignItems:
                                                                                                    "center",
                                                                                                gap:
                                                                                                    "8px",
                                                                                                padding:
                                                                                                    "9px 10px",
                                                                                                background:
                                                                                                    "#fff",
                                                                                                border:
                                                                                                    "1px solid var(--border, #e2e8f0)",
                                                                                                borderRadius:
                                                                                                    "7px"
                                                                                            }}
                                                                                        >

                                                                                            <strong
                                                                                                style={{
                                                                                                    fontSize:
                                                                                                        "13px"
                                                                                                }}
                                                                                            >
                                                                                                {
                                                                                                    formatFeatureName(
                                                                                                        feature
                                                                                                    )
                                                                                                }
                                                                                            </strong>


                                                                                            <span>
                                                                                                {
                                                                                                    String(
                                                                                                        oldValue
                                                                                                    )
                                                                                                }
                                                                                            </span>


                                                                                            <span
                                                                                                style={{
                                                                                                    textAlign:
                                                                                                        "center",
                                                                                                    fontWeight:
                                                                                                        700
                                                                                                }}
                                                                                            >
                                                                                                →
                                                                                            </span>


                                                                                            <strong>
                                                                                                {
                                                                                                    String(
                                                                                                        newValue
                                                                                                    )
                                                                                                }
                                                                                            </strong>

                                                                                        </div>

                                                                                    );

                                                                                }
                                                                            )
                                                                        }

                                                                    </div>

                                                                )
                                                                : (

                                                                    <div className="clinical-note">
                                                                        No feature changes were returned.
                                                                    </div>

                                                                )
                                                        }


                                                        <div
                                                            style={{
                                                                display:
                                                                    "grid",
                                                                gridTemplateColumns:
                                                                    "repeat(3, minmax(0, 1fr))",
                                                                gap:
                                                                    "1px",
                                                                background:
                                                                    "var(--line, #dbe4ee)",
                                                                marginTop:
                                                                    "14px",
                                                                border:
                                                                    "1px solid var(--line, #dbe4ee)"
                                                            }}
                                                        >

                                                            <div className="metric-tile">

                                                                <div className="metric-tile-label">
                                                                    New Prediction
                                                                </div>

                                                                <div
                                                                    className="metric-tile-value"
                                                                    style={{
                                                                        fontSize:
                                                                            "17px"
                                                                    }}
                                                                >
                                                                    {
                                                                        prediction
                                                                    }
                                                                </div>

                                                            </div>


                                                            <div className="metric-tile">

                                                                <div className="metric-tile-label">
                                                                    Features Changed
                                                                </div>

                                                                <div
                                                                    className="metric-tile-value"
                                                                    style={{
                                                                        fontSize:
                                                                            "17px"
                                                                    }}
                                                                >
                                                                    {
                                                                        numberOfChanges
                                                                    }
                                                                </div>

                                                            </div>


                                                            <div className="metric-tile">

                                                                <div className="metric-tile-label">
                                                                    Change Magnitude
                                                                </div>

                                                                <div
                                                                    className="metric-tile-value"
                                                                    style={{
                                                                        fontSize:
                                                                            "17px"
                                                                    }}
                                                                >

                                                                    {
                                                                        magnitude !==
                                                                        null &&
                                                                        magnitude !==
                                                                        undefined
                                                                            ? Number(
                                                                                magnitude
                                                                            ).toFixed(
                                                                                2
                                                                            )
                                                                            : "—"
                                                                    }

                                                                </div>

                                                            </div>

                                                        </div>

                                                    </div>

                                                );

                                            }
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
                                        No counterfactual profile was found.
                                    </strong>

                                    <br />

                                    The model did not return a valid
                                    alternative profile for this{" "}
                                    {disease || "disease"} case within
                                    the configured counterfactual search
                                    space.

                                </div>

                            )
                    }


                    <div
                        className="clinical-note"
                        style={{
                            marginTop:
                                "24px"
                        }}
                    >

                        Counterfactual explanations are hypothetical
                        model-based scenarios. They describe changes
                        that may alter the model output and must not
                        be interpreted as treatment recommendations,
                        prescriptions, or clinically required targets.

                    </div>

                </div>

            </div>

        </div>

    );

}


/* ============================================================
   MAIN FEATURE IMPORTANCE COMPONENT
============================================================ */

function FeatureImportance({

    features,

    limeFeatures,

    agreement,

    counterfactuals,

    disease = "heart"

}) {

    const hasShap =
        Array.isArray(features) &&
        features.length > 0;


    const hasLime =
        Array.isArray(limeFeatures) &&
        limeFeatures.length > 0;


    /*
     * SHAP-LIME Agreement is available for ALL FOUR diseases.
     *
     * Heart Disease
     * Diabetes
     * Chronic Kidney Disease
     * Stroke
     *
     * Backend agreement is preferred.
     * If backend agreement is absent, a canonicalized
     * SHAP/LIME overlap is calculated locally.
     */

    const showAgreement =
        Boolean(agreement) ||
        (
            hasShap &&
            hasLime
        );


    /*
     * Counterfactual UI is available for ALL diseases.
     *
     * The backend decides whether actual counterfactual
     * profiles exist.
     */

    const showCounterfactual =
        true;


    if (
        !hasShap &&
        !hasLime &&
        !showAgreement &&
        !showCounterfactual
    ) {

        return null;

    }


    return (

        <>

            {/* =================================================
                SHAP + LIME
            ================================================= */}

            {
                (
                    hasShap ||
                    hasLime
                ) && (

                    <div
                        className="wrap mt-24"
                    >

                        <div
                            className="explain-grid"
                        >

                            {
                                hasShap && (

                                    <ExplanationCard

                                        title="SHAP Evidence"

                                        subtitle="Feature contribution to the model decision"

                                        items={
                                            features
                                        }

                                        type="shap"

                                    />

                                )
                            }


                            {
                                hasLime && (

                                    <ExplanationCard

                                        title="LIME Evidence"

                                        subtitle="Local explanation for this patient"

                                        items={
                                            limeFeatures
                                        }

                                        type="lime"

                                    />

                                )
                            }

                        </div>

                    </div>

                )
            }


            {/* =================================================
                SHAP-LIME AGREEMENT
            ================================================= */}

            {
                showAgreement && (

                    <AgreementSection

                        agreement={
                            agreement
                        }

                        features={
                            features
                        }

                        limeFeatures={
                            limeFeatures
                        }

                    />

                )
            }


            {/* =================================================
                COUNTERFACTUAL
            ================================================= */}

            {
                showCounterfactual && (

                    <CounterfactualSection

                        counterfactuals={
                            counterfactuals
                        }

                        disease={
                            disease
                        }

                    />

                )
            }

        </>

    );

}


export default FeatureImportance;