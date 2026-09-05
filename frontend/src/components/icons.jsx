// ==========================================================
// Shared line-icon set.
// Plain inline SVGs, no external icon package required.
// ==========================================================

const base = {
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.6,
    strokeLinecap: "round",
    strokeLinejoin: "round"
};

export function IconPulse({ size = 18, className = "" }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className} {...base}>
            <path d="M2 12h4l2 7 4-14 2 7h8" />
        </svg>
    );
}

export function IconHeart({ size = 18, className = "" }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className} {...base}>
            <path d="M12 20s-7-4.4-9.5-8.8C1 8 2.2 4.8 5.3 4.1 7.5 3.6 9.8 4.6 12 7c2.2-2.4 4.5-3.4 6.7-2.9 3.1.7 4.3 3.9 2.8 7.1C19 15.6 12 20 12 20z" />
        </svg>
    );
}

export function IconDroplet({ size = 18, className = "" }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className} {...base}>
            <path d="M12 3s6.5 7 6.5 11.5a6.5 6.5 0 0 1-13 0C5.5 10 12 3 12 3z" />
        </svg>
    );
}

export function IconKidney({ size = 18, className = "" }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className} {...base}>
            <path d="M9 3c-3 0-5 3-5 7.5S6 20 10 20c2 0 2.5-1.6 2-3.2-.6-1.8-2-2.4-2-4.3 0-2.2 2-2.7 2-5C12 4.7 10.8 3 9 3z" />
        </svg>
    );
}

export function IconBrain({ size = 18, className = "" }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className} {...base}>
            <path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-1.5 5.6A3.5 3.5 0 0 0 8 18a3 3 0 0 0 3-1" />
            <path d="M15 4a3 3 0 0 1 3 3 3 3 0 0 1 1.5 5.6A3.5 3.5 0 0 1 16 18a3 3 0 0 1-3-1" />
            <path d="M9 4c1.7 0 3 1.3 3 3v9" />
        </svg>
    );
}

export function IconAlertTriangle({ size = 18, className = "" }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className} {...base}>
            <path d="M10.6 3.9 2.4 18a1.5 1.5 0 0 0 1.3 2.3h16.6a1.5 1.5 0 0 0 1.3-2.3L13.4 3.9a1.6 1.6 0 0 0-2.8 0z" />
            <path d="M12 9.5v4.2" />
            <path d="M12 17h.01" />
        </svg>
    );
}

export function IconCheckCircle({ size = 18, className = "" }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className} {...base}>
            <circle cx="12" cy="12" r="9" />
            <path d="M8.3 12.3l2.4 2.4 5-5.2" />
        </svg>
    );
}

export function IconDownload({ size = 18, className = "" }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className} {...base}>
            <path d="M12 3v12" />
            <path d="M7.5 10.5 12 15l4.5-4.5" />
            <path d="M4 19.5h16" />
        </svg>
    );
}

export function IconRefresh({ size = 18, className = "" }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className} {...base}>
            <path d="M20 11A8 8 0 0 0 6.3 6.3L4 8.6" />
            <path d="M4 4v4.6h4.6" />
            <path d="M4 13a8 8 0 0 0 13.7 4.7L20 15.4" />
            <path d="M20 20v-4.6h-4.6" />
        </svg>
    );
}

export function IconClock({ size = 18, className = "" }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className} {...base}>
            <circle cx="12" cy="12" r="9" />
            <path d="M12 7v5l3.2 2" />
        </svg>
    );
}

export function IconLayers({ size = 18, className = "" }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className} {...base}>
            <path d="m12 3 9 5-9 5-9-5 9-5z" />
            <path d="m3 13 9 5 9-5" />
        </svg>
    );
}

export function IconUser({ size = 18, className = "" }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className} {...base}>
            <circle cx="12" cy="8" r="3.4" />
            <path d="M5 20c1.2-3.6 4-5.4 7-5.4s5.8 1.8 7 5.4" />
        </svg>
    );
}

export function IconChart({ size = 18, className = "" }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className} {...base}>
            <path d="M4 20V10" />
            <path d="M12 20V4" />
            <path d="M20 20v-7" />
        </svg>
    );
}

export function IconTarget({ size = 18, className = "" }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" className={className} {...base}>
            <circle cx="12" cy="12" r="8.5" />
            <circle cx="12" cy="12" r="4.5" />
            <circle cx="12" cy="12" r="0.6" fill="currentColor" stroke="none" />
        </svg>
    );
}
