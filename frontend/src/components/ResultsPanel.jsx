import ScoreGauge from "./ScoreGauge.jsx";

function ChipList({ items, variant }) {
  if (!items || items.length === 0) {
    return <p className="empty-note">None detected</p>;
  }
  return (
    <div className="chip-list">
      {items.map((skill) => (
        <span key={skill} className={`chip ${variant}`}>
          {skill}
        </span>
      ))}
    </div>
  );
}

export default function ResultsPanel({ result }) {
  if (!result) return null;
  const { match_score, verdict, skill_gap } = result;

  return (
    <div className="panel results">
      <div className="gauge-wrap">
        <ScoreGauge score={match_score} />
        <span className="verdict">{verdict}</span>
      </div>

      <div className="skill-columns">
        <div className="skill-col">
          <h4>Matched</h4>
          <ChipList items={skill_gap.matched_skills} variant="matched" />
        </div>
        <div className="skill-col">
          <h4>Missing (in JD, not resume)</h4>
          <ChipList items={skill_gap.missing_skills} variant="missing" />
        </div>
        <div className="skill-col">
          <h4>Extra (in resume, not JD)</h4>
          <ChipList items={skill_gap.resume_only_skills} variant="extra" />
        </div>
      </div>
    </div>
  );
}
