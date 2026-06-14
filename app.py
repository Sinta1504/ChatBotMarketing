"""
app.py - Streamlit version of MarketBot
HTML, CSS, JS dari index.html di-embed langsung.
Logika FSM (FSM.py) dan engine (engine.py) diport ke JavaScript agar
berjalan sepenuhnya di browser tanpa memerlukan Flask backend.
"""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="MarketBot — Konsultan Pemasaran Digital",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Sembunyikan toolbar/header/footer Streamlit agar tampilan persis HTML asli
st.markdown("""
<style>
  #MainMenu, header, footer { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  [data-testid="stAppViewContainer"] { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

HTML = r"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MarketBot — Konsultan Pemasaran Digital</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Sora:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --ink:        #0f1623;
  --ink-2:      #2d3748;
  --ink-3:      #64748b;
  --paper:      #f8fafc;
  --white:      #ffffff;
  --brand:      #4f46e5;
  --brand-2:    #7c3aed;
  --brand-glow: #818cf8;
  --accent:     #06b6d4;
  --success:    #10b981;
  --warn:       #f59e0b;
  --surface:    #ffffff;
  --surface-2:  #f1f5f9;
  --border:     #e2e8f0;
  --shadow-sm:  0 1px 3px rgba(0,0,0,.08);
  --shadow-md:  0 4px 16px rgba(0,0,0,.10);
  --shadow-lg:  0 12px 40px rgba(0,0,0,.14);
  --r-sm:       8px;
  --r-md:       14px;
  --r-lg:       20px;
  --r-xl:       28px;
  --font-ui:    'Plus Jakarta Sans', sans-serif;
  --font-head:  'Sora', sans-serif;
  --nav-h:      64px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: var(--font-ui);
  background: var(--paper);
  color: var(--ink);
  line-height: 1.6;
  overflow-x: hidden;
}
a { text-decoration: none; color: inherit; }

/* ─── CHAT PAGE OVERLAY ─────────────────────────────────── */
#chatPage {
  display: none;
  position: fixed;
  inset: 0;
  z-index: 1100;
  background: #0d1117;
  flex-direction: column;
}
#chatPage.active { display: flex; }

/* ─── NAVBAR ─────────────────────────────────────────────────────────── */
nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 999;
  height: var(--nav-h);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 clamp(20px,5vw,60px);
  background: rgba(255,255,255,.92);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  transition: background .3s;
}
.nav-logo {
  display: flex; align-items: center; gap: 10px;
  font-family: var(--font-head); font-weight: 700; font-size: 1.15rem;
  color: var(--brand); cursor: pointer;
}
.nav-logo-dot {
  width: 32px; height: 32px; border-radius: 8px;
  background: linear-gradient(135deg, var(--brand), var(--brand-2));
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: .85rem; font-weight: 800;
}
.nav-links {
  display: flex; align-items: center; gap: 4px;
  list-style: none;
}
.nav-links a {
  padding: 8px 16px; border-radius: var(--r-sm);
  font-weight: 500; font-size: .9rem; color: var(--ink-2);
  transition: all .2s; cursor: pointer;
}
.nav-links a:hover, .nav-links a.active {
  background: var(--surface-2); color: var(--brand);
}
.nav-cta {
  background: linear-gradient(135deg, var(--brand), var(--brand-2)) !important;
  color: #fff !important; padding: 9px 20px !important;
  border-radius: var(--r-sm) !important;
  box-shadow: 0 2px 12px rgba(79,70,229,.3);
  transition: transform .15s, box-shadow .15s !important;
}
.nav-cta:hover { transform: translateY(-1px); box-shadow: 0 4px 18px rgba(79,70,229,.4) !important; }
.nav-hamburger { display: none; cursor: pointer; padding: 8px; border-radius: 8px; border: none; background: transparent; }
.nav-hamburger span { display: block; width: 22px; height: 2px; background: var(--ink-2); margin: 5px 0; border-radius: 2px; transition: all .3s; }

/* ─── MAIN CONTENT ─────────────────────────────────────────────── */
#mainContent { overflow-x: hidden; }
.section { display: block; scroll-margin-top: var(--nav-h); }

/* ─── HOME ────────────────────────────────────────────────────────── */
#home {
  background: linear-gradient(160deg, #eef2ff 0%, #f8fafc 50%, #ecfdf5 100%);
  padding-top: var(--nav-h);
  /* Padding dikurangi agar tidak terlalu jauh */
  padding-bottom: 40px;
}
.hero {
  max-width: 1100px; margin: 0 auto;
  /* Padding atas/bawah dikurangi agar section lebih rapat */
  padding: clamp(40px,6vh,80px) clamp(20px,5vw,60px) 40px;
  display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(79,70,229,.08); border: 1px solid rgba(79,70,229,.18);
  color: var(--brand); padding: 6px 14px; border-radius: 99px;
  font-size: .8rem; font-weight: 600; margin-bottom: 20px;
}
.hero-badge-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--success); animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }
.hero h1 {
  font-family: var(--font-head); font-size: clamp(2rem,3.8vw,3rem);
  font-weight: 700; line-height: 1.15; margin-bottom: 18px; color: var(--ink);
}
.hero h1 span { color: var(--brand); }
.hero-sub { font-size: 1.02rem; color: var(--ink-3); max-width: 480px; margin-bottom: 32px; line-height: 1.7; }
.hero-btns { display: flex; gap: 12px; flex-wrap: wrap; }
.btn-primary {
  display: inline-flex; align-items: center; gap: 8px;
  background: linear-gradient(135deg, var(--brand), var(--brand-2));
  color: #fff; padding: 13px 26px; border-radius: var(--r-md);
  font-weight: 600; font-size: .95rem; border: none; cursor: pointer;
  box-shadow: 0 4px 20px rgba(79,70,229,.35); transition: all .2s;
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(79,70,229,.45); }
.btn-outline {
  display: inline-flex; align-items: center; gap: 8px;
  border: 1.5px solid var(--border); background: var(--white);
  color: var(--ink-2); padding: 12px 24px; border-radius: var(--r-md);
  font-weight: 600; font-size: .95rem; cursor: pointer; transition: all .2s;
}
.btn-outline:hover { border-color: var(--brand); color: var(--brand); background: rgba(79,70,229,.04); }
.hero-visual { position: relative; display: flex; justify-content: center; align-items: center; }
.hero-card {
  background: var(--white); border-radius: var(--r-xl); padding: 28px;
  box-shadow: var(--shadow-lg); width: 100%; max-width: 380px;
  border: 1px solid var(--border);
}
.hero-card-header {
  display: flex; align-items: center; gap: 10px; margin-bottom: 20px;
  padding-bottom: 14px; border-bottom: 1px solid var(--border);
}
.hc-avatar {
  width: 40px; height: 40px; border-radius: 12px;
  background: linear-gradient(135deg, var(--brand), var(--brand-2));
  display: flex; align-items: center; justify-content: center; color: #fff; font-size: 1.1rem;
}
.hc-name { font-weight: 700; font-size: .9rem; }
.hc-status { font-size: .75rem; color: var(--success); display: flex; align-items: center; gap: 4px; }
.hc-status::before { content:''; width:6px; height:6px; border-radius:50%; background:var(--success); display:inline-block; }
.chat-bubble { padding: 10px 14px; border-radius: 12px; margin-bottom: 10px; font-size: .85rem; max-width: 90%; }
.chat-bubble.bot { background: var(--surface-2); color: var(--ink-2); border-bottom-left-radius: 4px; }
.chat-bubble.user {
  background: linear-gradient(135deg, var(--brand), var(--brand-2));
  color: #fff; margin-left: auto; border-bottom-right-radius: 4px;
}
.typing-indicator { display: flex; gap: 4px; padding: 10px 14px; }
.typing-indicator span { width: 7px; height: 7px; border-radius: 50%; background: var(--ink-3); animation: typing .8s infinite; }
.typing-indicator span:nth-child(2) { animation-delay: .15s; }
.typing-indicator span:nth-child(3) { animation-delay: .3s; }
@keyframes typing { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-5px)} }

/* stats row */
.stats-row {
  max-width: 1100px; margin: 0 auto;
  /* Padding dikurangi agar lebih rapat */
  padding: 20px clamp(20px,5vw,60px);
  display: grid; grid-template-columns: repeat(4,1fr); gap: 20px;
}
.stat-card {
  background: var(--white); border: 1px solid var(--border); border-radius: var(--r-lg);
  padding: 24px; text-align: center; box-shadow: var(--shadow-sm); transition: box-shadow .2s;
}
.stat-card:hover { box-shadow: var(--shadow-md); }
.stat-num { font-family: var(--font-head); font-size: 2rem; font-weight: 700; color: var(--brand); }
.stat-label { font-size: .82rem; color: var(--ink-3); margin-top: 4px; }

/* features grid */
.features { max-width: 1100px; margin: 0 auto; padding: 0 clamp(20px,5vw,60px) 40px; }
.features-title { text-align: center; margin-bottom: 40px; }
.features-title h2 { font-family: var(--font-head); font-size: 1.9rem; font-weight: 700; margin-bottom: 10px; }
.features-title p { color: var(--ink-3); font-size: 1rem; }
.features-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 24px; }
.feature-card {
  background: var(--white); border: 1px solid var(--border); border-radius: var(--r-lg);
  padding: 28px; transition: all .25s;
}
.feature-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); border-color: var(--brand-glow); }
.feature-icon { width: 48px; height: 48px; border-radius: 12px; margin-bottom: 16px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; }
.feature-card h3 { font-size: 1rem; font-weight: 700; margin-bottom: 8px; }
.feature-card p { font-size: .88rem; color: var(--ink-3); line-height: 1.6; }

/* ─── ABOUT ──────────────────────────────────────────────────────────── */
#about { background: var(--paper); padding-top: var(--nav-h); }
.about-inner {
  max-width: 1000px; margin: 0 auto;
  /* Padding dikurangi agar lebih rapat */
  padding: clamp(30px,5vh,60px) clamp(20px,5vw,60px) 40px;
}
.section-badge {
  display: inline-block; background: rgba(79,70,229,.08); color: var(--brand);
  padding: 5px 14px; border-radius: 99px; font-size: .78rem; font-weight: 600;
  margin-bottom: 14px; border: 1px solid rgba(79,70,229,.15);
}
.about-inner h2 { font-family: var(--font-head); font-size: clamp(1.7rem,3vw,2.4rem); font-weight: 700; margin-bottom: 20px; }
.about-inner > p { color: var(--ink-3); line-height: 1.8; margin-bottom: 14px; font-size: .97rem; }
.about-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; align-items: start; margin-top: 32px; }
.fsm-visual { background: var(--white); border: 1px solid var(--border); border-radius: var(--r-xl); padding: 24px; box-shadow: var(--shadow-md); }
.fsm-title { font-weight: 700; font-size: .9rem; color: var(--ink-3); margin-bottom: 14px; text-transform: uppercase; letter-spacing: .05em; }
.fsm-states { display: flex; flex-wrap: wrap; gap: 8px; }
.fsm-state { padding: 5px 11px; border-radius: 6px; font-size: .78rem; font-weight: 600; background: var(--surface-2); color: var(--ink-2); border: 1px solid var(--border); }
.fsm-state.input { background: rgba(79,70,229,.08); color: var(--brand); border-color: rgba(79,70,229,.2); }
.fsm-state.analysis { background: rgba(6,182,212,.08); color: #0891b2; border-color: rgba(6,182,212,.2); }
.fsm-state.final { background: rgba(16,185,129,.08); color: #059669; border-color: rgba(16,185,129,.2); }
.complexity-card { background: linear-gradient(135deg, var(--brand), var(--brand-2)); border-radius: var(--r-xl); padding: 24px; color: #fff; }
.complexity-card h3 { font-family: var(--font-head); font-size: 1.1rem; margin-bottom: 16px; }
.complexity-num { font-size: 2.5rem; font-weight: 800; line-height: 1; }
.complexity-label { font-size: .85rem; opacity: .8; margin-top: 4px; }
.complexity-list { margin-top: 16px; display: grid; gap: 6px; }
.complexity-item { display: flex; justify-content: space-between; align-items: center; font-size: .85rem; opacity: .9; }
.complexity-item span:last-child { font-weight: 700; opacity: 1; }
.dev-section { margin-top: 32px; }
.dev-section h3 { font-family: var(--font-head); font-size: 1.3rem; margin-bottom: 18px; }
.dev-cards { display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; }
.dev-card { background: var(--white); border: 1px solid var(--border); border-radius: var(--r-md); padding: 20px; transition: all .2s; }
.dev-card:hover { box-shadow: var(--shadow-md); border-color: var(--brand-glow); }
.dev-card-num { width: 28px; height: 28px; border-radius: 8px; background: linear-gradient(135deg,var(--brand),var(--brand-2)); color: #fff; font-size: .78rem; font-weight: 700; display: flex; align-items: center; justify-content: center; margin-bottom: 10px; }
.dev-card h4 { font-size: .88rem; font-weight: 700; margin-bottom: 6px; }
.dev-card p { font-size: .8rem; color: var(--ink-3); line-height: 1.5; }

/* ─── TIPS SECTION ───────────────────────────────── */
#tips { background: linear-gradient(160deg, #f0fdf4 0%, var(--paper) 100%); padding-top: var(--nav-h); }
.tips-inner { max-width: 1000px; margin: 0 auto; padding: clamp(30px,5vh,60px) clamp(20px,5vw,60px) 40px; }
.tips-inner h2 { font-family: var(--font-head); font-size: clamp(1.7rem,3vw,2.4rem); font-weight: 700; margin-bottom: 8px; }
.tips-inner > p { color: var(--ink-3); margin-bottom: 36px; font-size: .97rem; line-height: 1.7; }
.tips-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 36px; }
.tip-card {
  background: var(--white); border: 1px solid var(--border); border-radius: var(--r-lg);
  padding: 24px; transition: all .25s; position: relative; overflow: hidden;
}
.tip-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; background: linear-gradient(90deg, var(--brand), var(--accent)); transform:scaleX(0); transform-origin:left; transition:transform .3s; }
.tip-card:hover::before { transform:scaleX(1); }
.tip-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
.tip-icon { font-size: 1.8rem; margin-bottom: 12px; }
.tip-card h3 { font-size: .95rem; font-weight: 700; margin-bottom: 8px; color: var(--ink); }
.tip-card p { font-size: .85rem; color: var(--ink-3); line-height: 1.6; }
.tips-cta {
  text-align: center; background: linear-gradient(135deg, var(--brand), var(--brand-2));
  border-radius: var(--r-xl); padding: 40px; color: #fff;
}
.tips-cta h3 { font-family: var(--font-head); font-size: 1.5rem; margin-bottom: 10px; }
.tips-cta p { opacity: .85; font-size: .95rem; margin-bottom: 24px; }
.tips-cta-btn {
  display: inline-flex; align-items: center; gap: 8px;
  background: #fff; color: var(--brand);
  padding: 13px 28px; border-radius: var(--r-md);
  font-weight: 700; font-size: .95rem; cursor: pointer; border: none;
  transition: all .2s; box-shadow: 0 4px 20px rgba(0,0,0,.2);
}
.tips-cta-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 32px rgba(0,0,0,.25); }

/* ─── SARAN ──────────────────────────────────────────────────────────── */
#saran { background: var(--paper); padding-top: var(--nav-h); }
.saran-inner { max-width: 1000px; margin: 0 auto; padding: clamp(30px,5vh,60px) clamp(20px,5vw,60px) 40px; }
.saran-inner h2 { font-family: var(--font-head); font-size: clamp(1.7rem,3vw,2.4rem); font-weight: 700; margin-bottom: 8px; }
.saran-inner > p { color: var(--ink-3); margin-bottom: 36px; font-size: .97rem; }
.saran-cards { display: grid; grid-template-columns: repeat(2,1fr); gap: 20px; }
.saran-card { background: var(--white); border: 1px solid var(--border); border-radius: var(--r-xl); padding: 24px; transition: all .25s; position: relative; overflow: hidden; }
.saran-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; background: linear-gradient(90deg, var(--brand), var(--brand-2)); transform:scaleX(0); transform-origin:left; transition:transform .3s; }
.saran-card:hover::before { transform:scaleX(1); }
.saran-card:hover { box-shadow: var(--shadow-md); transform: translateY(-3px); }
.saran-num { width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, var(--brand), var(--brand-2)); color: #fff; font-weight: 800; font-size: .85rem; display: flex; align-items: center; justify-content: center; margin-bottom: 14px; }
.saran-card h3 { font-size: 1rem; font-weight: 700; margin-bottom: 8px; color: var(--ink); }
.saran-card p { font-size: .88rem; color: var(--ink-3); line-height: 1.7; }
.saran-card ul { font-size: .88rem; color: var(--ink-3); line-height: 1.7; padding-left: 18px; margin-top: 8px; }
.saran-card ul li { margin-bottom: 4px; }
.saran-highlight { margin-top: 32px; background: linear-gradient(135deg, var(--brand), var(--brand-2)); border-radius: var(--r-xl); padding: 32px; color: #fff; display: grid; grid-template-columns: 1fr auto; gap: 24px; align-items: center; }
.saran-highlight h3 { font-family: var(--font-head); font-size: 1.2rem; margin-bottom: 8px; }
.saran-highlight p { opacity: .85; font-size: .9rem; line-height: 1.6; }
.saran-highlight-num { font-family: var(--font-head); font-size: 3rem; font-weight: 800; opacity: .6; }

/* ─── FOOTER ──────────────────────────────────────────────────────────── */
footer { background: var(--ink); color: rgba(255,255,255,.5); text-align: center; padding: 24px 20px; font-size: .82rem; }
footer span { color: rgba(255,255,255,.8); font-weight: 600; }

/* ═══════════════════════════════════════════════════════════════════════
   CHATBOT PAGE
═══════════════════════════════════════════════════════════════════════ */
.chat-nav {
  height: var(--nav-h);
  background: rgba(13,17,23,.97);
  border-bottom: 1px solid rgba(255,255,255,.08);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 clamp(20px,5vw,60px);
  flex-shrink: 0;
}
.chat-nav-logo {
  display: flex; align-items: center; gap: 10px;
  font-family: var(--font-head); font-weight: 700; font-size: 1.15rem;
  color: #a5b4fc; cursor: pointer;
}
.chat-nav-links { display: flex; align-items: center; gap: 4px; list-style: none; }
.chat-nav-links a {
  padding: 8px 16px; border-radius: var(--r-sm);
  font-weight: 500; font-size: .9rem; color: #94a3b8;
  transition: all .2s; cursor: pointer; display: block;
}
.chat-nav-links a:hover { background: rgba(255,255,255,.08); color: #f1f5f9; }
.chat-nav-back {
  background: rgba(255,255,255,.07) !important;
  border: 1px solid rgba(255,255,255,.12) !important;
  color: #e2e8f0 !important;
  border-radius: var(--r-sm);
}
.chat-nav-back:hover { background: rgba(255,255,255,.12) !important; }

.chatbot-topbar {
  background: rgba(255,255,255,.03); border-bottom: 1px solid rgba(255,255,255,.07);
  padding: 10px clamp(16px,4vw,40px);
  display: flex; align-items: center; justify-content: space-between;
  flex-shrink: 0;
}
.chatbot-topbar-left { display: flex; align-items: center; gap: 12px; }
.bot-avatar-live {
  width: 40px; height: 40px; border-radius: 12px;
  background: linear-gradient(135deg, var(--brand), var(--brand-2));
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem; position: relative; flex-shrink: 0;
}
.bot-avatar-live::after { content:''; position:absolute; bottom:2px; right:2px; width:10px; height:10px; border-radius:50%; background:var(--success); border:2px solid #0d1117; }
.bot-info-name { color: #f1f5f9; font-weight: 700; font-size: .95rem; }
.bot-info-sub { color: #64748b; font-size: .78rem; }
.progress-container { display: flex; align-items: center; gap: 12px; }
.progress-text { color: #64748b; font-size: .78rem; white-space: nowrap; }
.progress-bar-wrap { width: 140px; height: 4px; background: rgba(255,255,255,.1); border-radius: 2px; overflow: hidden; }
.progress-bar-fill { height: 100%; background: linear-gradient(90deg, var(--brand), var(--accent)); border-radius: 2px; transition: width .4s ease; }

.chatbot-body {
  flex: 1; overflow-y: auto; padding: 20px clamp(16px,4vw,40px);
  display: flex; flex-direction: column; gap: 0;
  scrollbar-width: thin; scrollbar-color: rgba(255,255,255,.1) transparent;
}
.chatbot-body::-webkit-scrollbar { width: 4px; }
.chatbot-body::-webkit-scrollbar-thumb { background: rgba(255,255,255,.1); border-radius: 2px; }

.msg { display: flex; gap: 10px; margin-bottom: 12px; max-width: 720px; align-self: flex-start; width: 100%; }
.msg.user { align-self: flex-end; flex-direction: row-reverse; width: auto; }
.msg-avatar { width: 34px; height: 34px; border-radius: 10px; flex-shrink: 0; background: linear-gradient(135deg, var(--brand), var(--brand-2)); display: flex; align-items: center; justify-content: center; font-size: .85rem; margin-top: 2px; }
.msg.user .msg-avatar { background: linear-gradient(135deg, #334155, #1e293b); }
.msg-bubble { padding: 12px 16px; border-radius: 16px; font-size: .9rem; line-height: 1.6; max-width: 560px; }
.msg.bot .msg-bubble { background: rgba(255,255,255,.07); color: #e2e8f0; border-bottom-left-radius: 4px; border: 1px solid rgba(255,255,255,.06); }
.msg.user .msg-bubble { background: linear-gradient(135deg, var(--brand), var(--brand-2)); color: #fff; border-bottom-right-radius: 4px; }

/* Options */
.options-grid { padding: 0 0 0 44px; margin-bottom: 12px; display: flex; flex-wrap: wrap; gap: 8px; max-width: 720px; }
.opt-btn { padding: 8px 16px; border-radius: var(--r-sm); background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.12); color: #cbd5e1; font-size: .85rem; font-weight: 500; cursor: pointer; transition: all .18s; font-family: var(--font-ui); }
.opt-btn:hover { background: rgba(79,70,229,.25); border-color: var(--brand-glow); color: #fff; transform: translateY(-1px); }
.opt-btn:active { transform: scale(.97); }
.opt-group-label { width: 100%; color: #64748b; font-size: .75rem; font-weight: 600; text-transform: uppercase; letter-spacing: .07em; margin-top: 8px; margin-bottom: 2px; }

/* ─── CHAT INPUT BAR ─────────────────────────────────────────────────── */
.chat-input-area {
  flex-shrink: 0;
  padding: 12px clamp(16px,4vw,40px);
  background: rgba(255,255,255,.02);
  border-top: 1px solid rgba(255,255,255,.07);
  display: flex; align-items: center; gap: 10px;
}
.chat-input-wrap {
  flex: 1; display: flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.12);
  border-radius: var(--r-md); padding: 10px 14px; transition: border-color .2s;
}
.chat-input-wrap:focus-within { border-color: var(--brand-glow); background: rgba(255,255,255,.09); }
.chat-input {
  flex: 1; background: transparent; border: none; outline: none;
  color: #e2e8f0; font-family: var(--font-ui); font-size: .9rem;
}
.chat-input::placeholder { color: #475569; }
.chat-send-btn {
  width: 38px; height: 38px; border-radius: 10px; border: none; cursor: pointer;
  background: linear-gradient(135deg, var(--brand), var(--brand-2));
  color: #fff; display: flex; align-items: center; justify-content: center;
  font-size: 1rem; transition: all .18s; flex-shrink: 0;
}
.chat-send-btn:hover { transform: scale(1.05); box-shadow: 0 4px 16px rgba(79,70,229,.4); }
.chat-send-btn:disabled { opacity: .4; cursor: default; transform: none; }

/* ─── RESULT CARD ──────────────────────────────────────────────────── */
.result-card {
  margin: 0 0 16px 44px;
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.1);
  border-radius: var(--r-xl);
  overflow: hidden;
  max-width: 680px;
  animation: slideUp .4s ease;
}
@keyframes slideUp { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:none} }

.result-header {
  padding: 20px 24px;
  background: linear-gradient(135deg, rgba(79,70,229,.35), rgba(124,58,237,.35));
  border-bottom: 1px solid rgba(255,255,255,.08);
}
.result-header h3 { color: #f1f5f9; font-family: var(--font-head); font-size: 1.1rem; margin-bottom: 4px; }
.result-header p { color: #94a3b8; font-size: .83rem; }

.result-section { padding: 16px 24px; border-bottom: 1px solid rgba(255,255,255,.06); }
.result-section:last-child { border-bottom: none; }
.result-section-title {
  display: flex; align-items: center; gap: 8px;
  color: #94a3b8; font-size: .75rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: .08em; margin-bottom: 12px;
}
.result-section-title .rs-icon { font-size: 1rem; }

.result-chips { display: flex; flex-wrap: wrap; gap: 7px; }
.result-chip {
  padding: 6px 14px; border-radius: 20px; font-size: .82rem; font-weight: 500;
  background: rgba(79,70,229,.15); color: #a5b4fc;
  border: 1px solid rgba(79,70,229,.25);
}
.result-chip.platform { background: rgba(6,182,212,.12); color: #67e8f9; border-color: rgba(6,182,212,.25); }
.result-chip.promo { background: rgba(245,158,11,.1); color: #fcd34d; border-color: rgba(245,158,11,.25); }
.result-chip.content { background: rgba(16,185,129,.1); color: #6ee7b7; border-color: rgba(16,185,129,.25); }

.influencer-box {
  background: rgba(139,92,246,.12); border: 1px solid rgba(139,92,246,.2);
  border-radius: var(--r-md); padding: 12px 16px;
  color: #c4b5fd; font-size: .88rem; line-height: 1.5;
}

.seg-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.seg-item { background: rgba(255,255,255,.04); border-radius: 10px; padding: 10px 14px; border: 1px solid rgba(255,255,255,.05); }
.seg-key { font-size: .7rem; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; margin-bottom: 3px; }
.seg-val { font-size: .87rem; color: #e2e8f0; font-weight: 500; }

/* Typing */
.typing-msg { display: flex; gap: 10px; margin-bottom: 12px; }
.typing-dots { display: flex; gap: 5px; padding: 12px 16px; background: rgba(255,255,255,.07); border-radius: 16px; border-bottom-left-radius: 4px; border: 1px solid rgba(255,255,255,.06); }
.typing-dots span { width: 7px; height: 7px; border-radius: 50%; background: #64748b; animation: td .8s infinite; }
.typing-dots span:nth-child(2) { animation-delay: .15s; }
.typing-dots span:nth-child(3) { animation-delay: .3s; }
@keyframes td { 0%,100%{transform:translateY(0);opacity:.5} 50%{transform:translateY(-5px);opacity:1} }

/* Confirmation Bubble (Updated: Ungu) */
.confirm-bubble {
  /* Ganti ke Ungu sesuai request */
  background: rgba(124, 58, 237, 0.15); 
  border: 1px solid rgba(124, 58, 237, 0.3);
  color: #c4b5fd;
  padding: 10px 16px;
  border-radius: 16px;
  margin-bottom: 10px;
  font-size: 0.9rem;
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: fit-content;
}
.confirm-actions { display: flex; gap: 8px; margin-top: 5px; }
.confirm-btn {
  padding: 5px 12px; border-radius: 8px; font-size: 0.8rem; font-weight: 600; cursor: pointer; border: none;
}
.confirm-yes { background: var(--brand); color: white; }
.confirm-yes:hover { opacity: 0.9; }
.confirm-no { background: rgba(255,255,255,0.1); color: #94a3b8; }
.confirm-no:hover { background: rgba(255,255,255,0.2); }

/* Error toast (Updated: Ungu) */
.error-toast {
  /* Ganti ke Ungu sesuai request */
  background: rgba(124, 58, 237, 0.15);
  border: 1px solid rgba(124, 58, 237, 0.3);
  color: #c4b5fd;
  border-radius: var(--r-sm); padding: 10px 14px;
  font-size: .83rem; margin: 0 0 10px 44px; max-width: 560px;
  animation: fadeIn .3s ease;
}
@keyframes fadeIn { from{opacity:0;transform:translateY(4px)} to{opacity:1;transform:none} }

/* Welcome screen */
.welcome-screen { display: flex; flex-direction: column; align-items: center; justify-content: center; flex: 1; padding: 40px 20px; text-align: center; }
.welcome-icon { width: 72px; height: 72px; border-radius: 20px; background: linear-gradient(135deg, var(--brand), var(--brand-2)); display: flex; align-items: center; justify-content: center; font-size: 2rem; margin-bottom: 24px; box-shadow: 0 8px 32px rgba(79,70,229,.4); }
.welcome-screen h2 { font-family: var(--font-head); color: #f1f5f9; font-size: 1.7rem; margin-bottom: 12px; }
.welcome-screen p { color: #64748b; max-width: 420px; font-size: .95rem; line-height: 1.7; margin-bottom: 28px; }
.welcome-btn { background: linear-gradient(135deg, var(--brand), var(--brand-2)); color: #fff; border: none; padding: 14px 32px; border-radius: var(--r-md); font-size: 1rem; font-weight: 600; cursor: pointer; font-family: var(--font-ui); box-shadow: 0 6px 24px rgba(79,70,229,.4); transition: all .2s; }
.welcome-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 32px rgba(79,70,229,.5); }

/* End screen */
.end-screen { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px 20px; text-align: center; margin: 16px 0 16px 44px; max-width: 500px; background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.08); border-radius: var(--r-xl); }
.end-icon { font-size: 3rem; margin-bottom: 16px; animation: confetti .6s ease; }
@keyframes confetti { 0%{transform:scale(0) rotate(-20deg)} 80%{transform:scale(1.2)} 100%{transform:scale(1)} }
.end-screen h2 { font-family: var(--font-head); color: #f1f5f9; font-size: 1.6rem; margin-bottom: 10px; }
.end-screen p { color: #64748b; margin-bottom: 24px; font-size: .95rem; }
.end-btn { background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.15); color: #e2e8f0; padding: 11px 24px; border-radius: var(--r-md); font-family: var(--font-ui); font-size: .9rem; font-weight: 600; cursor: pointer; transition: all .2s; }
.end-btn:hover { background: rgba(255,255,255,.14); }

/* ─── RESPONSIVE ──────────────────────────────────────────────────────── */
@media (max-width: 768px) {
  nav .nav-links { display: none; }
  .nav-hamburger { display: flex; flex-direction: column; }
  .nav-links.open { display: flex; flex-direction: column; position: fixed; top: var(--nav-h); left: 0; right: 0; background: var(--white); padding: 12px; border-bottom: 1px solid var(--border); box-shadow: var(--shadow-md); z-index: 998; }
  .hero { grid-template-columns: 1fr; }
  .hero-visual { display: none; }
  .stats-row { grid-template-columns: repeat(2,1fr); }
  .features-grid { grid-template-columns: 1fr; }
  .about-grid { grid-template-columns: 1fr; }
  .dev-cards { grid-template-columns: 1fr; }
  .saran-cards { grid-template-columns: 1fr; }
  .saran-highlight { grid-template-columns: 1fr; }
  .seg-grid { grid-template-columns: 1fr; }
  .progress-container { display: none; }
  .tips-grid { grid-template-columns: 1fr; }
  .chat-nav-links { display: none; }
  .result-card { margin-left: 0; max-width: 100%; }
  .options-grid { padding-left: 0; }
  .error-toast { margin-left: 0; }
}
</style>
</head>
<body>

<!-- ═══════════ MAIN NAVBAR ═══════════ -->
<nav id="mainNav">
  <div class="nav-logo" onclick="goHome()">
    <div class="nav-logo-dot">M</div>
    MarketBot
  </div>
  <ul class="nav-links" id="navLinks">
    <li><a href="#home" class="nav-link active" data-section="home" onclick="closeNav()">Beranda</a></li>
    <li><a href="#about" class="nav-link" data-section="about" onclick="closeNav()">Tentang</a></li>
    <li><a href="#tips" class="nav-link" data-section="tips" onclick="closeNav()">Tips Marketing</a></li>
    <!-- FAQ DIHAPUS SESUAI REQUEST -->
    <li><a href="javascript:void(0)" class="nav-cta nav-link" onclick="openChatPage()">Mulai Konsultasi &rarr;</a></li>
  </ul>
  <button class="nav-hamburger" onclick="toggleNav()" aria-label="Menu">
    <span></span><span></span><span></span>
  </button>
</nav>

<!-- ═══════════ MAIN SCROLL CONTENT ═══════════ -->
<div id="mainContent">

<!-- HOME -->
<section id="home" class="section">
  <div class="hero">
    <div class="hero-content">
      <div class="hero-badge">
        <div class="hero-badge-dot"></div>
        Konsultan Pemasaran Digital
      </div>
      <h1>Strategi Marketing<br>yang <span>Tepat</span> untuk<br>Bisnis Anda</h1>
      <p class="hero-sub" style="text-align: justify;">MarketBot menggunakan Finite State Machine dengan 22 state dan banyak kombinasi untuk memberikan rekomendasi pemasaran yang dipersonalisasi untuk Pebisnis Indonesia.</p>
      <div class="hero-btns">
        <button class="btn-primary" onclick="openChatPage()">Mulai Konsultasi Gratis</button>
        <a href="#about" class="btn-outline">Pelajari Lebih Lanjut</a>
      </div>
    </div>
    <div class="hero-visual">
      <div class="hero-card">
        <div class="hero-card-header">
          <div class="hc-avatar">&#x1F916;</div>
          <div>
            <div class="hc-name">MarketBot</div>
            <div class="hc-status">Online sekarang</div>
          </div>
        </div>
        <div class="chat-bubble bot">Halo&#x1F44B;! Apa jenis usaha anda?</div>
        <div class="chat-bubble user">Barbershop</div>
        <div class="chat-bubble bot">Siapa target pelanggan utama anda?</div>
        <div class="chat-bubble user">Mahasiswa usia 19&ndash;24 tahun</div>
        <div class="typing-indicator"><span></span><span></span><span></span></div>
      </div>
    </div>
  </div>

  <div class="stats-row">
    <div class="stat-card"><div class="stat-num">22</div><div class="stat-label">State FSM</div></div>
    <div class="stat-card"><div class="stat-num">50</div><div class="stat-label">Kategori Usaha</div></div>
    <div class="stat-card"><div class="stat-num">12</div><div class="stat-label">Variabel Input</div></div>
  </div>

  <div class="features">
    <div class="features-title">
      <h2>Fitur Unggulan MarketBot</h2>
      <p>Didesain untuk membantu pebisnis Indonesia menemukan strategi pemasaran terbaik</p>
    </div>
    <div class="features-grid">
      <div class="feature-card"><div class="feature-icon" style="background:rgba(79,70,229,.1);">&#x1F3AF;</div><h3>Rekomendasi Terpersonalisasi</h3><p style="text-align: justify;">Strategi pemasaran disesuaikan dengan karakteristik unik bisnis anda berdasarkan 12 variabel input.</p></div>
      <div class="feature-card"><div class="feature-icon" style="background:rgba(6,182,212,.1);">&#x1F4F1;</div><h3>Pilihan Platform Media Sosial</h3><p style="text-align: justify;">Temukan platform yang paling efektif berdasarkan target usia dan profil pelanggan bisnis anda.</p></div>
      <div class="feature-card"><div class="feature-icon" style="background:rgba(16,185,129,.1);">&#x1F4A1;</div><h3>Ide Konten &amp; Program Promo</h3><p style="text-align: justify;">Dapatkan ide konten kreatif dan program promosi yang sesuai dengan tujuan pemasaran anda.</p></div>
      <div class="feature-card"><div class="feature-icon" style="background:rgba(245,158,11,.1);">&#x1F91D;</div><h3>Panduan Influencer Marketing</h3><p style="text-align: justify;">Rekomendasi tier influencer yang tepat sesuai anggaran dan target pasar bisnis anda.</p></div>
      <div class="feature-card"><div class="feature-icon" style="background:rgba(239,68,68,.1);">&#x1F5FA;&#xFE0F;</div><h3>Segmentasi Pasar Cerdas</h3><p style="text-align: justify;">Analisis segmentasi pasar berdasarkan usia, profesi, gaya hidup, dan lokasi target anda.</p></div>
      <div class="feature-card"><div class="feature-icon" style="background:rgba(139,92,246,.1);">&#x26A1;</div><h3>Berbasis Teori Automata</h3><p style="text-align: justify;">Dibangun menggunakan konsep Finite State Machine (FSM) dari mata kuliah Teori Bahasa &amp; Otomata.</p></div>
    </div>
  </div>
</section>

<!-- ABOUT -->
<section id="about" class="section">
  <div class="about-inner">
    <div class="section-badge">Tentang</div>
    <h2>Chatbot Konsultan Pemasaran<br>Berbasis Finite State Machine</h2>
    <p style="text-align: justify;">MarketBot adalah ChatBot konsultan pemasaran digital yang dibangun menggunakan arsitektur <strong>Finite State Machine (FSM)</strong> untuk memberikan rekomendasi strategi yang terstruktur dan presisi. Dengan logika sistem yang terukur, dapat memandu anda melalui 12 tahapan konsultasi yang sistematis, mulai dari profil bisnis, analisis audiens, hingga penentuan taktik promosi, guna memastikan setiap saran yang diberikan selaras dengan tujuan unik bisnis anda.</p>
    <p style="text-align: justify;">Lebih dari sekadar chatbot, MarketBot adalah sistem navigasi strategis yang dirancang untuk memberikan panduan taktis yang siap eksekusi. Dengan menjaga integritas alur kerja melalui mekanisme transisi yang teruji, saya berkomitmen untuk memangkas kerumitan dalam perencanaan pemasaran Anda dan memberikan insight berbasis data yang relevan agar bisnis anda mampu tumbuh maksimal di pasar yang kompetitif.</p>

    <div class="about-grid">
      <div>
        <div class="fsm-visual">
          <div class="fsm-title">Peta State FSM (q0 &ndash; q21)</div>
          <div class="fsm-states">
            <div class="fsm-state">Mulai</div>
            <div class="fsm-state input">Jenis Usaha</div>
            <div class="fsm-state input">Target Usia</div>
            <div class="fsm-state input">Profesi</div>
            <div class="fsm-state input">Gaya Hidup</div>
            <div class="fsm-state input">Anggaran</div>
            <div class="fsm-state input">Tujuan</div>
            <div class="fsm-state input">Lokasi</div>
            <div class="fsm-state input">Tahap Bisnis</div>
            <div class="fsm-state input">Media Lama</div>
            <div class="fsm-state input">Frekuensi</div>
            <div class="fsm-state input">Kompetisi</div>
            <div class="fsm-state input">Jenis Pelanggan</div>
            <div class="fsm-state analysis">Analisis Strategi</div>
            <div class="fsm-state analysis">Analisis Medsos</div>
            <div class="fsm-state analysis">Analisis Konten</div>
            <div class="fsm-state analysis">Analisis Influencer</div>
            <div class="fsm-state analysis">Analisis Promo</div>
            <div class="fsm-state analysis">Segmentasi</div>
            <div class="fsm-state analysis">Ringkasan Semua Analisis</div>
            <div class="fsm-state">Konsultasi Lagi?</div>
            <div class="fsm-state final">Selesai &#x2713;</div>
          </div>
          <div style="margin-top:14px;font-size:.8rem;color:var(--ink-3);display:flex;gap:12px;flex-wrap:wrap;">
            <span style="display:flex;align-items:center;gap:5px;"><span style="width:10px;height:10px;border-radius:3px;background:rgba(79,70,229,.15);border:1px solid rgba(79,70,229,.3);display:inline-block"></span>Input</span>
            <span style="display:flex;align-items:center;gap:5px;"><span style="width:10px;height:10px;border-radius:3px;background:rgba(6,182,212,.12);border:1px solid rgba(6,182,212,.2);display:inline-block"></span>Analisis</span>
            <span style="display:flex;align-items:center;gap:5px;"><span style="width:10px;height:10px;border-radius:3px;background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.2);display:inline-block"></span>Final</span>
          </div>
        </div>
      </div>
      <div class="complexity-card">
        <h3>&#x1F4CA; Kompleksitas Sistem</h3>
        <div class="complexity-list">
          <div class="complexity-item"><span>Jenis usaha</span><span>50</span></div>
          <div class="complexity-item"><span>Target usia</span><span>15</span></div>
          <div class="complexity-item"><span>Target profesi</span><span>12</span></div>
          <div class="complexity-item"><span>Gaya hidup</span><span>10</span></div>
          <div class="complexity-item"><span>Anggaran promosi</span><span>12</span></div>
          <div class="complexity-item"><span>Tujuan pemasaran</span><span>20</span></div>
          <div class="complexity-item"><span>Lokasi target</span><span>8</span></div>
          <div class="complexity-item"><span>Tahap bisnis</span><span>6</span></div>
          <div class="complexity-item"><span>Media promosi</span><span>10</span></div>
          <div class="complexity-item"><span>Frekuensi promo</span><span>6</span></div>
          <div class="complexity-item"><span>Tingkat kompetisi</span><span>5</span></div>
          <div class="complexity-item"><span>Jenis pelanggan</span><span>8</span></div>
        </div>
      </div>
    </div>

    <div class="dev-section">
      <h3>Output yang Dihasilkan Chatbot</h3>
      <div class="dev-cards">
        <div class="dev-card"><div class="dev-card-num">01</div><h4>Strategi Promosi</h4><p style="text-align: justify;">Rekomendasi strategi promosi yang sesuai dengan anggaran, tahap bisnis, dan tingkat kompetisi.</p></div>
        <div class="dev-card"><div class="dev-card-num">02</div><h4>Platform Media Sosial</h4><p style="text-align: justify;">Platform yang paling efektif berdasarkan target usia dan profil pelanggan bisnis.</p></div>
        <div class="dev-card"><div class="dev-card-num">03</div><h4>Jenis Konten</h4><p style="text-align: justify;">Ide konten yang relevan dengan gaya hidup dan kebiasaan target pelanggan.</p></div>
        <div class="dev-card"><div class="dev-card-num">04</div><h4>Influencer Marketing</h4><p style="text-align: justify;">Tier influencer yang tepat (nano/micro/macro) sesuai anggaran yang tersedia.</p></div>
        <div class="dev-card"><div class="dev-card-num">05</div><h4>Program Promo</h4><p style="text-align: justify;">Ide program promosi yang selaras dengan tujuan pemasaran yang ingin dicapai.</p></div>
        <div class="dev-card"><div class="dev-card-num">06</div><h4>Segmentasi Pasar</h4><p style="text-align: justify;">Ringkasan profil segmentasi pasar berdasarkan seluruh variabel input yang diberikan.</p></div>
      </div>
    </div>
  </div>
</section>

<!-- TIPS MARKETING -->
<section id="tips" class="section">
  <div class="tips-inner">
    <div class="section-badge">Tips Marketing</div>
    <h2>Tips Marketing Digital</h2>
    <p>Sebelum konsultasi, kenali prinsip-prinsip dasar pemasaran digital yang bisa langsung diterapkan untuk bisnis anda.</p>

    <div class="tips-grid">
      <div class="tip-card"><div class="tip-icon">&#x1F3AF;</div><h3>Kenali Target Pasar anda</h3><p style="text-align: justify;">Semakin spesifik target anda, semakin efisien anggaran iklan. Tentukan usia, lokasi, profesi, dan gaya hidup pelanggan ideal sejak awal.</p></div>
      <div class="tip-card"><div class="tip-icon">&#x1F4F1;</div><h3>Pilih Platform yang Tepat</h3><p style="text-align: justify;">Tidak semua platform cocok untuk semua bisnis. TikTok untuk anak muda, Facebook untuk 30+, LinkedIn untuk B2B. Fokus 1&ndash;2 platform dulu.</p></div>
      <div class="tip-card"><div class="tip-icon">&#x1F4DD;</div><h3>Konsistensi Konten</h3><p style="text-align: justify;">Posting rutin lebih penting daripada sesekali viral. Buat konten kalender mingguan dan pertahankan tone &amp; estetika yang konsisten.</p></div>
      <div class="tip-card"><div class="tip-icon">&#x1F4B0;</div><h3>Optimalkan Anggaran Kecil</h3><p style="text-align: justify;">Mulai dari konten organik dan Google My Business. Setelah ada traksi, baru investasikan budget ke iklan berbayar secara bertahap.</p></div>
      <div class="tip-card"><div class="tip-icon">&#x1F91D;</div><h3>Manfaatkan Micro-Influencer</h3><p style="text-align: justify;">Influencer kecil (1K&ndash;50K followers) sering punya engagement lebih tinggi dan lebih terjangkau. Pilih yang relevan dengan niche bisnis anda.</p></div>
      <div class="tip-card"><div class="tip-icon">&#x1F4CA;</div><h3>Ukur Hasil Setiap Bulan</h3><p style="text-align: justify;">Pantau metrik seperti reach, engagement rate, dan konversi. Data adalah panduan untuk mengalokasikan anggaran secara lebih cerdas.</p></div>
    </div>

    <div class="tips-cta">
      <h3>Siap mendapatkan strategi yang dipersonalisasi?</h3>
      <p>Jawab pertanyaan singkat dan MarketBot akan merancang strategi pemasaran khusus untuk bisnis anda.</p>
      <button class="tips-cta-btn" onclick="openChatPage()">Mulai Konsultasi Sekarang</button>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  &copy; 2026 <span>MarketBot </span> Dibuat dengan &#x2764;&#xFE0F; untuk Pebisnis Indonesia.
</footer>

</div><!-- end #mainContent -->

<!-- ═══════════ CHAT PAGE ═══════════ -->
<div id="chatPage">
  <nav class="chat-nav">
    <div class="chat-nav-logo" onclick="closeChatPage()">
      <div class="nav-logo-dot">M</div>
      MarketBot
    </div>
    <ul class="chat-nav-links">
      <li><a onclick="closeChatPage('home')">Beranda</a></li>
      <li><a onclick="closeChatPage('about')">Tentang</a></li>
      <li><a onclick="closeChatPage('tips')">Tips Marketing</a></li>
      <!-- FAQ DIHAPUS -->
      <li><a onclick="closeChatPage()" class="chat-nav-back">&larr; Kembali</a></li>
    </ul>
  </nav>

  <div class="chatbot-topbar">
    <div class="chatbot-topbar-left">
      <div class="bot-avatar-live">&#x1F916;</div>
      <div>
        <div class="bot-info-name">MarketBot</div>
        <div class="bot-info-sub" id="botSubStatus">Konsultan Pemasaran Digital</div>
      </div>
    </div>
    <div class="progress-container">
      <span class="progress-text" id="progressText">Siap memulai</span>
      <div class="progress-bar-wrap">
        <div class="progress-bar-fill" id="progressBar" style="width:0%"></div>
      </div>
    </div>
  </div>

  <div class="chatbot-body" id="chatBody">
    <div class="welcome-screen" id="welcomeScreen">
      <div class="welcome-icon">&#x1F916;</div>
      <h2>Selamat Datang di MarketBot</h2>
      <p>Saya akan membantu menemukan strategi pemasaran terbaik untuk bisnis anda melalui pertanyaan singkat. Proses konsultasi hanya membutuhkan waktu 3&ndash;5 menit.</p>
      <button class="welcome-btn" onclick="startChat()">Mulai Konsultasi Sekarang &rarr;</button>
    </div>
  </div>

  <div class="chat-input-area">
    <div class="chat-input-wrap">
      <input
        type="text"
        id="chatInput"
        class="chat-input"
        placeholder="Ketik jawaban anda atau pilih opsi di atas..."
        autocomplete="off"
        disabled
      />
    </div>
    <button class="chat-send-btn" id="sendBtn" onclick="processInput()" disabled title="Kirim">
      &#x27A4;
    </button>
  </div>
</div>

<!-- ═══════════ JS ═══════════ -->
<script>
// ═══════════════════════════════════════════════════════════════
// FSM.py → JavaScript (port langsung)
// ═══════════════════════════════════════════════════════════════
const STATES = {
  "q0":"Mulai","q1":"Pilih Jenis Usaha","q2":"Pilih Target Usia",
  "q3":"Pilih Target Profesi","q4":"Pilih Target Gaya Hidup",
  "q5":"Pilih Anggaran Promosi","q6":"Pilih Tujuan Pemasaran",
  "q7":"Pilih Lokasi Target","q8":"Pilih Tahap Bisnis",
  "q9":"Pilih Media Promosi Sebelumnya","q10":"Pilih Frekuensi Promosi",
  "q11":"Pilih Tingkat Kompetisi","q12":"Pilih Jenis Pelanggan",
  "q13":"Analisis Strategi Promosi","q14":"Analisis Media Sosial",
  "q15":"Analisis Jenis Konten","q16":"Analisis Influencer Marketing",
  "q17":"Analisis Program Promo","q18":"Analisis Segmentasi Pasar",
  "q19":"Ringkasan Hasil Konsultasi","q20":"Konsultasi Lagi?","q21":"Selesai"
};
const INITIAL_STATE = "q0";
const FINAL_STATE   = "q21";

const OPTIONS = {
  "q1": {
    "Makanan & Minuman":["Restoran","Warung makan","Coffee shop","Bakery","Toko kue","Catering","Minuman kekinian","Frozen food"],
    "Fashion & Kecantikan":["Toko pakaian pria","Toko pakaian wanita","Toko pakaian anak","Hijab & muslim fashion","Toko sepatu","Toko tas","Toko aksesoris","Skincare","Kosmetik","Klinik kecantikan","Salon","Barbershop"],
    "Jasa":["Fotografi","Videografi","Desain grafis","Percetakan","Event organizer","Wedding organizer","Cleaning service","Konsultan bisnis","Konsultan pajak","Jasa penerjemah"],
    "Pendidikan":["Bimbingan belajar","Kursus bahasa","Kursus komputer","Pelatihan kerja","Kursus musik"],
    "Teknologi":["Software house","Pengembang aplikasi","Produk digital","Toko komputer","Servis komputer"],
    "Lainnya":["Laundry","Toko furniture","Toko dekorasi rumah","Toko tanaman hias","Bengkel motor","Bengkel mobil","Cuci kendaraan","Rental kendaraan","Pet shop","Agen travel"]
  },
  "q2":["Anak-anak (5\u20138 th)","Anak-anak (9\u201312 th)","Remaja awal (13\u201315 th)","Remaja (16\u201318 th)","Mahasiswa awal (19\u201321 th)","Mahasiswa akhir (22\u201324 th)","Dewasa muda (25\u201329 th)","Dewasa muda (30\u201334 th)","Dewasa (35\u201339 th)","Dewasa (40\u201344 th)","Pra-lansia (45\u201349 th)","Pra-lansia (50\u201354 th)","Lansia muda (55\u201364 th)","Lansia (65+ th)","Semua usia"],
  "q3":["Pelajar","Mahasiswa","Pegawai negeri","Karyawan swasta","Wirausaha","Freelancer","Ibu rumah tangga","Guru dan dosen","Tenaga kesehatan","Pekerja lapangan","Pensiunan","Semua profesi"],
  "q4":["Pecinta olahraga","Pengguna teknologi aktif","Pecinta traveling","Pecinta kuliner","Pecinta fashion","Orang tua muda","Komunitas hobi","Peduli kesehatan","Pencari promo/diskon","Pekerja mobilitas tinggi"],
  "q5":["< Rp250.000","Rp250.000\u2013500.000","Rp500.001\u20131.000.000","Rp1\u20132,5 juta","Rp2,5\u20135 juta","Rp5\u201310 juta","Rp10\u201325 juta","Rp25\u201350 juta","Rp50\u2013100 juta","Rp100\u2013250 juta","> Rp250 juta","Belum menentukan"],
  "q6":["Meningkatkan penjualan","Meningkatkan brand awareness","Menambah followers","Memperkenalkan produk baru","Meningkatkan loyalitas","Menjangkau pasar baru","Menghabiskan stok lama","Meningkatkan engagement","Meningkatkan traffic website","Mendapatkan leads","Meningkatkan reservasi","Mengumpulkan data pelanggan","Meningkatkan repeat order","Memperkuat citra merek","Mengungguli kompetitor","Meningkatkan kunjungan toko","Meningkatkan konversi online","Mengedukasi pelanggan","Menyiapkan bisnis baru","Mempertahankan pangsa pasar"],
  "q7":["Lingkungan sekitar usaha","Kecamatan","Kabupaten/Kota","Provinsi","Nasional","Asia Tenggara","Internasional","Belum menentukan"],
  "q8":["Baru memulai","< 1 tahun","1\u20133 tahun","3\u20135 tahun","> 5 tahun","Franchise/cabang banyak"],
  "q9":["Belum pernah promosi","Instagram","TikTok","Facebook","WhatsApp Business","Marketplace","Website","Google Ads","Influencer marketing","Promosi offline"],
  "q10":["Setiap hari","2\u20133x seminggu","Seminggu sekali","Sebulan sekali","Saat momen tertentu","Belum pernah promosi"],
  "q11":["Sangat rendah","Rendah","Sedang","Tinggi","Sangat tinggi"],
  "q12":["Pelanggan baru","Pelanggan tetap","Pelanggan loyal","Sensitif terhadap harga","Pelanggan premium","Pembeli impulsif","Pelanggan korporat (B2B)","Semua pelanggan"],
  "q20":["Ya, konsultasi lagi","Tidak, selesai"]
};

const PROMPTS = {
  "q0": "Selamat datang! \uD83D\uDC4B Saya adalah <strong>MarketBot</strong> \u2014 konsultan pemasaran digital Anda. Saya akan membantu menemukan strategi terbaik untuk bisnis Anda melalui beberapa pertanyaan singkat.",
  "q1": "Pertama, <strong>apa jenis usaha Anda?</strong> Pilih kategori yang paling sesuai:",
  "q2": "Siapa <strong>target usia</strong> pelanggan utama bisnis Anda?",
  "q3": "Apa <strong>profesi</strong> target pelanggan Anda?",
  "q4": "Bagaimana <strong>gaya hidup</strong> target pelanggan Anda?",
  "q5": "Berapa <strong>anggaran promosi</strong> yang Anda siapkan per bulan?",
  "q6": "Apa <strong>tujuan utama pemasaran</strong> Anda saat ini?",
  "q7": "Di mana <strong>lokasi target pasar</strong> Anda?",
  "q8": "Sudah berapa lama bisnis Anda berjalan? (<strong>tahap perkembangan</strong>)",
  "q9": "Media promosi apa yang <strong>sudah pernah Anda gunakan</strong>?",
  "q10": "Seberapa sering Anda melakukan <strong>promosi</strong>?",
  "q11": "Bagaimana <strong>tingkat persaingan</strong> di industri Anda?",
  "q12": "Siapa <strong>jenis pelanggan utama</strong> bisnis Anda?",
  "q19": "\u2705 Analisis selesai!",
  "q20": "Apakah Anda ingin melakukan <strong>konsultasi lagi</strong> untuk bisnis lain?",
  "q21": "Terima kasih telah menggunakan <strong>MarketBot</strong>! \uD83C\uDF89 Semoga strategi ini membantu bisnis Anda berkembang. Sukses selalu!"
};

const KEY_MAP = {
  "q1":"jenis_usaha","q2":"target_usia","q3":"target_profesi","q4":"gaya_hidup",
  "q5":"anggaran","q6":"tujuan","q7":"lokasi","q8":"tahap_bisnis",
  "q9":"media_sebelumnya","q10":"frekuensi","q11":"tingkat_kompetisi","q12":"jenis_pelanggan"
};

function fsmTransition(state, _input) {
  const flow = ["q0","q1","q2","q3","q4","q5","q6","q7","q8","q9","q10","q11","q12",
                "q13","q14","q15","q16","q17","q18","q19","q20"];
  if (flow.includes(state)) {
    const idx = flow.indexOf(state);
    if (idx + 1 < flow.length) return flow[idx + 1];
  }
  if (state === "q20") {
    return _input === "Ya, konsultasi lagi" ? "q1" : "q21";
  }
  return "q21";
}

function getOptions(state) {
  const opts = OPTIONS[state];
  if (!opts) return null;
  if (!Array.isArray(opts)) {
    // grouped (q1)
    return Object.entries(opts).map(([group, items]) => ({ group, items }));
  }
  return opts;
}

function stateToStep(state) {
  const m = {"q1":1,"q2":2,"q3":3,"q4":4,"q5":5,"q6":6,"q7":7,"q8":8,"q9":9,"q10":10,"q11":11,"q12":12,"q20":13};
  return m[state] || 0;
}

// ═══════════════════════════════════════════════════════════════
// engine.py → JavaScript (port langsung)
// ═══════════════════════════════════════════════════════════════
const PLATFORM_BY_AGE = {
  "Anak-anak (5\u20138 th)":["YouTube Kids","TikTok (parental)"],
  "Anak-anak (9\u201312 th)":["YouTube","TikTok"],
  "Remaja awal (13\u201315 th)":["TikTok","Instagram","YouTube"],
  "Remaja (16\u201318 th)":["TikTok","Instagram","YouTube","Twitter/X"],
  "Mahasiswa awal (19\u201321 th)":["Instagram","TikTok","Twitter/X","YouTube"],
  "Mahasiswa akhir (22\u201324 th)":["Instagram","LinkedIn","TikTok","YouTube"],
  "Dewasa muda (25\u201329 th)":["Instagram","LinkedIn","Facebook","YouTube"],
  "Dewasa muda (30\u201334 th)":["Facebook","Instagram","LinkedIn","WhatsApp Business"],
  "Dewasa (35\u201339 th)":["Facebook","WhatsApp Business","LinkedIn"],
  "Dewasa (40\u201344 th)":["Facebook","WhatsApp Business","YouTube"],
  "Pra-lansia (45\u201349 th)":["Facebook","WhatsApp Business"],
  "Pra-lansia (50\u201354 th)":["Facebook","WhatsApp Business","YouTube"],
  "Lansia muda (55\u201364 th)":["Facebook","WhatsApp Business"],
  "Lansia (65+ th)":["Facebook","WhatsApp Business"],
  "Semua usia":["Instagram","TikTok","Facebook","YouTube","WhatsApp Business"]
};

const STRATEGY_BY_BUDGET = {
  "< Rp250.000":["Fokus pada konten organik media sosial","Manfaatkan WhatsApp Business secara gratis","Gunakan Google My Business untuk visibilitas lokal","Buat konten UGC (User Generated Content) dari pelanggan"],
  "Rp250.000\u2013500.000":["Iklan Instagram/Facebook boosting sederhana","Paid promote di akun lokal yang relevan","Konten organik + 1 paid post per minggu"],
  "Rp500.001\u20131.000.000":["Facebook & Instagram Ads dengan targeting spesifik","Kolaborasi micro-influencer lokal","Konten video pendek TikTok / Reels"],
  "Rp1\u20132,5 juta":["Multi-platform ads (Meta + TikTok)","Google Ads untuk search intent","Email marketing campaign","Micro-influencer 2\u20133 akun"],
  "Rp2,5\u20135 juta":["Full-funnel marketing (awareness \u2192 conversion)","Influencer marketing nano/micro","Retargeting campaign","A/B testing iklan"],
  "Rp5\u201310 juta":["Influencer marketing kategori mid-tier","Google Ads + Meta Ads terintegrasi","Landing page khusus kampanye","Video production untuk konten iklan"],
  "Rp10\u201325 juta":["Brand campaign multi-channel","Kolaborasi influencer 5\u201310 akun","SEO + Content marketing","Podcast advertising"],
  "Rp25\u201350 juta":["Campaign terintegrasi online + offline","Macro-influencer marketing","Event digital / webinar berbayar","PR digital di media online"],
  "Rp50\u2013100 juta":["Brand ambassador jangka panjang","Multi-channel attribution tracking","Native advertising di media nasional","Programmatic advertising"],
  "Rp100\u2013250 juta":["Celebrity endorsement","TV/radio spot + digital integration","Sponsorship event nasional","Full agency management"],
  "> Rp250 juta":["National brand campaign","360\u00B0 integrated marketing","Celebrity brand ambassador","Mass media advertising"],
  "Belum menentukan":["Mulai dengan strategi organik tanpa biaya","Tentukan ROI target sebelum berinvestasi","Trial kecil dengan budget Rp100\u2013200k untuk test market"]
};

const CONTENT_BY_LIFESTYLE = {
  "Pecinta olahraga":["Video workout/tips olahraga","Before-after transformation","Challenge konten"],
  "Pengguna teknologi aktif":["Review produk/tutorial","Tech tips","Infografis data"],
  "Pecinta traveling":["Konten wisata lokal","Tips perjalanan","Foto destinasi"],
  "Pecinta kuliner":["Food photography","Behind-the-scenes masak","Review & rekomendasi"],
  "Pecinta fashion":["Outfit of the day (OOTD)","Style tips","Fashion haul"],
  "Orang tua muda":["Parenting tips","Produk keluarga","Konten edukatif anak"],
  "Komunitas hobi":["Tutorial hobi","Community showcase","Event komunitas"],
  "Peduli kesehatan":["Tips kesehatan","Konten edukatif medis","Testimoni produk sehat"],
  "Pencari promo/diskon":["Flash sale announcement","Voucher & promo","Perbandingan harga"],
  "Pekerja mobilitas tinggi":["Quick tips & hack","Konten singkat 15\u201330 detik","Podcast"]
};

const INFLUENCER_BY_BUDGET = {
  "< Rp250.000":"Tidak direkomendasikan (gunakan kolaborasi barter)",
  "Rp250.000\u2013500.000":"Nano-influencer (1K\u201310K followers) \u2013 barter/Rp50\u2013200rb",
  "Rp500.001\u20131.000.000":"Nano-influencer \u2013 Rp200\u2013500rb per post",
  "Rp1\u20132,5 juta":"Micro-influencer (10K\u2013100K) \u2013 Rp500rb\u20132jt per post",
  "Rp2,5\u20135 juta":"Micro-influencer \u2013 Rp2\u20135jt, 1\u20132 kolaborasi",
  "Rp5\u201310 juta":"Mid-tier influencer (100K\u2013500K) \u2013 Rp5\u201310jt",
  "Rp10\u201325 juta":"Mid-tier, 2\u20133 akun \u2013 Rp5\u201310jt per akun",
  "Rp25\u201350 juta":"Macro-influencer (500K\u20131M) \u2013 Rp20\u201350jt",
  "Rp50\u2013100 juta":"Macro/Mega influencer \u2013 Rp50\u2013100jt",
  "Rp100\u2013250 juta":"Mega-influencer/Selebriti \u2013 Rp100\u2013250jt",
  "> Rp250 juta":"Celebrity brand ambassador jangka panjang",
  "Belum menentukan":"Mulai dengan nano-influencer barter untuk test market"
};

const PROMO_BY_GOAL = {
  "Meningkatkan penjualan":["Flash sale 24 jam","Bundle produk hemat","Cashback pembelian pertama"],
  "Meningkatkan brand awareness":["Giveaway challenge","Konten viral campaign","Hashtag brand"],
  "Menambah followers":["Follow & share contest","Giveaway berhadiah","Collab dengan kreator lain"],
  "Memperkenalkan produk baru":["Early bird discount","Free trial/sample","Pre-order exclusive"],
  "Meningkatkan loyalitas":["Loyalty point program","Member exclusive deal","Birthday promo"],
  "Menjangkau pasar baru":["Ads targeting baru","Influencer di segmen baru","Event/pameran"],
  "Menghabiskan stok lama":["Clearance sale","Bundle stok lama+baru","Diskon bertingkat"],
  "Meningkatkan engagement":["Kuis interaktif","Polling & survey","Challenge konten"],
  "Meningkatkan traffic website":["Blog SEO + CTA","Google Ads search","Email newsletter"],
  "Mendapatkan leads":["Free ebook/webinar","Formulir landing page","Lead magnet promo"],
  "Meningkatkan reservasi":["Early booking discount","Paket spesial weekend","Referral program"],
  "Mengumpulkan data pelanggan":["Survey berhadiah","Loyalty card digital","Newsletter opt-in"],
  "Meningkatkan repeat order":["Subscription program","Reminder notifikasi","Reward pelanggan setia"],
  "Memperkuat citra merek":["Storytelling brand","CSR campaign","Behind-the-scenes konten"],
  "Mengungguli kompetitor":["Competitive pricing","Unique selling proposition campaign","Comparative ads"],
  "Meningkatkan kunjungan toko":["Check-in promo","Geo-targeting ads","Event toko fisik"],
  "Meningkatkan konversi online":["Retargeting cart abandonment","Social proof / review","One-click checkout promo"],
  "Mengedukasi pelanggan":["Tutorial konten seri","Webinar gratis","FAQ campaign"],
  "Menyiapkan bisnis baru":["Soft launch campaign","Waitlist exclusive","Teaser content 2\u20134 minggu"],
  "Mempertahankan pangsa pasar":["Customer retention program","Competitive monitoring","Brand defense campaign"]
};

function generateRecommendations(data) {
  const usia      = data["target_usia"]       || "Semua usia";
  const anggaran  = data["anggaran"]           || "Belum menentukan";
  const gaya_hidup= data["gaya_hidup"]         || "";
  const tujuan    = data["tujuan"]             || "Meningkatkan penjualan";
  const kompetisi = data["tingkat_kompetisi"]  || "Sedang";
  const tahap     = data["tahap_bisnis"]       || "Baru memulai";
  const usaha     = data["jenis_usaha"]        || "";

  // q13 – Strategi Promosi
  let strategi = [...(STRATEGY_BY_BUDGET[anggaran] || STRATEGY_BY_BUDGET["Belum menentukan"])];
  if (kompetisi === "Tinggi" || kompetisi === "Sangat tinggi") {
    strategi.push("Lakukan competitive analysis mingguan");
    strategi.push("Fokus pada diferensiasi unik produk/jasa Anda");
  }
  if (tahap === "Baru memulai") {
    strategi.unshift("Bangun profil media sosial yang konsisten dan profesional terlebih dahulu");
  }

  // q14 – Platform
  const platform = PLATFORM_BY_AGE[usia] || ["Instagram","Facebook","WhatsApp Business"];

  // q15 – Konten
  let konten = [...(CONTENT_BY_LIFESTYLE[gaya_hidup] || ["Foto produk berkualitas tinggi","Video testimoni pelanggan","Behind-the-scenes proses bisnis","Tips & informasi edukatif seputar industri"])];
  konten.push("Konten seasonal (hari besar, momen nasional)");
  konten.push("User Generated Content (UGC) dari pelanggan");

  // q16 – Influencer
  const influencer = INFLUENCER_BY_BUDGET[anggaran] || "Mulai dengan nano-influencer barter";

  // q17 – Promo
  const promo = PROMO_BY_GOAL[tujuan] || ["Flash sale","Promo loyalty pelanggan"];

  // q18 – Segmentasi
  const segmentasi = {
    "Jenis Usaha": usaha,
    "Target Usia": usia,
    "Profesi": data["target_profesi"] || "-",
    "Gaya Hidup": gaya_hidup,
    "Lokasi": data["lokasi"] || "-",
    "Tahap Bisnis": tahap,
    "Jenis Pelanggan": data["jenis_pelanggan"] || "-"
  };

  return { strategi_promosi: strategi, platform_medsos: platform, jenis_konten: konten, influencer, program_promo: promo, segmentasi };
}

// ═══════════════════════════════════════════════════════════════
// app.py logic (state machine + session) → JavaScript
// ═══════════════════════════════════════════════════════════════
let sessionState = INITIAL_STATE;
let sessionData  = {};

function apiStart() {
  sessionState = INITIAL_STATE;
  sessionData  = {};
  return {
    state: INITIAL_STATE,
    message: PROMPTS["q0"],
    next_state: "q1",
    options: getOptions("q1"),
    next_prompt: PROMPTS["q1"],
    step: 0,
    total_steps: 12
  };
}

function apiMessage(userInput) {
  const currentState = sessionState;

  // 1. Store answer
  if (KEY_MAP[currentState]) {
    sessionData[KEY_MAP[currentState]] = userInput;
  }

  // 2. Transition
  let nextState = fsmTransition(currentState, userInput);
  sessionState = nextState;

  // 3. Analysis states → skip to q19
  if (["q13","q14","q15","q16","q17","q18"].includes(nextState)) {
    const recs = generateRecommendations(sessionData);
    sessionState = "q19";
    return {
      state: "q19",
      message: PROMPTS["q19"],
      recommendations: recs,
      options: OPTIONS["q20"],
      next_prompt: PROMPTS["q20"],
      step: 13,
      total_steps: 13,
      type: "result"
    };
  }

  // 4. Result state
  if (nextState === "q19") {
    const recs = generateRecommendations(sessionData);
    return {
      state: "q19",
      message: PROMPTS["q19"],
      recommendations: recs,
      options: OPTIONS["q20"],
      next_prompt: PROMPTS["q20"],
      step: 13,
      total_steps: 13,
      type: "result"
    };
  }

  // 5. q20
  if (nextState === "q20") {
    return {
      state: "q20",
      message: PROMPTS["q20"],
      options: OPTIONS["q20"],
      step: stateToStep(nextState),
      total_steps: 13,
      type: "question"
    };
  }

  // 6. Final
  if (nextState === FINAL_STATE) {
    return { state: "q21", message: PROMPTS["q21"], type: "end" };
  }

  // 7. Normal q1-q12
  return {
    state: nextState,
    message: PROMPTS[nextState] || "",
    options: getOptions(nextState),
    step: stateToStep(nextState),
    total_steps: 12,
    type: "question"
  };
}

function apiRestart() {
  sessionState = "q1";
  sessionData  = {};
  return {
    state: "q1",
    message: PROMPTS["q1"],
    options: getOptions("q1"),
    step: 1,
    total_steps: 12,
    type: "question"
  };
}

// ═══════════════════════════════════════════════════════════════
// UI (sama persis dengan index.html)
// ═══════════════════════════════════════════════════════════════

// ── NAV ────────────────────────────────────────────────────────────────────
function toggleNav() { document.getElementById('navLinks').classList.toggle('open'); }
function closeNav() { document.getElementById('navLinks').classList.remove('open'); }
function goHome() {
  document.getElementById('home').scrollIntoView({ behavior: 'smooth' });
  closeNav();
}

const sections = document.querySelectorAll('#mainContent .section');
const navLinks = document.querySelectorAll('.nav-link[data-section]');
function setActive(id) {
  navLinks.forEach(a => a.classList.toggle('active', a.dataset.section === id));
}
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => { if (entry.isIntersecting) setActive(entry.target.id); });
}, { rootMargin: `-64px 0px -55% 0px`, threshold: 0 });
sections.forEach(s => observer.observe(s));

// ── CHAT PAGE ──────────────────────────────────────────────────────────────
let chatActive = false;
let isProcessing = false;
let currentOptions = []; // Menyimpan opsi valid saat ini untuk Fuzzy Matching
let pendingConfirmation = null; // Menyimpan teks yang sedang dikonfirmasi

function openChatPage() {
  document.getElementById('chatPage').classList.add('active');
  document.body.style.overflow = 'hidden';
}
function closeChatPage(section) {
  document.getElementById('chatPage').classList.remove('active');
  document.body.style.overflow = '';
  if (section) {
    setTimeout(() => {
      const el = document.getElementById(section);
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }, 80);
  }
}

// ── FUZZY LOGIC (AI UNDERSTANDING) ───────────────────────────────────────
const SIMILARITY_THRESHOLD = 0.65; 

function normalize(s) {
  return s.toLowerCase().replace(/[^a-z0-9\u00C0-\u024F]/gi,' ').replace(/\s+/g,' ').trim();
}

function similarity(a, b) {
  a = normalize(a); b = normalize(b);
  if (a === b) return 1.0;
  if (b.includes(a) || a.includes(b)) return 0.9; 
  
  const aW = a.split(' '), bW = b.split(' ');
  let matches = 0;
  aW.forEach(w => { if (w.length > 2 && bW.some(bw => bw.includes(w) || w.includes(bw))) matches++; });
  return matches / Math.max(aW.length, bW.length);
}

function findBestMatch(input, options) {
  if (!options || !options.length) return null;
  let best = null, bestScore = 0;
  
  let flatOptions = [];
  options.forEach(opt => {
    if (typeof opt === 'object' && opt.items) flatOptions.push(...opt.items);
    else if (typeof opt === 'string') flatOptions.push(opt);
  });

  flatOptions.forEach(opt => {
    const score = similarity(input, opt);
    if (score > bestScore) { bestScore = score; best = opt; }
  });
  return bestScore >= SIMILARITY_THRESHOLD ? { match: best, score: bestScore } : null;
}

// ── CHATBOT CORE ──────────────────────────────────────────────────────────
async function startChat() {
  if (isProcessing) return;
  
  document.getElementById('welcomeScreen').style.display = 'none';
  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');
  chatInput.disabled = false;
  sendBtn.disabled = false;
  chatInput.focus();

  try {
    await fetchStart();
  } catch (error) {
    showToast("Gagal memulai konsultasi. Silakan refresh halaman.");
  }
}

async function fetchStart() {
  showTyping(true);
  try {
    const data = apiStart();
    
    addBotMessage(data.message);
    
    if (data.next_state && data.next_prompt) {
      setTimeout(() => {
        addBotMessage(data.next_prompt);
        renderOptions(data.options);
        updateProgress(data.step, data.total_steps);
      }, 600);
    }
  } catch (e) {
    console.error(e);
    showToast("Terjadi kesalahan.");
  } finally {
    showTyping(false);
  }
}

// HANDLER UNTUK KONFIRMASI TYPO (PERBAIKAN)
function handleConfirmChoice(choice) {
  if (choice) {
    // Jika user klik "Ya", kirim teks yang sudah dikonfirmasi
    sendOption(pendingConfirmation);
  } else {
    // Jika "Tidak", hapus bubble
    removeConfirmationBubble();
  }
}

// INPUT UTAMA (Handle Ketik Manual atau Klik Tombol)
function processInput() {
  const input = document.getElementById('chatInput');
  const text = input.value.trim();
  if (!text) return;
  
  input.value = ''; 
  
  // Jika sedang mode konfirmasi typo
  if (pendingConfirmation) {
    if (text.toLowerCase().includes('ya') || text.toLowerCase().includes('yes')) {
      sendOption(pendingConfirmation); 
    } else if (text.toLowerCase().includes('tidak') || text.toLowerCase().includes('no')) {
      removeConfirmationBubble(); 
    } else {
      showToast("Silakan jawab Ya atau Tidak.");
    }
    return;
  }

  // Cek Fuzzy Match jika mengetik manual
  const match = findBestMatch(text, currentOptions);
  
  if (match && match.score < 1.0) {
    // Ada typo tapi mirip -> Minta konfirmasi
    askConfirmation(text, match.match);
  } else if (match && match.score === 1.0) {
    // Persis sama -> Kirim langsung
    sendOption(match.match);
  } else {
    // Tidak mirip sama sekali -> Peringatan
    showToast("Maaf, saya tidak mengerti. Silakan pilih opsi di atas atau ketik kata kunci yang mirip.");
  }
}

// Fungsi menangani klik tombol opsi (Lewati fuzzy match)
function sendOptionDirect(optionText) {
  sendOption(optionText);
}

async function sendOption(optionText) {
  if (isProcessing) return;
  
  if (pendingConfirmation) removeConfirmationBubble();
  
  isProcessing = true;
  addUserMessage(optionText);
  removeOptions();
  
  showTyping(true);

  try {
    const data = apiMessage(optionText);
    showTyping(false);

    setTimeout(() => {
      handleResponse(data);
      isProcessing = false;
    }, 500);

  } catch (e) {
    console.error(e);
    showTyping(false);
    showToast("Gagal mengirim pesan.");
    isProcessing = false;
  }
}

// Fungsi Minta Konfirmasi Typo (Updated: Tombol berfungsi)
function askConfirmation(userText, matchText) {
  pendingConfirmation = matchText;
  
  const div = document.createElement('div');
  div.id = 'confirmationBubble';
  div.className = 'msg bot confirm-bubble';
  // PERBAIKAN: Tombol langsung memanggil fungsi handleConfirmChoice
  div.innerHTML = `
    <div>Apakah maksud anda: <strong>"${matchText}"</strong>?</div>
    <div class="confirm-actions">
      <button class="confirm-btn confirm-yes" onclick="handleConfirmChoice(true)">Ya</button>
      <button class="confirm-btn confirm-no" onclick="handleConfirmChoice(false)">Tidak</button>
    </div>
  `;
  document.getElementById('chatBody').appendChild(div);
  scrollToBottom();
  
  // Isi input dummy biar user fokus konfirmasi
  const input = document.getElementById('chatInput');
  input.placeholder = "Ketik 'Ya' atau 'Tidak'untuk konfirmasi...";
}

function removeConfirmationBubble() {
  const el = document.getElementById('confirmationBubble');
  if (el) el.remove();
  pendingConfirmation = null;
  document.getElementById('chatInput').placeholder = "Ketik jawaban anda atau pilih opsi di atas...";
}

// ── HANDLE RESPONSE & RECOMMENDATIONS ────────────────────────────────────────
function handleResponse(data) {
  if (data.step !== undefined && data.total_steps !== undefined) {
    updateProgress(data.step, data.total_steps);
  }

  if (data.recommendations) {
    addBotMessage(data.message);
    const recHTML = buildResultHTML(data.recommendations);
    const recDiv = document.createElement('div');
    recDiv.innerHTML = recHTML;
    document.getElementById('chatBody').appendChild(recDiv);
    scrollToBottom();

    if (data.options) {
      setTimeout(() => {
        renderOptions(data.options);
      }, 800);
    }
  } 
  else if (data.state === 'q21' || data.type === 'end') {
    addBotMessage(data.message);
    const endHTML = `
      <div class="end-screen">
        <div class="end-icon">&#x1F389;</div>
        <h2>Konsultasi Selesai!</h2>
        <p>Strategi pemasaran telah siap. Semoga rekomendasi ini membantu bisnis anda berkembang.</p>
        <button class="end-btn" onclick="resetChat()">Konsultasi Lagi</button>
        <button class="end-btn" style="margin-top:8px;" onclick="closeChatPage('home')">&larr; Kembali ke Beranda</button>
      </div>
    `;
    const endDiv = document.createElement('div');
    endDiv.innerHTML = endHTML;
    document.getElementById('chatBody').appendChild(endDiv);
    scrollToBottom();
  } 
  else {
    addBotMessage(data.message);
    renderOptions(data.options);
  }
}

// ── RENDER RECOMMENDATIONS ───────────────────────────────────────────────────
function buildResultHTML(recs) {
  let html = `<div class="result-card">
    <div class="result-header">
      <h3>Berikut strategi pemasaran untuk bisnis anda:</h3>
    </div>`;

  const icons = {
    'strategi_promosi': '\uD83D\uDE80', 'platform_medsos': '\uD83D\uDCF1', 'jenis_konten': '\uD83C\uDFA8',
    'influencer': '\uD83E\uDD1D', 'program_promo': '\uD83C\uDF81', 'segmentasi': '\uD83C\uDFAF'
  };

  for (const [key, value] of Object.entries(recs)) {
    const title = key.replace(/_/g, ' ').toUpperCase();
    const icon = icons[key] || '\uD83D\uDCCC';
    
    html += `<div class="result-section">
      <div class="result-section-title"><span class="rs-icon">${icon}</span> ${title}</div>`;

    if (Array.isArray(value)) {
      let chipClass = '';
      if (key === 'platform_medsos') chipClass = 'platform';
      if (key === 'program_promo') chipClass = 'promo';
      if (key === 'jenis_konten') chipClass = 'content';

      html += `<div class="result-chips">`;
      value.forEach(item => {
        html += `<div class="result-chip ${chipClass}">${item}</div>`;
      });
      html += `</div>`;
    } else if (typeof value === 'object' && value !== null) {
      html += `<div class="seg-grid">`;
      for (const [k, v] of Object.entries(value)) {
        html += `
          <div class="seg-item">
            <div class="seg-key">${k}</div>
            <div class="seg-val">${v}</div>
          </div>`;
      }
      html += `</div>`;
    } else {
      html += `<div class="influencer-box">${value}</div>`;
    }
    html += `</div>`;
  }
  html += `</div>`;
  return html;
}

// ── UI HELPERS ────────────────────────────────────────────────────────────
function addBotMessage(text) {
  const div = document.createElement('div');
  div.className = 'msg bot';
  div.innerHTML = `
    <div class="msg-avatar">\uD83E\uDD16</div>
    <div class="msg-bubble">${text}</div>
  `;
  document.getElementById('chatBody').appendChild(div);
  scrollToBottom();
}

function addUserMessage(text) {
  const div = document.createElement('div');
  div.className = 'msg user';
  div.innerHTML = `
    <div class="msg-avatar">\uD83D\uDC64</div>
    <div class="msg-bubble">${text}</div>
  `;
  document.getElementById('chatBody').appendChild(div);
  scrollToBottom();
}

function renderOptions(options) {
  if (!options) return;
  
  currentOptions = options;

  const container = document.createElement('div');
  container.className = 'options-grid';

  options.forEach(opt => {
    if (typeof opt === 'object' && opt.group) {
      const label = document.createElement('div');
      label.className = 'opt-group-label';
      label.innerText = opt.group;
      container.appendChild(label);
      
      if (opt.items) {
        opt.items.forEach(item => {
          container.appendChild(createBtn(item));
        });
      }
    } else {
      container.appendChild(createBtn(opt));
    }
  });
  document.getElementById('chatBody').appendChild(container);
  scrollToBottom();
}

function createBtn(text) {
  const btn = document.createElement('button');
  btn.className = 'opt-btn';
  btn.innerText = text;
  btn.onclick = () => sendOptionDirect(text);
  return btn;
}

function removeOptions() {
  const grids = document.querySelectorAll('.options-grid');
  grids.forEach(g => g.remove());
}

function showTyping(show) {
  const existing = document.getElementById('typingIndicator');
  if (show) {
    if (!existing) {
      const div = document.createElement('div');
      div.id = 'typingIndicator';
      div.className = 'typing-msg';
      div.innerHTML = `
        <div class="msg-avatar" style="opacity:0.5">\uD83E\uDD16</div>
        <div class="typing-dots"><span></span><span></span><span></span></div>
      `;
      document.getElementById('chatBody').appendChild(div);
      scrollToBottom();
    }
  } else {
    if (existing) existing.remove();
  }
}

function updateProgress(step, total) {
  const bar = document.getElementById('progressBar');
  const text = document.getElementById('progressText');
  if (total > 0) {
    const pct = Math.round((step / total) * 100);
    bar.style.width = `${pct}%`;
    text.innerText = `Langkah ${step} dari ${total}`;
  }
}

function scrollToBottom() {
  const chatBody = document.getElementById('chatBody');
  chatBody.scrollTop = chatBody.scrollHeight;
}

function showToast(msg) {
  const div = document.createElement('div');
  div.className = 'error-toast';
  div.innerText = msg;
  document.getElementById('chatBody').appendChild(div);
  scrollToBottom();
  setTimeout(() => div.remove(), 3000);
}

function resetChat() {
  const data = apiRestart();
  const chatBody = document.getElementById('chatBody');
  chatBody.innerHTML = `
    <div class="welcome-screen" id="welcomeScreen" style="display:flex">
      <div class="welcome-icon">\uD83E\uDD16</div>
      <h2>Selamat Datang di MarketBot</h2>
      <p>Saya akan membantu anda menemukan strategi pemasaran terbaik untuk bisnis anda melalui pertanyaan singkat. Proses konsultasi hanya membutuhkan waktu 3\u20135 menit.</p>
      <button class="welcome-btn" onclick="startChat()">Mulai Konsultasi Sekarang \u2192</button>
    </div>
  `;
  document.getElementById('progressBar').style.width = '0%';
  document.getElementById('progressText').innerText = 'Siap memulai';
  startChat();
}

// Enter key to send
document.getElementById('chatInput').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') processInput();
});
</script>
</body>
</html>"""

components.html(HTML, height=900, scrolling=True)
