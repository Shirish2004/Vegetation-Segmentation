import cv2
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('D:/SEM7/DSE406_SDSA/ASSIGNMENT1/model.h5')

# Function to assess vegetation quality
def assess_vegetation_quality(mask):
    vegetation_pixels = (mask > 0).sum() / mask.size * 100
    if vegetation_pixels < 30:
        return f"PV {vegetation_pixels}"
    elif 30 <= vegetation_pixels <= 60:
        return f"MV {vegetation_pixels}"
    else:
        return f"GV {vegetation_pixels}"

# Open the webcam
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (224, 224))
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = np.expand_dims(frame_gray, axis=-1)  # Adding channel dimension

    
    input_image = frame_gray / 255.0  # Normaliing to [0, 1]
    input_image = np.expand_dims(input_image, axis=0)  # Adding batch dimension
    mask = model.predict(input_image)[0]

    
    threshold = 0.05 # based on experimentation
    binary_mask = (mask > threshold).astype(np.uint8) * 255

    # Assessing vegetation quality
    vegetation_quality = assess_vegetation_quality(binary_mask)

    # Overlaying the mask on the frame
    masked_frame = cv2.addWeighted(frame, 0.5, cv2.cvtColor(binary_mask, cv2.COLOR_GRAY2BGR), 0.5, 0)

    # Results with mask and quality
    cv2.putText(masked_frame, vegetation_quality, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Real-time Segmentation", masked_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
