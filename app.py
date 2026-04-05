import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from data import DATA, get_RuH, check_limit

st.title("Breakwater Crest Height Estimator")

g = 9.81

# ==== INPUT ====
st.subheader("Input Parameters")

Hs = st.number_input("Wave Height Hs (m)", min_value=0.1)
HWS = st.number_input("Highest Water Surface (HWS) (m)")
cot_theta = st.number_input("cot(theta)", min_value=0.1)
armor_type = st.selectbox("Armor Type", list(DATA.keys()))

# ==== INIT SESSION STATE ====
if "results" not in st.session_state:
    st.session_state.results = None

# ==== BUTTON ====
if st.button("Run Analysis"):

    # Wave calculations
    T = 15.6 * np.sqrt(Hs / g)
    L = 1.56 * T**2
    Ir = (1 / cot_theta) / np.sqrt(Hs / L)

    valid = check_limit(armor_type, Ir)

    if valid:
        Ru_H = get_RuH(armor_type, Ir)
        Ru = Ru_H * Hs
        E = Ru + HWS

        # Store results
        st.session_state.results = {
            "T": T,
            "L": L,
            "Ir": Ir,
            "Ru_H": Ru_H,
            "Ru": Ru,
            "E": E,
            "armor_type": armor_type
        }
    else:
        st.session_state.results = {"error": True}

# ==== DISPLAY RESULTS ====
if st.session_state.results:

    res = st.session_state.results

    if "error" in res:
        st.error("Ir exceeds valid range for selected armor type")
    else:
        st.subheader("Results")
        st.write(f"T = {res['T']:.3f} s")
        st.write(f"L = {res['L']:.3f} m")
        st.write(f"Ir = {res['Ir']:.3f}")
        st.write(f"Ru/H = {res['Ru_H']:.3f}")
        st.write(f"Ru = {res['Ru']:.3f} m")
        st.success(f"Crest Height (E) = {res['E']:.3f} m")

        # ==== GRAPH ====
        data_points = DATA[res["armor_type"]]
        xp = [p[0] for p in data_points]
        yp = [p[1] for p in data_points]

        fig, ax = plt.subplots()
        ax.plot(xp, yp)
        ax.scatter(res["Ir"], res["Ru_H"])

        ax.set_xlabel("Ir (Iribarren Number)")
        ax.set_ylabel("Ru/H")
        ax.set_title(f"{res['armor_type']} Run-up Curve")

        st.pyplot(fig)
