import streamlit as st
import pandas as pd
from layout_engine import (
    default_grid_template, compute_rooms_geometry, validate_spans,
    alignment_self_check, render_grid_floorplan, figure_to_png_bytes,
    MAX_BEAM_SPAN_DEFAULT,
)

st.set_page_config(page_title="AI Vastu Architect & Structural Expert", page_icon="🏗️", layout="wide")

st.title("🏗️ AI Vastu Architect & Structural Engineer")
st.markdown("Plot ke dimensions aur facing enter karein, aur expert-level AI prompts generate karein.")

# Input Section
st.header("1. Plot Details")
col1, col2, col3 = st.columns(3)
with col1:
    width = st.number_input("Plot Width / Frontage (ft)", min_value=10.0, value=30.0)
with col2:
    length = st.number_input("Plot Length / Depth (ft)", min_value=10.0, value=50.0)
with col3:
    facing = st.selectbox("Plot Facing", ["East", "West", "North", "South", "North-East", "North-West", "South-East", "South-West"])

project_type = st.selectbox("Project Category", ["Luxury Bungalow", "Modern Villa", "Premium Residence"])

st.markdown("---")

if st.button("Generate Expert Prompts", type="primary"):
    area = width * length

    st.header("2. Your Generated Prompts")
    st.info("In prompts ko copy karein aur ChatGPT (o1/GPT-4) ya Claude (Sonnet) me paste karein detail output ke liye. 3D prompts Midjourney/DALL-E ke liye bhi use kar sakte hain.")

    # 1. 2D Floor Plan Prompt
    st.subheader("📐 1. 2D Floor Plan (Vastu Expert)")
    prompt_2d = f"""Act as a Master Architect and Indian Vastu Shastra Expert (referencing authoritative texts like Vishwakarma Prakash, Manasara Shilpa Shastra, and Mayamatam).
I have a plot of {width} ft x {length} ft (Total Area: {area} sq ft). The plot is {facing} facing.
Design a highly optimized, fully Vastu-compliant 2D floor plan for a {project_type}.
Please provide:
1. Exact placement of the Main Entrance, Master Bedroom, Kitchen, Pooja Room, and Toilets with Vastu logic.
2. Dimensions of each room in feet.
3. Circulation area, corridor width, and ventilation details.
4. Setback margins as per typical Indian municipal norms.
Output this in a clear, structured table and provide a descriptive walk-through."""
    st.code(prompt_2d, language="markdown")
    st.download_button("⬇️ Download 2D Prompt", prompt_2d, file_name="1_2d_floor_plan_prompt.txt", key="dl_2d")

    # 2. 3D Elevation Prompt
    st.subheader("🏘️ 2. 3D Exterior Elevation")
    prompt_3d = f"""Act as a world-class 3D Architectural Visualizer.
Create a descriptive prompt for a photorealistic 3D exterior render of a {facing}-facing {project_type} built on a {width} ft x {length} ft plot.
Include details about:
1. Architectural style (e.g., Contemporary, Modern Indian).
2. Materials (e.g., exposed concrete, teak wood louvers, natural stone cladding, glass railings).
3. Lighting (warm ambient exterior lighting, sunset golden hour, photorealistic 8k).
4. Boundary wall design, main gate styling, and landscaping (aligned with Vastu — avoid heavy structures in North-East).
(Make the description vivid enough to be directly used in Midjourney or DALL-E)."""
    st.code(prompt_3d, language="markdown")
    st.download_button("⬇️ Download 3D Prompt", prompt_3d, file_name="2_3d_elevation_prompt.txt", key="dl_3d")

    # 3. Structure, Column & Beam Layout Prompt
    st.subheader("🏗️ 3. Structure Layout (Column & Beam Grid)")
    prompt_structure = f"""Act as a Senior Structural Engineer working in India.
Based on a {width} ft x {length} ft {project_type}, provide a detailed conceptual framework for the structural layout.
1. Suggest an optimal column grid layout (spacing between columns to avoid architectural obstruction, typically 10-15 ft c/c).
2. Define the primary and secondary beam placements, with beam depth guidance (span/12 to span/15 rule of thumb).
3. Suggest the standard column sizes (e.g., 9x12, 9x15, 12x18) for a G+2 structure based on standard load distribution, along with concrete grade (M20/M25).
4. Highlight where heavy load-bearing columns will be required (e.g., near staircase/lift cores, cantilever areas).
5. Recommend foundation type (isolated/raft) based on typical soil conditions.
Explain the logic strictly aligning with IS 456 and IS 1893 standard practices."""
    st.code(prompt_structure, language="markdown")
    st.download_button("⬇️ Download Structure Prompt", prompt_structure, file_name="3_structure_prompt.txt", key="dl_structure")

    # 4. Sariya / Reinforcement Details Prompt
    st.subheader("⛓️ 4. Reinforcement (Sariya) & Strength of Materials")
    prompt_steel = f"""Act as a Structural Engineering Professor specializing in Strength of Materials and RCC Design.
For a standard G+2 {project_type} on a {width} ft x {length} ft plot, provide technical rules of thumb for reinforcement detailing (Sariya/Steel).
Include:
1. Recommended steel grades (e.g., Fe500, Fe550) and concrete grades (e.g., M20, M25).
2. Exact mm sizes of TMT bars for main bars and distribution bars in footing, columns, beams, and slabs.
3. Explain the logic of Shear Stress and Bending Moment in determining stirrup (ring) spacing near beam-column joints (confinement zones per IS 13920) vs. mid-span.
4. Give specific rules for development length, lap zones, minimum clear cover to prevent corrosion, and minimum/maximum steel percentage as per IS 456.
5. Present the final answer as a clear table: Member | Bar Dia (mm) | Spacing | Grade of Steel | Clear Cover | Relevant IS Clause.
Be highly technical and precise. Note that final bar sizes must be verified by a licensed structural engineer after formal load analysis."""
    st.code(prompt_steel, language="markdown")
    st.download_button("⬇️ Download Rebar Prompt", prompt_steel, file_name="4_rebar_sariya_prompt.txt", key="dl_steel")

    # 5. Home/Bangla/Villa Complete Execution Prompt
    st.subheader("🛋️ 5. Luxury Bungalow/Villa Ecosystem")
    prompt_luxury = f"""Act as a Turnkey Luxury Project Manager and Architect.
For a {facing}-facing {project_type} on a {width}x{length} ft plot, provide a holistic execution strategy.
Cover:
1. Landscape integration (green areas, water bodies in the North-East, avoid heavy structures in South-West).
2. Automation and smart home wiring points.
3. HVAC (Air conditioning) ducting strategy or optimal split AC unit placements to not ruin the elevation.
4. Premium material suggestions for flooring, plumbing fixtures, and facades.
5. Provide a high-level sequence of construction stages for a flawless finish, from foundation to handover."""
    st.code(prompt_luxury, language="markdown")
    st.download_button("⬇️ Download Villa Prompt", prompt_luxury, file_name="5_luxury_villa_prompt.txt", key="dl_luxury")

    st.markdown("---")
    st.warning(
        "⚠️ Ye AI-generated prompts hain, actual structural calculation/certification nahi. "
        "Construction se pehle licensed Architect aur Structural Engineer se drawings verify zaroor karvayein."
    )
else:
    st.info("Dimensions bharke '🚀 Generate Expert Prompts' button dabayein.")

st.markdown("---")

# =========================================================================
# SECTION 3: STRUCTURALLY-ALIGNED TO-SCALE 2D LAYOUT (real column grid)
# =========================================================================
st.header("3. 📐 Structurally-Aligned To-Scale 2D Layout")
st.caption(
    "Ye engine AI image-generator use NAHI karta. Saare rooms ek SHARED grid "
    "(x-lines/y-lines) se bante hain — isliye columns hamesha vertically "
    "aligned rehte hain (real RCC continuity), aur har room ka span 15 ft "
    "(editable) se zyada nahi jaane diya jata bina warning ke."
)

if "grid_template" not in st.session_state:
    st.session_state.grid_template = default_grid_template()
if "_last_plot_size3" not in st.session_state or st.session_state._last_plot_size3 != (width, length):
    st.session_state._last_plot_size3 = (width, length)

max_span = st.slider(
    "Max Safe Beam Span (ft)", min_value=8.0, max_value=20.0,
    value=MAX_BEAM_SPAN_DEFAULT, step=0.5,
    help="Iske upar span wale rooms ke liye warning aayegi (intermediate column ya deeper beam chahiye).",
)

with st.expander("🔧 Grid & Room List Edit Karein (Advanced, optional)"):
    st.markdown(
        "**x_ratios** = West→East bay proportions (comma-separated), "
        "**y_ratios** = North→South bay proportions (comma-separated). "
        "Rooms in bays ko *merge* karke bante hain — `col_start/col_end/row_start/row_end` "
        "in ratio-lists ke INDEX hain (0-based). Kyunki sab rooms same grid use karte hain, "
        "column alignment hamesha guaranteed rehta hai — chahe aap kuch bhi edit karein."
    )
    x_ratios_str = st.text_input("x_ratios (West→East)", value=", ".join(str(v) for v in st.session_state.grid_template["x_ratios"]))
    y_ratios_str = st.text_input("y_ratios (North→South)", value=", ".join(str(v) for v in st.session_state.grid_template["y_ratios"]))
    rooms_df = st.data_editor(
        pd.DataFrame(st.session_state.grid_template["rooms"]),
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "name": st.column_config.TextColumn("Room Name"),
            "col_start": st.column_config.NumberColumn("Col Start (idx)", step=1),
            "col_end": st.column_config.NumberColumn("Col End (idx)", step=1),
            "row_start": st.column_config.NumberColumn("Row Start (idx)", step=1),
            "row_end": st.column_config.NumberColumn("Row End (idx)", step=1),
        },
        key="rooms_editor",
    )

col_a, col_b = st.columns([1, 1])
with col_a:
    render_btn = st.button("🖼️ Generate Structurally-Aligned Drawing", type="primary", use_container_width=True)
with col_b:
    reset_btn = st.button("↺ Reset to Corrected Default Template", use_container_width=True)

if reset_btn:
    st.session_state.grid_template = default_grid_template()
    st.rerun()

if render_btn:
    try:
        x_ratios = [float(v.strip()) for v in x_ratios_str.split(",") if v.strip()]
        y_ratios = [float(v.strip()) for v in y_ratios_str.split(",") if v.strip()]
        rooms = rooms_df.dropna().to_dict("records")
        rooms = [
            {**r, "col_start": int(r["col_start"]), "col_end": int(r["col_end"]),
             "row_start": int(r["row_start"]), "row_end": int(r["row_end"])}
            for r in rooms if r.get("name")
        ]
        template = {"x_ratios": x_ratios, "y_ratios": y_ratios, "rooms": rooms}

        rooms_geo, x_lines, y_lines = compute_rooms_geometry(template, width, length)
        fig = render_grid_floorplan(rooms_geo, x_lines, y_lines, width, length, facing=facing)
        st.pyplot(fig, use_container_width=True)

        # --- Transparency: prove alignment + flag long spans ---
        align_check = alignment_self_check(rooms_geo, x_lines, y_lines)
        span_warnings = validate_spans(rooms_geo, max_span=max_span)

        with st.expander("✅ Structural Self-Check", expanded=bool(span_warnings)):
            if align_check["all_aligned"]:
                st.success("Column alignment: PASS — har room boundary ek shared grid-line par hai (structural continuity guaranteed).")
            else:
                st.error(f"Column alignment: FAIL — {align_check['misaligned_rooms']}")

            if span_warnings:
                st.warning(f"{len(span_warnings)} beam-span issue(s) mile:")
                for w in span_warnings:
                    st.write(w)
            else:
                st.success(f"Beam spans: PASS — koi bhi room {max_span:.0f}ft se zyada span nahi kar raha.")

        png_bytes = figure_to_png_bytes(fig)
        st.download_button(
            "⬇️ Download Structurally-Aligned Floor Plan (PNG)",
            data=png_bytes,
            file_name=f"aligned_floorplan_{int(width)}x{int(length)}.png",
            mime="image/png",
        )
    except Exception as e:
        st.error(f"Layout banane me error: {e}. Ratios/rooms table check karein.")
else:
    st.info("Default template already Vastu + structurally corrected hai — seedha button dabayein, ya expander me edit karein.")
