import gradio as gr

# -----------------------------
# Example metric values
# -----------------------------
ACCURACY_VALUE  = 0.9   # e.g. 0.0 to 1.0
PRECISION_VALUE = 0.8
RECALL_VALUE    = 0.7
F1_VALUE        = 0.85

def transform_metric(metric_value, preference):
    """
    If 'Higher is better', we keep the metric as is.
    If 'Lower is better', assume metric ranges 0..1, so transform via (1 - value).
    """
    if preference == "Higher is better":
        return metric_value
    else:
        # 'Lower is better' → invert the metric
        return 1 - metric_value

def normalize_weights(a, p, r, f):
    """
    If sum of weights > 1, scale each proportionally so sum = 1.
    """
    s = a + p + r + f
    if s > 1:
        a = a / s
        p = p / s
        r = r / s
        f = f / s
    return a, p, r, f

def update_sliders(acc, prec, rec, f1):
    """
    Whenever any slider changes,
    1) check if total sum > 1
    2) if so, proportionally scale them down
    3) return updated slider values
    """
    a, p, r, f = normalize_weights(acc, prec, rec, f1)
    return (
        gr.update(value=a),
        gr.update(value=p),
        gr.update(value=r),
        gr.update(value=f)
    )

def calculate_weighted_score(acc, prec, rec, f1,
                             acc_pref, prec_pref, rec_pref, f1_pref):
    """
    1) Normalize weights if sum > 1
    2) Transform each metric if 'Lower is better'
    3) Multiply each metric's adjusted value by its weight
    4) Return final combined score + a summary
    """
    # Ensure we’re not above 1
    a, p, r, f = normalize_weights(acc, prec, rec, f1)

    # Transform the actual metric values based on preference
    acc_transformed = transform_metric(ACCURACY_VALUE,  acc_pref)
    prec_transformed = transform_metric(PRECISION_VALUE, prec_pref)
    rec_transformed = transform_metric(RECALL_VALUE,    rec_pref)
    f1_transformed = transform_metric(F1_VALUE,         f1_pref)

    # Weighted score
    final_score = (a * acc_transformed +
                   p * prec_transformed +
                   r * rec_transformed +
                   f * f1_transformed)

    # Build output text
    summary = f"""
**Weights**  
- Accuracy:  {a:.2f}  
- Precision: {p:.2f}  
- Recall:    {r:.2f}  
- F1-score:  {f:.2f}  

**Preferences**  
- Accuracy:  {acc_pref}  
- Precision: {prec_pref}  
- Recall:    {rec_pref}  
- F1-score:  {f1_pref}

**Metric Values Used** (after preference adjustment)  
- Accuracy → {acc_transformed:.2f}  
- Precision → {prec_transformed:.2f}  
- Recall → {rec_transformed:.2f}  
- F1 → {f1_transformed:.2f}  

**Final Weighted Score** = {final_score:.4f}
"""
    return summary

def build_interface():
    with gr.Blocks() as demo:
        gr.Markdown("## Dynamic Weighting Interface with Preferences")
        gr.Markdown(
            "Each slider sets the metric's *relative weight*. The total weight cannot exceed **1**. "
            "If moving a slider pushes the sum above 1, all sliders get **scaled down** to fit."
        )

        with gr.Row():
            with gr.Column():
                acc_slider = gr.Slider(
                    minimum=0, maximum=1,
                    value=0.25, step=0.01,
                    label="Accuracy Weight",
                    interactive=True
                )
                prec_slider = gr.Slider(
                    minimum=0, maximum=1,
                    value=0.25, step=0.01,
                    label="Precision Weight",
                    interactive=True
                )
                rec_slider = gr.Slider(
                    minimum=0, maximum=1,
                    value=0.25, step=0.01,
                    label="Recall Weight",
                    interactive=True
                )
                f1_slider = gr.Slider(
                    minimum=0, maximum=1,
                    value=0.25, step=0.01,
                    label="F1-score Weight",
                    interactive=True
                )

            with gr.Column():
                acc_pref = gr.Radio(["Higher is better", "Lower is better"],
                                    label="Accuracy Preference",
                                    value="Higher is better")
                prec_pref = gr.Radio(["Higher is better", "Lower is better"],
                                     label="Precision Preference",
                                     value="Higher is better")
                rec_pref = gr.Radio(["Higher is better", "Lower is better"],
                                    label="Recall Preference",
                                    value="Higher is better")
                f1_pref = gr.Radio(["Higher is better", "Lower is better"],
                                   label="F1 Preference",
                                   value="Higher is better")

        # Text area to display result
        output_text = gr.Markdown(label="Output")

        # Each slider triggers an update of *all* slider values if sum>1
        acc_slider.change(
            fn=update_sliders,
            inputs=[acc_slider, prec_slider, rec_slider, f1_slider],
            outputs=[acc_slider, prec_slider, rec_slider, f1_slider]
        )
        prec_slider.change(
            fn=update_sliders,
            inputs=[acc_slider, prec_slider, rec_slider, f1_slider],
            outputs=[acc_slider, prec_slider, rec_slider, f1_slider]
        )
        rec_slider.change(
            fn=update_sliders,
            inputs=[acc_slider, prec_slider, rec_slider, f1_slider],
            outputs=[acc_slider, prec_slider, rec_slider, f1_slider]
        )
        f1_slider.change(
            fn=update_sliders,
            inputs=[acc_slider, prec_slider, rec_slider, f1_slider],
            outputs=[acc_slider, prec_slider, rec_slider, f1_slider]
        )

        # Button to calculate final weighted score
        calculate_button = gr.Button("Calculate Final Score")
        calculate_button.click(
            fn=calculate_weighted_score,
            inputs=[acc_slider, prec_slider, rec_slider, f1_slider,
                    acc_pref, prec_pref, rec_pref, f1_pref],
            outputs=[output_text]
        )

    return demo

# Uncomment to run locally:
if __name__ == "__main__":
  app = build_interface()
  app.launch()
