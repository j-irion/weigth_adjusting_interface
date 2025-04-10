import streamlit as st

def main():
  st.title("Weight Adjustment Interface")

  # Initialize session state
  if 'weights' not in st.session_state:
    st.session_state.weights = [0.25, 0.25, 0.25, 0.25]
  if 'submitted' not in st.session_state:
    st.session_state.submitted = False

  # Keep track of each column's selected metric in session_state
  for i in range(4):
    if f"metric_select_{i}" not in st.session_state:
      st.session_state[f"metric_select_{i}"] = "None"

  metrics = [
    {"name": "Metric 1", "direction": "higher"},
    {"name": "Metric 2", "direction": "higher"},
    {"name": "Metric 3", "direction": "lower"},
    {"name": "Metric 4", "direction": "lower"},
    {"name": "Metric 5", "direction": "higher"},
    {"name": "Metric 6", "direction": "lower"},
    {"name": "Metric 7", "direction": "higher"},
    {"name": "Metric 8", "direction": "lower"}
  ]

  metric_names = [m["name"] for m in metrics]

  # Create sliders
  cols = st.columns(4)
  for i in range(4):
    with cols[i]:
      # Build the list of used metrics (except current selection)
      used_metrics = [
        st.session_state[f"metric_select_{j}"]
        for j in range(4) if j != i
      ]

      # Build possible options for this selectbox
      current_selection = st.session_state[f"metric_select_{i}"]
      options_for_this_col = ["None"] + [
        m for m in metric_names
        if (m not in used_metrics) or (m == current_selection)
      ]

      # Metric selection dropdown
      selected_metric = st.selectbox(
        "Select Metric",
        options=options_for_this_col,
        index=options_for_this_col.index(current_selection),
        key=f"metric_select_{i}"
      )

      # If a valid metric is selected, find and display its direction
      if selected_metric != "None":
        direction = next(m["direction"]
                         for m in metrics if m["name"] == selected_metric)
        st.caption(f"{direction.capitalize()} is better")
      else:
        st.caption("No metric selected")

      st.session_state.weights[i] = st.slider(
        f"Weight",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.weights[i],
        step=0.05,
        key=f"weight_{i}"
      )
  # Calculate total weight
  total_weight = sum(st.session_state.weights)

  # Validation
  if total_weight > 1.0:
    st.error("Total weights exceed 100%! Current total: {:.2f}".format(total_weight))
  elif total_weight < 1.0:
    st.error("Total weights are less than 100%! Current total: {:.2f}".format(total_weight))
  else:
    st.success("Valid configuration! Total: 1.00")

  # Submit button with conditional disabling
  submit_disabled = total_weight != 1.0
  if st.button("Submit Configuration", disabled=submit_disabled):
    st.session_state.submitted = True

  # Show results after submission
  if st.session_state.submitted:
    st.divider()
    st.subheader(" Submitted Configuration:")
    for i in range(4):
      st.write(
        f"{metric_names[i]}: {st.session_state.weights[i]:.2f}"
      )

if __name__ == "__main__":
  main()