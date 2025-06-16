import streamlit as st
from rectpack import newPacker
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.title("2D Cutting Optimization with Visualization")

# Step 1: Inputs
num_sheets = st.number_input("Enter number of available sheets", min_value=1, step=1)

available_sheets = []
st.subheader("Available Sheet Dimensions")
for i in range(num_sheets):
    st.markdown(f"*Sheet {i+1}*")
    length = st.number_input(f"Length of Sheet {i+1}", min_value=1, key=f"sheet_length_{i}")
    width = st.number_input(f"Width of Sheet {i+1}", min_value=1, key=f"sheet_width_{i}")
    qty = st.number_input(f"Quantity of Sheet {i+1}", min_value=1, key=f"sheet_qty_{i}")
    for _ in range(qty):
        available_sheets.append((length, width))

num_pieces = st.number_input("Enter number of required cut pieces", min_value=1, step=1)

required_pieces = []
st.subheader("Required Cut Pieces")
for i in range(num_pieces):
    st.markdown(f"*Piece {i+1}*")
    length = st.number_input(f"Length of Piece {i+1}", min_value=1, key=f"piece_length_{i}")
    width = st.number_input(f"Width of Piece {i+1}", min_value=1, key=f"piece_width_{i}")
    quantity = st.number_input(f"Quantity of Piece {i+1}", min_value=1, key=f"piece_qty_{i}")
    for _ in range(quantity):
        required_pieces.append((length, width))

# Step 2: Optimization using rectpack
if st.button("Optimize Cutting Plan"):
    st.subheader("Optimized Packing Plan")

    packer = newPacker(rotation=False)

    # Add rectangles (pieces)
    for r in required_pieces:
        packer.add_rect(*r)

    # Add bins (sheets)
    for s in available_sheets:
        packer.add_bin(*s)

    # Perform packing
    packer.pack()

    bin_results = packer[0].rect_list()

    # Step 3: Visualization
    for i, abin in enumerate(packer):
        fig, ax = plt.subplots(figsize=(6, 6))
        sheet_size = (abin.width, abin.height)
        ax.set_title(f"Sheet {i+1}: {sheet_size[0]} x {sheet_size[1]}")
        ax.set_xlim(0, sheet_size[0])
        ax.set_ylim(0, sheet_size[1])
        ax.set_aspect('equal')
        ax.invert_yaxis()

        for rect in abin:
            x = rect.x
            y = rect.y
            w = rect.width
            h = rect.height
            rid = ""
            color = (0.5, 0.8, 0.8)
            ax.add_patch(patches.Rectangle((x, y), w, h, edgecolor='black', facecolor=color, lw=2))
            ax.text(x + w / 2, y + h / 2, f"{w}x{h}", ha='center', va='center', fontsize=8)

        st.pyplot(fig)

    # Step 4: Summary Table
    st.subheader("Packing Summary")
    summary = []
    for i, abin in enumerate(packer):
        for rect in abin:
            x = rect.x
            y = rect.y
            w = rect.width
            h = rect.height
            rid = ""
            summary.append({
                "Sheet No": i + 1,
                "Position (X, Y)": f"{x}, {y}",
                "Piece Size": f"{w} x {h}"
            })

    # Step 5: Wastage Summary
    st.subheader("Wastage Summary")
    wastage_data = []
    for i, abin in enumerate(packer):
        sheet_area = abin.width * abin.height
        used_area = sum(rect.width * rect.height for rect in abin)
        wastage = sheet_area - used_area
        wastage_percent = (wastage / sheet_area) * 100
        wastage_data.append({
            "Sheet No": i + 1,
            "Sheet Area": sheet_area,
            "Used Area": used_area,
            "Wasted Area": wastage,
            "Wastage %": f"{wastage_percent:.2f}%"
        })
    st.table(wastage_data)

    st.table(summary)