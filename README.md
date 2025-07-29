# ZeroTouch - A virtual mouse with both hand & eye tracking.

A Python code that allows you to control your computer mouse using hand gestures or eye movements through computer vision and machine learning.

## Features

- **Hand Tracking Mode**: Control mouse cursor with index finger movement and click by pinching thumb and index finger
- **Eye Tracking Mode**: Control mouse cursor with head/nose movement and click by blinking
- **Smooth Movement**: Built-in smoothing algorithms for stable cursor control
- **Real-time Switching**: Switch between hand and eye tracking modes during runtime
- **Visual Feedback**: Live video feed with tracking indicators and status information

## Requirements

- Python 3.7 or higher
- Webcam/Camera
- Operating System: Windows, macOS, or Linux


## Usage

1. Run the code.

2. Position yourself in front of the camera with good lighting

3. Use keyboard controls:
   - **'h'** - Switch to Hand tracking mode
   - **'e'** - Switch to Eye tracking mode  
   - **'q'** - Quit the application

### Hand Tracking Mode
- Move your index finger to control the cursor
- Pinch your thumb and index finger together to click
- Keep your hand visible and well-lit for best results

### Eye Tracking Mode
- Move your head/nose to control the cursor
- Blink both eyes simultaneously to click
- Keep your face centered and well-lit for best results

## Technical Details

This application uses:
- **OpenCV** for computer vision and camera handling
- **MediaPipe** for hand and face landmark detection
- **PyAutoGUI** for mouse control automation

### Key Components

- `VirtualMouse` class: Main application controller
- `process_hand()`: Handles hand gesture recognition and mouse control
- `process_eye()`: Handles eye/face tracking and blink detection
- `smooth_movement()`: Applies smoothing algorithms for stable cursor movement

## Configuration

You can adjust these parameters in the code:
- `smoothing`: Controls cursor movement smoothness (default: 0.2)
- `min_detection_confidence`: MediaPipe detection threshold (default: 0.7)
- `min_tracking_confidence`: MediaPipe tracking threshold (default: 0.7)
- Click sensitivity thresholds for both hand pinch and eye blink detection

## Troubleshooting

**Camera not working:**
- Ensure your camera is not being used by another application
- Try changing the camera index in `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` or higher

**Poor tracking accuracy:**
- Ensure good lighting conditions
- Keep your hand/face clearly visible in the camera frame
- Avoid background clutter
- Adjust detection confidence thresholds if needed

**Mouse movement too sensitive/slow:**
- Adjust the `smoothing` parameter (lower = more responsive, higher = more stable)
- Modify the coordinate mapping calculations in the respective processing functions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google MediaPipe team for the excellent hand and face tracking models
- OpenCV community for computer vision tools
- PyAutoGUI developers for mouse automation capabilities
