

# Lane Detection & Road Perception System

### Real-Time Computer Vision Pipeline for Safer Autonomous Navigation

This project implements a real-time road perception system that detects:

* Lane boundaries
* Potholes and road hazards
* Zebra crossings
* Traffic signals

It combines **classical computer vision techniques** with **deep learning-based object detection (YOLOv8)** to simulate perception modules used in **Advanced Driver Assistance Systems (ADAS)** and autonomous vehicles.

---

## 🚗 Why This Project Matters

Modern vehicles rely on perception systems to:

* Maintain lane alignment
* Detect road hazards
* Recognize pedestrian crossings
* Identify traffic signal states

This type of pipeline forms the foundation of:

* Self-driving vehicle stacks
* ADAS features
* Robotics navigation systems
* Smart traffic analytics

This project demonstrates how such a system can be built using Python-based vision frameworks.

---

## 🧠 Core Objective

Develop a real-time vision system capable of analyzing video streams and extracting structured road information.

For each frame, the system:

1. Detects lane boundaries
2. Identifies potholes and surface hazards
3. Recognizes zebra crossings
4. Detects traffic signals
5. Overlays visual annotations in real time

---

## 🏗 System Architecture

The perception pipeline follows a structured multi-stage approach:

Video Input
↓
Frame Preprocessing (OpenCV)

* Grayscale conversion
* Gaussian blur
* Canny edge detection
* Region-of-interest masking

↓
Lane Estimation

* Hough Line Transform
* Line fitting and smoothing

↓
YOLOv8 Inference

* Pothole detection
* Traffic signal detection
* Zebra crossing detection

↓
Bounding box rendering + lane overlay

↓
Annotated output stream

This hybrid architecture reflects how deterministic geometric methods complement neural object detection in real-world autonomous systems.

---

## 🔬 Technical Implementation

### 1. Lane Detection (Classical Computer Vision)

Implemented using:

* Canny edge detection
* Region-of-interest filtering
* Hough Line Transform
* Line fitting / smoothing

Benefits:

* Interpretable results
* Low computational cost
* Reliable under controlled lighting

This demonstrates strong fundamentals in image processing and geometric transformations.

---

### 2. Hazard & Signal Detection (YOLOv8)

Custom-trained YOLOv8 models are used for:

* Pothole detection
* Traffic signal recognition
* Zebra crossing detection

Key engineering aspects:

* Loading pretrained custom weights (.pt files)
* Frame-by-frame inference
* Confidence threshold tuning
* Bounding box stabilization
* Real-time detection loop

This reflects applied deep learning deployment in a live video pipeline.

---

### 3. Real-Time Processing

The system:

* Processes frames sequentially
* Maintains near real-time inference
* Uses efficient NumPy operations
* Minimizes rendering overhead

This demonstrates awareness of runtime and performance constraints typical in CV systems.

---

## 📊 Estimated Performance

* Lane Detection Accuracy: ~90%+ (normal lighting)
* YOLOv8 Detection mAP: ~0.85+
* Real-time Performance: ~25–30 FPS (GPU)
* Frame Processing Time: <100ms

Performance varies based on lighting, dataset quality, and hardware.

---

## 🛠 Technology Stack

* Python
* OpenCV
* Ultralytics YOLOv8
* NumPy
* Optional Tkinter (UI)

---

## 📂 Project Structure

```
Lane-Detection-System-Project/
│
├── pythonProject/
│   └── main.py                      # Entry point for video processing
│
├── yolov8-roadpothole-detection-main/
│   ├── Lane_Detection.py            # Classical lane detection module
│   ├── zebra.py                     # Zebra crossing detection
│   ├── test.py                      # Pothole detection logic
│   ├── ui.py                        # Optional UI layer
│   ├── view_ss.py                   # Output visualization
│   ├── best.pt                      # Custom YOLOv8 pothole model
│   └── best1.pt                     # Custom YOLOv8 signal model
│
├── cam_cal/                         # Camera calibration files
├── Input/                           # Input test videos
├── Lane_Detect_Output/              # Annotated output videos
├── templates/                       # UI templates
└── README.md
```

This structure separates classical CV modules from deep learning detection logic, reflecting modular system design.

---

## 🧪 Engineering Challenges Addressed

* Handling noisy frames in variable lighting
* Integrating classical CV and neural inference coherently
* Reducing bounding box flicker
* Maintaining stable lane overlays
* Preserving near real-time performance

These reflect common production challenges in perception systems.

---

## 💼 Recruiter-Relevant Skills Demonstrated

### For Machine Learning / AI Roles

* Deep learning model integration
* Real-time inference pipelines
* Confidence threshold optimization
* Hybrid system design

### For Computer Vision Roles

* Edge detection & Hough transform
* Region masking & geometric reasoning
* Multi-stage perception architecture

### For Software Engineering Roles

* Modular system design
* Organized codebase structure
* Efficient video processing logic
* Model deployment workflow

---

## 🔍 Limitations

* Reduced accuracy under fog, rain, or poor visibility
* Camera calibration required for optimal lane detection
* Performance dependent on dataset diversity

These limitations reflect realistic CV deployment constraints.

---

## 🚀 Future Improvements

* Sensor fusion with LiDAR or depth cameras
* Lane curvature prediction using polynomial regression
* Lane departure warning system
* Model quantization for edge devices
* Integration into ROS-based autonomous stacks
* Temporal smoothing using Kalman filtering

---

## 🎯 Professional Impact

This project demonstrates:

* Applied computer vision engineering
* Real-time AI system integration
* Deployment-level deep learning usage
* Understanding of autonomous perception pipelines

It reflects capability beyond academic exercises and aligns with roles in AI, ML, computer vision, robotics, and autonomous systems.

---

## 👨‍💻 Author

Atharva Thorat
Master’s in Computer Science – University of Southern California
Focused on AI systems, perception engineering, and applied machine learning.

