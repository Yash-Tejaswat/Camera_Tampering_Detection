import cv2
import numpy as np
import pygame

pygame.mixer.init()

def detect_tampering(camera):
    fgbg = cv2.createBackgroundSubtractorMOG2()
    kernel = np.ones((5, 5), np.uint8)
    alarm_sound = pygame.mixer.Sound('beep.mp3')
    alarm_triggered = False

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        variance = np.var(gray)

        # Check if the mean brightness is below a certain threshold or variance is very low
        if mean_brightness < 60 or variance < 70:  # Adjust the thresholds as needed
            cv2.putText(frame, "CAMERA BLOCKED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if not alarm_triggered:
                alarm_sound.play(-1)  # -1 makes the sound loop until stopped
                alarm_triggered = True  # To prevent the sound from starting again

        if alarm_triggered and (mean_brightness >= 60 and variance >= 70):
            alarm_sound.stop()
            alarm_triggered = False  # Reset to allow the alarm to trigger again if needed

        cv2.imshow('Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()