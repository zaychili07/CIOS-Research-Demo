
from __future__ import annotations

from io import BytesIO
from pathlib import Path
import json

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

try:
    import tifffile
except Exception:
    tifffile = None


APP_ROOT = Path(__file__).resolve().parent
DATA_ROOT = APP_ROOT / "data"
METRICS = json.loads((DATA_ROOT / "research_metrics.json").read_text(encoding="utf-8"))

st.set_page_config(
    page_title="CIOS — Reality. Carefully Reconstructed.",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.1rem; padding-bottom: 3rem; max-width: 1480px;}
    h1, h2, h3 {letter-spacing:-0.02em;}
    .hero {
        padding:1.7rem 2rem; border:1px solid rgba(130,130,130,.26); border-radius:22px;
        background:linear-gradient(135deg,rgba(16,31,50,.96),rgba(51,24,62,.88)); margin-bottom:1rem;
    }
    .hero-kicker {font-size:.78rem; letter-spacing:.14em; opacity:.72; font-weight:800;}
    .hero-title {font-size:3rem; line-height:1.03; font-weight:850; margin:.28rem 0 .35rem 0;}
    .hero-sub {font-size:1.06rem; opacity:.88; max-width:980px;}
    .pill {display:inline-block;padding:.24rem .7rem;border:1px solid rgba(150,150,150,.35);
        border-radius:999px;margin:.2rem .25rem .2rem 0;font-size:.82rem;}
    .notice {padding:.8rem 1rem;border-radius:14px;border:1px solid rgba(150,150,150,.28);background:rgba(80,80,80,.06);}
    .synthetic {padding:.8rem 1rem;border-radius:14px;border:1px solid rgba(230,170,50,.35);background:rgba(230,170,50,.09);}
    div[data-testid="stMetric"] {border:1px solid rgba(120,120,120,.22);padding:.9rem 1rem;border-radius:16px;}
    </style>
    """,
    unsafe_allow_html=True,
)


def hero():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">PROJECT SIXTH SENSE · CIOS</div>
            <div class="hero-title">Reality. Carefully Reconstructed.</div>
            <div class="hero-sub">
                An interactive research demo for 3D+t cell tracking, lineage reconstruction,
                temporal motion reasoning, evidence governance, and the experiments that did not earn authority.
            </div>
            <div style="margin-top:.8rem">
                <span class="pill">3D + time</span>
                <span class="pill">AVG3</span>
                <span class="pill">Lineage reasoning</span>
                <span class="pill">Uncertainty preserved</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def bar(title, labels, values, y_title="Score"):
    fig = go.Figure(go.Bar(
        x=labels, y=values, text=[f"{v:.4f}" for v in values], textposition="outside"
    ))
    fig.update_layout(
        title=title, yaxis_title=y_title, height=360, margin=dict(l=20,r=20,t=55,b=20),
        yaxis=dict(range=[0, max(values)*1.18 if values else 1])
    )
    return fig


@st.cache_data
def load_builtin_demo():
    arr = np.load(DATA_ROOT / "illustrative_microscopy_demo.npz", allow_pickle=False)["volume"]
    tracks = pd.read_csv(DATA_ROOT / "illustrative_tracks.csv")
    return arr, tracks


def normalize_plane(image):
    arr = np.asarray(image)
    if arr.ndim == 3 and arr.shape[-1] in (3,4):
        return arr
    arr = arr.astype(np.float32)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        return np.zeros_like(arr, dtype=np.uint8)
    lo, hi = np.percentile(finite, [1, 99.5])
    if hi <= lo:
        lo, hi = float(finite.min()), float(finite.max() or 1)
    out = np.clip((arr-lo)/max(hi-lo,1e-9),0,1)
    return (out*255).astype(np.uint8)


def load_uploaded_volume(upload):
    raw = upload.getvalue()
    suffix = Path(upload.name).suffix.lower()
    if suffix == ".npy":
        return np.load(BytesIO(raw), allow_pickle=False)
    if suffix == ".npz":
        archive = np.load(BytesIO(raw), allow_pickle=False)
        keys = list(archive.files)
        if not keys:
            raise ValueError("NPZ archive contains no arrays.")
        return archive[keys[0]]
    if suffix in (".tif",".tiff"):
        if tifffile is None:
            raise RuntimeError("TIFF support is unavailable.")
        return tifffile.imread(BytesIO(raw))
    if suffix in (".png",".jpg",".jpeg"):
        return np.asarray(Image.open(BytesIO(raw)))
    raise ValueError("Supported image formats: NPY, NPZ, TIFF, PNG, JPG.")


def home():
    hero()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("AVG3 Hit@1", f"{METRICS['avg3']['avg3_hit1']:.3f}",
              f"+{METRICS['avg3']['avg3_hit1']-METRICS['avg3']['raw_hit1']:.3f} vs raw")
    c2.metric("AVG3 MRR", f"{METRICS['avg3']['avg3_mrr']:.3f}",
              f"+{METRICS['avg3']['avg3_mrr']-METRICS['avg3']['raw_mrr']:.3f} vs raw")
    c3.metric("Kaggle private", f"{METRICS['kaggle']['final_d_private']:.3f}",
              f"+{METRICS['kaggle']['final_d_private']-METRICS['kaggle']['baseline_private']:.3f} vs baseline")
    c4.metric("Known visible division miss", "0 / 3", "Open limitation")

    left,right = st.columns([1.25,1])
    with left:
        st.subheader("What CIOS is")
        st.write(
            "CIOS is a research system for reconstructing cellular relationships over time. "
            "It treats motion, graph structure, lineage, provenance, and uncertainty as separate evidence domains "
            "rather than letting a single model output become biological truth."
        )
        st.markdown(
            '<div class="notice"><b>Research rule:</b> a promising result does not automatically earn authority.</div>',
            unsafe_allow_html=True
        )
    with right:
        st.plotly_chart(bar(
            "Competition result",
            ["Baseline public","Final D public","Baseline private","Final D private"],
            [METRICS["kaggle"]["baseline_public"],METRICS["kaggle"]["final_d_public"],
             METRICS["kaggle"]["baseline_private"],METRICS["kaggle"]["final_d_private"]]
        ), use_container_width=True)
        st.caption("Competition tracking scores — not classification accuracy.")


def observation():
    hero()
    st.header("Observation Viewer")

    source = st.radio(
        "Data source",
        ["Built-in illustrative demo", "Upload your own microscopy"],
        horizontal=True,
    )

    if source == "Built-in illustrative demo":
        volume, tracks = load_builtin_demo()
        st.markdown(
            '<div class="synthetic"><b>ILLUSTRATIVE SYNTHETIC DEMO.</b> '
            'This visualization is included only so the public app is interactive. '
            'It is not CIOS experimental microscopy evidence and is not used for any reported metric.</div>',
            unsafe_allow_html=True
        )
        t = st.slider("Time", 0, volume.shape[0]-1, 5)
        z = st.slider("Z plane", 0, volume.shape[1]-1, volume.shape[1]//2)
        current_tracks = tracks[tracks["t"] == t].copy()
        plane = normalize_plane(volume[t,z])

        left,right = st.columns([1.05,1])
        with left:
            st.image(plane, caption=f"Illustrative synthetic volume · t={t} · z={z}", use_container_width=True)
        with right:
            fig = go.Figure()
            for track_id, group in tracks[tracks["t"] <= t].groupby("track_id"):
                fig.add_trace(go.Scatter3d(
                    x=group["x"], y=group["y"], z=group["z"],
                    mode="lines+markers", name=f"track {track_id}",
                    marker=dict(size=3)
                ))
            fig.update_layout(
                height=520, margin=dict(l=0,r=0,t=10,b=0),
                scene=dict(xaxis_title="X",yaxis_title="Y",zaxis_title="Z")
            )
            st.plotly_chart(fig, use_container_width=True)

        st.caption("The demo includes one illustrative split event to make lineage visualization understandable.")

    else:
        st.info("Uploads are processed only in the active app session. They are not part of CIOS research evidence.")
        image_file = st.file_uploader(
            "Upload microscopy array/image",
            type=["npy","npz","tif","tiff","png","jpg","jpeg"],
            max_upload_size=100,
        )
        coord_file = st.file_uploader(
            "Optional coordinate CSV with x/y/z and optional t/track_id",
            type=["csv"],
            max_upload_size=20,
        )

        if image_file is None:
            st.warning("Upload a microscopy image/array to begin.")
            return

        try:
            arr = load_uploaded_volume(image_file)
        except Exception as exc:
            st.error(str(exc))
            return

        st.write("Array shape:", tuple(arr.shape))

        if arr.ndim == 2:
            plane = arr
            context_t = None
        elif arr.ndim == 3:
            z = st.slider("Plane",0,arr.shape[0]-1,arr.shape[0]//2)
            plane = arr[z]
            context_t = None
        elif arr.ndim == 4:
            t = st.slider("Time",0,arr.shape[0]-1,0)
            z = st.slider("Z",0,arr.shape[1]-1,arr.shape[1]//2)
            plane = arr[t,z]
            context_t = t
        else:
            st.error("Expected a 2D, 3D, or 4D array.")
            return

        left,right = st.columns([1.05,1])
        with left:
            st.image(normalize_plane(plane), caption=image_file.name, use_container_width=True)
        with right:
            if coord_file is None:
                st.info("Upload a coordinate CSV to add a 3D track view.")
            else:
                try:
                    df = pd.read_csv(coord_file)
                    lookup = {c.lower():c for c in df.columns}
                    if not all(k in lookup for k in ("x","y","z")):
                        raise ValueError("Coordinate CSV must contain x, y, and z columns.")
                    df = df.rename(columns={lookup["x"]:"x",lookup["y"]:"y",lookup["z"]:"z"})
                    if "t" in lookup:
                        df = df.rename(columns={lookup["t"]:"t"})
                    if context_t is not None and "t" in df.columns:
                        df = df[df["t"] <= context_t]

                    fig = go.Figure(go.Scatter3d(
                        x=df["x"],y=df["y"],z=df["z"],mode="markers",marker=dict(size=3)
                    ))
                    fig.update_layout(
                        height=520,margin=dict(l=0,r=0,t=10,b=0),
                        scene=dict(xaxis_title="X",yaxis_title="Y",zaxis_title="Z")
                    )
                    st.plotly_chart(fig,use_container_width=True)
                except Exception as exc:
                    st.error(str(exc))


def avg3():
    hero()
    st.header("AVG3 Motion Intelligence")
    st.latex(r"v_{\mathrm{AVG3}}(t)=\frac{p_t-p_{t-3}}{3}")
    st.latex(r"R_{\mathrm{BI}}=\sqrt{\frac{R_F^2+R_B^2}{2}}")

    c1,c2,c3 = st.columns(3)
    c1.metric("Pseudo-gap scenarios",f"{METRICS['avg3']['scenarios']:,}")
    c2.metric("Hit@1",f"{METRICS['avg3']['avg3_hit1']:.4f}",
              f"+{METRICS['avg3']['avg3_hit1']-METRICS['avg3']['raw_hit1']:.4f}")
    c3.metric("MRR",f"{METRICS['avg3']['avg3_mrr']:.4f}",
              f"+{METRICS['avg3']['avg3_mrr']-METRICS['avg3']['raw_mrr']:.4f}")

    st.plotly_chart(bar(
        "Continuation diagnostics",
        ["Raw Hit@1","AVG3 Hit@1","Raw MRR","AVG3 MRR"],
        [METRICS["avg3"]["raw_hit1"],METRICS["avg3"]["avg3_hit1"],
         METRICS["avg3"]["raw_mrr"],METRICS["avg3"]["avg3_mrr"]]
    ), use_container_width=True)

    st.caption("Pseudo-gap continuation diagnostics only — not hidden-test results.")
    st.write(
        "AVG3 is used as motion evidence, not as biological identity authority. "
        "A candidate can be motion-consistent and still be rejected by downstream graph or evidence rules."
    )


def evidence():
    hero()
    st.header("Evidence & Failure")
    st.subheader("ATR: strong geometry, no graph authority")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Geometry",
        x=["All evaluated","Hard subset"],
        y=[21/21,7/7], text=["21/21","7/7"], textposition="outside"
    ))
    fig.add_trace(go.Bar(
        name="Gated success",
        x=["All evaluated","Hard subset"],
        y=[19/21,5/7], text=["19/21","5/7"], textposition="outside"
    ))
    fig.update_layout(barmode="group",height=380,yaxis=dict(range=[0,1.15]),yaxis_title="Rate")
    st.plotly_chart(fig,use_container_width=True)

    st.warning(
        "ATR localized all evaluated references geometrically, but the detector-support gate did not clear "
        "the preregistered performance requirement. Synthetic latent-node insertion therefore remained unauthorized."
    )

    a,b,c = st.columns(3)
    a.metric("A-selected edges removed by final D","0")
    b.metric("Target-parent swaps","0")
    c.metric("Independent D − A",f"+{METRICS['independent_d']['delta']:.4f}")


def results():
    hero()
    st.header("Results")
    st.warning("Scores stay attached to their evaluation populations. Local, independent, and Kaggle results are not interchangeable.")

    left,right = st.columns(2)
    with left:
        st.plotly_chart(bar(
            "Independent A vs D",
            ["A baseline","D ownership-safe"],
            [METRICS["independent_d"]["a_score"],METRICS["independent_d"]["d_score"]]
        ),use_container_width=True)
    with right:
        st.plotly_chart(bar(
            "Kaggle baseline vs final D",
            ["Baseline public","Final D public","Baseline private","Final D private"],
            [METRICS["kaggle"]["baseline_public"],METRICS["kaggle"]["final_d_public"],
             METRICS["kaggle"]["baseline_private"],METRICS["kaggle"]["final_d_private"]]
        ),use_container_width=True)

    st.subheader("What the competition exposed")
    st.markdown(
        """
        - Better local motion estimates do not guarantee better global graph assignment.
        - Aggregate gains can hide per-field regressions.
        - Fresh-to-rule validation is not enough if the upstream detector already saw the embryo.
        - Division reconstruction remained a structural weakness.
        - A failed or HOLD experiment is still useful when it identifies the causal limitation.
        """
    )


def frontier():
    hero()
    st.header("Research Frontier")
    st.write(
        "CIOS is continuing beyond the competition. The next phase is focused on making local evidence "
        "predict unseen biological reality more reliably."
    )
    for i,item in enumerate(METRICS["priorities"],1):
        st.markdown(f"**{i}. {item}**")
    st.markdown(
        '<div class="notice"><b>Next principle:</b> validation foundation first, then deeper intelligence.</div>',
        unsafe_allow_html=True
    )


PAGES = {
    "Mission Control":home,
    "Observation Viewer":observation,
    "AVG3 Motion Intelligence":avg3,
    "Evidence & Failure":evidence,
    "Results":results,
    "Research Frontier":frontier,
}

st.sidebar.markdown("## CIOS Public Research Demo")
st.sidebar.caption("Interactive portfolio build · scientific execution disabled")
page = st.sidebar.radio("Navigate", list(PAGES))
st.sidebar.divider()
st.sidebar.markdown("**Final competition config**")
st.sidebar.code(METRICS["kaggle"]["final_candidate"],language=None)
st.sidebar.markdown("**Authority boundary**")
st.sidebar.write("AVG3 contributes motion evidence. ATR latent-node insertion remains HOLD.")
st.sidebar.divider()
st.sidebar.caption("Project Sixth Sense · We Detect What Others Miss.")

PAGES[page]()
