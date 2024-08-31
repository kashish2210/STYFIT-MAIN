# views.py
from django.shortcuts import render

# views.py
from django.http import StreamingHttpResponse, HttpResponse
import cv2
import os
import cvzone
from cvzone.PoseModule import PoseDetector
from .try1 import main_loop
import mediapipe as mp
import math


def generate_frames(shirtType):
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    # Desired width and height
    width = 1280
    height = 720

    detector = PoseDetector()

    if shirtType == "2d":
        # Define shirt folder path and other variables
        shirtFolderPath = os.path.join("Resources", "Shirts")
    elif shirtType == "3d":
        shirtFolderPath = os.path.join("Resources3d", "3d_shirt")
    listShirts = os.listdir(shirtFolderPath)
    fixedRatio = 262 / 190  # widthOfShirt/widthOfPoint11to12
    shirtRatioHeightWidth = 581 / 440
    imageNumber = 0
    imgButtonRight = cv2.imread(r"Resources/button.png", cv2.IMREAD_UNCHANGED)
    imgButtonLeft = cv2.flip(imgButtonRight, 1)
    counterRight = 0
    counterLeft = 0
    selectionSpeed = 10

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read frame from video.")
            break

        # Resize the frame
        img = cv2.resize(img, (width, height))

        # Apply pose detection
        img = detector.findPose(img)
        lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False)

        if lmList:
            lm11 = lmList[11][0:2]
            lm12 = lmList[12][0:2]

            widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
            if widthOfShirt > 0:
                imgShirtPath = os.path.join(shirtFolderPath, listShirts[imageNumber])
                imgShirt = cv2.imread(imgShirtPath, cv2.IMREAD_UNCHANGED)

                if imgShirt is not None:
                    imgShirt = cv2.resize(
                        imgShirt,
                        (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)),
                    )

                    currentScale = (lm11[0] - lm12[0]) / 190
                    offset = int(44 * currentScale), int(48 * currentScale)

                    overlay_coords = (lm12[0] - offset[0], lm12[1] - offset[1])

                    try:
                        img = cvzone.overlayPNG(img, imgShirt, overlay_coords)
                    except Exception as e:
                        print(f"Error overlaying PNG: {e}")

            img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
            img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

            if lmList[16][0] < 300:
                counterRight += 1
                cv2.ellipse(
                    img,
                    (139, 360),
                    (66, 66),
                    0,
                    0,
                    counterRight * selectionSpeed,
                    (0, 255, 0),
                    20,
                )
                if counterRight * selectionSpeed > 360:
                    counterRight = 0
                    if imageNumber < len(listShirts) - 1:
                        imageNumber += 1
            elif lmList[15][0] > 900:
                counterLeft += 1
                cv2.ellipse(
                    img,
                    (1138, 360),
                    (66, 66),
                    0,
                    0,
                    counterLeft * selectionSpeed,
                    (0, 255, 0),
                    20,
                )
                if counterLeft * selectionSpeed > 360:
                    counterLeft = 0
                    if imageNumber > 0:
                        imageNumber -= 1
            else:
                counterRight = 0
                counterLeft = 0

        # Encode the frame as JPEG
        ret, buffer = cv2.imencode(".jpg", img)
        frame = buffer.tobytes()

        # Stream the frame with a boundary
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")

    cap.release()


def webcam_feed(request):
    """View that streams the webcam feed."""
    return StreamingHttpResponse(
        generate_frames("2d"), content_type="multipart/x-mixed-replace; boundary=frame"
    )


def webcam_feed3d(request):
    """View that streams the webcam feed."""
    return StreamingHttpResponse(
        generate_frames("3d"), content_type="multipart/x-mixed-replace; boundary=frame"
    )


def webcam_page(request):
    """View to render the HTML page with the webcam stream."""
    print(os.getcwd())
    return render(request, "webcam.html")


def customize3d(request):
    main_loop()
    return HttpResponse("Done")


def tryon3d(request):
    return render(request, "3dtryon.html")


def generate_measurement_stream():
    # Initialize Mediapipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Initialize OpenCV for webcam capture
    cap = cv2.VideoCapture(0)

    # Function to calculate the Euclidean distance between two landmarks
    def calculate_distance(point1, point2):
        return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB for Mediapipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb_frame)

        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark

            # Get key landmarks for height measurement (shoulders and hips)
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
            left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

            # Estimate height as the distance between the mid-point of shoulders and ankles
            shoulder_mid_x = (left_shoulder.x + right_shoulder.x) / 2
            shoulder_mid_y = (left_shoulder.y + right_shoulder.y) / 2
            ankle_mid_x = (left_ankle.x + right_ankle.x) / 2
            ankle_mid_y = (left_ankle.y + right_ankle.y) / 2
            height = math.sqrt(
                (shoulder_mid_x - ankle_mid_x) ** 2
                + (shoulder_mid_y - ankle_mid_y) ** 2
            )

            # Estimate waist size as the distance between the hips
            waist_size = calculate_distance(left_hip, right_hip)

            # Scale to a more readable number (the scale is relative to the size of the image)
            height_in_cm = (
                height * 300
            )  # Scaling factor (adjust based on camera distance)
            waist_size_in_cm = waist_size * 200  # Scaling factor

            # Display the estimated height and waist size on the frame
            cv2.putText(
                frame,
                f"Height: {int(height_in_cm)} cm",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame,
                f"Waist: {int(waist_size_in_cm)} cm",
                (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

            # Draw the pose landmarks on the frame
            mp.solutions.drawing_utils.draw_landmarks(
                frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

        # Encode the frame in JPEG format
        ret, jpeg = cv2.imencode(".jpg", frame)
        if not ret:
            continue

        # Convert the image to bytes and yield it
        frame = jpeg.tobytes()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")

    cap.release()
    pose.close()


def measurement_feed(request):
    return StreamingHttpResponse(
        generate_measurement_stream(),
        content_type="multipart/x-mixed-replace; boundary=frame",
    )


def measurement_page(request):
    return render(request, "measurement_page.html")
