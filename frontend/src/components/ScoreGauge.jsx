export default function ScoreGauge({ score }) {
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const clamped = Math.max(0, Math.min(100, score));
  const offset = circumference - (clamped / 100) * circumference;

  const color = clamped >= 75 ? "#0f6e6e" : clamped >= 50 ? "#e8a33d" : "#c65b4e";

  return (
    <svg width="160" height="160" viewBox="0 0 160 160">
      <circle cx="80" cy="80" r={radius} fill="none" stroke="#dfe2dc" strokeWidth="10" />
      <circle
        cx="80"
        cy="80"
        r={radius}
        fill="none"
        stroke={color}
        strokeWidth="10"
        strokeLinecap="round"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        transform="rotate(-90 80 80)"
        style={{ transition: "stroke-dashoffset 0.6s ease, stroke 0.3s ease" }}
      />
      <text
        x="80"
        y="76"
        textAnchor="middle"
        fontFamily="Space Grotesk, sans-serif"
        fontSize="34"
        fontWeight="700"
        fill="#14181f"
      >
        {clamped.toFixed(0)}
      </text>
      <text
        x="80"
        y="98"
        textAnchor="middle"
        fontFamily="JetBrains Mono, monospace"
        fontSize="11"
        letterSpacing="0.08em"
        fill="#8a8f84"
      >
        MATCH %
      </text>
    </svg>
  );
}
