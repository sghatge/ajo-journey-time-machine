from __future__ import annotations
import json
from pathlib import Path
import streamlit as st
from src.audit import append_audit, verify_audit
from src.risk import assess_risk
from src.simulator import parse_events, simulate

ROOT = Path(__file__).parent
AUDIT = ROOT / "audit.jsonl"
st.set_page_config(page_title="Journey Time Machine | OPSFORGE", page_icon="🧭", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:Manrope,sans-serif}
.stApp{background:radial-gradient(ellipse at 12% 0%,#17304b 0%,#0a1220 43%,#080d17 100%);color:#edf3ff}
[data-testid="stHeader"]{background:transparent}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#101d30,#0b1422);border-right:1px solid #26364d}
.block-container{padding-top:2rem;max-width:1440px}
.eyebrow,.kicker{color:#70d7e8;font-family:'DM Mono',monospace;letter-spacing:.16em;text-transform:uppercase;font-size:.72rem}
.hero{border:1px solid #31536a;border-radius:22px;padding:1.7rem 1.9rem;background:linear-gradient(120deg,rgba(20,52,77,.85),rgba(16,27,45,.78));box-shadow:0 20px 70px #0004;margin-bottom:1.4rem}
.hero h1{font-size:clamp(2.1rem,4vw,3.5rem);letter-spacing:-.055em;line-height:1.05;margin:.5rem 0;color:#f3f7ff}
.hero p{color:#aabbd2;max-width:780px;line-height:1.7}
.status-row{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:1rem}
.pill{margin:0}
.pill{display:inline-block;border:1px solid #3a7180;color:#9be9f1;border-radius:99px;padding:.32rem .7rem;font: .7rem 'DM Mono',monospace;letter-spacing:.08em;margin-right:.35rem}
.metric{border:1px solid #2a3b52;border-radius:16px;padding:1rem 1.1rem;background:linear-gradient(145deg,#192a42,#0d1828);min-height:112px}
.metric small{color:#9eafc7;text-transform:uppercase;letter-spacing:.1em}
.metric strong{display:block;color:#f1f6ff;font-size:2rem;letter-spacing:-.04em;margin:.2rem 0}
.metric span{color:#8296b2;font-size:.75rem}
.panel{border:1px solid #2a3b52;background:#111e30cc;border-radius:16px;padding:1.1rem 1.2rem;min-height:140px}
.panel h4{color:#eaf2ff;margin:0 0 .4rem}.panel p{color:#9eb0c8;font-size:.86rem;line-height:1.6}
div.stButton>button[kind="primary"]{background:linear-gradient(100deg,#62cddd,#779cff);color:#071321;border:0;border-radius:11px;font-weight:800}
[data-testid="stMetric"]{background:#122039;border:1px solid #2a3b52;border-radius:14px;padding:1rem}
.stTabs [data-baseweb="tab-list"]{gap:1rem;border-bottom:1px solid #2a3b52}
.stTabs [aria-selected="true"]{color:#82deeb!important}
@media(max-width:700px){.block-container{padding:1rem .85rem 2rem}.hero{padding:1.25rem 1.1rem;border-radius:17px;margin-bottom:1rem}.hero h1{font-size:2.25rem;line-height:1.05}.hero p{font-size:1rem;line-height:1.55}.eyebrow,.kicker{letter-spacing:.11em;font-size:.65rem}.metric{min-height:94px;padding:.8rem}.metric strong{font-size:1.65rem}.panel{padding:1rem;min-height:auto}.stTabs [data-baseweb="tab-list"]{gap:.35rem}.stTabs [data-baseweb="tab"]{padding:.45rem .55rem;font-size:.82rem}}
</style>
""", unsafe_allow_html=True)

def metric(label, value, note):
    st.markdown(f'<div class="metric"><small>{label}</small><strong>{value}</strong><span>{note}</span></div>', unsafe_allow_html=True)

def fixture():
    return json.loads((ROOT / "data" / "sample_events.json").read_text(encoding="utf-8"))

def apply_scenario(name, rows):
    rows = [dict(r) for r in rows]
    if name == "Consent pressure test":
        for i, row in enumerate(rows):
            if i % 2 == 0: row["consent"] = "pending"
    elif name == "Opt-out pressure test":
        for i, row in enumerate(rows):
            if i % 2 == 0: row["opted_out"] = True
    elif name == "Duplicate-event test" and rows:
        rows.append(dict(rows[0]))
    return rows

with st.sidebar:
    st.markdown('<div class="eyebrow">OPSFORGE / CONTROL ROOM</div>', unsafe_allow_html=True)
    st.title("About this lab")
    st.caption("A synthetic-data-only shadow simulator for journey assurance.")
    st.divider()
    st.caption("ENGINE · DETERMINISTIC")
    st.caption("DATA · SYNTHETIC ONLY")
    st.caption("CONTROL · HUMAN APPROVAL")
    st.info("Choose a scenario and run it from the main workspace. No campaigns are sent or changed.")

st.markdown('<div class="hero"><div class="eyebrow">AUTONOMOUS JOURNEY ASSURANCE / LAB 01</div><h1>Journey Time Machine</h1><p>Pressure-test customer journey logic before it reaches a production workflow. Inspect consent decisions, projected actions, risk signals and tamper-evident run evidence — in a controlled synthetic environment.</p><div class="status-row"><span class="pill">● SHADOW MODE</span><span class="pill">SYNTHETIC DATA</span><span class="pill">HUMAN-IN-THE-LOOP</span></div></div>', unsafe_allow_html=True)
st.markdown('<div class="kicker">01 / RUN CONFIGURATION</div><h3>Configure your test</h3>', unsafe_allow_html=True)
cfg1, cfg2, cfg3 = st.columns([2, 1, 1])
with cfg1:
    scenario = st.selectbox("Test scenario", ["Baseline fixture","Consent pressure test","Opt-out pressure test","Duplicate-event test"], key="main_scenario")
with cfg2:
    seed = st.number_input("Run seed", min_value=0, max_value=999999, value=42, key="main_seed")
with cfg3:
    st.markdown("<div style=\'height:1.85rem\'></div>", unsafe_allow_html=True)
    run = st.button("▶  Run simulation", type="primary", use_container_width=True)
st.caption("Repeatable synthetic tests · no production data · no campaign activation")
st.markdown('<div class="kicker">02 / MISSION STATUS</div><h3>Simulation workspace</h3>', unsafe_allow_html=True)

if run:
    try:
        events = parse_events(apply_scenario(scenario, fixture()))
        result = simulate(events, seed=int(seed))
        risk = assess_risk(result)
        entry = append_audit({"run_id":result.run_id,"risk":risk,"mode":"synthetic","scenario":scenario}, path=AUDIT)
        st.session_state["result"] = result.model_dump(mode="json")
        st.session_state["risk"] = risk
        st.session_state["scenario"] = scenario
        st.session_state["audit"] = entry
        st.toast("Simulation completed and evidence recorded.", icon="✅")
    except Exception as exc:
        st.error(f"Simulation failed: {exc}")

if "result" not in st.session_state:
    a,b=st.columns([1.3,1])
    with a: st.markdown('<div class="panel"><div class="kicker">READY STATE</div><h4>Awaiting your first run</h4><p>Choose a scenario in the control panel and run the deterministic engine. The bundled fixture contains five synthetic profiles demonstrating fail-closed consent handling.</p></div>',unsafe_allow_html=True)
    with b: st.markdown('<div class="panel"><div class="kicker">ASSURANCE DIMENSIONS</div><h4>What you can inspect</h4><p>Eligibility decisions · Projected channel actions · Risk classification · Hash-chain audit integrity</p></div>',unsafe_allow_html=True)
    st.info("Start with **Baseline fixture**, then compare the consent and opt-out pressure tests.")
else:
    result=st.session_state["result"]; risk=st.session_state["risk"]; entry=st.session_state["audit"]
    cols=st.columns(4)
    values=[("Profiles evaluated",risk["profiles_evaluated"],"Synthetic profiles"),("Eligible profiles",result["eligible_profiles"],"Passed eligibility gate"),("Excluded profiles",result["excluded_profiles"],"Fail-closed exclusions"),("Projected actions",risk["projected_actions"],"Not sent · Simulation only")]
    for col,(label,value,note) in zip(cols,values):
        with col: metric(label,str(value),note)
    overview,paths,findings,evidence=st.tabs(["◈  Overview","⌁  Journey paths","⚑  Findings","⛓  Audit evidence"])
    with overview:
        left,right=st.columns([1,1])
        with left:
            st.markdown("#### Risk decision")
            st.metric("Risk classification",risk["severity"],risk["decision"].replace("_"," ").title())
            st.progress(float(risk["exclusion_rate"]),text=f'Exclusion rate · {risk["exclusion_rate"]:.1%}')
            st.caption(f'Scenario: {st.session_state["scenario"]} · Run ID: {result["run_id"]}')
        with right:
            st.markdown("#### Eligibility distribution")
            st.bar_chart({"Profiles":{"Eligible":result["eligible_profiles"],"Excluded":result["excluded_profiles"]}})
        st.caption("Prototype heuristic based on synthetic exclusions and projected action volume; not an Adobe product control or production safety certification.")
    with paths:
        st.markdown("#### Profile-level trace explorer")
        for profile,path in result["profile_paths"].items():
            with st.expander(f'{profile}  ·  {" → ".join(path)}'):
                st.code("  →  ".join(path))
                st.caption("Simplified illustrative trace from the MVP simulator.")
    with findings:
        st.markdown("#### Explainable engine findings")
        if risk["findings"]:
            for finding in risk["findings"]: st.warning(finding,icon="⚑")
        else: st.success("No findings raised for this synthetic run.")
    with evidence:
        st.markdown("#### Chain of custody")
        valid=verify_audit(path=AUDIT)
        x,y=st.columns(2)
        x.metric("Hash-chain integrity","VALID" if valid else "FAILED")
        y.metric("Recorded at (UTC)",entry["timestamp"][:19].replace("T"," "))
        st.caption("Latest record SHA-256")
        st.code(entry["hash"])
        report={"simulation":result,"risk":risk,"scenario":st.session_state["scenario"],"audit_record":entry,"audit_chain_valid":valid}
        st.download_button("↓  Export run evidence (JSON)",json.dumps(report,indent=2),file_name=f'{result["run_id"]}-evidence.json',mime="application/json")

st.divider()
st.markdown('<div class="kicker">GUARDRAILS / READ THIS FIRST</div>',unsafe_allow_html=True)
a,b,c=st.columns(3)
with a: st.markdown('<div class="panel"><h4>🔒 Synthetic by design</h4><p>Use only bundled synthetic events. Never upload customer records, identifiers or production exports.</p></div>',unsafe_allow_html=True)
with b: st.markdown('<div class="panel"><h4>🧪 Advisory simulation</h4><p>This is a small deterministic model, not a full AEP/AJO runtime emulator or proof of production safety.</p></div>',unsafe_allow_html=True)
with c: st.markdown('<div class="panel"><h4>🧑‍⚖️ Human control</h4><p>No publish, pause, send or activation capability exists. Future integrations require security and semantic validation.</p></div>',unsafe_allow_html=True)
st.caption("OPSFORGE · AJO JOURNEY TIME MACHINE · Independent open-source assurance prototype · Not affiliated with or certified by Adobe.")
