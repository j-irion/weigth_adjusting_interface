import streamlit as st

def main():
  st.title("Weight Adjustment Interface")

  # Initialize session state
  if 'weights' not in st.session_state:
    st.session_state.weights = [0.25, 0.25, 0.25, 0.25]
  if 'submitted' not in st.session_state:
    st.session_state.submitted = False

  metric_names = ["Metric 1", "Metric 2", "Metric 3", "Metric 4"]

  # Create sliders
  cols = st.columns(4)
  for i in range(4):
    with cols[i]:
      st.subheader(f"{metric_names[i]}")
      st.session_state.weights[i] = st.slider(
        f"Weight",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.weights[i],
        step=0.01,
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