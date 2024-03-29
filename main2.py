import face_recognition
import cv2
import numpy as np

from urllib import request

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    raise Exception("Could not open video device")

# Load a sample picture and learn how to recognize it.
me_image = face_recognition.load_image_file("me.jpg")
me_face_encoding = face_recognition.face_encodings(me_image)[0]

BO_image = face_recognition.load_image_file("obama.jpeg")
BO_face_encoding = face_recognition.face_encodings(BO_image)[0]

# Load a second sample picture and learn how to recognize it.
EM_image = face_recognition.load_image_file("elon.jpg")
EM_face_encoding = face_recognition.face_encodings(EM_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    me_face_encoding,
    BO_face_encoding,
    EM_face_encoding
]
known_face_names = [
    "Jul",
    "Obama",
    "Elon"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                form_url = "https://docs.google.com/forms/d/e/1FAIpQLSc3p4w6voPxybQYsRa8evj-i7XIDwZ96M6jSdbtvrIl7yEFSg/formResponse?usp=pp_url&entry.118791722={}&submit=Submit".format(name)
                request.urlopen(form_url)

                #https://docs.google.com/forms/d/e/1FAIpQLSc3p4w6voPxybQYsRa8evj-i7XIDwZ96M6jSdbtvrIl7yEFSg/formResponse?usp=pp_url&entry.118791722={}


            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
