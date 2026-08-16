import streamlit as st
import pandas as pd
from layout_engine import default_room_template, normalize_layout, render_floorplan, figure_to_png_bytes, validate_sums

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
# SECTION 3: ACCURATE TO-SCALE 2D LAYOUT (code-generated, not AI image)
# =========================================================================
st.header("3. 📐 Accurate To-Scale 2D Layout (Real Math — No AI Image Guesswork)")
st.caption(
    "Ye section AI image-generator use NAHI karta. Ye Python code se seedha "
    "to-scale drawing banata hai, jisme room dimensions ka SUM hamesha plot "
    "ke width/length ke exactly barabar hota hai — koi mismatch possible nahi."
)

if "room_df" not in st.session_state or st.session_state.get("_last_plot_size") != (width, length):
    st.session_state.room_df = pd.DataFrame(default_room_template(width, length))
    st.session_state._last_plot_size = (width, length)

st.markdown(
    "**Room list edit karein (optional):** `width_ratio` aur `height_ratio` sirf "
    "*proportions* hain (actual ft nahi) — inhe app khud normalize karke exact "
    "feet me convert karta hai, taaki dimensions kabhi mismatch na ho. Same "
    "`row` number wale cells ek hi horizontal strip me side-by-side aayenge."
)

edited_df = st.data_editor(
    st.session_state.room_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "row": st.column_config.NumberColumn("Row #", help="Same row number = same horizontal strip", step=1),
        "room": st.column_config.TextColumn("Room Name"),
        "width_ratio": st.column_config.NumberColumn("Width Ratio", help="Relative proportion within its row"),
        "height_ratio": st.column_config.NumberColumn("Height Ratio", help="Relative proportion of total length (use same value for all cells in a row)"),
    },
    key="room_editor",
)

col_a, col_b = st.columns([1, 1])
with col_a:
    render_btn = st.button("🖼️ Generate To-Scale Drawing", type="primary", use_container_width=True)
with col_b:
    reset_btn = st.button("↺ Reset to Default Template", use_container_width=True)

if reset_btn:
    st.session_state.room_df = pd.DataFrame(default_room_template(width, length))
    st.rerun()

if render_btn:
    room_list = edited_df.to_dict("records")
    # basic cleanup — drop empty rows, ensure numeric types
    room_list = [
        r for r in room_list
        if r.get("room") and r.get("width_ratio") and r.get("height_ratio")
    ]
    if not room_list:
        st.error("Kam se kam ek valid room row chahiye.")
    else:
        layout_rows = normalize_layout(room_list, width, length)
        fig = render_floorplan(layout_rows, width, length, facing=facing)
        st.pyplot(fig, use_container_width=True)

        # Self-check so you can SEE the math is correct
        check = validate_sums(layout_rows, width, length)
        with st.expander("✅ Dimension Self-Check (transparency)"):
            st.write(f"Sum of row heights = **{check['total_height']}'** vs Plot Length = **{check['plot_length']}'** → Match: {check['height_match']}")
            st.write(f"Row-wise width sums = **{check['row_width_sums']}** vs Plot Width = **{check['plot_width']}'** → Match: {check['width_match']}")

        png_bytes = figure_to_png_bytes(fig)
        st.download_button(
            "⬇️ Download To-Scale Floor Plan (PNG)",
            data=png_bytes,
            file_name=f"to_scale_floorplan_{int(width)}x{int(length)}.png",
            mime="image/png",
        )
else:
    st.info("Table adjust karke '🖼️ Generate To-Scale Drawing' dabayein.")
