import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import io
import base64

def generate_gradcam(model, img_array, target_class_idx=None, original_pil_image=None, alpha=0.45):
    """
    Computes Grad-CAM feature map overlay for MobileNetV2 backbone in model.
    Returns dict containing base64 heatmap, overlay, method name, and target layer.
    """
    if model is None:
        raise ValueError("Model is not loaded.")

    try:
        base_model = model.layers[0]  # mobilenetv2_1.00_224
        target_layer_name = "mobilenetv2_1.00_224/out_relu"
        target_layer = base_model.get_layer("out_relu")

        # Sub-model mapping base inputs -> target feature layer outputs
        conv_submodel = tf.keras.Model(
            inputs=base_model.inputs,
            outputs=target_layer.output
        )

        with tf.GradientTape() as tape:
            # 1. Obtain feature maps from backbone
            conv_outputs = conv_submodel(img_array)
            tape.watch(conv_outputs)

            # 2. Pass feature maps through outer model layers (GAP -> Dense 128 -> Dense 27)
            x = conv_outputs
            for layer in model.layers[1:]:
                x = layer(x)

            preds = x
            if target_class_idx is None:
                target_class_idx = int(tf.argmax(preds[0]))

            # Logit / probability score for target class
            class_score = preds[:, target_class_idx]

        # 3. Compute gradients of target class score w.r.t feature maps
        grads = tape.gradient(class_score, conv_outputs)
        if grads is None:
            # Fallback if gradient is zero/None
            grads = tf.zeros_like(conv_outputs)

        # 4. Global Average Pooling of gradients across spatial dimensions (height, width)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

        # 5. Weight feature maps by gradient importances
        conv_outputs_val = conv_outputs[0]
        heatmap = conv_outputs_val @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)

        # 6. Apply ReLU to keep positive contributions only
        heatmap = tf.maximum(heatmap, 0.0)

        # 7. Normalize heatmap safely to [0, 1]
        max_val = tf.reduce_max(heatmap)
        if max_val > 0:
            heatmap = heatmap / max_val
        heatmap_np = heatmap.numpy()

        # Handle zero / uniform heatmap edge case
        if np.isnan(heatmap_np).any() or np.all(heatmap_np == 0):
            heatmap_np = np.zeros((7, 7), dtype=np.float32)

        # 8. Resize heatmap to (224, 224)
        heatmap_resized = cv2.resize(heatmap_np, (224, 224))
        heatmap_uint8 = np.uint8(255 * heatmap_resized)

        # Apply JET colormap
        colormap_bgr = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
        colormap_rgb = cv2.cvtColor(colormap_bgr, cv2.COLOR_BGR2RGB)

        # Prepare base RGB image
        if original_pil_image is not None:
            base_img = original_pil_image.resize((224, 224))
            base_np = np.array(base_img.convert('RGB'))
        else:
            base_np = np.uint8(np.clip(img_array[0] * 255.0, 0, 255))

        # Superimpose colormap on base image
        overlay_np = cv2.addWeighted(base_np, 1.0 - alpha, colormap_rgb, alpha, 0)

        # Convert to Base64 PNG data URLs
        def image_to_base64(img_np):
            pil_img = Image.fromarray(img_np)
            buf = io.BytesIO()
            pil_img.save(buf, format="PNG")
            return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode('utf-8')

        heatmap_b64 = image_to_base64(colormap_rgb)
        overlay_b64 = image_to_base64(overlay_np)

        return {
            "heatmap": heatmap_b64,
            "overlay": overlay_b64,
            "method": "Grad-CAM",
            "target_layer": target_layer_name
        }

    except Exception as e:
        raise RuntimeError(f"Grad-CAM generation error: {str(e)}")
