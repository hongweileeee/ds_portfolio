import streamlit as st
import mediapipe as mp
import cv2
import numpy as np
import pandas as pd
import pickle
import tensorflow as tf
from tensorflow.keras.models import load_model
import tempfile
import os

tf.__version__ = "2.13.0"
mp.__version__ = "0.10.9"

# Define custom CSS for background color and font family
custom_css = """
<style>
.banner-container {
    background-image: url("https://miro.medium.com/v2/resize:fit:1200/1*XqMxaQCcJZ7jhiDZ-8sdqg.jpeg");
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: local;
    height: 300px; /* Set the height of the banner */
    margin-bottom: 0px; /* Add margin to separate the banner from the content */
}

/* Change background color and text styles for title elements */
.title-container {
    background-color: #d5ff45; /* Yellow background color */
    padding: 20px; /* Add padding to the title container */
    margin-bottom: 0px; /* Add margin below the title container */
}

/* Change font family for all text elements */
body {
    font-family: 'Poppins', sans-serif; /* Poppins font family */
    font-size: 16px;
    background-color: #ffffff !important; /* Set background color to white */
}

/* Change font family specifically for headings */
h1 {
    font-family: 'Poppins', sans-serif; /* Poppins font family */
    font-size: 23px; /* Change to your desired font size */
    text-align: center; /* Center align h1 */
    color: #000000; /* Black text color for h1 */
}

/* Style h3 inside title-container */
.title-container h3 {
    font-family: 'Poppins', sans-serif; /* Poppins font family */
    font-size: 19px; /* Font size for h3 */
    text-align: center; /* Center align h3 */
    color: #000000; /* Black text color for h3 */
}

/* Custom CSS for specific text */
.special-text {
    color: #d5ff45; /* Yellow text color */
    font-size: 24px; /* Font size for specific text */
    text-align: center; /* Center align specific text */
    font-weight: bold; /* Bold font weight for specific text */
    margin-top: 20px; /* Add margin above specific text */
    margin-bottom: 20px; /* Add margin below specific text */
}

/* Style for the file uploader text */
.file-uploader-text {
    color: #ffffff; /* Red text color */
    font-size: 12px; /* Font size for the text */
    font-weight: bold; /* Bold font weight */
    text-align: center; /* Center align the text */
}

</style>
"""

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown('<div class="banner-container"></div>', unsafe_allow_html=True)

# Title (with center alignment using custom CSS)
st.markdown('<div class="title-container"><h1>ZOOM ALLY</h1><h3>Keep Running.</h3></div>', unsafe_allow_html=True)

# Specific text with custom styling
st.markdown('<div class="special-text">Are you overstriding?</div>', unsafe_allow_html=True)

# Render the styled text using Markdown syntax
st.markdown('<p class="file-uploader-text">Upload a video and we\'ll do the rest</p>', unsafe_allow_html=True)

# Load the pre-trained Keras model
model = load_model('../models/cnn_lstm_model.h5')

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results

def draw_landmarks(image, results):
    # Define colors for the left and right sides
    right_color = (255, 0, 0)  # Green color for the left side
    left_color = (0, 255, 0)  # Blue color for the right side

    # Loop through all connections and draw them with the specified colors
    for connection in mp_pose.POSE_CONNECTIONS:
        # Get the landmarks for each end of the connection
        landmark_from = connection[0]
        landmark_to = connection[1]

        # Extract the coordinates for the landmarks
        from_x, from_y = int(results.pose_landmarks.landmark[landmark_from].x * image.shape[1]), int(results.pose_landmarks.landmark[landmark_from].y * image.shape[0])
        to_x, to_y = int(results.pose_landmarks.landmark[landmark_to].x * image.shape[1]), int(results.pose_landmarks.landmark[landmark_to].y * image.shape[0])

        # Check if the connection is for the left side (odd index) or right side (even index)
        if landmark_from % 2 == 0:
            color = right_color  # Right side color
        else:
            color = left_color  # Left side color

        # Draw the connection line with the specified color
        cv2.line(image, (from_x, from_y), (to_x, to_y), color, 2)

    return image

def duplicate_frames(df, max_frames):
    num_dup = max_frames - len(df)

    if num_dup > 0 and num_dup < len(df):
        # Duplicate frames up to the required number of duplicates
        dup_frames = df.loc[:num_dup - 1].copy()
        df = pd.concat([df, dup_frames], ignore_index=True)
    elif num_dup > len(df):
        # Calculate the number of times to duplicate based on the original DataFrame length
        num_duplicates = (max_frames // len(df)) - 1
        orig_df_len = len(df)  # Store the original DataFrame length
        remainder = max_frames % len(df)  # Calculate the remainder
        for _ in range(num_duplicates):
            df = pd.concat([df, df[:orig_df_len]], ignore_index=True)  # Duplicate original rows

        # Add the remaining rows from the original DataFrame to fill up to max_frames
        df = pd.concat([df, df[:remainder]], ignore_index=True)

    return df

def calculate_angle(df, a, b, c):
    a_x = a + '_x'
    a_y = a + '_y'
    b_x = b + '_x'
    b_y = b + '_y'
    c_x = c + '_x'
    c_y = c + '_y'

    radians = np.arctan2(df[c_y].values - df[b_y].values, df[c_x].values - df[b_x].values) - \
              np.arctan2(df[a_y].values - df[b_y].values, df[a_x].values - df[b_x].values)
    angles = np.abs(radians * 180.0 / np.pi)
    angles = np.where(angles > 180.0, 360 - angles, angles)
    return angles

def calculate_shank_angle(df, ankle, knee):
    ankle_x = ankle + '_x'
    ankle_y = ankle + '_y'
    knee_x = knee + '_x'
    knee_y = knee + '_y'

    angle_rad = np.arctan2(df[knee_y] - df[ankle_y], df[knee_x] - df[ankle_x])
    angle_deg = np.degrees(angle_rad) + 90

    return angle_deg

def calculate_lean_angle(df, a, b):
    a_x = a + '_x'
    a_y = a + '_y'
    b_x = b + '_x'
    b_y = b + '_y'

    radians = np.arctan2(0 - df[b_y].values, df[b_x].values - df[b_x].values) - \
              np.arctan2(df[a_y].values - df[b_y].values, df[a_x].values - df[b_x].values)
    angles = np.abs(radians * 180.0 / np.pi)
    angles = np.where(angles > 180.0, 360 - angles, angles)
    return angles

# Load the scaler object
# Load the scaler object from the pickle file
with open('../models/scaler.pkl', 'rb') as f:
    ss = pickle.load(f)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils # Draws the points and lines between points

# File uploader
uploaded_file = st.file_uploader(label="", type=["mp4"])

if uploaded_file is not None:
    vid = uploaded_file.name
    with open(vid, mode='wb') as f:
        f.write(uploaded_file.read())

    # Use VideoCapture to read frames directly from the uploaded video file
    video_capture = cv2.VideoCapture(vid)
    if video_capture.isOpened():
        features = []  # Initialize features list here
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break  # Break the loop if there are no more frames
            image, results = mediapipe_detection(frame, pose)
            keypoints = results.pose_landmarks.landmark
            keypoints_noface = keypoints[11:]

            for keypoint in keypoints_noface:
                feature_list = [value for keypoint in keypoints_noface for value in [keypoint.x, keypoint.y, keypoint.z, keypoint.visibility]]
            features.append(feature_list)  # Append feature_list for each keypoint

        column_names = ['left_shoulder_x', 'left_shoulder_y', 'left_shoulder_z', 'left_shoulder_vis', 
                        'right_shoulder_x', 'right_shoulder_y', 'right_shoulder_z', 'right_shoulder_vis', 
                        'left_elbow_x', 'left_elbow_y', 'left_elbow_z', 'left_elbow_vis', 
                        'right_elbow_x', 'right_elbow_y', 'right_elbow_z', 'right_elbow_vis', 
                        'left_wrist_x', 'left_wrist_y', 'left_wrist_z', 'left_wrist_vis', 
                        'right_wrist_x', 'right_wrist_y', 'right_wrist_z', 'right_wrist_vis', 
                        'left_pinky_x', 'left_pinky_y', 'left_pinky_z', 'left_pinky_vis', 
                        'right_pinky_x', 'right_pinky_y', 'right_pinky_z', 'right_pinky_vis', 
                        'left_index_x', 'left_index_y', 'left_index_z', 'left_index_vis', 
                        'right_index_x', 'right_index_y', 'right_index_z', 'right_index_vis', 
                        'left_thumb_x', 'left_thumb_y', 'left_thumb_z', 'left_thumb_vis', 
                        'right_thumb_x', 'right_thumb_y', 'right_thumb_z', 'right_thumb_vis', 
                        'left_hip_x', 'left_hip_y', 'left_hip_z', 'left_hip_vis', 
                        'right_hip_x', 'right_hip_y', 'right_hip_z', 'right_hip_vis', 
                        'left_knee_x', 'left_knee_y', 'left_knee_z', 'left_knee_vis', 
                        'right_knee_x', 'right_knee_y', 'right_knee_z', 'right_knee_vis', 
                        'left_ankle_x', 'left_ankle_y', 'left_ankle_z', 'left_ankle_vis', 
                        'right_ankle_x', 'right_ankle_y', 'right_ankle_z', 'right_ankle_vis', 
                        'left_heel_x', 'left_heel_y', 'left_heel_z', 'left_heel_vis', 
                        'right_heel_x', 'right_heel_y', 'right_heel_z', 'right_heel_vis', 
                        'left_foot_index_x', 'left_foot_index_y', 'left_foot_index_z', 'left_foot_index_vis',
                            'right_foot_index_x', 'right_foot_index_y', 'right_foot_index_z', 'right_foot_index_vis']

        df = pd.DataFrame(features, columns=column_names)

        df_dup = duplicate_frames(df, 258)

        df_dup['right_knee_angle'] = calculate_angle(df_dup, 'right_hip', 'right_knee', 'right_ankle')
        df_dup['left_knee_angle'] = calculate_angle(df_dup, 'left_hip', 'left_knee', 'left_ankle')
        df_dup['left_shank_angle'] = calculate_shank_angle(df_dup, 'left_ankle', 'left_knee')
        df_dup['right_shank_angle'] = calculate_shank_angle(df_dup, 'right_ankle', 'right_knee')
        df_dup['left_ankle_change'] = np.gradient(df_dup['left_ankle_y'])
        df_dup['right_ankle_change'] = np.gradient(df_dup['right_ankle_y'])
        df_dup['left_ankle_hip_distance'] = np.sqrt((df_dup['left_ankle_x'] - df_dup['left_hip_x']) ** 2 + 
                                    (df_dup['left_ankle_y'] - df_dup['left_hip_y']) ** 2)
        df_dup['right_ankle_hip_distance'] = np.sqrt((df_dup['right_ankle_x'] - df_dup['right_hip_x']) ** 2 + 
                                    (df_dup['right_ankle_y'] - df_dup['right_hip_y']) ** 2)
        df_dup['left_lean_angle'] = calculate_lean_angle(df_dup, 'left_shoulder', 'left_hip')
        df_dup['right_lean_angle'] = calculate_lean_angle(df_dup, 'right_shoulder', 'right_hip')

        # Scale the data
        X = ss.transform(df_dup)

        # Reshape data to have 1 sample, 258 frames and 98 features
        X_pred = np.expand_dims(X, axis=0)

        # Make predictions with the model
        predictions = model.predict(X_pred)
        max_probabilities = np.max(predictions, axis=1)
        threshold = 0.7
        labels = (max_probabilities > threshold).astype(int)
        flat_labels = np.array(labels).flatten()

        if flat_labels == 1:
            st.markdown('<div class="special-text">You are overstriding in this video</div>', unsafe_allow_html=True)
            st.markdown('<div class="file-uploader-text">Some tips for you! <br> * Lean forward slightly <br> * Take smaller steps <br> * Increase your cadence </div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="special-text">You are running with good form <br> Keep it up!</div>', unsafe_allow_html=True)

        # Calculate frame indices based on conditions
        landing_frame = np.argmax(df_dup['left_shank_angle'].values) + 1
        max_left_ankle_y_frame = np.argmax(df_dup['left_ankle_y'].values)
        max_left_ankle_x_frame = np.argmax(df_dup['left_ankle_x'].values)

        # Display frames with pose skeleton based on conditions
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, landing_frame)
        ret, frame_landing = video_capture.read()

        video_capture.set(cv2.CAP_PROP_POS_FRAMES, max_left_ankle_y_frame)
        ret, frame_max_left_ankle_y = video_capture.read()

        video_capture.set(cv2.CAP_PROP_POS_FRAMES, max_left_ankle_x_frame)
        ret, frame_max_left_ankle_x = video_capture.read()

        if ret:
            # Perform pose detection on each frame
            image_landing, results_landing = mediapipe_detection(frame_landing, pose)
            image_max_left_ankle_y, results_max_left_ankle_y = mediapipe_detection(frame_max_left_ankle_y, pose)
            image_max_left_ankle_x, results_max_left_ankle_x = mediapipe_detection(frame_max_left_ankle_x, pose)

            # Draw landmarks on the frames
            draw_landmarks(image_landing, results_landing)
            draw_landmarks(image_max_left_ankle_y, results_max_left_ankle_y)
            draw_landmarks(image_max_left_ankle_x, results_max_left_ankle_x)

            # Convert frames to RGB format after drawing landmarks
            frame_landing_rgb = cv2.cvtColor(image_landing, cv2.COLOR_BGR2RGB)
            frame_max_left_ankle_y_rgb = cv2.cvtColor(image_max_left_ankle_y, cv2.COLOR_BGR2RGB)
            frame_max_left_ankle_x_rgb = cv2.cvtColor(image_max_left_ankle_x, cv2.COLOR_BGR2RGB)

            # Display frames side by side using st.columns
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image(frame_landing_rgb, channels="RGB", caption="Initial Contact")
            with col2:
                st.image(frame_max_left_ankle_y_rgb, channels="RGB", caption="Stance Position")
            with col3:
                st.image(frame_max_left_ankle_x_rgb, channels="RGB", caption="Toe-Off")

    else:
        st.error("Failed to open the uploaded video file.")
else:
    st.warning("Please upload an MP4 video.")   