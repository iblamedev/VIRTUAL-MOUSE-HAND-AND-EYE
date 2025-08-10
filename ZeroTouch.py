import cv2
import mediapipe as mp
import pyautogui
#The uses are mentioned in comment lines.
class VirtualMouse:
    def __init__(self):
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        
        # Initialize MediaPipe solutions
        self.hand_detector = mp.solutions.hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            refine_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
        # Initialize drawing utils
        self.drawing_utils = mp.solutions.drawing_utils
        
        # Get screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Control mode
        self.mode = "hand"  # can be "hand" or "eye"
        
        # Initialize previous coordinates
        self.prev_x, self.prev_y = 0, 0
        
        # Smoothing factor (reduced for less sensitivity)
        self.smoothing = 0.2  # Reduced for more stability
        
        # Click state
        self.is_clicking = False
        
        # Prevent pyautogui from raising exceptions
        pyautogui.FAILSAFE = False

    def smooth_movement(self, new_x, new_y):
        # Enhanced smoothing with acceleration
        dx = new_x - self.prev_x
        dy = new_y - self.prev_y
        
        # Apply stronger smoothing for small movements
        smooth_factor = self.smoothing if abs(dx) + abs(dy) < 100 else self.smoothing * 1.5
        
        self.prev_x = self.prev_x + dx * smooth_factor
        self.prev_y = self.prev_y + dy * smooth_factor
        return self.prev_x, self.prev_y

    def process_hand(self, frame, frame_height, frame_width):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hand_output = self.hand_detector.process(rgb_frame)
        hands = hand_output.multi_hand_landmarks

        if hands:
            for hand in hands:
                self.drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark

                # Get index finger tip and thumb tip
                index = landmarks[8]
                thumb = landmarks[4]
                
                # Draw landmarks
                index_x = int(index.x * frame_width)
                index_y = int(index.y * frame_height)
                thumb_x = int(thumb.x * frame_width)
                thumb_y = int(thumb.y * frame_height)
                
                cv2.circle(frame, (index_x, index_y), 10, (0, 255, 255))
                cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 255))

                # Calculate screen coordinates
                screen_x = self.screen_width / frame_width * index_x
                screen_y = self.screen_height / frame_height * index_y

                # Apply smoothing
                screen_x, screen_y = self.smooth_movement(screen_x, screen_y)
                
                # Move mouse
                pyautogui.moveTo(int(screen_x), int(screen_y))

                # Calculate 3D distance for click detection
                distance = ((index.x - thumb.x) ** 2 + 
                          (index.y - thumb.y) ** 2 + 
                          (index.z - thumb.z) ** 2) ** 0.5
                
                # Draw distance indicator
                cv2.putText(frame, f"Pinch: {distance:.3f}", (10, 150), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # Click detection
                if distance < 0.04:  # Slightly reduced threshold
                    if not self.is_clicking:
                        self.is_clicking = True
                        pyautogui.click()
                        cv2.putText(frame, "Click!", (10, 180), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                else:
                    self.is_clicking = False

    def process_eye(self, frame, frame_height, frame_width):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_output = self.face_mesh.process(rgb_frame)
        landmark_points = face_output.multi_face_landmarks

        if landmark_points:
            landmarks = landmark_points[0].landmark

            # Use nose tip for more stable cursor control
            nose_tip = landmarks[4]
            
            # Calculate screen coordinates with boundary padding
            padding = 0.1  # 10% screen padding
            screen_x = (self.screen_width * (padding + (1 - 2 * padding) * nose_tip.x))
            screen_y = (self.screen_height * (padding + (1 - 2 * padding) * nose_tip.y))
            
            # Apply smoothing
            screen_x, screen_y = self.smooth_movement(screen_x, screen_y)
            
            # Move mouse
            pyautogui.moveTo(int(screen_x), int(screen_y))

            # Improved blink detection
            left_eye = [landmarks[159], landmarks[145]]  # Upper and lower landmarks
            right_eye = [landmarks[386], landmarks[374]]
            
            left_eye_distance = abs(left_eye[0].y - left_eye[1].y)
            right_eye_distance = abs(right_eye[0].y - right_eye[1].y)
            
            # Draw eye state
            cv2.putText(frame, f"Eye gap: {left_eye_distance:.4f}", (10, 150), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Blink detection
            if left_eye_distance < 0.015 and right_eye_distance < 0.015:
                if not self.is_clicking:
                    self.is_clicking = True
                    pyautogui.click()
                    cv2.putText(frame, "Click!", (10, 180), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                self.is_clicking = False

            # Visualize eye tracking points
            for landmark in left_eye + right_eye:
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))

    def run(self):
        while True:
            # Read frame
            ret, frame = self.cap.read()
            if not ret:
                break

            # Flip frame horizontally
            frame = cv2.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape

            # Process based on mode
            if self.mode == "hand":
                self.process_hand(frame, frame_height, frame_width)
            else:
                self.process_eye(frame, frame_height, frame_width)

            # Add mode indicator and instructions
            mode_text = f"Mode: {'Hand' if self.mode == 'hand' else 'Eye'} tracking"
            cv2.putText(frame, mode_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (0, 255, 0), 2)
            cv2.putText(frame, "Press 'h' for hand mode", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'e' for eye mode", (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to quit", (10, 120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Show frame
            cv2.imshow('Virtual Mouse', frame)

            # Handle key presses
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('h'):
                self.mode = "hand"
            elif key == ord('e'):
                self.mode = "eye"

        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    virtual_mouse = VirtualMouse()
    virtual_mouse.run()